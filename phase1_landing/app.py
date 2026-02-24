# =============================================================================
# AI Commerce School — Phase 1: 랜딩페이지
# =============================================================================
# 목적: 시장 반응 검증 + 사전 신청자 수집
# 배포: Streamlit Cloud
# 데이터: Google Sheets (Fallback: 로컬 CSV)
# =============================================================================
#
# 실행:
#   streamlit run streamlit_app.py
#
# Secrets 설정 (Streamlit Cloud → Settings → Secrets):
#   [gcp_service_account]
#   type = "service_account"
#   project_id = "your-project-id"
#   private_key_id = "..."
#   private_key = "-----BEGIN RSA PRIVATE KEY-----\n..."
#   client_email = "..."
#   client_id = "..."
#   auth_uri = "..."
#   token_uri = "..."
#
#   [sheets]
#   spreadsheet_id = "your-spreadsheet-id"
#   worksheet_name = "신청자"
# =============================================================================

import sys
from pathlib import Path

# 모듈 경로 표준화 (로컬 + Streamlit Cloud 호환)
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from shared.config import PAGE_CONFIG, APP_NAME, APP_TAGLINE
from phase1_landing.components import (
    inject_global_css,
    render_hero,
    render_stats,
    render_problem,
    render_solution,
    render_targets,
    render_curriculum,
    render_differentiators,
    render_application_form,
    render_footer,
)

# ---------------------------------------------------------------------------
# 페이지 초기화
# ---------------------------------------------------------------------------
st.set_page_config(**PAGE_CONFIG)
inject_global_css()

# ---------------------------------------------------------------------------
# 네비게이션 (고정 상단바 시뮬레이션)
# ---------------------------------------------------------------------------
nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
with nav_col1:
    st.markdown(f"""
    <div style="padding:16px 10%; font-size:1.1rem; font-weight:800; color:#6C63FF;">
        🛒 {APP_NAME}
    </div>
    """, unsafe_allow_html=True)
with nav_col3:
    st.markdown("""
    <div style="padding:12px 10%; text-align:right;">
        <a href="#apply" style="background:#6C63FF; color:white; padding:8px 20px;
           border-radius:20px; font-size:0.85rem; font-weight:600; text-decoration:none;">
            사전 신청
        </a>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 메인 콘텐츠 (섹션 순서 = 전환율 최적화 기준)
# ---------------------------------------------------------------------------
render_hero()           # 1. 히어로 — 슬로건 + CTA
render_stats()          # 2. 소셜 프루프 — 수치 신뢰감
render_problem()        # 3. 문제 정의 — 공감 형성
render_solution()       # 4. 해결책 — 3층 AI 구조
render_targets()        # 5. 대상 세그먼트 — "나를 위한 것"
render_curriculum()     # 6. 10주 커리큘럼 — 구체성 제공
render_differentiators()# 7. 차별점 — 경쟁 우위
render_application_form()# 8. 신청 폼 — 행동 유도 (CTA)
render_footer()         # 9. 푸터
