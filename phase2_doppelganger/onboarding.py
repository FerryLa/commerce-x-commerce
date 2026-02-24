# =============================================================================
# Phase 2 — 강사 온보딩 UI
# =============================================================================
# 5단계 플로우:
#   Step 1: 기본 정보 입력
#   Step 2: AI 인터뷰 (Claude가 강사에게 질문 → 페르소나 추출)
#   Step 3: Q&A 직접 등록
#   Step 4: 자료 텍스트 업로드
#   Step 5: 도플갱어 완성 + 코드 발급
# =============================================================================

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from phase2_doppelganger import doppelganger_engine as engine
from phase2_doppelganger import storage
from shared.config import INTERVIEW_MIN_TURNS, QA_MIN_COUNT

# ---------------------------------------------------------------------------
# 진입점
# ---------------------------------------------------------------------------

STEPS = ["기본 설정", "AI 인터뷰", "Q&A 등록", "자료 업로드", "완성! 🎉"]


def render_onboarding() -> None:
    _init_session()
    _render_header()
    _render_progress()

    step = st.session_state.ob_step
    if step == 1:
        _step1_basic_info()
    elif step == 2:
        _step2_interview()
    elif step == 3:
        _step3_qa()
    elif step == 4:
        _step4_upload()
    elif step == 5:
        _step5_complete()


# ---------------------------------------------------------------------------
# 세션 초기화
# ---------------------------------------------------------------------------

