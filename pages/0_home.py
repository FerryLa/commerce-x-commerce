import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

import streamlit as st
from shared.config import APP_NAME
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

inject_global_css()

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

render_hero()
render_stats()
render_one_on_one()
render_problem()
render_ai_tools()
render_solution()
render_targets()
render_curriculum()
render_cta_banner()
render_application_form()
render_footer()
