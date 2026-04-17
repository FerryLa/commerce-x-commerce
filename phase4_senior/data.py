# Mock 데이터 — 시니어·주니어 지식 자산 네트워크

NODES_DATA = [
    # === 시니어 ===
    {
        "id": "s1", "label": "김○○\n시니어 (65)", "type": "Senior",
        "name": "김○○", "age": 65, "region": "군산",
        "skills": ["자동차 정비"], "experience_years": 30,
        "reputation_score": 87,
        "bio": "30년간 자동차 정비소 운영. 창업 불안을 직접 극복한 경험 보유.",
        "contributions": [
            {"event": "주니어A 멘토링 (3회)", "score": 28.8},
            {"event": "창업 불안 문제 해결", "score": 13.5},
            {"event": "지역 네트워크 연결", "score": 8.0},
        ],
    },
    {
        "id": "s2", "label": "이○○\n시니어 (62)", "type": "Senior",
        "name": "이○○", "age": 62, "region": "전주",
        "skills": ["교육 설계"], "experience_years": 25,
        "reputation_score": 73,
        "bio": "초등학교 교사 25년. 학습 설계 및 아이 동기부여 전문가.",
        "contributions": [
            {"event": "주니어B 멘토링 (2회)", "score": 17.2},
            {"event": "커뮤니티 강의", "score": 15.0},
            {"event": "지역 교육 네트워크", "score": 8.0},
        ],
    },
    {
        "id": "s3", "label": "박○○\n시니어 (68)", "type": "Senior",
        "name": "박○○", "age": 68, "region": "부산",
        "skills": ["제조업 관리"], "experience_years": 35,
        "reputation_score": 91,
        "bio": "대형 조선소 생산관리 35년. 스마트팩토리 전환 프로젝트 경험.",
        "contributions": [
            {"event": "스마트팩토리 컨설팅", "score": 27.0},
            {"event": "청년 취업 세미나", "score": 20.0},
            {"event": "문제 해결 기여", "score": 13.5},
        ],
    },
    {
        "id": "s4", "label": "최○○\n시니어 (60)", "type": "Senior",
        "name": "최○○", "age": 60, "region": "군산",
        "skills": ["노사 조정"], "experience_years": 20,
        "reputation_score": 65,
        "bio": "20년간 노사관계 전문가. 번아웃 극복 멘토링 다수 경험.",
        "contributions": [
            {"event": "번아웃 상담 (5회)", "score": 20.0},
            {"event": "커뮤니티 조정", "score": 10.0},
            {"event": "지역 연결", "score": 8.0},
        ],
    },

    # === 주니어 ===
    {
        "id": "j1", "label": "주니어A\n(28)", "type": "Junior",
        "name": "주니어A", "age": 28, "region": "군산",
        "goal": "자동차 브랜드 창업", "crisis": "창업 불안",
        "bio": "자동차 브랜드 창업을 준비 중. 실무 멘토와 정서적 지지가 필요.",
    },
    {
        "id": "j2", "label": "주니어B\n(24)", "type": "Junior",
        "name": "주니어B", "age": 24, "region": "전주",
        "goal": "교육 스타트업 창업", "crisis": "번아웃",
        "bio": "에듀테크 스타트업 준비. 번아웃 상태로 방향성 고민 중.",
    },
    {
        "id": "j3", "label": "주니어C\n(31)", "type": "Junior",
        "name": "주니어C", "age": 31, "region": "부산",
        "goal": "스마트팩토리 취업", "crisis": "취업 장벽",
        "bio": "제조업 IT 직군 취업 준비. 실무 경험자 멘토링이 절실.",
    },

    # === 스킬 ===
    {"id": "sk1", "label": "자동차 정비", "type": "Skill", "demand": "높음"},
    {"id": "sk2", "label": "교육 설계",   "type": "Skill", "demand": "중간"},
    {"id": "sk3", "label": "제조업 관리", "type": "Skill", "demand": "높음"},
    {"id": "sk4", "label": "노사 조정",   "type": "Skill", "demand": "낮음"},

    # === 지역 ===
    {"id": "r1", "label": "군산", "type": "Region", "province": "전북"},
    {"id": "r2", "label": "전주", "type": "Region", "province": "전북"},
    {"id": "r3", "label": "부산", "type": "Region", "province": "경남"},

    # === 문제 ===
    {"id": "p1", "label": "번아웃",    "type": "Problem", "severity": "높음"},
    {"id": "p2", "label": "창업 불안", "type": "Problem", "severity": "중간"},
    {"id": "p3", "label": "취업 장벽", "type": "Problem", "severity": "높음"},
]

