# =============================================================================
# Phase 3 — 직무 / 자격증 / 기업 추천 엔진
# =============================================================================
# 1. 규칙 기반: 카테고리 점수 → 직무 적합도 계산 + 자격증 매핑
# 2. Claude AI: 개인화 커리어 코칭 메시지 스트리밍
# =============================================================================

import sys
from pathlib import Path
from typing import Generator, List

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import anthropic
from shared.config import CLAUDE_MODEL_FAST, get_anthropic_api_key


# ---------------------------------------------------------------------------
# 직무 프로파일
# ---------------------------------------------------------------------------

JOB_PROFILES = [
    {
        "title": "MD (상품 기획 · 바이어)",
        "icon": "🛍️",
        "desc": "상품 소싱, 플랫폼 등록, 판매 전략 수립, 재고 관리",
        "key_cats": ["플랫폼 운영", "공급망 & 물류"],
        "bonus_cats": ["데이터 & KPI"],
        "companies": ["쿠팡", "무신사", "올리브영", "11번가", "지그재그"],
    },
    {
        "title": "퍼포먼스 마케터",
        "icon": "📣",
        "desc": "Meta·구글 광고 운영, ROAS 최적화, 타겟 세그먼트 분석",
        "key_cats": ["퍼포먼스 마케팅", "데이터 & KPI"],
        "bonus_cats": ["콘텐츠 & 브랜딩"],
        "companies": ["마켓컬리", "에이블리", "카카오커머스", "배달의민족"],
    },
    {
        "title": "이커머스 오퍼레이터",
        "icon": "⚙️",
        "desc": "플랫폼 전반 운영, 발주·배송·CS 관리, 운영 효율화",
        "key_cats": ["플랫폼 운영", "데이터 & KPI"],
        "bonus_cats": ["공급망 & 물류"],
        "companies": ["스마트스토어 셀러", "쿠팡 파트너스", "티몬", "위메프"],
    },
    {
        "title": "콘텐츠 마케터",
        "icon": "✍️",
        "desc": "상세페이지 기획, SNS 콘텐츠 제작, 브랜드 빌딩, 인플루언서 협업",
        "key_cats": ["콘텐츠 & 브랜딩", "퍼포먼스 마케팅"],
        "bonus_cats": ["AI 도구 활용"],
        "companies": ["무신사", "29CM", "오늘의집", "당근마켓"],
    },
    {
        "title": "이커머스 데이터 분석가",
        "icon": "📊",
        "desc": "구매 퍼널 분석, KPI 대시보드 구축, A/B 테스트 설계",
        "key_cats": ["데이터 & KPI", "퍼포먼스 마케팅"],
        "bonus_cats": ["AI 도구 활용"],
        "companies": ["카카오", "네이버", "쿠팡", "GS리테일 디지털"],
    },
    {
        "title": "AI 자동화 전문가",
        "icon": "🤖",
        "desc": "업무 자동화 구축, AI 도구 도입, n8n 워크플로우 설계",
        "key_cats": ["AI 도구 활용", "데이터 & KPI"],
        "bonus_cats": ["퍼포먼스 마케팅"],
        "companies": ["스타트업", "이커머스 솔루션사", "SaaS 기업"],
    },
]


# ---------------------------------------------------------------------------
# 자격증 추천 데이터
# ---------------------------------------------------------------------------

CERT_RECOMMENDATIONS = {
    "퍼포먼스 마케팅": [
        {"name": "Meta Blueprint 인증", "org": "Meta"},
        {"name": "구글 애널리틱스 4 인증 (GAIQ)", "org": "Google"},
        {"name": "카카오 광고 자격증", "org": "카카오"},
    ],
    "콘텐츠 & 브랜딩": [
        {"name": "컴퓨터그래픽스운용기능사", "org": "한국산업인력공단"},
        {"name": "GTQ (그래픽기술자격)", "org": "한국생산성본부"},
    ],
    "플랫폼 운영": [
        {"name": "전자상거래관리사 2급", "org": "대한상공회의소"},
        {"name": "유통관리사 2급", "org": "대한상공회의소"},
    ],
    "데이터 & KPI": [
        {"name": "ADsP (데이터 분석 준전문가)", "org": "한국데이터산업진흥원"},
        {"name": "SQLD (SQL 개발자)", "org": "한국데이터산업진흥원"},
        {"name": "빅데이터 분석기사", "org": "한국데이터산업진흥원"},
    ],
    "AI 도구 활용": [
        {"name": "Google AI Essentials", "org": "Google"},
        {"name": "Coursera AI for Everyone", "org": "deeplearning.ai"},
    ],
    "공급망 & 물류": [
        {"name": "물류관리사", "org": "국토교통부"},
        {"name": "유통관리사 2급", "org": "대한상공회의소"},
    ],
}


