# =============================================================================
# Phase 2 — 학생 채팅 UI
# =============================================================================
# 플로우:
#   1. 접속 코드 입력
#   2. 강사 도플갱어와 채팅 (스트리밍)
#   3. 대화 기록 자동 저장
# =============================================================================

import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from phase2_doppelganger import doppelganger_engine as engine
from phase2_doppelganger import storage


# ---------------------------------------------------------------------------
# 진입점
# ---------------------------------------------------------------------------

def render_chat() -> None:
    if "chat_instructor" not in st.session_state:
        _render_code_entry()
    else:
        _render_chat_interface()


# ---------------------------------------------------------------------------
# 코드 입력 화면
# ---------------------------------------------------------------------------

def _render_code_entry() -> None:
    # 온보딩에서 테스트로 넘어온 경우 자동 입력
    auto_code = st.session_state.pop("chat_test_code", None)

    st.markdown("""
    <div style="text-align:center; padding:60px 20px 32px;">
        <div style="font-size:3.5rem;">🤖</div>
        <h2 style="font-size:1.8rem; font-weight:900; margin:12px 0 8px;">
            AI 도플갱어와 학습 시작
        </h2>
        <p style="color:#666; font-size:0.95rem;">
            강사님께 받은 접속 코드를 입력하세요
        </p>
    </div>
    """, unsafe_allow_html=True)

    _, col_c, _ = st.columns([1, 2, 1])
    with col_c:
        code_input = st.text_input(
            "접속 코드",
            value=auto_code or "",
            placeholder="6자리 코드 입력 (예: A3B7K2)",
            label_visibility="collapsed",
            max_chars=6,
        ).strip().upper()

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("학습 시작 →", type="primary", use_container_width=True):
            if not code_input:
                st.error("접속 코드를 입력해주세요.")
                return

            instructor = storage.get_instructor(code_input)
            if not instructor:
                st.error("❌ 유효하지 않은 코드입니다. 강사님께 코드를 다시 확인해주세요.")
                return

            st.session_state.chat_instructor = instructor
            st.session_state.chat_messages = []
            st.session_state.chat_conv_saved = False
            st.rerun()

    # 자동 입력 코드가 있으면 즉시 시도
    if auto_code:
        instructor = storage.get_instructor(auto_code)
        if instructor:
            st.session_state.chat_instructor = instructor
            st.session_state.chat_messages = []
            st.session_state.chat_conv_saved = False
            st.rerun()


# ---------------------------------------------------------------------------
# 채팅 인터페이스
# ---------------------------------------------------------------------------

def _render_chat_interface() -> None:
    instructor = st.session_state.chat_instructor
    name = instructor.get("name", "강사")
    specialty = instructor.get("specialty", "")
    code = instructor.get("instructor_id", "")

    # ── 상단 헤더 ──────────────────────────────────────────────────────────
    col_info, col_btn = st.columns([4, 1])
    with col_info:
        st.markdown(f"""
        <div style="padding:8px 0;">
            <span style="font-size:1.15rem; font-weight:900;">🤖 {name} 도플갱어</span>
            <span style="font-size:0.82rem; color:#2BC0B8; margin-left:10px;
                         background:#E8FAF9; padding:2px 10px; border-radius:20px;">
                ● 온라인
            </span>
            <br>
            <span style="font-size:0.82rem; color:#888;">{specialty}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        if st.button("코드 변경", use_container_width=True):
            for key in ["chat_instructor", "chat_messages", "chat_conv_saved"]:
                st.session_state.pop(key, None)
            st.rerun()

    st.divider()

    # ── 초기 인사 ──────────────────────────────────────────────────────────
    if not st.session_state.get("chat_messages"):
        greeting = (
            f"안녕하세요! 저는 **{name}**의 AI 도플갱어입니다. 😊\n\n"
            f"**{specialty}** 분야에 대해 궁금한 것을 편하게 물어보세요!\n"
            f"반복해서 학습하고 싶은 내용도 언제든지 질문하세요."
        )
        st.session_state.chat_messages = [
            {"role": "assistant", "content": greeting}
        ]

    # ── 메시지 렌더링 ──────────────────────────────────────────────────────
    for msg in st.session_state.chat_messages:
        avatar = "🤖" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

    # ── 채팅 입력 ──────────────────────────────────────────────────────────
    user_input = st.chat_input(f"{name} 도플갱어에게 질문하기...")

    if user_input:
        # 사용자 메시지 추가
        st.session_state.chat_messages.append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)

        # 도플갱어 응답 (스트리밍)
        with st.chat_message("assistant", avatar="🤖"):
            try:
                response = st.write_stream(
                    engine.stream_doppelganger(
                        messages=st.session_state.chat_messages,
                        system_prompt=instructor["system_prompt"],
                    )
                )
            except ValueError as e:
                st.error(str(e))
                return

        st.session_state.chat_messages.append(
            {"role": "assistant", "content": response}
        )

        # 대화 저장 (3번째 exchange 이후 자동 저장)
        user_count = sum(
            1 for m in st.session_state.chat_messages if m["role"] == "user"
        )
        if user_count >= 2:
            storage.save_conversation(code, st.session_state.chat_messages)

        st.rerun()

    # ── 하단 — 대화 통계 ───────────────────────────────────────────────────
    msg_count = len([m for m in st.session_state.chat_messages if m["role"] == "user"])
    if msg_count > 0:
        stats = storage.get_instructor_stats(code)
        st.markdown(
            f'<div style="text-align:center; font-size:0.78rem; color:#BBBBBB; '
            f'padding:12px 0;">이번 세션 {msg_count}개 질문 · '
            f'총 누적 대화 {stats.get("total_conversations", 0)}건</div>',
            unsafe_allow_html=True,
        )
