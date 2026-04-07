# test_model.py
from dotenv import load_dotenv
from huggingface_hub import login
from transformers import pipeline
import torch
import os

# .env 로드
load_dotenv()
login(token=os.getenv("HF_TOKEN"))

# 이하 기존 코드 동일
device = 0 if torch.cuda.is_available() else -1
print(f"사용 디바이스: {'GPU' if device == 0 else 'CPU'}")

print("모델 로드 중... (최초 실행 시 시간이 걸립니다)")
qa_pipeline = pipeline(
    "question-answering",
    model="monologg/koelectra-base-v3-finetuned-korquad",
    device=device,
)
print("✅ 모델 로드 완료")

test_cases = [
    {
        "context": "세종대왕은 1397년 5월 15일에 태어났으며, 한국의 문자인 훈민정음을 1443년에 창제하였다.",
        "question": "세종대왕은 언제 훈민정음을 창제했나요?",
    },
    {
        "context": "대한민국의 수도는 서울이며, 인구는 약 950만 명이다. 서울은 한강을 중심으로 남북으로 나뉜다.",
        "question": "대한민국의 수도는 어디인가요?",
    },
    {
        "context": "파이썬은 1991년 귀도 반 로섬이 발표한 프로그래밍 언어로, 간결한 문법과 높은 가독성이 특징이다.",
        "question": "파이썬을 만든 사람은 누구인가요?",
    },
]

print("\n--- 추론 결과 ---")
for i, tc in enumerate(test_cases):
    result = qa_pipeline(question=tc["question"], context=tc["context"])
    print(f"\n[테스트 {i+1}]")
    print(f"  질문: {tc['question']}")
    print(f"  답변: {result['answer']}")
    print(f"  신뢰도: {result['score']:.4f}")
    print(f"  위치: {result['start']}~{result['end']}")