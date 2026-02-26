# =============================================================================
# Phase 3 — 이커머스 역량 진단 대시보드
# =============================================================================
# 플로우:
#   Step 0 (intro)      : 소개 화면
#   Step 1 (assessment) : 12개 역량 설문
#   Step 2 (results)    : 레이더 차트 + 직무 추천 + 자격증 + 일정
# =============================================================================

import sys
from pathlib import Path
from datetime import date

import streamlit as st

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from phase3_dashboard import assessment as asmt
from phase3_dashboard import radar_chart as rc
from phase3_dashboard import recommender as rec
from phase3_dashboard import calendar_view as cal

# ---------------------------------------------------------------------------
# 진입점
# ---------------------------------------------------------------------------


def render_dashboard() -> None:
    _init_session()
    _inject_css()

    step = st.session_state.p3_step
    if step == "intro":
        _render_intro()
    elif step == "assessment":
        _render_assessment()
    elif step == "results":
        _render_results()


# ---------------------------------------------------------------------------
# 세션 초기화
# ---------------------------------------------------------------------------


def _init_session() -> None:
    defaults = {
        "p3_step": "intro",
        "p3_answers": {},   # {sub_item_key: score_index (0-4)}
        "p3_scores": None,  # calculate_scores() 결과
        "p3_goals": [],     # [{date, title}] 사용자 목표
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# ---------------------------------------------------------------------------
# CSS 인젝션
# ---------------------------------------------------------------------------


def _inject_css() -> None:
    st.markdown(
        """
        <style>
        /* 카드 스타일 */
        .p3-card {
            background: #FFFFFF;
            border: 1px solid #E8E8E8;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 16px;
        }
        .p3-card-accent {
            background: #FFF8F5;
            border: 1.5px solid #FA5D29;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 16px;
        }
        /* 점수 배지 */
        .score-badge {
            display: inline-block;
            font-size: 0.78rem;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 100px;
            color: #fff;
        }
        /* 직무 카드 핏 바 */
        .fit-bar-bg {
            background: #F0F0F0;
            border-radius: 100px;
            height: 8px;
            margin-top: 6px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Step 0 — 소개 화면
# ---------------------------------------------------------------------------


def _render_intro() -> None:
    st.markdown(
        """
        <div style="text-align:center; padding:60px 20px 40px;">
            <div style="font-size:3.5rem; margin-bottom:12px;">📊</div>
            <h1 style="font-size:2rem; font-weight:900; letter-spacing:-0.03em; margin:0 0 12px;">
                이커머스 역량 진단
            </h1>
            <p style="font-size:1.05rem; color:#555; max-width:520px; margin:0 auto 8px;">
                12개 문항으로 나의 이커머스 핵심 역량을 진단하고,<br>
                맞춤 직무·자격증·학습 일정을 한눈에 확인하세요.
            </p>
            <p style="font-size:0.88rem; color:#AAAAAA; margin:0;">
                소요 시간 약 3분 · AI 개인화 코칭 포함
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 6개 역량 미리보기
    cols = st.columns(3)
    for i, cat in enumerate(asmt.CATEGORIES):
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="p3-card" style="text-align:center; padding:18px 12px;">
                    <div style="font-size:1.8rem;">{cat['icon']}</div>
                    <div style="font-size:0.88rem; font-weight:700; color:#333; margin-top:6px;">
                        {cat['name']}
                    </div>
                    <div style="font-size:0.78rem; color:#888; margin-top:4px;">
                        {cat['sub_items'][0]['name']}<br>{cat['sub_items'][1]['name']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    _, col_c, _ = st.columns([1, 2, 1])
    with col_c:
        if st.button("역량 진단 시작 →", type="primary", use_container_width=True):
            st.session_state.p3_step = "assessment"
            st.rerun()


# ---------------------------------------------------------------------------
# Step 1 — 역량 진단 설문
# ---------------------------------------------------------------------------


def _render_assessment() -> None:
    # 헤더
    st.markdown(
        """
        <div style="text-align:center; padding:32px 0 8px;">
            <h2 style="font-size:1.6rem; font-weight:900; margin:0 0 6px;">이커머스 역량 진단</h2>
            <p style="color:#666; font-size:0.92rem; margin:0;">
                각 항목에서 현재 본인의 수준을 솔직하게 선택해주세요.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="background:#FA5D29; height:3px; border-radius:2px; margin-bottom:28px;"></div>',
        unsafe_allow_html=True,
    )

    with st.form("assessment_form"):
        answers: dict = {}

        for cat in asmt.CATEGORIES:
            # 카테고리 구분선 + 제목
            st.markdown(
                f"""
                <div style="display:flex; align-items:center; gap:10px;
                            margin:8px 0 4px; padding:10px 0 0;">
                    <span style="font-size:1.4rem;">{cat['icon']}</span>
                    <span style="font-size:1.05rem; font-weight:800; color:#111;">
                        {cat['name']}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            for sub in cat["sub_items"]:
                st.markdown(
                    f'<div style="font-size:0.9rem; color:#444; margin:10px 0 4px; font-weight:600;">'
                    f'{sub["name"]}</div>'
                    f'<div style="font-size:0.85rem; color:#666; margin-bottom:6px;">'
                    f'{sub["question"]}</div>',
                    unsafe_allow_html=True,
                )

                prev = st.session_state.p3_answers.get(sub["key"], 0)
                answers[sub["key"]] = st.radio(
                    label=sub["question"],
                    options=list(range(len(asmt.SCORE_OPTIONS))),
                    format_func=lambda i: asmt.SCORE_OPTIONS[i],
                    index=prev,
                    horizontal=True,
                    key=f"radio_{sub['key']}",
                    label_visibility="collapsed",
                )
                st.markdown('<div style="height:2px; background:#F3F3F3; margin:6px 0 14px;"></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_back, col_submit = st.columns([1, 3])
        with col_back:
            back = st.form_submit_button("← 처음으로", use_container_width=True)
        with col_submit:
            submitted = st.form_submit_button(
                "결과 보기 →", type="primary", use_container_width=True
            )

    if submitted:
        st.session_state.p3_answers = answers
        st.session_state.p3_scores = asmt.calculate_scores(answers)
        st.session_state.p3_step = "results"
        st.rerun()

    if back:
        st.session_state.p3_step = "intro"
        st.rerun()


# ---------------------------------------------------------------------------
# Step 2 — 결과 대시보드
# ---------------------------------------------------------------------------


def _render_results() -> None:
    scores = st.session_state.p3_scores
    if not scores:
        st.session_state.p3_step = "intro"
        st.rerun()
        return

    cat_scores = scores["categories"]
    total = scores["total"]
    strongest = scores["strongest"]
    weakest = scores["weakest"]

    # ── 결과 헤더 ─────────────────────────────────────────────────────────
    level = asmt.get_level_label(total)
    level_color = asmt.get_level_color(total)

    st.markdown(
        f"""
        <div style="text-align:center; padding:32px 0 20px;">
            <h2 style="font-size:1.7rem; font-weight:900; margin:0 0 10px;">
                진단 완료! 내 역량 리포트
            </h2>
            <div style="display:inline-flex; gap:16px; flex-wrap:wrap; justify-content:center;">
                <span style="background:#F3F3F3; border-radius:100px; padding:6px 18px;
                             font-size:0.9rem; font-weight:700; color:#333;">
                    종합 <b style="color:{level_color};">{total:.0f}점</b>
                </span>
                <span style="background:{level_color}22; border:1px solid {level_color};
                             border-radius:100px; padding:6px 18px;
                             font-size:0.9rem; font-weight:700; color:{level_color};">
                    {level} 수준
                </span>
                <span style="background:#FFF0EB; border-radius:100px; padding:6px 18px;
                             font-size:0.9rem; color:#FA5D29; font-weight:600;">
                    강점 {strongest}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── 탭 구성 ───────────────────────────────────────────────────────────
    tab_chart, tab_jobs, tab_certs, tab_calendar = st.tabs(
        ["📊 역량 차트", "💼 직무 추천", "🎓 자격증 & 기업", "📅 학습 일정"]
    )

    # ── 탭 1: 레이더 차트 + 점수 상세 ────────────────────────────────────
    with tab_chart:
        col_chart, col_scores = st.columns([3, 2])

        with col_chart:
            fig = rc.build_radar_chart(cat_scores, title="이커머스 역량 레이더")
            st.plotly_chart(fig, use_container_width=True)

        with col_scores:
            st.markdown("#### 카테고리별 점수")
            for cat in asmt.CATEGORIES:
                name = cat["name"]
                score = cat_scores.get(name, 0)
                color = asmt.get_level_color(score)
                label = asmt.get_level_label(score)
                bar_pct = round(score)

                st.markdown(
                    f"""
                    <div style="margin-bottom:14px;">
                        <div style="display:flex; justify-content:space-between;
                                    align-items:center; margin-bottom:4px;">
                            <span style="font-size:0.88rem; font-weight:700; color:#333;">
                                {cat['icon']} {name}
                            </span>
                            <span class="score-badge" style="background:{color};">
                                {score:.0f}점 · {label}
                            </span>
                        </div>
                        <div class="fit-bar-bg">
                            <div style="width:{bar_pct}%; height:8px; background:{color};
                                        border-radius:100px; transition:width 0.3s;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.divider()

        # 세부 항목 표
        st.markdown("#### 세부 항목 상세")
        sub_cols = st.columns(2)
        all_subs = [
            (sub["name"], scores["sub_items"].get(sub["key"], 0))
            for cat in asmt.CATEGORIES
            for sub in cat["sub_items"]
        ]
        for idx, (name, score) in enumerate(all_subs):
            with sub_cols[idx % 2]:
                color = asmt.get_level_color(score)
                st.markdown(
                    f'<div style="font-size:0.83rem; color:#555; padding:4px 0;">'
                    f'{name} — <b style="color:{color};">{score:.0f}점</b></div>',
                    unsafe_allow_html=True,
                )

        st.divider()

        # AI 코칭 메시지
        st.markdown("#### AI 커리어 코치 메시지")
        ai_key = f"p3_ai_coaching_{total:.0f}"
        if ai_key not in st.session_state:
            with st.spinner("AI 코치가 분석 중..."):
                coaching_text = st.write_stream(rec.stream_ai_coaching(scores))
                st.session_state[ai_key] = coaching_text
        else:
            st.markdown(st.session_state[ai_key])

    # ── 탭 2: 직무 추천 ───────────────────────────────────────────────────
    with tab_jobs:
        st.markdown("#### 나의 역량에 맞는 직무 TOP 3")
        st.caption("현재 역량 점수를 바탕으로 적합도를 계산했습니다.")

        jobs = rec.get_job_recommendations(cat_scores, top_n=3)

        for rank, job in enumerate(jobs, 1):
            fit_pct = job["fit_pct"]
            fit_color = "#2ECC71" if fit_pct >= 70 else "#F39C12" if fit_pct >= 50 else "#E74C3C"

            with st.container():
                st.markdown(
                    f"""
                    <div class="p3-card" style="{'border-color:#FA5D29; background:#FFF8F5;' if rank == 1 else ''}">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                            <div>
                                <span style="font-size:0.8rem; color:#FA5D29; font-weight:800;">
                                    {'TOP PICK' if rank == 1 else f'#{rank}'}
                                </span>
                                <div style="font-size:1.1rem; font-weight:900; color:#111; margin:4px 0 2px;">
                                    {job['icon']} {job['title']}
                                </div>
                                <div style="font-size:0.84rem; color:#666;">
                                    {job['desc']}
                                </div>
                            </div>
                            <div style="text-align:right; min-width:72px;">
                                <div style="font-size:1.5rem; font-weight:900; color:{fit_color};">
                                    {fit_pct}%
                                </div>
                                <div style="font-size:0.75rem; color:#AAAAAA;">적합도</div>
                            </div>
                        </div>
                        <div class="fit-bar-bg" style="margin-top:12px;">
                            <div style="width:{fit_pct}%; height:8px; background:{fit_color};
                                        border-radius:100px;"></div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # 갭 분석
            gaps = rec.get_gap_analysis(cat_scores, job)
            meaningful_gaps = [g for g in gaps if g["gap"] > 0]
            if meaningful_gaps:
                with st.expander(f"🔍 '{job['title']}' 갭 분석 보기"):
                    for g in meaningful_gaps:
                        g_color = "#E74C3C" if g["gap"] >= 30 else "#F39C12" if g["gap"] >= 15 else "#2ECC71"
                        st.markdown(
                            f'<div style="font-size:0.85rem; padding:4px 0;">'
                            f'<b>{g["category"]}</b> : 현재 {g["current"]}점 → 목표 {g["target"]}점 '
                            f'<span style="color:{g_color}; font-weight:700;">'
                            f'({g["gap"]}점 부족)</span></div>',
                            unsafe_allow_html=True,
                        )

        # 추천 기업 유형
        st.markdown("#### 역량 프로파일 유사 채용 기업 유형")
        top_job = jobs[0]
        companies = top_job.get("companies", [])
        company_tags = " ".join(
            f'<span style="background:#F3F3F3; border-radius:8px; padding:4px 12px; '
            f'font-size:0.85rem; font-weight:600; color:#444; margin:4px;">{c}</span>'
            for c in companies
        )
        st.markdown(
            f'<div style="display:flex; flex-wrap:wrap; gap:4px; padding:8px 0;">'
            f"{company_tags}</div>",
            unsafe_allow_html=True,
        )
        st.caption(
            f"* '{top_job['title']}' 직무 기준. 실제 채용 여부는 각 기업 채용 공고를 확인해주세요."
        )

    # ── 탭 3: 자격증 & 기업 ──────────────────────────────────────────────
    with tab_certs:
        st.markdown("#### 취약 역량 보완을 위한 자격증 추천")
        st.caption(f"점수가 낮은 2개 카테고리 기준 — 취약점: **{weakest}**")

        certs = rec.get_cert_recommendations(cat_scores, n_weak_cats=2)

        if certs:
            for cert in certs:
                weak_score = cat_scores.get(cert["category"], 0)
                weak_color = asmt.get_level_color(weak_score)
                st.markdown(
                    f"""
                    <div class="p3-card" style="padding:16px 20px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <div style="font-size:0.95rem; font-weight:800; color:#111;">
                                    🎓 {cert['name']}
                                </div>
                                <div style="font-size:0.82rem; color:#888; margin-top:3px;">
                                    {cert['org']}
                                </div>
                            </div>
                            <span class="score-badge" style="background:{weak_color}; font-size:0.75rem;">
                                {cert['category']} {weak_score:.0f}점
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("모든 역량이 우수합니다! 심화 자격증을 알아보세요.")

        st.divider()

        # 전체 자격증 목록 (카테고리별)
        with st.expander("전체 자격증 목록 보기 (카테고리별)"):
            for cat_name, cert_list in rec.CERT_RECOMMENDATIONS.items():
                score = cat_scores.get(cat_name, 0)
                color = asmt.get_level_color(score)
                st.markdown(
                    f'<div style="font-weight:700; color:#333; margin:12px 0 6px;">'
                    f'{cat_name} <span style="color:{color}; font-size:0.85rem;">{score:.0f}점</span></div>',
                    unsafe_allow_html=True,
                )
                for cert in cert_list:
                    st.markdown(
                        f'<div style="font-size:0.85rem; color:#555; padding:3px 0 3px 12px;">'
                        f'• {cert["name"]} — {cert["org"]}</div>',
                        unsafe_allow_html=True,
                    )

    # ── 탭 4: 학습 일정 캘린더 ───────────────────────────────────────────
    with tab_calendar:
        st.markdown("#### 학습 일정 캘린더")

        # 필터
        col_filter, col_goal = st.columns([2, 3])
        with col_filter:
            selected_cats = st.multiselect(
                "카테고리 필터",
                options=["자격증", "컨퍼런스", "목표"],
                default=["자격증", "컨퍼런스", "목표"],
                label_visibility="collapsed",
            )

        # 목표 추가
        with col_goal:
            with st.popover("목표 일정 추가 +"):
                goal_date = st.date_input(
                    "날짜",
                    value=date.today(),
                    min_value=date.today(),
                    key="goal_date_input",
                )
                goal_title = st.text_input(
                    "목표 제목",
                    placeholder="예: ADsP 1차 시험 목표",
                    key="goal_title_input",
                )
                if st.button("추가", key="add_goal_btn"):
                    if goal_title.strip():
                        st.session_state.p3_goals.append(
                            {
                                "date": goal_date.strftime("%Y-%m-%d"),
                                "title": goal_title.strip(),
                            }
                        )
                        st.success("목표가 추가되었습니다!")
                        st.rerun()
                    else:
                        st.error("목표 제목을 입력해주세요.")

        st.markdown("<br>", unsafe_allow_html=True)

        # 이벤트 렌더링
        events = cal.get_upcoming_events(
            include_categories=selected_cats if selected_cats else None,
            user_goals=st.session_state.p3_goals,
        )

        if not events:
            st.info("선택한 카테고리의 일정이 없습니다.")
        else:
            grouped = cal.group_by_month(events)
            for month_label, month_events in grouped.items():
                st.markdown(
                    f'<div style="font-size:0.95rem; font-weight:800; color:#FA5D29; '
                    f'margin:18px 0 8px; padding-bottom:4px; border-bottom:2px solid #FA5D2922;">'
                    f'{month_label}</div>',
                    unsafe_allow_html=True,
                )
                for ev in month_events:
                    date_str = ev["date_obj"].strftime("%m.%d (%a)")
                    # 한글 요일
                    weekday_map = {"Mon": "월", "Tue": "화", "Wed": "수",
                                   "Thu": "목", "Fri": "금", "Sat": "토", "Sun": "일"}
                    for en, ko in weekday_map.items():
                        date_str = date_str.replace(en, ko)

                    detail_html = (
                        f'<span style="color:#AAAAAA; font-size:0.78rem;"> — {ev["detail"]}</span>'
                        if ev.get("detail")
                        else ""
                    )
                    is_goal = ev["category"] == "목표"
                    bg = "#FAF0FF" if is_goal else "#FAFAFA"

                    st.markdown(
                        f"""
                        <div style="display:flex; align-items:flex-start; gap:12px;
                                    background:{bg}; border-radius:10px;
                                    padding:10px 14px; margin-bottom:6px;">
                            <div style="min-width:70px; font-size:0.83rem; color:#666;
                                        font-weight:600; padding-top:1px;">
                                {date_str}
                            </div>
                            <div style="flex:1;">
                                <span style="color:{ev['color']}; font-weight:700;
                                             font-size:0.88rem;">
                                    {ev['icon']} {ev['title']}
                                </span>
                                {detail_html}
                            </div>
                            <div>
                                <span style="background:{ev['color']}22; color:{ev['color']};
                                             font-size:0.72rem; font-weight:700;
                                             padding:2px 8px; border-radius:100px;">
                                    {ev['category']}
                                </span>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

    # ── 하단 재진단 버튼 ──────────────────────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.divider()
    col_retry, col_share = st.columns(2)
    with col_retry:
        if st.button("다시 진단하기", use_container_width=True):
            for k in ["p3_step", "p3_answers", "p3_scores"]:
                st.session_state.pop(k, None)
            # AI 코칭 캐시도 삭제
            for k in list(st.session_state.keys()):
                if k.startswith("p3_ai_coaching_"):
                    del st.session_state[k]
            st.rerun()
    with col_share:
        st.markdown(
            '<div style="text-align:center; font-size:0.82rem; color:#AAAAAA; padding:10px 0;">'
            "결과를 캡처하여 포트폴리오에 첨부해보세요</div>",
            unsafe_allow_html=True,
        )
