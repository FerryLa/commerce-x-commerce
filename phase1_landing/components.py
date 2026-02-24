# =============================================================================
# AI Commerce School — 랜딩페이지 UI 컴포넌트
# =============================================================================
# 각 섹션을 독립 함수로 분리 → 재사용성 + 유지보수성 확보
# =============================================================================

import streamlit as st
import sys
from pathlib import Path

# shared 모듈 경로 등록
sys.path.insert(0, str(Path(__file__).parent.parent))
from shared.config import (
    APP_NAME, APP_SLOGAN, BRAND_COLORS,
    CURRICULUM, TARGET_SEGMENTS, DIFFERENTIATORS, SOCIAL_PROOF,
)


# ---------------------------------------------------------------------------
# 전역 CSS 주입
# ---------------------------------------------------------------------------

def inject_global_css() -> None:
    """다크 테마 + 브랜드 컬러 시스템 적용."""
    c = BRAND_COLORS
    st.markdown(f"""
    <style>
    /* ── 기반 리셋 ─────────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Pretendard:wght@300;400;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: {c['dark']};
        color: {c['text']};
    }}
    .stApp {{ background-color: {c['dark']}; }}
    .block-container {{ padding: 0 !important; max-width: 100% !important; }}

    /* ── 섹션 공통 ─────────────────────────────────────────────────────── */
    .section {{
        padding: 80px 10%;
    }}
    .section-alt {{
        padding: 80px 10%;
        background-color: {c['surface']};
    }}

    /* ── 히어로 ─────────────────────────────────────────────────────────── */
    .hero {{
        background: linear-gradient(135deg, {c['dark']} 0%, #0f3460 50%, {c['dark']} 100%);
        padding: 120px 10% 100px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }}
    .hero::before {{
        content: '';
        position: absolute;
        width: 600px; height: 600px;
        border-radius: 50%;
        background: radial-gradient(circle, {c['primary']}22 0%, transparent 70%);
        top: -200px; right: -100px;
    }}
    .hero-badge {{
        display: inline-block;
        background: {c['primary']}33;
        border: 1px solid {c['primary']};
        color: {c['primary']};
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 24px;
        letter-spacing: 0.05em;
    }}
    .hero-title {{
        font-size: clamp(2rem, 5vw, 3.5rem);
        font-weight: 800;
        line-height: 1.2;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #ffffff 0%, {c['accent']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .hero-sub {{
        font-size: 1.15rem;
        color: {c['muted']};
        margin-bottom: 40px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.7;
    }}

    /* ── 버튼 ───────────────────────────────────────────────────────────── */
    .cta-btn {{
        display: inline-block;
        background: linear-gradient(135deg, {c['primary']}, {c['secondary']});
        color: white !important;
        font-size: 1.1rem;
        font-weight: 700;
        padding: 16px 40px;
        border-radius: 50px;
        border: none;
        cursor: pointer;
        text-decoration: none;
        box-shadow: 0 8px 30px {c['primary']}55;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    .cta-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 12px 40px {c['primary']}77;
    }}
    .cta-btn-secondary {{
        display: inline-block;
        background: transparent;
        color: {c['text']} !important;
        font-size: 1rem;
        font-weight: 600;
        padding: 14px 32px;
        border-radius: 50px;
        border: 1px solid {c['muted']};
        cursor: pointer;
        text-decoration: none;
        margin-left: 16px;
        transition: border-color 0.2s;
    }}
    .cta-btn-secondary:hover {{ border-color: {c['primary']}; }}

    /* ── 카드 ───────────────────────────────────────────────────────────── */
    .card {{
        background: {c['surface']};
        border: 1px solid #ffffff11;
        border-radius: 16px;
        padding: 28px;
        height: 100%;
        transition: border-color 0.3s, transform 0.3s;
    }}
    .card:hover {{
        border-color: {c['primary']}55;
        transform: translateY(-4px);
    }}
    .card-icon {{ font-size: 2rem; margin-bottom: 12px; }}
    .card-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: white;
        margin-bottom: 8px;
    }}
    .card-desc {{
        font-size: 0.9rem;
        color: {c['muted']};
        line-height: 1.6;
        white-space: pre-line;
    }}

    /* ── 통계 배지 ──────────────────────────────────────────────────────── */
    .stat-box {{
        text-align: center;
        padding: 24px;
    }}
    .stat-number {{
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, {c['primary']}, {c['accent']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    .stat-label {{
        font-size: 0.9rem;
        color: {c['muted']};
        margin-top: 4px;
    }}

    /* ── 커리큘럼 타임라인 ──────────────────────────────────────────────── */
    .timeline-item {{
        display: flex;
        gap: 20px;
        margin-bottom: 28px;
        padding: 20px;
        border-left: 3px solid {c['primary']};
        background: {c['surface']};
        border-radius: 0 12px 12px 0;
    }}
    .timeline-week {{
        font-size: 0.8rem;
        font-weight: 700;
        color: {c['primary']};
        white-space: nowrap;
        min-width: 60px;
        padding-top: 2px;
    }}
    .timeline-content {{ flex: 1; }}
    .timeline-topic {{
        font-size: 1rem;
        font-weight: 700;
        color: white;
        margin-bottom: 4px;
    }}
    .timeline-desc {{ font-size: 0.85rem; color: {c['muted']}; }}
    .timeline-output {{
        font-size: 0.82rem;
        color: {c['accent']};
        margin-top: 6px;
        font-weight: 600;
    }}

    /* ── 섹션 제목 ──────────────────────────────────────────────────────── */
    .section-title {{
        font-size: clamp(1.6rem, 3vw, 2.2rem);
        font-weight: 800;
        color: white;
        margin-bottom: 8px;
    }}
    .section-subtitle {{
        font-size: 1rem;
        color: {c['muted']};
        margin-bottom: 48px;
        line-height: 1.6;
    }}

    /* ── 구분선 ─────────────────────────────────────────────────────────── */
    .divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, {c['primary']}44, transparent);
        margin: 0 10%;
    }}

    /* ── 폼 ─────────────────────────────────────────────────────────────── */
    .form-section {{
        background: linear-gradient(135deg, {c['surface']}, #0f3460);
        border: 1px solid {c['primary']}33;
        border-radius: 24px;
        padding: 48px;
        max-width: 680px;
        margin: 0 auto;
    }}
    .form-title {{
        font-size: 1.6rem;
        font-weight: 800;
        color: white;
        margin-bottom: 8px;
        text-align: center;
    }}
    .form-subtitle {{
        font-size: 0.95rem;
        color: {c['muted']};
        text-align: center;
        margin-bottom: 32px;
    }}

    /* Streamlit 기본 요소 오버라이드 */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select {{
        background-color: #0a0a1a !important;
        border-color: #ffffff22 !important;
        color: {c['text']} !important;
        border-radius: 10px !important;
    }}
    .stButton > button {{
        background: linear-gradient(135deg, {c['primary']}, {c['secondary']}) !important;
        color: white !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 12px 32px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        width: 100% !important;
        box-shadow: 0 6px 20px {c['primary']}44 !important;
    }}

    /* ── 푸터 ───────────────────────────────────────────────────────────── */
    .footer {{
        text-align: center;
        padding: 48px 10%;
        border-top: 1px solid #ffffff11;
        color: {c['muted']};
        font-size: 0.85rem;
    }}
    .footer-brand {{
        font-size: 1.1rem;
        font-weight: 700;
        color: {c['primary']};
        margin-bottom: 8px;
    }}
    </style>
    """, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 섹션별 컴포넌트
# ---------------------------------------------------------------------------

def render_hero() -> None:
    """히어로 섹션 — 슬로건 + CTA."""
    st.markdown(f"""
    <div class="hero">
        <div class="hero-badge">🚀 2026 BETA 오픈 — 선착순 50명</div>
        <h1 class="hero-title">
            10주 안에<br>이커머스 실무 포트폴리오 완성
        </h1>
        <p class="hero-sub">
            비전공자도, 부트캠프 수료자도, 경력 전환자도<br>
            AI를 활용해 이커머스에서 바로 생산성을 낼 수 있는 인재가 됩니다.
        </p>
        <p style="font-size:0.95rem; color:#888; margin-top: 12px;">
            이론 → 재현 → 배포 → <span style="color:#4ECDC4; font-weight:700;">KPI 연결</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


def render_stats() -> None:
    """소셜 프루프 통계 배지."""
    st.markdown('<div class="section" style="padding-top:60px; padding-bottom:60px;">', unsafe_allow_html=True)
    cols = st.columns(len(SOCIAL_PROOF))
    for col, item in zip(cols, SOCIAL_PROOF):
        with col:
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{item['stat']}</div>
                <div class="stat-label">{item['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)


def render_problem() -> None:
    """문제 정의 섹션 — 왜 지금인가."""
    st.markdown("""
    <div class="section-alt">
        <div class="section-title">왜 지금인가?</div>
        <div class="section-subtitle">
            AI 시대가 열리며 채용 시장 구조가 바뀌고 있습니다.<br>
            기업은 이제 "바로 생산성을 낼 수 있는 AI 인재"만을 원합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    problems = [
        ("🤖", "AI 도래로 채용 축소", "단순 주니어 직무는 줄어들고 있습니다. 기업은 AI를 활용해 바로 생산성을 낼 수 있는 인재를 원합니다."),
        ("🔗", "교육-채용 구조적 단절", "부트캠프 졸업생은 넘치나, 기업이 원하는 실무 역량과의 괴리가 큽니다."),
        ("📚", "이론만 있고 실무 재현 없음", "이론 중심 교육으로는 실제 업무 수행 능력을 검증할 수 없습니다."),
        ("💼", "AI를 배웠지만 직무 연결 안 됨", "AI 도구는 배웠지만 실제 이커머스 직무에 적용하는 법을 모릅니다."),
    ]

    st.markdown('<div class="section-alt" style="padding-top:0;">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, (icon, title, desc) in enumerate(problems):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="card" style="margin-bottom:16px;">
                <div class="card-icon">{icon}</div>
                <div class="card-title">{title}</div>
                <div class="card-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_solution() -> None:
    """3층 AI 구조 해결책 섹션."""
    st.markdown("""
    <div class="section">
        <div class="section-title">우리의 해결 방식</div>
        <div class="section-subtitle">
            단순 교육이 아닌, AI 기반 이커머스 인재 공급 인프라입니다.<br>
            3층 구조로 학습 격차부터 채용까지 연결합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    layers = [
        {
            "layer": "Layer 1", "color": "#4ECDC4",
            "icon": "🤖", "title": "AI 코치 (기본 제공)",
            "desc": "모든 학습자에게 제공되는 AI 기반 학습 지원 시스템. 기초 개념 재설명, 실습 가이드, 개인화 학습 경로 제공으로 비전공자의 학습 격차를 제거합니다.",
            "tag": "학습 격차 제거",
        },
        {
            "layer": "Layer 2", "color": "#6C63FF",
            "icon": "👥", "title": "C2C 직무 멘토 (인간 강사)",
            "desc": "현직 이커머스 실무자가 1:1 멘토로 참여합니다. 포트폴리오 첨삭, 실무 시뮬레이션, 채용 관점 피드백으로 실무 신뢰도를 구축합니다.",
            "tag": "실무 신뢰도",
        },
        {
            "layer": "Layer 3", "color": "#FF6B6B",
            "icon": "🧠", "title": "AI 강사 복제 모델",
            "desc": "강사의 노하우를 AI가 학습해 분신을 생성합니다. 학생은 저가로 AI 강사를, 고가로 실제 강사를 이용. 강사 1명이 수백 명을 동시 코칭 가능합니다.",
            "tag": "확장성 확보",
        },
    ]

    st.markdown('<div class="section" style="padding-top:0;">', unsafe_allow_html=True)
    for layer in layers:
        st.markdown(f"""
        <div class="card" style="margin-bottom:20px; border-left: 4px solid {layer['color']};">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px;">
                <div style="flex:1;">
                    <div style="font-size:0.75rem; font-weight:700; color:{layer['color']}; letter-spacing:0.1em; margin-bottom:6px;">
                        {layer['layer']} ·
                        <span style="background:{layer['color']}22; padding: 2px 10px; border-radius:20px;">
                            {layer['tag']}
                        </span>
                    </div>
                    <div class="card-title">{layer['icon']} {layer['title']}</div>
                    <div class="card-desc">{layer['desc']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_targets() -> None:
    """대상 세그먼트 섹션."""
    st.markdown("""
    <div class="section-alt">
        <div class="section-title">이런 분들을 위한 트랙입니다</div>
        <div class="section-subtitle">이커머스 업계 취업을 원하는 모든 분들을 위해 설계되었습니다.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-alt" style="padding-top:0;">', unsafe_allow_html=True)
    cols = st.columns(3)
    for col, seg in zip(cols, TARGET_SEGMENTS):
        with col:
            st.markdown(f"""
            <div class="card">
                <div class="card-icon">{seg['icon']}</div>
                <div class="card-title">{seg['title']}</div>
                <div class="card-desc">{seg['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_curriculum() -> None:
    """10주 커리큘럼 타임라인 섹션."""
    st.markdown("""
    <div class="section">
        <div class="section-title">📅 10주 실무 트랙</div>
        <div class="section-subtitle">
            이론 → 재현 → 배포 → KPI 연결의 4단계 구조로<br>
            졸업 시 KPI 기반 포트폴리오를 완성합니다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section" style="padding-top:0; max-width:800px; margin:0 auto;">', unsafe_allow_html=True)
    for item in CURRICULUM:
        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-week">{item['week']}</div>
            <div class="timeline-content">
                <div class="timeline-topic">{item['topic']}</div>
                <div class="timeline-desc">{item['content']}</div>
                <div class="timeline-output">📌 결과물: {item['output']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_differentiators() -> None:
    """차별화 포인트 섹션."""
    st.markdown("""
    <div class="section-alt">
        <div class="section-title">AI Commerce School의 차별점</div>
        <div class="section-subtitle">기존 부트캠프, 온라인 강의와는 다릅니다.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-alt" style="padding-top:0;">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, diff in enumerate(DIFFERENTIATORS):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="card" style="margin-bottom:16px;">
                <div class="card-icon">{diff['icon']}</div>
                <div class="card-title">{diff['title']}</div>
                <div class="card-desc">{diff['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_application_form() -> None:
    """사전 신청 폼 섹션."""
    st.markdown("""
    <div class="section" id="apply">
        <div class="section-title" style="text-align:center;">🎯 사전 신청하기</div>
        <div class="section-subtitle" style="text-align:center;">
            선착순 50명 · 얼리버드 혜택 제공 · 합격 기준 없음<br>
            <span style="color:#FF6B6B; font-weight:600;">신청 후 48시간 내 안내 연락드립니다</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 폼은 Streamlit 네이티브 컴포넌트 사용 (보안 + 상태관리)
    with st.container():
        col_l, col_form, col_r = st.columns([1, 2, 1])
        with col_form:
            st.markdown('<div class="form-section">', unsafe_allow_html=True)

            name = st.text_input("이름 *", placeholder="홍길동")
            email = st.text_input("이메일 *", placeholder="example@email.com")
            phone = st.text_input("연락처 *", placeholder="010-1234-5678")

            background = st.selectbox(
                "현재 배경 *",
                options=["선택해주세요", "비전공자 (이커머스 취업 희망)", "부트캠프 수료자", "경력 전환자 (타 업종 → 이커머스)", "기타"],
                index=0,
            )

            track = st.selectbox(
                "관심 트랙",
                options=["AI 퍼포먼스 마케팅 (1기 오픈)", "AI 이커머스 오퍼레이터 (예정)", "AI 데이터 분석가 (예정)"],
            )

            motivation = st.text_area(
                "신청 동기 (선택)",
                placeholder="간단하게 왜 신청하셨는지 알려주세요. 커리큘럼 설계에 반영됩니다.",
                height=100,
            )

            source = st.selectbox(
                "어디서 알게 되셨나요?",
                options=["SNS", "유튜브", "지인 추천", "블로그/뉴스", "검색", "기타"],
            )

            st.markdown("<br>", unsafe_allow_html=True)

            submitted = st.button("🚀 무료 사전 신청하기", use_container_width=True)

            if submitted:
                _handle_form_submission({
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "background": background if background != "선택해주세요" else "",
                    "track": track,
                    "motivation": motivation,
                    "source": source,
                })

            st.markdown('</div>', unsafe_allow_html=True)

    # 신뢰 배지
    st.markdown("""
    <div style="text-align:center; padding: 24px 0; color: #888; font-size:0.85rem;">
        🔒 개인정보는 신청 안내 외 절대 사용되지 않습니다 &nbsp;·&nbsp;
        ✉️ 48시간 내 연락 &nbsp;·&nbsp;
        ❌ 합격 기준 없음
    </div>
    """, unsafe_allow_html=True)


def _handle_form_submission(form_data: dict) -> None:
    """폼 제출 처리 (유효성 검사 → 저장 → 피드백)."""
    from phase1_landing.sheets_connector import validate_application, append_application

    errors = validate_application(form_data)

    if errors:
        for err in errors:
            st.error(f"⚠️ {err}")
        return

    with st.spinner("신청 정보를 저장하는 중..."):
        result = append_application(form_data)

    if result["success"]:
        st.success("✅ 사전 신청이 완료되었습니다! 48시간 내에 연락드리겠습니다. 🎉")
        st.balloons()
    else:
        st.error(f"❌ {result['message']}")


def render_footer() -> None:
    """푸터."""
    st.markdown("""
    <div class="footer">
        <div class="footer-brand">AI Commerce School</div>
        <div>이커머스 산업 특화 AI 실무 인재 양성 플랫폼</div>
        <br>
        <div>© 2026 AI Commerce School. All rights reserved. &nbsp;·&nbsp; Confidential MVP</div>
    </div>
    """, unsafe_allow_html=True)
