# =============================================================================
# AI Commerce School — Google Sheets 연동 모듈
# =============================================================================
# 거버넌스: 외부 데이터 저장소 접근을 단일 모듈에서 관리
# 보안: 서비스 계정 키는 Streamlit Secrets에서만 로드
# Fallback: Sheets 미연동 시 로컬 CSV에 저장 (데이터 유실 방지)
# =============================================================================

import csv
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import streamlit as st

logger = logging.getLogger(__name__)

# 로컬 Fallback 저장 경로
FALLBACK_CSV = Path("data/applications_fallback.csv")

# Google Sheets 헤더 (컬럼 순서 표준화)
SHEET_HEADERS = [
    "신청일시", "이름", "이메일", "연락처",
    "배경", "동기", "관심트랙", "출처",
]


# ---------------------------------------------------------------------------
# 내부 유틸
# ---------------------------------------------------------------------------

def _get_gspread_client():
    """
    gspread 클라이언트를 생성한다.
    Streamlit Secrets의 gcp_service_account 섹션을 사용.
    """
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds_dict = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
    return gspread.authorize(creds)


def _save_to_csv_fallback(row: dict) -> None:
    """Google Sheets 연동 실패 시 로컬 CSV에 저장 (데이터 유실 방지)."""
    FALLBACK_CSV.parent.mkdir(parents=True, exist_ok=True)
    file_exists = FALLBACK_CSV.exists()

    with open(FALLBACK_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SHEET_HEADERS)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    logger.warning(f"[Fallback] CSV 저장 완료: {FALLBACK_CSV}")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def append_application(form_data: dict) -> dict:
    """
    사전 신청 데이터를 Google Sheets에 추가한다.

    Args:
        form_data: {
            "name": str,
            "email": str,
            "phone": str,
            "background": str,       # 비전공자 / 부트캠프수료자 / 경력전환자
            "motivation": str,
            "track": str,            # 관심 트랙
            "source": str,           # 유입 경로
        }

    Returns:
        {"success": bool, "message": str, "storage": "sheets" | "csv" | "none"}
    """
    row = {
        "신청일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "이름": form_data.get("name", ""),
        "이메일": form_data.get("email", ""),
        "연락처": form_data.get("phone", ""),
        "배경": form_data.get("background", ""),
        "동기": form_data.get("motivation", ""),
        "관심트랙": form_data.get("track", ""),
        "출처": form_data.get("source", "직접"),
    }

    # ── Google Sheets 시도 ──────────────────────────────────────────────────
    try:
        from shared.config import get_sheets_config
        cfg = get_sheets_config()

        if not cfg["credentials"]:
            raise ValueError("Sheets 인증 정보 없음 — CSV fallback 사용")

        client = _get_gspread_client()
        spreadsheet = client.open_by_key(cfg["spreadsheet_id"])
        worksheet = spreadsheet.worksheet(cfg["worksheet_name"])

        # 헤더가 없으면 자동 삽입
        existing = worksheet.get_all_values()
        if not existing:
            worksheet.append_row(SHEET_HEADERS)

        worksheet.append_row([row[h] for h in SHEET_HEADERS])
        logger.info(f"[Sheets] 신청 저장 완료: {row['이메일']}")
        return {"success": True, "message": "신청이 완료되었습니다!", "storage": "sheets"}

    except Exception as e:
        logger.error(f"[Sheets] 저장 실패: {e}")

    # ── CSV Fallback ────────────────────────────────────────────────────────
    try:
        _save_to_csv_fallback(row)
        return {"success": True, "message": "신청이 완료되었습니다!", "storage": "csv"}
    except Exception as e:
        logger.error(f"[CSV] Fallback 저장 실패: {e}")
        return {"success": False, "message": "저장 중 오류가 발생했습니다. 다시 시도해주세요.", "storage": "none"}


def validate_application(form_data: dict) -> list[str]:
    """
    신청 폼 유효성 검사.

    Returns:
        오류 메시지 리스트 (빈 리스트 = 유효)
    """
    errors = []

    name = form_data.get("name", "").strip()
    if not name or len(name) < 2:
        errors.append("이름을 2자 이상 입력해주세요.")

    email = form_data.get("email", "").strip()
    if not email or "@" not in email or "." not in email.split("@")[-1]:
        errors.append("유효한 이메일 주소를 입력해주세요.")

    phone = form_data.get("phone", "").strip()
    digits = phone.replace("-", "").replace(" ", "")
    if not digits.isdigit() or len(digits) < 10:
        errors.append("유효한 연락처를 입력해주세요. (예: 010-1234-5678)")

    background = form_data.get("background", "")
    if not background:
        errors.append("현재 배경을 선택해주세요.")

    return errors
