# Day 5 — [프로젝트 1] 정형 데이터 예측 서비스

AIFFEL AI 엔지니어 1기 | 모델 배포 기초 Day 5

## 프로젝트 개요

California Housing 데이터셋을 활용한 주택 가격 예측 서비스입니다.  
Day 1~4에서 배운 기술을 통합하여 End-to-End 서비스를 구축합니다.

```
Streamlit (입력 폼) → FastAPI (추론 API) → PyTorch 모델 (가격 예측)
```

## 폴더 구조

```
model-serving-course/
├── app/
│   ├── model_utils.py          ← Day 1~4에서 만든 것 (MNIST용, 건드리지 않음)
│   ├── schemas.py              ← Day 2에서 만든 것 (MNIST용, 건드리지 않음)
│   ├── housing_model.py        ← NEW: HousingModel + HousingPredictor
│   ├── housing_schemas.py      ← NEW: HousingRequest, HousingResponse
│   └── housing_api.py          ← NEW: FastAPI 서버
├── frontend/
│   ├── app_dashboard.py        ← Day 4에서 만든 것 (MNIST용, 건드리지 않음)
│   └── app_housing.py          ← NEW: Streamlit 대시보드
├── models/
│   ├── housing_preprocessing.json  ← 정규화 파라미터 (mean, std)
│   └── housing_model.pth           ← 학습 후 생성 (gitignore)
├── notebooks/
│   └── day5_project1_train.py  ← 모델 학습 스크립트
├── requirements.txt
└── README.md
```

## 실행 방법

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 모델 학습 (최초 1회)

```bash
python notebooks/day5_project1_train.py
```

### 3. FastAPI 서버 실행 (터미널 1)

```bash
uvicorn app.housing_api:app --reload --port 8000
```

### 4. Streamlit 실행 (터미널 2)

```bash
streamlit run frontend/app_housing.py --server.port 8501
```

### 5. 접속

| 서비스 | URL |
|--------|-----|
| Streamlit 프론트 | http://localhost:8501 |
| Swagger UI | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

## 모델 성능

| 지표 | 값 |
|------|----|
| 아키텍처 | MLP (8 → 64 → 32 → 1) |
| 파라미터 수 | 2,689개 |
| Test MSE | 0.3166 |
| Test MAE | $38,862 (실제 금액) |

## Day별 사용 기술

| 섹션 | Day 1 | Day 2 | Day 3 | Day 4 |
|------|-------|-------|-------|-------|
| 모델 학습 | 직렬화 | - | - | - |
| FastAPI | - | Pydantic, Swagger | run_in_executor | - |
| Streamlit | - | - | - | API 호출, 에러 처리 |
