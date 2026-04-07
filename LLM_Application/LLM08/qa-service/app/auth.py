# -*- coding: utf-8 -*-
# app/auth.py

from fastapi import Header, HTTPException

# 유효한 API Key 목록
VALID_API_KEYS = {
    "test-key-001": "사용자1",
    "test-key-002": "사용자2",
    "test-key-003": "사용자3",
}

async def verify_api_key(x_api_key: str = Header(None)) -> str:
    """
    X-API-Key 헤더를 검증합니다.
    """
    if x_api_key is None:
        raise HTTPException(
            status_code=401,
            detail="API Key가 없습니다. X-API-Key 헤더를 추가해주세요.",
        )
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="유효하지 않은 API Key입니다.",
        )
    return VALID_API_KEYS[x_api_key]