# ---------------------------------------------------------------------------
# 규칙 기반 추천 함수
# ---------------------------------------------------------------------------

def get_job_recommendations(cat_scores: dict, top_n: int = 3) -> List[dict]:
    """카테고리 점수 기반 직무 적합도 계산 → 상위 N개 반환."""
    results = []
    for job in JOB_PROFILES:
        key_avg = sum(cat_scores.get(c, 0) for c in job["key_cats"]) / len(job["key_cats"])
        bonus_avg = sum(cat_scores.get(c, 0) for c in job["bonus_cats"]) / len(job["bonus_cats"])
        fit = key_avg * 0.70 + bonus_avg * 0.30
        results.append({**job, "fit": fit, "fit_pct": min(round(fit), 100)})

    return sorted(results, key=lambda x: x["fit"], reverse=True)[:top_n]


def get_cert_recommendations(cat_scores: dict, n_weak_cats: int = 2) -> List[dict]:
    """가장 낮은 n_weak_cats 카테고리의 자격증 목록 반환."""
    sorted_cats = sorted(cat_scores.items(), key=lambda x: x[1])
    weak_cats = [name for name, _ in sorted_cats[:n_weak_cats]]

    certs = []
    seen = set()
    for cat in weak_cats:
        for cert in CERT_RECOMMENDATIONS.get(cat, []):
            if cert["name"] not in seen:
                certs.append({**cert, "category": cat})
                seen.add(cert["name"])
    return certs


def get_gap_analysis(cat_scores: dict, job: dict) -> List[dict]:
    """
    직무 vs 현재 역량 갭 분석.

    Returns:
        [{category, current, target, gap}, ...]  — 갭이 큰 순서
    """
    # 핵심 카테고리 목표: 80점, 보너스 카테고리 목표: 65점
    targets = {c: 80 for c in job["key_cats"]}
    targets.update({c: 65 for c in job["bonus_cats"]})

    gaps = []
    for cat, target in targets.items():
        current = cat_scores.get(cat, 0)
        gap = max(target - current, 0)
        gaps.append({"category": cat, "current": round(current), "target": target, "gap": gap})

    return sorted(gaps, key=lambda x: x["gap"], reverse=True)


# ---------------------------------------------------------------------------
# Claude AI 코칭 메시지 스트리밍
# ---------------------------------------------------------------------------

def stream_ai_coaching(scores: dict) -> Generator[str, None, None]:
    """
    역량 점수를 바탕으로 Claude가 개인화 커리어 코칭 메시지를 스트리밍 출력한다.

    Yields:
        스트리밍 텍스트 청크
    """
    api_key = get_anthropic_api_key()
    if not api_key:
        yield (
            "**AI 코칭을 사용하려면 Anthropic API 키가 필요합니다.**\n\n"
            "Streamlit Secrets에 `[anthropic] api_key = 'sk-ant-...'`를 등록해주세요."
        )
        return

    client = anthropic.Anthropic(api_key=api_key)

    cat_lines = "\n".join(
        f"- {name}: {score:.0f}점"
        for name, score in scores["categories"].items()
    )
    total = scores["total"]
    strongest = scores["strongest"]
    weakest = scores["weakest"]

    prompt = f"""당신은 이커머스 분야 커리어 코치입니다. 아래 역량 진단 결과를 바탕으로 따뜻하고 실용적인 커리어 조언을 해주세요.

[역량 진단 결과]
{cat_lines}

종합 평균: {total:.0f}점
최강점: {strongest}
핵심 취약점: {weakest}

[작성 규칙]
- 3개 단락으로 구성: ① 현재 역량 프로파일 요약 ② 지금 당장 집중할 핵심 액션 1가지 ③ 3개월 후 목표 상태
- 이커머스 실무자 시각에서 구체적인 수치와 액션을 포함
- 마크다운 볼드(**강조**)를 적절히 활용
- 전체 400~500자 이내로 작성"""

    with client.messages.stream(
        model=CLAUDE_MODEL_FAST,
        max_tokens=700,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            yield text
