# Commerce X Commerce

이커머스 산업 특화 AI 실무 인재 양성 플랫폼

---

## 변경 이력

### v0.2  (2026-02-24)

**[FEAT] Phase 2 AI 도플갱어 MVP 추가**
- 강사가 AI 인터뷰를 통해 본인의 AI 분신을 생성하는 5단계 온보딩 구현
- 학생이 6자리 코드로 AI 강사와 실시간 스트리밍 채팅하는 UI 구현
- Claude API(`claude-opus-4-5`) 스트리밍 연동 (`client.messages.stream`)
- 강사 프로파일 및 대화 로그를 JSON 파일로 로컬 저장하는 스토리지 구현
- Streamlit 멀티페이지 구조 도입 (`pages/` 디렉토리)

**[FEAT] 랜딩페이지 UI 현대화**
- 디자인 레퍼런스 : Fourmula AI, Voku Studio, Roshan Sahu (Awwwards)
- Inter Tight 폰트, 흰 배경 (#FFFFFF), 오렌지 포인트 (#FA5D29), `clamp()` 유체 타이포 적용
- Streamlit 테마를 라이트 모드로 전환 (`.streamlit/config.toml`)

**[FIX] HTML이 코드 텍스트로 노출되는 렌더링 오류 수정**
- 원인 : `st.markdown(unsafe_allow_html=True)`는 Markdown을 먼저 처리하므로, f-string 들여쓰기로 인해 동적 HTML 변수가 4-공백 코드블록으로 오인식됨
- 수정 : 모든 동적 HTML 섹션을 Python 문자열 연결(`+`)로 재구성, `st.columns()` 의존 제거 후 CSS Grid로 대체

**[FIX] UI 이모티콘 전면 제거**
- `shared/config.py` : TARGET_SEGMENTS, AI_TOOLS, ONE_ON_ONE_COMPARE, CURRICULUM, PAGE_CONFIG 의 이모티콘 제거
- `phase1_landing/components.py` : 히어로 태그, 버튼, 폼, 푸터 등 전체 제거
- `phase1_landing/app.py` : 네비게이션 바 이모티콘 제거

---

### v0.1  (2026-02-22)

**[FEAT] Phase 1 랜딩페이지 MVP**
- 사전 신청 폼 (이름, 이메일, 연락처, 배경, 트랙, 신청 동기, 유입 경로)
- Google Sheets 자동 기록 (`gspread` + `google-auth`), 실패 시 CSV 폴백
- Streamlit Cloud 배포 구성 (`streamlit_app.py` 루트 진입점)
- `.gitignore` 및 `secrets.toml.template` 보안 설정

---

## 프로젝트 구조

```
commerce-x-commerce/
├── streamlit_app.py                # 루트 진입점 (Streamlit Cloud 설정값)
├── phase1_landing/
│   ├── app.py                      # Phase 1 랜딩페이지 메인
│   ├── components.py               # UI 컴포넌트 (섹션별 분리)
│   └── sheets_connector.py         # Google Sheets 연동
├── phase2_doppelganger/
│   ├── __init__.py
│   ├── storage.py                  # 강사 프로파일 JSON 저장소
│   ├── doppelganger_engine.py      # Claude API 스트리밍 엔진
│   ├── onboarding.py               # 강사 5단계 온보딩 UI
│   └── chat_ui.py                  # 학생 채팅 UI
├── pages/
│   ├── 1_강사_온보딩.py             # Streamlit 멀티페이지 : 강사용
│   └── 2_학생_채팅.py               # Streamlit 멀티페이지 : 학생용
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
| Phase 3 | KPI 역량 대시보드 — 학습 성과 시각화 | 예정 |
