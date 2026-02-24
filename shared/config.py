# =============================================================================
# Commerce X Commerce — 공통 설정
# =============================================================================
# 거버넌스: 모든 설정값은 이 파일에서 중앙집중 관리
# 환경변수 또는 Streamlit Secrets에서 민감 정보를 로드
# =============================================================================

import os
import streamlit as st
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# 브랜드 상수
# ---------------------------------------------------------------------------
APP_NAME = "Commerce X Commerce"
APP_TAGLINE = "이커머스 산업 특화 AI 실무 인재 양성 플랫폼"
APP_SLOGAN = "1:1 AI 커리큘럼으로 이커머스 취업을 실현합니다"

BRAND_COLORS = {
    "bg":           "#FFFFFF",   # 메인 배경 — 클린 화이트
    "bg_alt":       "#F7F7F7",   # 섹션 교차 배경
    "bg_dark":      "#111111",   # 다크 섹션
    "text":         "#111111",   # 기본 텍스트
    "text_muted":   "#666666",   # 보조 텍스트
    "text_light":   "#AAAAAA",   # 약한 텍스트
    "accent":       "#FA5D29",   # 오렌지 — 주 CTA (Awwwards 공통)
    "accent_light": "#FFF0EB",   # 오렌지 연한 배경
    "border":       "#E8E8E8",   # 카드·구분선 보더
    "white":        "#FFFFFF",
    "black":        "#111111",
}


# ---------------------------------------------------------------------------
# 커리큘럼 데이터
# ---------------------------------------------------------------------------
CURRICULUM = [
    {"week": "1~2주", "topic": "이커머스 구조 + AI 기초",
     "content": "상품/광고 구조, KPI 이해, LLM 기초",
     "output": "KPI 정의서, AI 툴 활용 실습"},
    {"week": "3~4주", "topic": "실무 재현",
     "content": "상세페이지 AI 생성, 광고 카피 자동화, 리뷰 분석",
     "output": "AI 생성 콘텐츠 포트폴리오"},
    {"week": "5~6주", "topic": "자동화 설계",
     "content": "CRM 자동화, 리포트 자동 생성, 업무 프로세스 개선",
     "output": "자동화 워크플로우 설계서"},
    {"week": "7~8주", "topic": "프로젝트 구축",
     "content": "가상 브랜드 운영, 광고 시뮬레이션, 데이터 분석",
     "output": "광고 운영 리포트 + 데이터 분석"},
    {"week": "9~10주", "topic": "배포 + KPI 연결",
     "content": "포트폴리오 제작, 성과 수치 정리, JD 매칭",
     "output": "KPI 기반 포트폴리오 완성"},
]

TARGET_SEGMENTS = [
    {"title": "비전공자",
     "desc": "이커머스 취업 희망, AI 경험 전무\n→ 어디서 시작해야 할지 모름"},
    {"title": "부트캠프 수료자",
     "desc": "기초 기술 보유, 직무 연결 부재\n→ 실무 포트폴리오와 JD 매칭 필요"},
    {"title": "경력 전환자",
     "desc": "타 업종 경력 보유, 이커머스 전환 희망\n→ AI 활용 실무 역량 증명 필요"},
]

DIFFERENTIATORS = [
    {"title": "3층 AI 구조",
     "desc": "AI 코치 + C2C 멘토 + AI 강사 복제"},
    {"title": "KPI 기반 포트폴리오",
     "desc": "실무 생산성을 수치로 증명"},
    {"title": "기업 파이프라인",
     "desc": "수료 후 기업 채용 직접 연계"},
    {"title": "10주 집중 트랙",
     "desc": "이론 → 재현 → 배포 → KPI 연결"},
]

SOCIAL_PROOF = [
    {"stat": "10주", "label": "집중 완성 트랙"},
    {"stat": "1:1", "label": "맞춤 AI 커리큘럼"},
    {"stat": "6개+", "label": "실전 AI 도구 실습"},
    {"stat": "60%+", "label": "목표 취업 연결률"},
]

AI_TOOLS = [
    {"name": "Claude",           "desc": "AI 코치 & 콘텐츠 자동화"},
    {"name": "ChatGPT",          "desc": "광고 카피 & 아이디어 발굴"},
    {"name": "Midjourney",       "desc": "상품 이미지 & 썸네일 생성"},
    {"name": "n8n",              "desc": "업무 자동화 워크플로우"},
    {"name": "GA4",              "desc": "데이터 분석 & KPI 트래킹"},
    {"name": "쿠팡·스마트스토어", "desc": "플랫폼 실전 운영 실습"},
]

ONE_ON_ONE_COMPARE = [
    ("일방향 강의",    "1:1 AI 코치"),
    ("모두 같은 속도", "내 페이스대로"),
    ("이론 위주",      "실무 재현 중심"),
    ("수료증만 남음",  "KPI 포트폴리오"),
    ("취업 연결 없음", "기업 파이프라인 직결"),
]


# ---------------------------------------------------------------------------
# Google Sheets 설정
# ---------------------------------------------------------------------------
def get_sheets_config() -> dict:
    """
    Streamlit Secrets 또는 환경변수에서 Google Sheets 설정을 로드.
    Secrets 구조:
        [gcp_service_account]
        type = "service_account"
        ...
        [sheets]
        spreadsheet_id = "..."
        worksheet_name = "신청자"
    """
    try:
        # Streamlit Cloud 배포 시
        return {
            "credentials": dict(st.secrets["gcp_service_account"]),
            "spreadsheet_id": st.secrets["sheets"]["spreadsheet_id"],
            "worksheet_name": st.secrets["sheets"].get("worksheet_name", "신청자"),
        }
    except Exception:
        # 로컬 개발 시 — 환경변수 fallback
        return {
            "credentials": None,  # 로컬에선 None → CSV fallback 사용
            "spreadsheet_id": os.getenv("SHEETS_SPREADSHEET_ID", ""),
            "worksheet_name": os.getenv("SHEETS_WORKSHEET", "신청자"),
        }


# ---------------------------------------------------------------------------
# Streamlit 페이지 공통 설정
# ---------------------------------------------------------------------------
PAGE_CONFIG = {
    "page_title": APP_NAME,
    "page_icon": None,
    "layout": "wide",
    "initial_sidebar_state": "collapsed",
}


# ---------------------------------------------------------------------------
# Phase 2 — AI 도플갱어 설정
# ---------------------------------------------------------------------------
CLAUDE_MODEL = "claude-opus-4-5"        # 도플갱어 응답 / 인터뷰 진행
CLAUDE_MODEL_FAST = "claude-haiku-4-5"  # 페르소나 추출 등 단순 작업

DOPPELGANGER_MAX_TOKENS = 1024
INTERVIEW_MAX_TOKENS = 800
PERSONA_EXTRACT_MAX_TOKENS = 500

INTERVIEW_MIN_TURNS = 6   # 최소 인터뷰 교환 횟수 (user 기준)
QA_MIN_COUNT = 3          # 최소 Q&A 등록 수
KNOWLEDGE_BASE_LIMIT = 2000  # system prompt에 포함할 지식 베이스 최대 글자 수

def get_anthropic_api_key() -> str:
    """Streamlit Secrets 또는 환경변수에서 Anthropic API 키 로드."""
    try:
        return st.secrets["anthropic"]["api_key"]
    except Exception:
        return os.getenv("ANTHROPIC_API_KEY", "")
