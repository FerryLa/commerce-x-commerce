# =============================================================================
# Phase 3 — 이커머스 역량 진단 대시보드 (Streamlit Multipage 진입점)
# =============================================================================

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from phase3_dashboard.app import render_dashboard

st.set_page_config(
    page_title="역량 진단 | Commerce X Commerce",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

render_dashboard()