def _init_session() -> None:
    defaults = {
        "ob_step": 1,
        "ob_instructor": {},   # 강사 기본 정보
        "ob_interview": [],    # 인터뷰 메시지 [{role, content}]
        "ob_qa": [],           # 수동 Q&A [{q, a}]
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


# ---------------------------------------------------------------------------
# 공통 헤더 / 진행 바
# ---------------------------------------------------------------------------

def _render_header() -> None:
    st.markdown("""
    <div style="text-align:center; padding:32px 0 8px;">
        <span style="font-size:2.2rem;">🤖</span>
        <h1 style="font-size:1.8rem; font-weight:900; margin:8px 0 4px;">
            AI 도플갱어 만들기
        </h1>
        <p style="color:#666; font-size:0.95rem;">
            내 교육 스타일을 AI에 담아 반복 질문을 자동화하세요
        </p>
    </div>
    """, unsafe_allow_html=True)


def _render_progress() -> None:
    current = st.session_state.ob_step - 1
    cols = st.columns(len(STEPS))
    for i, (col, name) in enumerate(zip(cols, STEPS)):
        with col:
            if i < current:
                color, weight, symbol = "#2BC0B8", "600", "✓"
            elif i == current:
                color, weight, symbol = "#2BC0B8", "900", "●"
            else:
                color, weight, symbol = "#CCCCCC", "400", "○"
            st.markdown(
                f'<div style="text-align:center; color:{color}; '
                f'font-weight:{weight}; font-size:0.82rem; padding:4px 0;">'
                f'{symbol} {name}</div>',
                unsafe_allow_html=True,
            )
    st.divider()


# ---------------------------------------------------------------------------
# Step 1 — 기본 정보
# ---------------------------------------------------------------------------

def _step1_basic_info() -> None:
    st.subheader("👋 기본 정보")
    st.caption("도플갱어의 기반이 될 정보를 입력해주세요.")

    data = st.session_state.ob_instructor
    name = st.text_input(
        "이름 (학생에게 보이는 이름) *",
        value=data.get("name", ""),
        placeholder="예: 김철수 멘토",
    )
    specialty = st.text_input(
        "전문 분야 *",
        value=data.get("specialty", ""),
        placeholder="예: 이커머스 퍼포먼스 마케팅",
    )
    style = st.selectbox(
        "기본 교육 스타일",
        ["친근하고 대화하듯이", "전문적이고 체계적으로", "직설적이고 핵심만", "유머러스하게"],
        index=["친근하고 대화하듯이", "전문적이고 체계적으로",
               "직설적이고 핵심만", "유머러스하게"].index(
            data.get("style", "친근하고 대화하듯이")
        ),
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("다음 → AI 인터뷰 시작", type="primary", use_container_width=True):
        if not name.strip() or not specialty.strip():
            st.error("이름과 전문 분야는 필수입니다.")
            return

        st.session_state.ob_instructor.update(
            {"name": name.strip(), "specialty": specialty.strip(), "style": style}
        )

        # 인터뷰 첫 질문 세팅 (hardcoded opener)
        first_q = (
            f"안녕하세요, {name.strip()} 선생님! 😊 "
            f"AI 도플갱어를 만들어드리기 위한 인터뷰를 시작할게요. "
            f"먼저, **{specialty.strip()}** 분야를 가르치시면서 "
            f"학생들이 가장 자주 실수하거나 오해하는 부분이 무엇인가요?"
        )
        st.session_state.ob_interview = [{"role": "assistant", "content": first_q}]
        st.session_state.ob_step = 2
        st.rerun()


# ---------------------------------------------------------------------------
# Step 2 — AI 인터뷰
# ---------------------------------------------------------------------------

def _step2_interview() -> None:
    name = st.session_state.ob_instructor.get("name", "선생님")
    st.subheader("🎤 AI 인터뷰")
    st.caption(
        f"AI가 {name} 선생님의 교육 스타일과 전문 지식을 파악하기 위해 "
        f"질문드립니다. 자연스럽게 답변해주세요! (약 {INTERVIEW_MIN_TURNS}~8개 질문)"
    )

    # 메시지 표시
    for msg in st.session_state.ob_interview:
        avatar = "🤖" if msg["role"] == "assistant" else "🧑‍🏫"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # 인터뷰 완료 조건: [인터뷰 완료] 감지 또는 충분한 턴 수
    user_turns = sum(
        1 for m in st.session_state.ob_interview if m["role"] == "user"
    )
    auto_done = any(
        "[인터뷰 완료]" in m.get("content", "")
        for m in st.session_state.ob_interview
        if m["role"] == "assistant"
    )
    interview_done = auto_done or user_turns >= INTERVIEW_MIN_TURNS + 2

    if not interview_done:
        user_input = st.chat_input("답변을 입력하세요...")
        if user_input:
            st.session_state.ob_interview.append(
                {"role": "user", "content": user_input}
            )
            with st.chat_message("assistant", avatar="🤖"):
                try:
                    response = st.write_stream(
                        engine.stream_interview(st.session_state.ob_interview)
                    )
                except ValueError as e:
                    st.error(str(e))
                    return
            st.session_state.ob_interview.append(
                {"role": "assistant", "content": response}
            )
            st.rerun()
    else:
        st.success(f"✅ 인터뷰 완료! ({user_turns}개 질문 답변)")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("← 다시 인터뷰", use_container_width=True):
                st.session_state.ob_interview = []
                st.session_state.ob_step = 1
                st.rerun()
        with col2:
            if st.button(
                "다음 → Q&A 등록", type="primary", use_container_width=True
            ):
                with st.spinner("💭 인터뷰 내용으로 페르소나 분석 중..."):
                    try:
                        summary = engine.extract_persona_summary(
                            st.session_state.ob_interview
                        )
                        st.session_state.ob_instructor["persona_summary"] = summary
                    except ValueError as e:
                        st.error(str(e))
                        return
                st.session_state.ob_step = 3
                st.rerun()

    # 수동 완료 버튼 (충분히 답변했지만 AI가 감지 못했을 때)
    if user_turns >= INTERVIEW_MIN_TURNS and not interview_done:
        st.markdown("---")
        if st.button(
            f"✋ 인터뷰 충분히 했어요 ({user_turns}개 답변) → 다음 단계로",
            use_container_width=True,
        ):
            with st.spinner("💭 페르소나 분석 중..."):
                try:
                    summary = engine.extract_persona_summary(
                        st.session_state.ob_interview
                    )
                    st.session_state.ob_instructor["persona_summary"] = summary
                except ValueError as e:
                    st.error(str(e))
                    return
            st.session_state.ob_step = 3
            st.rerun()


# ---------------------------------------------------------------------------
# Step 3 — Q&A 직접 등록
# ---------------------------------------------------------------------------

def _step3_qa() -> None:
    st.subheader("📝 Q&A 직접 등록")
    st.caption(
        f"학생들이 자주 묻는 질문과 **내 스타일의** 답변을 등록하세요. "
        f"많을수록 도플갱어가 정확해집니다! (최소 {QA_MIN_COUNT}개)"
    )

    # 등록된 Q&A 목록
    for i, qa in enumerate(st.session_state.ob_qa):
        with st.expander(f"Q{i + 1}. {qa['q'][:50]}{'...' if len(qa['q']) > 50 else ''}", expanded=False):
            st.markdown(f"**Q:** {qa['q']}")
            st.markdown(f"**A:** {qa['a']}")
            if st.button("삭제 🗑️", key=f"del_qa_{i}"):
                st.session_state.ob_qa.pop(i)
                st.rerun()

    # Q&A 추가 폼
    with st.form("qa_add_form", clear_on_submit=True):
        new_q = st.text_area(
            "질문",
            placeholder="예: ROAS가 200%면 수익이 나는 건가요?",
            height=80,
        )
        new_a = st.text_area(
            "내 방식의 답변 (말투 포함)",
            placeholder="예: 좋은 질문이에요! ROAS 200%는 매출이 광고비의 2배라는 뜻인데, 순이익이 남는지는 마진율을 같이 봐야 해요. 예를 들어...",
            height=120,
        )
        if st.form_submit_button("Q&A 추가 ➕", use_container_width=True):
            if new_q.strip() and new_a.strip():
                st.session_state.ob_qa.append({"q": new_q.strip(), "a": new_a.strip()})
                st.rerun()
            else:
                st.error("질문과 답변을 모두 입력해주세요.")

    st.divider()
    count = len(st.session_state.ob_qa)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 이전", use_container_width=True):
            st.session_state.ob_step = 2
            st.rerun()
    with col2:
        btn_label = (
            f"다음 → 자료 업로드 ({count}개 등록됨)"
            if count >= QA_MIN_COUNT
            else f"다음 → 자료 업로드 ({count}/{QA_MIN_COUNT}개)"
        )
        if st.button(btn_label, type="primary", use_container_width=True):
            if count < QA_MIN_COUNT:
                st.error(f"최소 {QA_MIN_COUNT}개의 Q&A를 등록해주세요. (현재 {count}개)")
            else:
                st.session_state.ob_instructor["manual_qa"] = st.session_state.ob_qa
                st.session_state.ob_step = 4
                st.rerun()


# ---------------------------------------------------------------------------
# Step 4 — 자료 업로드
# ---------------------------------------------------------------------------

def _step4_upload() -> None:
    st.subheader("📚 자료 업로드")
    st.caption(
        "교안, 정리 노트, 자주 쓰는 설명 등을 텍스트로 붙여넣으세요. "
        "도플갱어의 지식 베이스가 됩니다. (선택 사항)"
    )

    kb = st.text_area(
        "교육 자료 텍스트",
        value=st.session_state.ob_instructor.get("knowledge_base", ""),
        placeholder=(
            "예시:\n"
            "- ROAS 계산: 매출 ÷ 광고비 × 100. ROAS 300% = 광고비 1만원으로 3만원 매출\n"
            "- 퍼포먼스 마케팅의 핵심은 측정 → 분석 → 개선의 반복\n"
            "- GA4 이벤트 설정 방법: 관리 → 데이터 스트림 → 이벤트 생성...\n\n"
            "자유롭게 붙여넣으세요."
        ),
        height=320,
    )

    char_count = len(kb)
    from shared.config import KNOWLEDGE_BASE_LIMIT
    color = "#2BC0B8" if char_count <= KNOWLEDGE_BASE_LIMIT else "#FF6B6B"
    st.markdown(
        f'<div style="font-size:0.85rem; color:{color};">'
        f"입력: {char_count:,}자 (권장: 500~{KNOWLEDGE_BASE_LIMIT:,}자)"
        f"{'  ⚠️ 초과분은 자동 축약됩니다.' if char_count > KNOWLEDGE_BASE_LIMIT else ''}"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← 이전", use_container_width=True):
            st.session_state.ob_step = 3
            st.rerun()
    with col2:
        if st.button("🤖 도플갱어 생성하기", type="primary", use_container_width=True):
            st.session_state.ob_instructor["knowledge_base"] = kb

            with st.spinner("🤖 AI 도플갱어를 생성하는 중..."):
                try:
                    system_prompt = engine.build_system_prompt(
                        st.session_state.ob_instructor
                    )
                    st.session_state.ob_instructor["system_prompt"] = system_prompt
                    code = storage.save_instructor(st.session_state.ob_instructor)
                    st.session_state.ob_instructor["instructor_id"] = code
                except Exception as e:
                    st.error(f"도플갱어 생성 실패: {e}")
                    return

            st.session_state.ob_step = 5
            st.rerun()


# ---------------------------------------------------------------------------
# Step 5 — 완성
# ---------------------------------------------------------------------------

def _step5_complete() -> None:
    data = st.session_state.ob_instructor
    name = data.get("name", "강사")
    code = data.get("instructor_id", "------")

    st.balloons()

    st.markdown(f"""
    <div style="text-align:center; padding:32px 0 24px;">
        <div style="font-size:3.5rem;">🤖✨</div>
        <h2 style="font-size:1.8rem; font-weight:900; color:#2BC0B8; margin:12px 0 8px;">
            {name}의 AI 도플갱어 완성!
        </h2>
        <p style="color:#666;">
            아래 접속 코드를 학생들에게 공유하세요
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 접속 코드 카드
    _, col_c, _ = st.columns([1, 2, 1])
    with col_c:
        st.markdown(f"""
        <div style="background:#F0FAFB; border:2px solid #2BC0B8;
                    border-radius:20px; padding:36px; text-align:center;">
            <div style="font-size:0.9rem; color:#888; margin-bottom:8px; font-weight:600;">
                학생 접속 코드
            </div>
            <div style="font-size:3rem; font-weight:900; color:#2BC0B8;
                        letter-spacing:10px; font-family:monospace;">
                {code}
            </div>
            <div style="font-size:0.82rem; color:#999; margin-top:10px;">
                학생 채팅 페이지 → 이 코드 입력
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 통계 미리보기
    col_a, col_b, col_c2 = st.columns(3)
    qa_count = len(data.get("manual_qa", []))
    kb_chars = len(data.get("knowledge_base", ""))
    interview_turns = sum(
        1 for m in st.session_state.ob_interview if m["role"] == "user"
    )
    with col_a:
        st.metric("인터뷰 답변", f"{interview_turns}개")
    with col_b:
        st.metric("등록 Q&A", f"{qa_count}개")
    with col_c2:
        st.metric("지식 베이스", f"{kb_chars:,}자")

    st.markdown("<br>", unsafe_allow_html=True)

    # 시스템 프롬프트 미리보기
    with st.expander("🔍 생성된 도플갱어 시스템 프롬프트 확인"):
        st.code(data.get("system_prompt", ""), language="text")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("💬 지금 바로 테스트", type="primary", use_container_width=True):
            # 학생 채팅 페이지로 이동 + 코드 자동 입력
            st.session_state["chat_test_code"] = code
            st.switch_page("pages/2_학생_채팅.py")
    with col2:
        if st.button("🆕 새 도플갱어 만들기", use_container_width=True):
            for key in ["ob_step", "ob_instructor", "ob_interview", "ob_qa"]:
                st.session_state.pop(key, None)
            st.rerun()
