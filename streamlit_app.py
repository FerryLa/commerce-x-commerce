# =============================================================================
# Commerce X Commerce — Streamlit Cloud 진입점
# =============================================================================
# Streamlit Cloud는 루트의 streamlit_app.py 또는 app.py를 자동 탐지합니다.
# 이 파일은 phase1_landing/app.py 를 import하여 실행합니다.
# =============================================================================

import sys
from pathlib import Path

# 루트 경로를 sys.path에 추가 (shared, phase1_landing 모듈 접근 보장)
ROOT = Path(__file__).parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Phase 1 랜딩페이지 실행
import phase1_landing.app  # noqa: F401, E402
