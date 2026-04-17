# =============================================================================
# Phase 4 — 시니어·주니어 지식 자산 네트워크
# =============================================================================

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from phase4_senior.app import render_network

st.set_page_config(
    page_title="시니어 자산 네트워크 | Commerce X Commerce",
    page_icon="🔗",
    layout="wide",
    initial_sidebar_state="expanded",
)

render_network()
