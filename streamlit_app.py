# =============================================================================
# Commerce X Commerce — 메인 진입점
# =============================================================================

import sys
from pathlib import Path

ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

pg = st.navigation([
    st.Page("pages/0_home.py",        title="홈",                    icon="🏠", default=True),
    st.Page("pages/1_onboarding.py",  title="강사 온보딩",           icon="👨‍🏫"),
    st.Page("pages/2_chat.py",        title="학생 채팅",             icon="💬"),
    st.Page("pages/3_dashboard.py",   title="역량 진단",             icon="📊"),
    st.Page("pages/4_network.py",     title="시니어 자산 네트워크",  icon="🔗"),
])
pg.run()
