# =============================================================================
# Phase 3 — 학습 일정 캘린더 뷰
# =============================================================================
# 구조:
#   - 2026년 자격증 시험 / 컨퍼런스 정적 데이터
#   - 사용자 개인 목표 등록 (session_state 기반)
# =============================================================================

from datetime import date, datetime
from typing import List

# ---------------------------------------------------------------------------
# 2026년 정적 일정 데이터
# ---------------------------------------------------------------------------

SCHEDULE_2026 = [
    # ── 자격증 ─────────────────────────────────────────────────────────────
    {
        "date": "2026-03-07",
        "title": "전자상거래관리사 2급 1회 원서접수 마감",
        "category": "자격증",
        "detail": "대한상공회의소 자격평가사업단",
    },
    {
        "date": "2026-03-28",
        "title": "전자상거래관리사 2급 1회 필기시험",
        "category": "자격증",
        "detail": "대한상공회의소 자격평가사업단",
    },
    {
        "date": "2026-04-11",
        "title": "ADsP (데이터 분석 준전문가) 1회 접수 마감",
        "category": "자격증",
        "detail": "한국데이터산업진흥원",
    },
    {
        "date": "2026-04-25",
        "title": "ADsP 1회 시험",
        "category": "자격증",
        "detail": "한국데이터산업진흥원",
    },
    {
        "date": "2026-04-19",
        "title": "SQLD 58회 시험",
        "category": "자격증",
        "detail": "한국데이터산업진흥원",
    },
    {
        "date": "2026-05-09",
        "title": "컴퓨터그래픽스운용기능사 1회 필기",
        "category": "자격증",
        "detail": "한국산업인력공단 Q-net",
    },
    {
        "date": "2026-06-07",
        "title": "유통관리사 2급 1회 필기",
        "category": "자격증",
        "detail": "대한상공회의소",
    },
    {
        "date": "2026-06-20",
        "title": "물류관리사 1차 시험",
        "category": "자격증",
        "detail": "국토교통부 / 한국교통연구원",
    },
    {
        "date": "2026-07-04",
        "title": "빅데이터 분석기사 필기 1회",
        "category": "자격증",
        "detail": "한국데이터산업진흥원",
    },
    {
        "date": "2026-09-05",
        "title": "ADsP 2회 시험",
        "category": "자격증",
        "detail": "한국데이터산업진흥원",
    },
    {
        "date": "2026-09-19",
        "title": "전자상거래관리사 2급 2회 필기",
        "category": "자격증",
        "detail": "대한상공회의소",
    },
    {
        "date": "2026-10-17",
        "title": "SQLD 59회 시험",
        "category": "자격증",
        "detail": "한국데이터산업진흥원",
    },
    {
        "date": "2026-11-14",
        "title": "빅데이터 분석기사 필기 2회",
        "category": "자격증",
        "detail": "한국데이터산업진흥원",
    },
    # ── 컨퍼런스 / 세미나 ──────────────────────────────────────────────────
    {
        "date": "2026-04-23",
        "title": "커머스 테크 서밋 2026 (예정)",
        "category": "컨퍼런스",
        "detail": "이커머스 기술·트렌드 컨퍼런스",
    },
    {
        "date": "2026-06-18",
        "title": "스마트스토어 판매자 데이 2026 (예정)",
        "category": "컨퍼런스",
        "detail": "네이버 쇼핑 / 스마트스토어 운영 전략 세미나",
    },
    {
        "date": "2026-08-22",
        "title": "AD:TECH Seoul 2026 (예정)",
        "category": "컨퍼런스",
        "detail": "퍼포먼스 마케팅·애드테크 국제 컨퍼런스",
    },
    {
        "date": "2026-10-29",
        "title": "이커머스 위크 2026 (예정)",
        "category": "컨퍼런스",
        "detail": "쿠팡·카카오·네이버 연합 이커머스 세미나",
    },
]


# ---------------------------------------------------------------------------
# 헬퍼 함수
# ---------------------------------------------------------------------------

CATEGORY_COLORS = {
    "자격증": "#FA5D29",
    "컨퍼런스": "#2BC0B8",
    "목표": "#9B59B6",
}

CATEGORY_ICONS = {
    "자격증": "📋",
    "컨퍼런스": "🎤",
    "목표": "🎯",
}


def get_upcoming_events(
    from_date: date | None = None,
    include_categories: List[str] | None = None,
    user_goals: List[dict] | None = None,
) -> List[dict]:
    """
    오늘 이후 일정을 날짜 오름차순으로 반환한다.

    Args:
        from_date:          기준일 (None이면 오늘)
        include_categories: 필터링할 카테고리 목록 (None이면 전체)
        user_goals:         사용자 목표 목록 [{date, title}, ...]

    Returns:
        이벤트 dict 목록 (date, title, category, detail, icon, color)
    """
    today = from_date or date.today()

    all_events: List[dict] = []

    # 정적 일정
    for ev in SCHEDULE_2026:
        ev_date = datetime.strptime(ev["date"], "%Y-%m-%d").date()
        if ev_date >= today:
            all_events.append({**ev, "date_obj": ev_date})

    # 사용자 목표
    for goal in (user_goals or []):
        ev_date = datetime.strptime(goal["date"], "%Y-%m-%d").date()
        if ev_date >= today:
            all_events.append(
                {
                    "date": goal["date"],
                    "title": goal["title"],
                    "category": "목표",
                    "detail": "",
                    "date_obj": ev_date,
                }
            )

    # 카테고리 필터
    if include_categories:
        all_events = [e for e in all_events if e["category"] in include_categories]

    # 정렬 + 아이콘 / 색상 주입
    all_events.sort(key=lambda x: x["date_obj"])
    for ev in all_events:
        ev["icon"] = CATEGORY_ICONS.get(ev["category"], "📌")
        ev["color"] = CATEGORY_COLORS.get(ev["category"], "#888888")

    return all_events


def group_by_month(events: List[dict]) -> dict:
    """이벤트 목록을 '2026년 N월' 키로 그룹화."""
    grouped: dict = {}
    for ev in events:
        key = ev["date_obj"].strftime("%Y년 %-m월") if hasattr(ev["date_obj"], "strftime") else ev["date"]
        # Windows 호환: %-m 대신 %m 사용 후 strip
        key = ev["date_obj"].strftime("%Y년 %m월").replace("년 0", "년 ").strip()
        grouped.setdefault(key, []).append(ev)
    return grouped
