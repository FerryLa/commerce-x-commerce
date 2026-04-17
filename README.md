# Commerce X Commerce

이커머스 산업 특화 AI 실무 인재 양성 플랫폼

**라이브 데모**: [commerce-x-commerce.streamlit.app](https://commerce-x-commerce-fug7dedsec9vwj9qhyvquq.streamlit.app/)

---

## 릴리즈

| 버전 | 날짜 | 내용 |
|---|---|---|
| v0.4 | 2026-04-17 | Phase 4 시니어·주니어 지식 자산 네트워크 — Knowledge Graph 시각화, Reputation 점수, 노인·청소년 일자리 정책 프레임 / pages 파일명 영문화 + st.navigation() 전환 |
| v0.3 | 2026-02-26 | Phase 3 이커머스 역량 진단 대시보드 — 레이더 차트, 직무 추천, 자격증, 캘린더 |
| v0.2 | 2026-02-24 | Phase 2 AI 도플갱어 MVP, 랜딩페이지 UI 현대화, HTML 렌더링 버그 수정, 이모티콘 제거 |
| v0.1 | 2026-02-22 | Phase 1 랜딩페이지 MVP, Google Sheets 연동, Streamlit Cloud 배포 구성 |

---

## 프로젝트 구조

```
commerce-x-commerce/
├── streamlit_app.py                # 루트 진입점 — st.navigation() 멀티페이지
├── pages/
│   ├── 0_home.py                   # 🏠 홈 (Phase 1 랜딩페이지)
│   ├── 1_onboarding.py             # 👨‍🏫 강사 온보딩
│   ├── 2_chat.py                   # 💬 학생 채팅
│   ├── 3_dashboard.py              # 📊 역량 진단
│   └── 4_network.py                # 🔗 시니어·주니어 지식 자산 네트워크
├── phase1_landing/
│   ├── app.py                      # Phase 1 랜딩페이지 컴포넌트
│   ├── components.py               # UI 섹션별 렌더 함수
│   └── sheets_connector.py         # Google Sheets 연동
├── phase2_doppelganger/
│   ├── storage.py                  # 강사 프로파일 JSON 저장소
│   ├── doppelganger_engine.py      # Claude API 스트리밍 엔진
│   ├── onboarding.py               # 강사 5단계 온보딩 UI
│   └── chat_ui.py                  # 학생 채팅 UI
├── phase3_dashboard/
│   ├── assessment.py               # 12개 역량 설문 정의 및 채점 로직
│   ├── radar_chart.py              # Plotly 6각형 레이더 차트
│   ├── recommender.py              # 직무 / 자격증 / 기업 추천 엔진 (Claude AI)
│   ├── calendar_view.py            # 2026 자격증·컨퍼런스 일정 + 목표 등록
│   └── app.py                      # 대시보드 진입점
├── phase4_senior/
│   ├── data.py                     # Mock 데이터 (시니어·주니어·스킬·지역·문제 노드)
│   └── app.py                      # Knowledge Graph 시각화 + Reputation 패널
├── docs/
│   └── senior-asset-platform/
│       ├── README.md               # 전체 개요 + 3-Layer 아키텍처
│       ├── knowledge-graph.md      # Neo4j 노드/관계 모델 + Cypher 쿼리
│       ├── reputation-engine.md    # SourceCred 응용 점수 산정
│       └── matching-algorithm.md  # 6차원 유사도 매칭 설계
├── shared/
│   └── config.py                   # 공통 설정 (브랜드, 모델명, 데이터)
├── requirements.txt
├── .streamlit/
│   ├── config.toml                 # 라이트 테마, 오렌지 primaryColor
│   └── secrets.toml.template       # Secrets 입력 가이드 (Git 제외)
└── README.md
```

---

## 로컬 실행

```bash
# 패키지 설치
pip install -r requirements.txt

# Secrets 설정
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
# secrets.toml 파일에 실제 값 입력 (Git 커밋 금지)

# 실행
streamlit run streamlit_app.py
```

> Google Sheets 연동 없이 실행하면 신청 데이터가 `data/applications_fallback.csv`에 로컬 저장됩니다.

---

## Streamlit Cloud 배포

### 1. 앱 생성

[share.streamlit.io](https://share.streamlit.io) 접속 후 **New app** 클릭.

| 항목 | 입력값 |
|---|---|
| Repository | `your-id/commerce-x-commerce` |
| Branch | `main` |
| Main file path | `streamlit_app.py` |

### 2. Secrets 등록

앱 배포 후 **Settings > Secrets** 에 아래 형식으로 입력합니다.

```toml
[anthropic]
api_key = "sk-ant-..."

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key = "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
client_email = "your-sa@your-project.iam.gserviceaccount.com"

[sheets]
spreadsheet_id = "your-spreadsheet-id"
worksheet_name = "신청자"
```

### 3. Google Sheets 사전 준비

1. [console.cloud.google.com](https://console.cloud.google.com) 에서 Google Sheets API, Google Drive API 활성화
2. IAM > 서비스 계정 생성 > JSON 키 다운로드
3. [sheets.google.com](https://sheets.google.com) 에서 새 스프레드시트 생성, 시트 이름 `신청자`로 변경
4. 스프레드시트 공유에 서비스 계정 이메일 추가 (편집자 권한)

---

## Secrets 로컬 파일 구조

```toml
# .streamlit/secrets.toml  (Git 커밋 금지 — .gitignore에 포함됨)

[anthropic]
api_key = "sk-ant-..."

[gcp_service_account]
type = "service_account"
project_id = ""
private_key_id = ""
private_key = ""
client_email = ""
client_id = ""
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"

[sheets]
spreadsheet_id = ""
worksheet_name = "신청자"
```

---

## 보안 체크리스트

- `secrets.toml` 이 `.gitignore` 에 포함되어 있는가
- 서비스 계정 권한이 Sheets 읽기/쓰기로 최소화되어 있는가
- GitHub 레포가 Private 으로 설정되어 있는가
- Streamlit Cloud Secrets 에만 API 키가 존재하는가

---

## Phase 로드맵

| Phase | 내용 | 상태 |
|---|---|---|
| Phase 1 | 랜딩페이지 + Google Sheets 사전 신청 수집 | 완료 |
| Phase 2 | AI 도플갱어 MVP — 강사 AI 분신 생성 및 학생 채팅 | 완료 (MVP) |
| Phase 3 | 이커머스 역량 진단 대시보드 | 완료 (MVP) |
| Phase 4 | 시니어·주니어 지식 자산 네트워크 — Knowledge Graph + Reputation Engine | 완료 (MVP) |
| Phase 5 | Neo4j 실DB 연동 + 프로필 등록/관리 | 예정 |
| Phase 6 | Reputation 자동 집계 API + 매칭 엔진 | 예정 |

---

## Phase 3 — 이커머스 역량 진단 대시보드 (프로토타입 설계)

이커머스 업무 역량을 진단하고, 직무·자격증·기업·일정을 한 화면에서 제공하는 개인화 대시보드.

### 역량 진단 모델

6각형 레이더 차트로 이커머스 핵심 역량을 시각화합니다.
상위 6개 카테고리 아래 각 2개 세부 항목, 총 12개 지표로 구성됩니다.

| 카테고리 | 세부 항목 1 | 세부 항목 2 |
|---|---|---|
| 퍼포먼스 마케팅 | 광고 운영 (Meta / GFA) | 데이터 분석 (GA4 / ROAS) |
| 콘텐츠 & 브랜딩 | 카피라이팅 | 이미지 / 영상 제작 |
| 플랫폼 운영 | 쿠팡 / 스마트스토어 | CS & 리뷰 관리 |
| 데이터 & KPI | 지표 설계 | 대시보드 시각화 |
| AI 도구 활용 | 프롬프트 엔지니어링 | 업무 자동화 (n8n) |
| 공급망 & 물류 | 소싱 & 원가 계산 | 재고 / 배송 관리 |

### 주요 기능 (예정)

**직무 추천**
- 진단 점수 기반으로 적합 직무 Top 3 추천 (MD / 마케터 / 오퍼레이터 등)
- 현재 역량과 목표 직무의 갭 분석 및 단기 개선 경로 제시

**자격증 & 기업 추천**
- 부족 역량 카테고리에 대응하는 관련 자격증 목록 제시
- 역량 프로필과 유사한 채용 중인 기업 리스트

**학습 일정 캘린더**
- 추천 자격증 시험일, 관련 컨퍼런스 / 세미나 일정을 자동 수집
- 월간 캘린더 뷰로 정리, 개인 목표 일정 등록 기능

### 예정 기술 스택

```
phase3_dashboard/
├── app.py                  # 대시보드 진입점
├── assessment.py           # 역량 진단 설문 및 채점 로직
├── radar_chart.py          # Plotly 6각형 레이더 차트
├── recommender.py          # 직무 / 자격증 / 기업 추천 엔진
└── calendar_sync.py        # 외부 일정 수집 및 캘린더 렌더링
```

의존 패키지 : `plotly`, `pandas`, `anthropic` (추천 생성), `requests` (일정 수집)