EDGES_DATA = [
    # HAS_SKILL
    {"source": "s1", "target": "sk1", "label": "보유 기술", "type": "HAS_SKILL"},
    {"source": "s2", "target": "sk2", "label": "보유 기술", "type": "HAS_SKILL"},
    {"source": "s3", "target": "sk3", "label": "보유 기술", "type": "HAS_SKILL"},
    {"source": "s4", "target": "sk4", "label": "보유 기술", "type": "HAS_SKILL"},

    # NEEDS
    {"source": "j1", "target": "sk1", "label": "필요 기술", "type": "NEEDS"},
    {"source": "j2", "target": "sk2", "label": "필요 기술", "type": "NEEDS"},
    {"source": "j3", "target": "sk3", "label": "필요 기술", "type": "NEEDS"},

    # LIVES_IN
    {"source": "s1", "target": "r1", "label": "거주", "type": "LIVES_IN"},
    {"source": "s2", "target": "r2", "label": "거주", "type": "LIVES_IN"},
    {"source": "s3", "target": "r3", "label": "거주", "type": "LIVES_IN"},
    {"source": "s4", "target": "r1", "label": "거주", "type": "LIVES_IN"},
    {"source": "j1", "target": "r1", "label": "거주", "type": "LIVES_IN"},
    {"source": "j2", "target": "r2", "label": "거주", "type": "LIVES_IN"},
    {"source": "j3", "target": "r3", "label": "거주", "type": "LIVES_IN"},

    # MENTORED
    {"source": "s1", "target": "j1", "label": "멘토링 ★4.8", "type": "MENTORED", "satisfaction": 4.8},
    {"source": "s2", "target": "j2", "label": "멘토링 ★4.3", "type": "MENTORED", "satisfaction": 4.3},

    # IN_CRISIS
    {"source": "j1", "target": "p2", "label": "위기 상태", "type": "IN_CRISIS"},
    {"source": "j2", "target": "p1", "label": "위기 상태", "type": "IN_CRISIS"},
    {"source": "j3", "target": "p3", "label": "위기 상태", "type": "IN_CRISIS"},

    # SOLVED
    {"source": "s1", "target": "p2", "label": "해결 경험", "type": "SOLVED"},
    {"source": "s4", "target": "p1", "label": "해결 경험", "type": "SOLVED"},
]

NODE_BY_ID = {n["id"]: n for n in NODES_DATA}

REGIONS = ["전체", "군산", "전주", "부산"]
NODE_TYPES = ["전체", "Senior", "Junior", "Skill", "Region", "Problem"]

# 노드 유형별 색상 (agraph)
NODE_COLORS = {
    "Senior":  "#FF6B6B",
    "Junior":  "#4ECDC4",
    "Skill":   "#45B7D1",
    "Region":  "#96CEB4",
    "Problem": "#FFD93D",
}

NODE_SIZES = {
    "Senior":  30,
    "Junior":  28,
    "Skill":   20,
    "Region":  22,
    "Problem": 18,
}

REPUTATION_BADGES = [
    (81, "👑 레전드"),
    (61, "🏆 마스터"),
    (41, "🌳 지혜"),
    (21, "🌿 성장"),
    (0,  "🌱 새싹"),
]

def get_badge(score: int) -> str:
    for threshold, badge in REPUTATION_BADGES:
        if score >= threshold:
            return badge
    return "🌱 새싹"
