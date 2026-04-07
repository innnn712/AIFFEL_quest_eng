# app/main.py
# FastAPI 서버

import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, Depends, HTTPException
from app.auth import verify_api_key
from app.schemas import PredictRequest, PredictResponse
from app.model_service import load_model, predict

# FastAPI 앱 생성
app = FastAPI(
    title="한국어 QA 서비스",
    description="지문과 질문을 입력하면 답변을 추출합니다.",
    version="1.0.0",
)

# 스레드풀 생성
executor = ThreadPoolExecutor(max_workers=1)

# 서버 시작 시 모델 한 번만 로드
@app.on_event("startup")
async def startup():
    app.state.model = load_model()
    print("✅ 모델 로드 완료")

# 헬스체크 엔드포인트
@app.get("/health")
async def health():
    return {"status": "ok"}

# 추론 엔드포인트
@app.post("/predict", response_model=PredictResponse)
async def predict_api(
    request: PredictRequest,
    api_key: str = Depends(verify_api_key),  # API Key 인증
):
    try:
        # 비동기 추론 (run_in_executor로 별도 스레드에서 실행)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            predict,
            app.state.model,
            request.context,
            request.question,
        )
        return PredictResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"추론 실패: {str(e)}")