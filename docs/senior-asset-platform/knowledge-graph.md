# Knowledge Graph 설계 — Neo4j 데이터 모델

> "사람은 표(Table)가 아닙니다. 관계로 이루어진 존재입니다."

---

## 1. 왜 그래프 DB인가?

일반 관계형 DB(MySQL/PostgreSQL)로 저장하면:

```
| 이름   | 기술         | 지역 |
|--------|-------------|------|
| 김○○  | 자동차 정비  | 군산 |
```

→ 표는 **관계를 표현하지 못합니다.**

Neo4j 그래프로 저장하면:

```
(김○○ 시니어)
  -[HAS_SKILL]→  (자동차 정비)
  -[LIVES_IN]→   (군산)
  -[MENTORED]→   (주니어A)  { satisfaction: 4.8 }
  -[SOLVED]→     (창업 초기 멘탈 관리 문제)

(주니어A)
  -[NEEDS]→      (자동차 브랜드 사업 지식)
  -[IN_CRISIS]→  (번아웃)
  -[LOCATED_IN]→ (군산)
```

→ **"군산 거주 시니어 중 창업 주니어의 번아웃 해소에 기여 가능한 사람"** 을 자동 탐색 가능

---

## 2. 노드(Node) 유형

| 노드 유형 | 색상 | 속성 | 설명 |
|---|---|---|---|
| `Senior` | #FF6B6B (빨강) | name, age, region, reputation_score | 시니어 인물 |
| `Junior` | #4ECDC4 (청록) | name, age, region, current_goal | 주니어 인물 |
| `Skill` | #45B7D1 (파랑) | name, category, demand_level | 기술/역량 |
| `Region` | #96CEB4 (초록) | name, province, population | 지역 |
| `Problem` | #FFEAA7 (노랑) | name, severity, category | 문제/위기 유형 |

---

## 3. 관계(Edge) 유형

| 관계 | 방향 | 속성 | 의미 |
|---|---|---|---|
| `HAS_SKILL` | Senior → Skill | years, proficiency | 기술 보유 |
| `NEEDS` | Junior → Skill | urgency | 기술 필요 |
| `LIVES_IN` | Person → Region | since | 거주 |
| `MENTORED` | Senior → Junior | satisfaction(1-5), sessions | 멘토링 완료 |
| `IN_CRISIS` | Junior → Problem | severity, duration | 위기 상태 |
| `SOLVED` | Senior → Problem | approach, success_rate | 문제 해결 경험 |
| `KNOWS` | Person ↔ Person | strength(1-10) | 인맥 |

---

## 4. Cypher 쿼리 예시 (Neo4j)

### 군산 지역 매칭 후보 탐색
```cypher
MATCH (s:Senior)-[:LIVES_IN]->(r:Region {name: "군산"})
      -[:LIVES_IN]-(j:Junior)
WHERE (s)-[:SOLVED]->(:Problem)<-[:IN_CRISIS]-(j)
RETURN s.name, j.name, s.reputation_score
ORDER BY s.reputation_score DESC
LIMIT 5
```

### 특정 기술이 필요한 주니어에게 적합한 시니어 찾기
```cypher
MATCH (j:Junior)-[:NEEDS]->(skill:Skill)<-[:HAS_SKILL]-(s:Senior)
WHERE j.name = "주니어A"
RETURN s.name, skill.name, s.reputation_score
ORDER BY s.reputation_score DESC
```

---

## 5. Mock 데이터 (MVP용)

```python
NODES = [
    # Seniors
    {"id": "s1", "label": "김○○ 시니어", "type": "Senior", "age": 65, "region": "군산", "skills": ["자동차 정비"], "score": 87},
    {"id": "s2", "label": "이○○ 시니어", "type": "Senior", "age": 62, "region": "전주", "skills": ["교육 설계"], "score": 73},
    {"id": "s3", "label": "박○○ 시니어", "type": "Senior", "age": 68, "region": "부산", "skills": ["제조업 관리"], "score": 91},
    {"id": "s4", "label": "최○○ 시니어", "type": "Senior", "age": 60, "region": "군산", "skills": ["노사 조정"], "score": 65},

    # Juniors
    {"id": "j1", "label": "주니어A",     "type": "Junior", "age": 28, "region": "군산", "goal": "자동차 브랜드 창업"},
    {"id": "j2", "label": "주니어B",     "type": "Junior", "age": 24, "region": "전주", "goal": "교육 스타트업"},
    {"id": "j3", "label": "주니어C",     "type": "Junior", "age": 31, "region": "부산", "goal": "스마트팩토리 취업"},

    # Skills
    {"id": "sk1", "label": "자동차 정비", "type": "Skill"},
    {"id": "sk2", "label": "교육 설계",   "type": "Skill"},
    {"id": "sk3", "label": "제조업 관리", "type": "Skill"},
    {"id": "sk4", "label": "노사 조정",   "type": "Skill"},

    # Regions
    {"id": "r1", "label": "군산", "type": "Region"},
    {"id": "r2", "label": "전주", "type": "Region"},
    {"id": "r3", "label": "부산", "type": "Region"},

    # Problems
    {"id": "p1", "label": "번아웃",     "type": "Problem"},
    {"id": "p2", "label": "창업 불안",  "type": "Problem"},
    {"id": "p3", "label": "취업 장벽",  "type": "Problem"},
]

EDGES = [
    # HAS_SKILL
    {"source": "s1", "target": "sk1", "label": "HAS_SKILL", "years": 30},
    {"source": "s2", "target": "sk2", "label": "HAS_SKILL", "years": 25},
    {"source": "s3", "target": "sk3", "label": "HAS_SKILL", "years": 35},
    {"source": "s4", "target": "sk4", "label": "HAS_SKILL", "years": 20},

    # NEEDS
    {"source": "j1", "target": "sk1", "label": "NEEDS"},
    {"source": "j2", "target": "sk2", "label": "NEEDS"},
    {"source": "j3", "target": "sk3", "label": "NEEDS"},

    # LIVES_IN
    {"source": "s1", "target": "r1", "label": "LIVES_IN"},
    {"source": "s2", "target": "r2", "label": "LIVES_IN"},
    {"source": "s3", "target": "r3", "label": "LIVES_IN"},
    {"source": "s4", "target": "r1", "label": "LIVES_IN"},
    {"source": "j1", "target": "r1", "label": "LIVES_IN"},
    {"source": "j2", "target": "r2", "label": "LIVES_IN"},
    {"source": "j3", "target": "r3", "label": "LIVES_IN"},

    # MENTORED (기완료)
    {"source": "s1", "target": "j1", "label": "MENTORED", "satisfaction": 4.8},
    {"source": "s2", "target": "j2", "label": "MENTORED", "satisfaction": 4.3},

    # IN_CRISIS
    {"source": "j1", "target": "p2", "label": "IN_CRISIS"},
    {"source": "j2", "target": "p1", "label": "IN_CRISIS"},
    {"source": "j3", "target": "p3", "label": "IN_CRISIS"},

    # SOLVED
    {"source": "s1", "target": "p2", "label": "SOLVED"},
    {"source": "s4", "target": "p1", "label": "SOLVED"},
]
```
