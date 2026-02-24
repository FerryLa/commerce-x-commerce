# =============================================================================
# Commerce X Commerce — Phase 1: 랜딩페이지
# =============================================================================
# 목적: 시장 반응 검증 + 사전 신청자 수집
# 배포: Streamlit Cloud  |  실행: streamlit run streamlit_app.py
# =============================================================================

import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from shared.config import PAGE_CONFIG, APP_NAME
from phase1_landing.components import (
    inject_global_css,
    render_hero,
    render_stats,
    render_one_on_one,
    render_problem,
    render_ai_tools,
    render_solution,
    render_targets,
    render_curriculum,
    render_cta_banner,
    render_application_form,
    render_footer,
)

# ---------------------------------------------------------------------------
# 페이지 초기화
# ---------------------------------------------------------------------------
st.set_page_config(**PAGE_CONFIG)
inject_global_css()

# ---------------------------------------------------------------------------
# 미니멀 네비게이션 바
# ---------------------------------------------------------------------------
nav_l, _, nav_r = st.columns([1, 4, 1])
with nav_l:
    st.markdown(f"""
    <div style="padding:18px 8%; font-size:1rem; font-weight:900;
                color:#111; letter-spacing:-0.02em;">
        {APP_NAME}
    </div>
    """, unsafe_allow_html=True)
with nav_r:
    st.markdown("""
    <div style="padding:14px 8%; text-align:right;">
        <a href="#apply"
           style="background:#FA5D29; color:#FFF; padding:9px 22px;
                  border-radius:100px; font-size:0.82rem; font-weight:700;
                  text-decoration:none; letter-spacing:-0.01em;">
            사전 신청
        </a>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div style="height:1px; background:#E8E8E8;"></div>', unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 섹션 순서 (전환율 최적화)
# ---------------------------------------------------------------------------
render_hero()             # 1. 히어로 — 1:1 가치 제안 + CTA
render_stats()            # 2. 소셜 프루프 숫자
render_one_on_one()       # 3. 기존 강의 vs 1:1 AI 비교 (핵심 차별화)
render_problem()          # 4. 문제 정의 — 공감
render_ai_tools()         # 5. 실전 AI 도구 목록
render_solution()         # 6. 3층 AI 구조
render_targets()          # 7. 대상 세그먼트
render_curriculum()       # 8. 10주 커리큘럼
render_cta_banner()       # 9. 풀너비 취업 연결 배너
render_application_form() # 10. 신청 폼
render_footer()           # 11. 푸터
