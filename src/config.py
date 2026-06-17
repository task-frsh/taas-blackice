"""환경변수 로더 — CLAUDE.md 8장 cascade 규칙.

로딩 순서 (뒤가 앞을 덮어씀):
1. 워크스페이스 공용 .env  (C:\\Users\\haneu\\claude\\.env)
2. 프로젝트 .env           (taas_blackice/.env)  ← TAAS 키는 여기

키는 코드에 절대 하드코딩하지 않는다. .env 파일에서만 읽는다.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# taas_blackice/ 프로젝트 루트
PROJECT_ROOT = Path(__file__).resolve().parent.parent
# 워크스페이스 루트 (claude/)
WORKSPACE_ROOT = PROJECT_ROOT.parent

# 1) 공용 .env → 2) 프로젝트 .env (override=True 로 프로젝트 값이 우선)
load_dotenv(WORKSPACE_ROOT / ".env", override=False)
load_dotenv(PROJECT_ROOT / ".env", override=True)


def get_taas_api_key() -> str:
    """TAAS API 키 반환. 없으면 친절한 에러로 안내."""
    key = os.getenv("TAAS_API_KEY", "").strip()
    if not key or key.startswith("여기에"):
        raise RuntimeError(
            "TAAS_API_KEY 가 설정되지 않았습니다.\n"
            f"→ {PROJECT_ROOT / '.env'} 파일을 만들고 TAAS_API_KEY=실제키 를 적어주세요.\n"
            "  (.env.example 을 복사해서 쓰면 됩니다)"
        )
    return key


def get_google_maps_api_key() -> str:
    """Google Maps 키 반환 (선택). 없으면 빈 문자열 — 무료 Carto 지도로 폴백."""
    return os.getenv("Google_MAPS_API_KEY", "").strip()
