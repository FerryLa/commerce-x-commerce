# =============================================================================
# Commerce X Commerce — 랜딩페이지 UI 컴포넌트
# =============================================================================
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from shared.config import (
    APP_NAME, BRAND_COLORS,
    CURRICULUM, TARGET_SEGMENTS,
    SOCIAL_PROOF, AI_TOOLS, ONE_ON_ONE_COMPARE,
)

C = BRAND_COLORS


# ---------------------------------------------------------------------------
# 전역 CSS  (style 블록은 Markdown 코드블록 규칙 영향 없음)
# ---------------------------------------------------------------------------

def inject_global_css() -> None:
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter+Tight:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');
html,body,[class*="css"],.stApp,p,span,div,h1,h2,h3,h4,label,button{font-family:'Inter Tight',-apple-system,BlinkMacSystemFont,sans-serif!important}
html,body,.stApp{background:#FFFFFF!important;color:#111!important}
.block-container{padding:0!important;max-width:100%!important}
header[data-testid="stHeader"]{background:transparent!important;box-shadow:none!important}
[data-testid="stSidebarNav"],[data-testid="stSidebar"]{display:none!important}
.display{font-size:clamp(44px,6vw,104px);font-weight:900;line-height:1.0;letter-spacing:-0.03em;color:#111;margin:0}
.display-md{font-size:clamp(32px,4vw,64px);font-weight:800;line-height:1.1;letter-spacing:-0.025em;color:#111;margin:0}
.display-sm{font-size:clamp(18px,2vw,26px);font-weight:700;line-height:1.2;letter-spacing:-0.015em;color:#111;margin:0}
.overline{font-size:.75rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#FA5D29}
.body-lg{font-size:1.05rem;color:#555;line-height:1.75;font-weight:400}
.body-sm{font-size:.88rem;color:#888;line-height:1.6}
.section{padding:96px 8%}
.section-alt{padding:96px 8%;background:#F7F7F7}
.section-dark{padding:96px 8%;background:#111111}
.tag{display:inline-block;background:#FFF0EB;border:1.5px solid #FA5D29;color:#FA5D29;padding:5px 14px;border-radius:100px;font-size:.75rem;font-weight:700;letter-spacing:.06em;margin-bottom:24px}
.btn{display:inline-block;background:#FA5D29;color:#FFF!important;font-weight:700;font-size:.95rem;padding:14px 36px;border-radius:100px;text-decoration:none!important;letter-spacing:-.01em;transition:background .2s,transform .15s}
.btn:hover{background:#D94E20;transform:translateY(-2px)}
.btn-ghost{display:inline-block;background:transparent;color:#111!important;font-weight:600;font-size:.95rem;padding:13px 32px;border-radius:100px;border:1.5px solid #CCC;text-decoration:none!important;margin-left:12px;transition:border-color .2s,color .2s}
.btn-ghost:hover{border-color:#FA5D29;color:#FA5D29!important}
.btn-white{display:inline-block;background:#FFF;color:#FA5D29!important;font-weight:800;font-size:.95rem;padding:14px 36px;border-radius:100px;text-decoration:none!important;transition:transform .15s,box-shadow .15s}
.btn-white:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,0,0,.15)}
.card{background:#FFF;border:1px solid #E8E8E8;border-radius:20px;padding:32px;height:100%;transition:border-color .25s,box-shadow .25s,transform .25s}
.card:hover{border-color:#FA5D29;box-shadow:0 8px 32px rgba(250,93,41,.1);transform:translateY(-4px)}
.stat-num{font-size:clamp(36px,4vw,68px);font-weight:900;color:#FA5D29;letter-spacing:-.04em;line-height:1.0}
.stat-lbl{font-size:.85rem;color:#888;font-weight:500;margin-top:4px}
.cmp-table{border:1px solid #E8E8E8;border-radius:20px;overflow:hidden;width:100%}
.cmp-head-l{padding:18px 28px;background:#F7F7F7;border-bottom:1px solid #E8E8E8;font-size:.74rem;font-weight:700;color:#999;letter-spacing:.12em;text-transform:uppercase}
.cmp-head-r{padding:18px 28px;background:#FFF8F5;border-bottom:1px solid #E8E8E8;font-size:.74rem;font-weight:700;color:#FA5D29;letter-spacing:.12em;text-transform:uppercase}
.cmp-l{padding:14px 28px;font-size:.9rem;color:#AAA;border-bottom:1px solid #F3F3F3}
.cmp-r{padding:14px 28px;font-size:.9rem;font-weight:600;border-bottom:1px solid #F3F3F3;background:#FFFCFA}
.cmp-l-last{padding:14px 28px;font-size:.9rem;color:#AAA}
.cmp-r-last{padding:14px 28px;font-size:.9rem;font-weight:700;color:#FA5D29;background:#FFF8F5}
.tl-row{display:flex;gap:28px;padding:22px 0;border-bottom:1px solid #F0F0F0;align-items:flex-start}
.tl-row:last-child{border-bottom:none}
.tl-wk{font-size:.7rem;font-weight:800;color:#FA5D29;min-width:68px;padding-top:3px;letter-spacing:.08em;text-transform:uppercase}
.tl-top{font-size:.95rem;font-weight:700;color:#111}
.tl-sub{font-size:.83rem;color:#888;margin-top:2px}
.tl-out{font-size:.78rem;font-weight:700;color:#FA5D29;margin-top:5px}
.cta-banner{background:#FA5D29;padding:96px 8%;text-align:center}
.footer-wrap{padding:56px 8%;border-top:1px solid #E8E8E8;background:#FFF}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{border-radius:12px!important;border:1.5px solid #E8E8E8!important;background:#FAFAFA!important;color:#111!important;font-family:'Inter Tight',sans-serif!important;font-size:.92rem!important}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{border-color:#FA5D29!important;box-shadow:0 0 0 3px rgba(250,93,41,.12)!important;background:#FFF!important}
.stSelectbox>div>div{border-radius:12px!important;border:1.5px solid #E8E8E8!important;background:#FAFAFA!important;font-family:'Inter Tight',sans-serif!important}
.stButton>button{background:#FA5D29!important;color:#FFF!important;border:none!important;border-radius:100px!important;padding:14px 32px!important;font-weight:700!important;font-size:.95rem!important;width:100%!important;font-family:'Inter Tight',sans-serif!important;letter-spacing:-.01em!important}
.stButton>button:hover{background:#D94E20!important}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 헬퍼: HTML을 안전하게 렌더링 (동적 콘텐츠는 여기로)
# ---------------------------------------------------------------------------

def _md(html: str) -> None:
    """단일 문자열로 구성된 HTML을 렌더링. Markdown 코드블록 오탐 방지."""
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# 1. 히어로  (정적 HTML — triple-quote 사용 가능)
# ---------------------------------------------------------------------------

def render_hero() -> None:
    _md('<div style="padding:120px 8% 96px;background:#FFF;border-bottom:1px solid #E8E8E8">'
        '<div class="tag">2026 BETA · 선착순 50명 모집</div>'
        '<h1 class="display">1:1 AI 커리큘럼으로<br>이커머스 취업을<br>'
        '<span style="color:#FA5D29">실현합니다</span></h1>'
        '<p class="body-lg" style="margin:28px 0 44px;max-width:540px">'
        '비전공자도, 부트캠프 수료자도, 경력 전환자도 —<br>'
        'AI 도구를 실전 활용해 10주 안에 KPI 포트폴리오를 완성합니다.</p>'
        '<a href="#apply" class="btn">무료 사전 신청 →</a>'
        '<a href="#curriculum" class="btn-ghost">커리큘럼 보기</a>'
        '</div>')


# ---------------------------------------------------------------------------
# 2. 소셜 프루프 숫자
# ---------------------------------------------------------------------------

def render_stats() -> None:
    items = "".join(
        f'<div style="text-align:center;padding:8px 0">'
        f'<div class="stat-num">{item["stat"]}</div>'
        f'<div class="stat-lbl">{item["label"]}</div>'
        f'</div>'
        for item in SOCIAL_PROOF
    )
    n = len(SOCIAL_PROOF)
    _md(f'<div style="padding:56px 8%;border-bottom:1px solid #E8E8E8">'
        f'<div style="display:grid;grid-template-columns:repeat({n},1fr);gap:32px">'
        f'{items}</div></div>')


# ---------------------------------------------------------------------------
# 3. 1:1 vs 기존 비교
# ---------------------------------------------------------------------------

def render_one_on_one() -> None:
    rows = ""
    for i, (bad, good) in enumerate(ONE_ON_ONE_COMPARE):
        last = i == len(ONE_ON_ONE_COMPARE) - 1
        lc = "cmp-l-last" if last else "cmp-l"
        rc = "cmp-r-last" if last else "cmp-r"
        rows += (f'<div style="display:grid;grid-template-columns:1fr 1fr">'
                 f'<div class="{lc}">{bad}</div>'
                 f'<div class="{rc}">{good}</div></div>')

    _md('<div class="section">'
        '<div class="overline" style="margin-bottom:16px">핵심 차별점</div>'
        '<h2 class="display-md">기존 강의와<br>다릅니다</h2>'
        '<p class="body-lg" style="margin:20px 0 52px;max-width:460px">'
        '열 명이 앉아 같은 속도로 듣는 강의 대신,<br>당신만을 위한 1:1 AI 커리큘럼.</p>'
        '<div style="max-width:640px">'
        '<div class="cmp-table">'
        '<div style="display:grid;grid-template-columns:1fr 1fr">'
        '<div class="cmp-head-l">기존 강의</div>'
        '<div class="cmp-head-r">Commerce X Commerce</div></div>'
        + rows +
        '</div></div></div>')


# ---------------------------------------------------------------------------
# 4. 문제 정의
# ---------------------------------------------------------------------------

def render_problem() -> None:
    problems = [
        ("AI 도래로 채용 축소",
         "단순 주니어 직무는 줄어들고 있습니다. 기업은 AI로 바로 생산성을 낼 인재를 원합니다."),
        ("교육-채용 구조적 단절",
         "부트캠프 졸업생은 넘치지만, 기업이 원하는 실무 역량과 괴리가 큽니다."),
        ("이론만 있고 실무 재현 없음",
         "이론 중심 교육으로는 실제 업무 수행 능력을 검증할 수 없습니다."),
        ("AI 배웠지만 직무 연결 안 됨",
         "AI 도구는 알지만 이커머스 직무에 적용하는 법을 모릅니다."),
    ]
    cards = "".join(
        f'<div class="card">'
        f'<div class="overline" style="margin-bottom:10px">0{i+1}</div>'
        f'<div class="display-sm" style="margin-bottom:10px">{title}</div>'
        f'<p class="body-sm">{desc}</p></div>'
        for i, (title, desc) in enumerate(problems)
    )
    _md('<div class="section-alt">'
        '<div class="overline" style="margin-bottom:16px">왜 지금인가</div>'
        '<h2 class="display-md">AI 시대,<br>채용 시장이 바뀌고 있습니다</h2>'
        '<p class="body-lg" style="margin:20px 0 52px;max-width:500px">'
        '기업은 이제 "바로 생산성을 낼 수 있는 AI 인재"만을 원합니다.</p>'
        f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">{cards}</div>'
        '</div>')


# ---------------------------------------------------------------------------
# 5. AI 도구 실습
# ---------------------------------------------------------------------------

def render_ai_tools() -> None:
    tools = "".join(
        f'<div class="card" style="text-align:center">'
        f'<div class="display-sm" style="margin-bottom:6px">{t["name"]}</div>'
        f'<p class="body-sm">{t["desc"]}</p></div>'
        for t in AI_TOOLS
    )
    _md('<div class="section">'
        '<div class="overline" style="margin-bottom:16px">실전 도구</div>'
        '<h2 class="display-md">이론 말고,<br>실제 도구를 씁니다</h2>'
        '<p class="body-lg" style="margin:20px 0 52px;max-width:460px">'
        '현업에서 쓰는 AI 도구를 직접 다루며 포트폴리오를 만듭니다.</p>'
        f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px">{tools}</div>'
        '</div>')


# ---------------------------------------------------------------------------
# 6. 해결책 — 3층 AI 구조
# ---------------------------------------------------------------------------

def render_solution() -> None:
    layers = [
        ("Layer 1", "#2BC0B8", "AI 코치",      "학습 격차 제거",
         "모든 학습자에게 제공. 기초 개념 재설명·실습 가이드·개인 학습 경로로 비전공자의 격차를 제거합니다."),
        ("Layer 2", "#FA5D29", "C2C 직무 멘토", "실무 신뢰도",
         "현직 이커머스 실무자가 1:1 멘토로 참여. 포트폴리오 첨삭·시뮬레이션·채용 관점 피드백."),
        ("Layer 3", "#502BD8", "AI 강사 복제",  "확장성 확보",
         "강사 노하우를 AI가 학습해 분신을 생성. 저가로 AI 강사를, 고가로 실제 강사를 이용."),
    ]
    cards = "".join(
        f'<div class="card" style="margin-bottom:16px;border-left:4px solid {c};border-radius:0 20px 20px 0">'
        f'<div style="font-size:.7rem;font-weight:800;color:{c};letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px">'
        f'{lid} &nbsp;·&nbsp;<span style="background:{c}22;padding:2px 10px;border-radius:100px">{tag}</span></div>'
        f'<div class="display-sm" style="margin-bottom:8px">{title}</div>'
        f'<p class="body-sm">{desc}</p></div>'
        for lid, c, title, tag, desc in layers
    )
    _md('<div class="section-alt">'
        '<div class="overline" style="margin-bottom:16px">해결 방식</div>'
        '<h2 class="display-md">3층 AI 구조로<br>학습부터 채용까지</h2>'
        '<p class="body-lg" style="margin:20px 0 52px;max-width:500px">'
        '단순 교육이 아닌, AI 기반 이커머스 인재 공급 인프라입니다.</p>'
        + cards +
        '</div>')


# ---------------------------------------------------------------------------
# 7. 대상 세그먼트
# ---------------------------------------------------------------------------

def render_targets() -> None:
    segs = "".join(
        f'<div class="card">'
        f'<div class="display-sm" style="margin-bottom:10px">{s["title"]}</div>'
        f'<p class="body-sm" style="white-space:pre-line">{s["desc"]}</p></div>'
        for s in TARGET_SEGMENTS
    )
    _md('<div class="section">'
        '<div class="overline" style="margin-bottom:16px">대상</div>'
        '<h2 class="display-md">이런 분들을 위해<br>설계했습니다</h2>'
        '<p class="body-lg" style="margin:20px 0 52px;max-width:460px">'
        '이커머스 업계 취업을 원하는 모든 분.</p>'
        f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px">{segs}</div>'
        '</div>')


# ---------------------------------------------------------------------------
# 8. 10주 커리큘럼
# ---------------------------------------------------------------------------

def render_curriculum() -> None:
    rows = "".join(
        f'<div class="tl-row">'
        f'<div class="tl-wk">{item["week"]}</div>'
        f'<div style="flex:1">'
        f'<div class="tl-top">{item["topic"]}</div>'
        f'<div class="tl-sub">{item["content"]}</div>'
        f'<div class="tl-out">→ {item["output"]}</div>'
        f'</div></div>'
        for item in CURRICULUM
    )
    _md('<div class="section-alt" id="curriculum">'
        '<div class="overline" style="margin-bottom:16px">커리큘럼</div>'
        '<h2 class="display-md">10주 실무 트랙</h2>'
        '<p class="body-lg" style="margin:20px 0 52px;max-width:500px">'
        '이론 → 재현 → 배포 → KPI 연결 4단계로<br>'
        '졸업 시 완성된 포트폴리오를 손에 쥡니다.</p>'
        '<div style="max-width:760px;margin:0 auto;background:#FFF;border:1px solid #E8E8E8;border-radius:20px;padding:8px 28px">'
        + rows +
        '</div></div>')


# ---------------------------------------------------------------------------
# 9. 풀너비 CTA 배너
# ---------------------------------------------------------------------------

def render_cta_banner() -> None:
    _md('<div class="cta-banner">'
        '<div class="overline" style="color:rgba(255,255,255,.6);margin-bottom:20px">취업 연결</div>'
        '<h2 style="font-size:clamp(28px,4vw,56px);font-weight:900;color:#FFF;letter-spacing:-.025em;margin:0 0 20px">'
        '수료 후, 기업 채용까지<br>직접 연결됩니다</h2>'
        '<p style="color:rgba(255,255,255,.72);font-size:1rem;margin:0 auto 40px;max-width:460px;line-height:1.75">'
        'KPI 포트폴리오 → 파트너 기업 제출 → 채용 인터뷰<br>'
        '수료생 전용 취업 파이프라인을 운영합니다.</p>'
        '<a href="#apply" class="btn-white">지금 신청하기 →</a>'
        '</div>')


# ---------------------------------------------------------------------------
# 10. 사전 신청 폼
# ---------------------------------------------------------------------------

def render_application_form() -> None:
    _md('<div class="section" id="apply">'
        '<div class="overline" style="margin-bottom:16px;text-align:center">사전 신청</div>'
        '<h2 class="display-md" style="text-align:center;margin-bottom:12px">무료 사전 신청</h2>'
        '<p class="body-lg" style="text-align:center;margin:0 0 48px">'
        '선착순 50명 · 합격 기준 없음 · '
        '<span style="color:#FA5D29;font-weight:700">48시간 내 안내 연락</span></p>'
        '</div>')

    _, col_form, _ = st.columns([1, 2, 1])
    with col_form:
        name       = st.text_input("이름 *",   placeholder="홍길동")
        email      = st.text_input("이메일 *", placeholder="example@email.com")
        phone      = st.text_input("연락처 *", placeholder="010-1234-5678")
        background = st.selectbox(
            "현재 배경 *",
            ["선택해주세요", "비전공자 (이커머스 취업 희망)",
             "부트캠프 수료자", "경력 전환자 (타 업종 → 이커머스)", "기타"],
        )
        track = st.selectbox(
            "관심 트랙",
            ["AI 퍼포먼스 마케팅 (1기 오픈)",
             "AI 이커머스 오퍼레이터 (예정)",
             "AI 데이터 분석가 (예정)"],
        )
        motivation = st.text_area(
            "신청 동기 (선택)",
            placeholder="간단하게 왜 신청하셨는지 알려주세요.",
            height=88,
        )
        source = st.selectbox(
            "어디서 알게 되셨나요?",
            ["SNS", "유튜브", "지인 추천", "블로그/뉴스", "검색", "기타"],
        )
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("무료 사전 신청하기", use_container_width=True):
            _handle_submission({
                "name":       name,
                "email":      email,
                "phone":      phone,
                "background": background if background != "선택해주세요" else "",
                "track":      track,
                "motivation": motivation,
                "source":     source,
            })

    _md('<div style="text-align:center;padding:20px 0;color:#AAA;font-size:.82rem">'
        '개인정보는 신청 안내 외 사용되지 않습니다 &nbsp;·&nbsp; 48시간 내 연락</div>')


def _handle_submission(form_data: dict) -> None:
    from phase1_landing.sheets_connector import validate_application, append_application
    errors = validate_application(form_data)
    if errors:
        for err in errors:
            st.error(err)
        return
    with st.spinner("저장하는 중..."):
        result = append_application(form_data)
    if result["success"]:
        st.success("사전 신청 완료! 48시간 내 연락드립니다.")
        st.balloons()
    else:
        st.error(result["message"])


# ---------------------------------------------------------------------------
# 11. 푸터
# ---------------------------------------------------------------------------

def render_footer() -> None:
    _md(f'<div class="footer-wrap">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px">'
        f'<div>'
        f'<div style="font-size:1rem;font-weight:800;color:#111;margin-bottom:4px">{APP_NAME}</div>'
        f'<div style="font-size:.82rem;color:#AAA">이커머스 산업 특화 AI 실무 인재 양성 플랫폼</div>'
        f'</div>'
        f'<div style="font-size:.82rem;color:#CCC">© 2026 Commerce X Commerce. All rights reserved.</div>'
        f'</div></div>')
