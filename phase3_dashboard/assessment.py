# =============================================================================
# Phase 3 — 역량 진단 설문 및 채점 로직
# =============================================================================
# 구조:
#   - 6개 카테고리, 카테고리당 2개 세부 항목 (총 12개 지표)
#   - 5점 리커트 척도 → 100점 환산
#   - 카테고리 점수 = 세부 항목 2개 평균
# =============================================================================

# ---------------------------------------------------------------------------
# 역량 카테고리 정의
# ---------------------------------------------------------------------------

CATEGORIES = [
    {
        "name": "퍼포먼스 마케팅",
        "icon": "📣",
        "color": "#FA5D29",
        "sub_items": [
            {
                "key": "ad_ops",
                "name": "광고 운영 (Meta / GFA)",
                "question": "Meta 광고·카카오 GFA 등 SNS 광고를 직접 설정·운영한 경험은?",
            },
            {
                "key": "data_analysis",
                "name": "데이터 분석 (GA4 / ROAS)",
                "question": "GA4, ROAS, CAC 등 광고 성과 지표를 분석하고 의사결정에 활용한 경험은?",
            },
        ],
    },
    {
        "name": "콘텐츠 & 브랜딩",
        "icon": "✍️",
        "color": "#9B59B6",
        "sub_items": [
            {
                "key": "copywriting",
                "name": "카피라이팅",
                "question": "상품 상세페이지·광고 카피·SNS 게시물 등 판매용 텍스트를 직접 작성한 경험은?",
            },
            {
                "key": "visual_content",
                "name": "이미지 / 영상 제작",
                "question": "상품 이미지 편집·썸네일·홍보 영상 등 비주얼 콘텐츠를 제작한 경험은?",
            },
        ],
    },
    {
        "name": "플랫폼 운영",
        "icon": "🛒",
        "color": "#E74C3C",
        "sub_items": [
            {
                "key": "platform_ops",
                "name": "쿠팡 / 스마트스토어",
                "question": "쿠팡 Wing·네이버 스마트스토어 등 오픈마켓 판매자 관리 경험은?",
            },
            {
                "key": "cs_review",
                "name": "CS & 리뷰 관리",
                "question": "고객 문의 처리·부정 리뷰 대응·리뷰 마케팅 등 CS 업무 경험은?",
            },
        ],
    },
    {
        "name": "데이터 & KPI",
        "icon": "📊",
        "color": "#2ECC71",
        "sub_items": [
            {
                "key": "kpi_design",
                "name": "지표 설계",
                "question": "비즈니스 목표에 맞는 KPI를 직접 설계하거나 관리한 경험은?",
            },
            {
                "key": "dashboard_viz",
                "name": "대시보드 시각화",
                "question": "Looker Studio·엑셀·스프레드시트 등으로 성과 대시보드를 구축한 경험은?",
            },
        ],
    },
    {
        "name": "AI 도구 활용",
        "icon": "🤖",
        "color": "#3498DB",
        "sub_items": [
            {
                "key": "prompt_eng",
                "name": "프롬프트 엔지니어링",
                "question": "ChatGPT·Claude 등 AI 도구를 업무에 활용하거나 프롬프트를 직접 설계한 경험은?",
            },
            {
                "key": "automation",
                "name": "업무 자동화 (n8n)",
                "question": "n8n·Zapier·구글 앱스 스크립트 등 업무 자동화 도구를 구축한 경험은?",
            },
        ],
    },
    {
        "name": "공급망 & 물류",
        "icon": "📦",
        "color": "#F39C12",
        "sub_items": [
            {
                "key": "sourcing",
                "name": "소싱 & 원가 계산",
                "question": "중국·국내 도매 소싱, 원가·마진 계산 등 상품 소싱 업무 경험은?",
            },
            {
                "key": "inventory",
                "name": "재고 / 배송 관리",
                "question": "재고 관리·발주·택배사 연동·풀필먼트 등 물류 운영 경험은?",
            },
        ],
    },
]

# ---------------------------------------------------------------------------
# 점수 척도
# ---------------------------------------------------------------------------

SCORE_OPTIONS = [
    "없음 — 처음 들어봄",
    "입문 — 개념은 알지만 실습 없음",
    "초급 — 따라하기 수준의 실습 경험",
    "중급 — 실무 적용, 성과 측정 경험",
    "고급 — 주도적 운영·최적화 경험",
]

# 선택지 인덱스(0~4) → 100점 기준 점수
SCORE_MAP = {0: 5, 1: 25, 2: 50, 3: 75, 4: 100}


# ---------------------------------------------------------------------------
# 채점
# ---------------------------------------------------------------------------

def calculate_scores(answers: dict) -> dict:
    """
    Args:
        answers: {sub_item_key: score_index (0-4)}

    Returns:
        {
            "categories": {category_name: score (0-100)},
            "sub_items":  {sub_item_key: score (0-100)},
            "total":      float,
            "strongest":  str (category name),
            "weakest":    str (category name),
        }
    """
    sub_scores = {key: SCORE_MAP[idx] for key, idx in answers.items()}

    cat_scores = {}
    for cat in CATEGORIES:
        keys = [sub["key"] for sub in cat["sub_items"]]
        raw = [sub_scores.get(k, 0) for k in keys]
        cat_scores[cat["name"]] = sum(raw) / len(raw)

    names = list(cat_scores.keys())
    strongest = max(names, key=lambda n: cat_scores[n])
    weakest = min(names, key=lambda n: cat_scores[n])
    total = sum(cat_scores.values()) / len(cat_scores)

    return {
        "categories": cat_scores,
        "sub_items": sub_scores,
        "total": total,
        "strongest": strongest,
        "weakest": weakest,
    }


def get_level_label(score: float) -> str:
    """점수 → 수준 레이블 변환."""
    if score >= 85:
        return "전문가"
    elif score >= 65:
        return "중급"
    elif score >= 40:
        return "초급"
    elif score >= 20:
        return "입문"
    else:
        return "미경험"


def get_level_color(score: float) -> str:
    """점수 → 색상."""
    if score >= 85:
        return "#2ECC71"
    elif score >= 65:
        return "#3498DB"
    elif score >= 40:
        return "#F39C12"
    elif score >= 20:
        return "#E74C3C"
    else:
        return "#AAAAAA"
