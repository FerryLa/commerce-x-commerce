# =============================================================================
# Phase 2 — 도플갱어 데이터 저장/로드
# =============================================================================
# MVP: 로컬 JSON 파일 기반 (Streamlit Cloud 세션 내 유지)
# Production: Google Sheets 마이그레이션 예정
# =============================================================================

import json
import logging
import random
import string
from datetime import datetime
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 경로 상수
# ---------------------------------------------------------------------------
DATA_DIR = Path("data")
INSTRUCTORS_FILE = DATA_DIR / "instructors.json"
CONVERSATIONS_DIR = DATA_DIR / "conversations"


def _ensure_dirs() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONVERSATIONS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# 강사 코드 생성
# ---------------------------------------------------------------------------
def _generate_code(length: int = 6) -> str:
    """숫자+대문자 조합 고유 코드 생성 (예: A3B7K2)"""
    chars = string.ascii_uppercase + string.digits
    return "".join(random.choices(chars, k=length))


# ---------------------------------------------------------------------------
# 강사 CRUD
# ---------------------------------------------------------------------------
def load_all_instructors() -> dict:
    """전체 강사 데이터 로드. {code: instructor_dict} 형태."""
    _ensure_dirs()
    if INSTRUCTORS_FILE.exists():
        try:
            with open(INSTRUCTORS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"[Storage] 강사 데이터 로드 실패: {e}")
    return {}


def _write_instructors(instructors: dict) -> None:
    _ensure_dirs()
    with open(INSTRUCTORS_FILE, "w", encoding="utf-8") as f:
        json.dump(instructors, f, ensure_ascii=False, indent=2)


def save_instructor(instructor_data: dict) -> str:
    """
    강사 데이터를 저장하고 고유 접속 코드를 반환한다.

    Args:
        instructor_data: 온보딩에서 수집한 강사 정보 dict

    Returns:
        6자리 접속 코드 (ex. "A3B7K2")
    """
    instructors = load_all_instructors()

    # 중복 없는 코드 생성
    code = _generate_code()
    while code in instructors:
        code = _generate_code()

    instructor_data["instructor_id"] = code
    instructor_data["created_at"] = datetime.now().isoformat()
    instructor_data["is_active"] = True
    instructor_data["total_conversations"] = 0

    instructors[code] = instructor_data
    _write_instructors(instructors)

    logger.info(f"[Storage] 강사 저장 완료: {instructor_data.get('name')} / 코드: {code}")
    return code


def get_instructor(code: str) -> Optional[dict]:
    """코드로 강사 데이터 조회. 없으면 None."""
    instructors = load_all_instructors()
    return instructors.get(code.upper().strip())


def update_instructor_stats(code: str) -> None:
    """대화 카운트 +1 업데이트."""
    instructors = load_all_instructors()
    if code in instructors:
        instructors[code]["total_conversations"] = (
            instructors[code].get("total_conversations", 0) + 1
        )
        _write_instructors(instructors)


# ---------------------------------------------------------------------------
# 대화 기록 저장
# ---------------------------------------------------------------------------
def save_conversation(instructor_id: str, messages: list) -> str:
    """
    학생-도플갱어 대화 기록을 저장한다.

    Returns:
        conversation_id 문자열
    """
    _ensure_dirs()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    conv_id = f"{instructor_id}_{ts}"
    conv_file = CONVERSATIONS_DIR / f"{conv_id}.json"

    payload = {
        "conversation_id": conv_id,
        "instructor_id": instructor_id,
        "messages": messages,
        "message_count": len(messages),
        "created_at": datetime.now().isoformat(),
    }

    try:
        with open(conv_file, "w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        update_instructor_stats(instructor_id)
    except IOError as e:
        logger.error(f"[Storage] 대화 저장 실패: {e}")

    return conv_id


def get_instructor_stats(code: str) -> dict:
    """강사의 누적 통계 반환."""
    instructor = get_instructor(code)
    if not instructor:
        return {}

    conv_files = list(CONVERSATIONS_DIR.glob(f"{code}_*.json"))
    total_messages = 0
    for f in conv_files:
        try:
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
                total_messages += data.get("message_count", 0)
        except Exception:
            pass

    return {
        "total_conversations": len(conv_files),
        "total_messages": total_messages,
        "created_at": instructor.get("created_at", ""),
    }
