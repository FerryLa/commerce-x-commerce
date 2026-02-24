# =============================================================================
# Phase 2 — 도플갱어 엔진
# =============================================================================
# 역할:
#   1. 강사 인터뷰 진행 (Claude가 질문 → 강사 답변)
#   2. 수집 데이터 → 도플갱어 System Prompt 자동 생성
#   3. 학생 채팅 스트리밍 응답
# =============================================================================

import os
import sys
from pathlib import Path
from typing import Generator

import anthropic

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
from shared.config import (
    CLAUDE_MODEL,
    CLAUDE_MODEL_FAST,
    DOPPELGANGER_MAX_TOKENS,
    INTERVIEW_MAX_TOKENS,
    PERSONA_EXTRACT_MAX_TOKENS,
    KNOWLEDGE_BASE_LIMIT,
    get_anthropic_api_key,
)


# ---------------------------------------------------------------------------
# 클라이언트
# ---------------------------------------------------------------------------
def _get_client() -> anthropic.Anthropic:
    api_key = get_anthropic_api_key()
    if not api_key:
        raise ValueError(
            "Anthropic API 키가 설정되지 않았습니다.\n"
            "Streamlit Secrets에 [anthropic] api_key = '...' 를 추가하거나\n"
            "환경변수 ANTHROPIC_API_KEY 를 설정해주세요."
        )
    return anthropic.Anthropic(api_key=api_key)


# ---------------------------------------------------------------------------
# 프롬프트 템플릿
# ---------------------------------------------------------------------------
INTERVIEW_SYSTEM = """당신은 AI 도플갱어 생성 전문가입니다.
강사의 교육 스타일, 전문 지식, 개성을 파악하기 위해 자연스러운 대화형 인터뷰를 진행합니다.

[규칙]
- 질문은 반드시 하나씩만 해주세요
- 이전 답변에 진심으로 공감하며 자연스럽게 이어주세요
- 총 {target_turns}개 핵심 영역을 파악한 후 [인터뷰 완료] 신호를 보내세요
- 마지막에는 수집된 인사이트를 bullet point로 정리해주세요

[파악할 핵심 영역]
1. 전문 분야와 경험 깊이
2. 학생들이 자주 하는 실수/오해
3. 설명 방식 (비유, 예시, 단계별 등)
4. 피드백 스타일 (직접적/부드럽게/질문으로 유도 등)
5. 교육 철학과 원칙
6. 동기부여 방식
7. 말투와 개성 (친근함/전문성/유머 등)"""

DOPPELGANGER_SYSTEM_TEMPLATE = """당신은 {name}의 AI 도플갱어입니다.
학생들의 반복 질문을 자동으로 처리하며, {name} 선생님과 최대한 비슷하게 소통합니다.

━━━━━━━━━━━━━━━━━━━━━━
🎯 전문 분야
{specialty}

🧠 교육 스타일 & 페르소나
{persona}

📝 자주 받는 질문과 내 답변 패턴
{qa_examples}

📚 전문 지식 베이스
{knowledge_base}
━━━━━━━━━━━━━━━━━━━━━━

[행동 수칙]
✓ {name} 선생님의 말투와 설명 방식을 100% 유지
✓ 답변 후 반드시 이해 확인 질문으로 반복 학습 유도
✓ 모르는 내용은 솔직하게: "{name} 선생님께 직접 여쭤보세요 😊"
✓ 틀린 답변: 부드럽게 교정 → 왜 틀렸는지 핵심만 설명
✓ 답변은 간결하게 (3~5문장, 필요 시 확장)
✓ 항상 학생 편에서 생각하고 격려"""


# ---------------------------------------------------------------------------
# 도플갱어 System Prompt 생성
# ---------------------------------------------------------------------------
def build_system_prompt(instructor_data: dict) -> str:
    """수집된 강사 데이터로 도플갱어 system prompt를 생성한다."""

    # Q&A 포맷
    qa_list = instructor_data.get("manual_qa", [])
    if qa_list:
        qa_text = "\n".join(
            f"Q: {item['q']}\nA: {item['a']}" for item in qa_list[:10]
        )
    else:
        qa_text = "(직접 등록된 Q&A 없음)"

    # 지식 베이스 (토큰 초과 방지)
    kb = instructor_data.get("knowledge_base", "").strip()
    if kb:
        kb = kb[:KNOWLEDGE_BASE_LIMIT]
        if len(instructor_data.get("knowledge_base", "")) > KNOWLEDGE_BASE_LIMIT:
            kb += "\n[... 이하 생략]"
    else:
        kb = "(업로드된 자료 없음)"

    return DOPPELGANGER_SYSTEM_TEMPLATE.format(
        name=instructor_data.get("name", "강사"),
        specialty=instructor_data.get("specialty", ""),
        persona=instructor_data.get("persona_summary", "친근하고 명확한 설명 스타일"),
        qa_examples=qa_text,
        knowledge_base=kb,
    )


# ---------------------------------------------------------------------------
# 인터뷰 스트리밍
# ---------------------------------------------------------------------------
def stream_interview(messages: list, target_turns: int = 7) -> Generator[str, None, None]:
    """
    강사 온보딩 인터뷰 스트리밍.

    Args:
        messages: 지금까지의 대화 [{role, content}, ...]
        target_turns: 목표 인터뷰 턴 수

    Yields:
        스트리밍 텍스트 청크
    """
    client = _get_client()
    system = INTERVIEW_SYSTEM.format(target_turns=target_turns)

    with client.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=INTERVIEW_MAX_TOKENS,
        system=system,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text


# ---------------------------------------------------------------------------
# 페르소나 요약 추출 (동기 호출)
# ---------------------------------------------------------------------------
def extract_persona_summary(interview_messages: list) -> str:
    """
    인터뷰 대화에서 강사의 핵심 특성을 구조화된 텍스트로 추출한다.

    Returns:
        bullet point 형태의 페르소나 요약 문자열
    """
    client = _get_client()

    # 대화 텍스트 구성
    interview_text = "\n".join(
        f"{'강사' if m['role'] == 'user' else 'AI 인터뷰어'}: {m['content']}"
        for m in interview_messages
    )

    response = client.messages.create(
        model=CLAUDE_MODEL_FAST,
        max_tokens=PERSONA_EXTRACT_MAX_TOKENS,
        messages=[
            {
                "role": "user",
                "content": f"""아래 인터뷰에서 강사의 핵심 특성을 추출해 간결하게 정리해주세요.

{interview_text}

출력 형식 (각 항목 1~2줄):
- 말투:
- 설명 방식:
- 자주 쓰는 표현/비유:
- 피드백 스타일:
- 교육 철학:
- 특이사항/개성:""",
            }
        ],
    )
    return response.content[0].text


# ---------------------------------------------------------------------------
# 도플갱어 채팅 스트리밍
# ---------------------------------------------------------------------------
def stream_doppelganger(
    messages: list, system_prompt: str
) -> Generator[str, None, None]:
    """
    도플갱어 채팅 응답 스트리밍.

    Args:
        messages: 학생-도플갱어 대화 [{role, content}, ...]
        system_prompt: build_system_prompt()로 생성된 프롬프트

    Yields:
        스트리밍 텍스트 청크
    """
    client = _get_client()

    with client.messages.stream(
        model=CLAUDE_MODEL,
        max_tokens=DOPPELGANGER_MAX_TOKENS,
        system=system_prompt,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text
