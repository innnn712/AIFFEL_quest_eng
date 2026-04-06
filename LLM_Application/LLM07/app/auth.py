# app/auth.py
"""
Day 6 - API Key 인증
"""
from fastapi import Header, HTTPException

# 유효한 API Key 목록
VALID_API_KEYS = {
    "test-key-001": "사용자A",
    "test-key-002": "사용자B",
    "test-key-003": "사용자C",
}


def verify_api_key(x_api_key: str = Header(...)) -> str:
    """
    X-API-Key 헤더를 검증합니다.

    Args:
        x_api_key: 요청 헤더의 X-API-Key 값

    Returns:
        인증된 사용자 이름

    Raises:
        HTTPException: API Key가 유효하지 않으면 401 에러
    """
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="유효하지 않은 API Key입니다.",
        )
    return VALID_API_KEYS[x_api_key]