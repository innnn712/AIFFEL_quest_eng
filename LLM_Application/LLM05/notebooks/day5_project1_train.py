"""
Day 5 — [프로젝트 1] 학습 스크립트
강의 슬라이드의 day5_project1.ipynb 내용을 실행 파일로 구성
"""
import os
import json
import numpy as np
import torch
import torch.nn as nn
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset, DataLoader

os.makedirs("models", exist_ok=True)

# ── 2.1 데이터 로드 및 탐색 ─────────────────────────────────────
print("=" * 50)
print("  2.1 데이터 로드")
print("=" * 50)

from sklearn.datasets import fetch_california_housing
data = fetch_california_housing()

X, y = data.data, data.target
feature_names = data.feature_names

print(f"샘플 수: {data.data.shape[0]:,}")
print(f"피처 수: {data.data.shape[1]}")
print(f"타겟: {data.target_names}")
print(f"\n피처 목록:")
for i, name in enumerate(feature_names):
    print(f"  {i+1}. {name}")

# 학습/테스트 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42   # *your code* — test_size와 random_state 설정
)
print(f"\n학습 데이터: {X_train.shape[0]:,}개")
print(f"테스트 데이터: {X_test.shape[0]:,}개")

# ── 2.2 전처리: 정규화 ──────────────────────────────────────────
print("\n" + "=" * 50)
print("  2.2 전처리: 정규화")
print("=" * 50)

# 학습 데이터의 평균/표준편차 계산 (테스트 데이터에는 학습 데이터의 통계를 사용)
train_mean = X_train.mean(axis=0)   # *your code* — 축(axis) 설정
train_std  = X_train.std(axis=0)    # *your code* — 축(axis) 설정

print(f"피처별 평균: {np.round(train_mean, 2)}")
print(f"피처별 표준편차: {np.round(train_std, 2)}")

# 정규화 적용
X_train_norm = (X_train - train_mean) / train_std   # *your code* — 정규화 공식
X_test_norm  = (X_test  - train_mean) / train_std   # 테스트에도 학습 데이터의 통계 사용

print(f"\n정규화 후 학습 데이터 평균: {np.round(X_train_norm.mean(axis=0), 4)}")
print(f"정규화 후 학습 데이터 표준편차: {np.round(X_train_norm.std(axis=0), 4)}")

# ── 텐서 변환 ──────────────────────────────────────────────────
X_train_tensor = torch.FloatTensor(X_train_norm)
y_train_tensor = torch.FloatTensor(y_train).unsqueeze(1)   # *your code* — (N,) → (N,1)
X_test_tensor  = torch.FloatTensor(X_test_norm)
y_test_tensor  = torch.FloatTensor(y_test).unsqueeze(1)

print(f"\nX_train 텐서: {X_train_tensor.shape}")
print(f"y_train 텐서: {y_train_tensor.shape}")

# ── 2.3 모델 정의 및 학습 ───────────────────────────────────────
print("\n" + "=" * 50)
print("  2.3 모델 정의 및 학습")
print("=" * 50)

# 모델 정의 (housing_model.py와 동일)
import sys
sys.path.insert(0, ".")
from app.housing_model import HousingModel

model = HousingModel(input_dim=8)
print(f"모델 구조:\n{model}")
print(f"파라미터 수: {sum(p.numel() for p in model.parameters()):,}")

# 학습 설정
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
train_loader  = DataLoader(train_dataset, batch_size=256, shuffle=True)

criterion = nn.MSELoss()                                    # *your code* — 회귀이므로 MSELoss
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)  # *your code* — Adam 옵티마이저

EPOCHS = 50

# 학습 루프
model.train()
for epoch in range(1, EPOCHS + 1):
    running_loss = 0.0
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()
        predictions = model(X_batch)          # *your code* — 순전파
        loss = criterion(predictions, y_batch) # *your code* — 손실 계산
        loss.backward()
        optimizer.step()
        running_loss += loss.item()

    if epoch % 10 == 0:
        avg_loss = running_loss / len(train_loader)
        print(f"Epoch {epoch:3d}/{EPOCHS} — Loss: {avg_loss:.4f}")

# ── 테스트 평가 ─────────────────────────────────────────────────
model.eval()
with torch.no_grad():
    test_preds = model(X_test_tensor)
    test_loss  = criterion(test_preds, y_test_tensor)

    # MAE (Mean Absolute Error) 계산
    mae = torch.abs(test_preds - y_test_tensor).mean().item()

print(f"\n테스트 MSE:  {test_loss.item():.4f}")
print(f"테스트 MAE:  {mae:.4f} ($100,000 단위)")
print(f"테스트 MAE:  ${mae * 100000:,.0f} (실제 금액)")

# ── 2.4 모델 및 전처리 파라미터 저장 ───────────────────────────
print("\n" + "=" * 50)
print("  2.4 모델 및 전처리 파라미터 저장")
print("=" * 50)

# 모델 가중치 저장
torch.save(model.state_dict(), "models/housing_model.pth")  # *your code* — state_dict 저장
size_kb = os.path.getsize("models/housing_model.pth") / 1024
print(f"✅ 모델 저장: models/housing_model.pth ({size_kb:.1f} KB)")

# 전처리 파라미터 저장 (배포 시 필수!)
preprocessing_params = {
    "mean": train_mean.tolist(),
    "std":  train_std.tolist(),
    "feature_names": feature_names,
}

with open("models/housing_preprocessing.json", "w") as f:
    json.dump(preprocessing_params, f, indent=2)
print(f"✅ 전처리 파라미터 저장: models/housing_preprocessing.json")

print("\n🎉 학습 완료!")
print("   다음 단계: uvicorn app.housing_api:app --port 8000")
