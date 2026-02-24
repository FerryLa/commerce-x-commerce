# =============================================================================
# Phase 2 — 학생 채팅 페이지 (Streamlit Multipage 진입점)
# =============================================================================

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from phase2_doppelganger.chat_ui import render_chat

st.set_page_config(
    page_title="학생 채팅 | Commerce X Commerce",
    page_icon="💬",
    layout="centered",
    initial_sidebar_state="collapsed",
)

render_chat()
