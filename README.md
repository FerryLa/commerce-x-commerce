# Commerce X Commerce — MVP 배포 가이드

이커머스 산업 특화 AI 실무 인재 양성 플랫폼

---

## 프로젝트 구조

```
commerce_x_commerce/
├── phase1_landing/
│   ├── app.py              # Phase 1: 랜딩페이지 메인
│   ├── components.py       # UI 컴포넌트 (섹션별 분리)
│   └── sheets_connector.py # Google Sheets 연동
├── phase2_ai_coach/        # Phase 2: AI 코치 (예정)
├── phase3_dashboard/       # Phase 3: KPI 대시보드 (예정)
├── shared/
│   └── config.py           # 공통 설정 (중앙집중 관리)
├── requirements.txt
├── .streamlit/
│   ├── config.toml         # 다크 테마 설정
│   └── secrets.toml.template  # Secrets 입력 가이드
└── README.md
```

---

## 배포 전 준비 — 두 가지 선행 작업

배포 3단계 전에 아래 두 가지를 먼저 완료해야 합니다.

### A. Google Sheets 연동 설정

신청 폼 데이터를 받을 스프레드시트와 서비스 계정을 만듭니다.

**1) Google Cloud 서비스 계정 생성**
1. [console.cloud.google.com](https://console.cloud.google.com) 접속
2. 새 프로젝트 생성 (또는 기존 프로젝트 선택)
3. API 및 서비스 → **Google Sheets API** 활성화
4. API 및 서비스 → **Google Drive API** 활성화
5. IAM → 서비스 계정 → 새 서비스 계정 생성
6. 키 탭 → 새 키 추가 → **JSON 다운로드** (이 파일이 Secrets에 들어갑니다)

**2) Google Sheets 준비**
1. [sheets.google.com](https://sheets.google.com)에서 새 스프레드시트 생성
2. 시트 이름을 `신청자`로 변경
3. 공유 → 서비스 계정 이메일 주소 추가 (편집자 권한)
4. URL에서 `spreadsheet_id` 복사
   ```
   https://docs.google.com/spreadsheets/d/[여기가 spreadsheet_id]/edit
   ```

### B. Secrets 파일 준비

`.streamlit/secrets.toml.template`을 참고해 실제 값을 채워둡니다.  
이 내용은 아래 **Step 3**에서 Streamlit Cloud에 붙여넣습니다.

---

## 배포 3단계

### Step 1 — GitHub 레포 생성 & 푸시

```bash
# 프로젝트 루트에서 실행
git init
git add .
git commit -m "feat: Phase 1 랜딩페이지 MVP"

# GitHub에서 새 레포 생성 후
git remote add origin https://github.com/your-id/commerce-x-commerce.git
git push -u origin main
```

> `.gitignore`에 반드시 추가하세요:
> ```
> .streamlit/secrets.toml
> data/
> *.pyc
> __pycache__/
> ```

### Step 2 — Streamlit Cloud 앱 생성

1. [share.streamlit.io](https://share.streamlit.io) 접속 → **New app**
2. 아래 정보 입력:

   | 항목 | 입력값 |
   |------|--------|
   | Repository | `your-id/commerce-x-commerce` |
   | Branch | `main` |
   | Main file path | `phase1_landing/app.py` |

3. **Deploy** 클릭 → 빌드 시작 (약 2~3분)

### Step 3 — Secrets 입력 (보안 핵심)

앱 배포 후 설정합니다.

1. Streamlit Cloud 대시보드 → 앱 선택 → **Settings → Secrets**
2. `.streamlit/secrets.toml.template` 내용을 복사 후 실제 값으로 교체해 붙여넣기
3. **Save** 클릭 → 앱 자동 재시작

```toml
# 이 형식으로 Secrets에 입력
[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key = "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----\n"
client_email = "your-sa@your-project.iam.gserviceaccount.com"
# ... (나머지 JSON 키 내용)

[sheets]
spreadsheet_id = "your-spreadsheet-id"
worksheet_name = "신청자"
```

배포 완료 후 `https://your-app-name.streamlit.app` URL이 생성됩니다.

---

## 로컬 테스트 (선택)

배포 전에 로컬에서 먼저 확인하려면:

```bash
pip install -r requirements.txt

# 로컬 Secrets 설정
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
# secrets.toml 파일에 실제 값 입력 (Git에 커밋 금지)

streamlit run phase1_landing/app.py
```

> Sheets 연동 없이 테스트하면 신청 데이터가 `data/applications_fallback.csv`에 저장됩니다.

---

## 보안 체크리스트

- [ ] `secrets.toml`이 `.gitignore`에 포함되어 있는가
- [ ] 서비스 계정 권한이 Sheets 읽기/쓰기로 최소화되어 있는가
- [ ] GitHub 레포가 Private으로 설정되어 있는가
- [ ] Streamlit Cloud Secrets에만 API 키가 존재하는가

---

## Phase 로드맵

| Phase | 내용 | 상태 |
|-------|------|------|
| Phase 1 | 랜딩페이지 + Google Sheets 사전 신청 | ✅ 완성 |
| Phase 2 | AI 코치 시스템 (Claude API 연동) | 🔜 다음 |
| Phase 3 | KPI 역량 대시보드 (6각형 레이더 차트) | 🔜 다음 |