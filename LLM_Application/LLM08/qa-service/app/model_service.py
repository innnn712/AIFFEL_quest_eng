# app/model_service.py
from transformers import pipeline
from dotenv import load_dotenv
from huggingface_hub import login
import torch
import os

load_dotenv()
login(token=os.getenv("HF_TOKEN"))

MODEL_NAME = "monologg/koelectra-base-v3-finetuned-korquad"

def load_model():
    device = 0 if torch.cuda.is_available() else -1
    model = pipeline(
        "question-answering",
        model=MODEL_NAME,
        device=device,
    )
    return model

def predict(model, context: str, question: str) -> dict:
    result = model(question=question, context=context)
    return {
        "success": True,
        "answer": result["answer"],
        "confidence": round(result["score"], 4),
        "start": result["start"],
        "end": result["end"],
    }