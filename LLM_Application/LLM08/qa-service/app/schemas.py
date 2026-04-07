# app/schemas.py
from pydantic import BaseModel, Field

class PredictRequest(BaseModel):
    context: str = Field(
        ...,
        min_length=10, # 지문의 최소 길이 ('안녕'과 같은 의미없는 짧은 문자열 차단 목적)
        max_length=1000, # 지문의 최대 길이 (보통 한국어 기준 1토큰은 1~2자 정도 512토큰은 약 500~1000자 정도)
        description="답변을 찾을 한국어 지문 (최소 10자, 최대 1000자)",
        example="세종대왕은 1397년 5월 15일에 태어났으며, 훈민정음을 1443년에 창제하였다."
    )


    question: str = Field(
        ...,
        min_length=5, # 질문의 최소 길이 (너무 짧은 질문은 차단 목적)
        max_length=150, # 질문의 최대 길이 (question에 남는 여유를 계산해보면 약 100토큰)
        description="지문을 바탕으로 답을 찾을 질문 (최소 5자, 최대 150자)",
        example="세종대왕은 언제 훈민정음을 창제했나요?"
    )

class PredictResponse(BaseModel):
    success: bool = Field(description="추론 성공 여부")
    answer: str = Field(description="지문에서 추출한 답변")
    confidence: float = Field(description="답변 신뢰도 (0.0 ~ 1.0)")
    start: int = Field(description="지문에서 답변 시작 위치")
    end: int = Field(description="지문에서 답변 끝 위치")