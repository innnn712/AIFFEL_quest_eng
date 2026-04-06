# notebooks/test3.py
import requests

API_BASE = "http://localhost:8000"
VALID_KEY = "test-key-001"

print("=" * 50)
print("  테스트 3: 입력 검증")
print("=" * 50)

# 빈 메시지 목록
resp = requests.post(f"{API_BASE}/chat",
    json={"messages": []},
    headers={"X-API-Key": VALID_KEY})
print(f"  빈 메시지        → HTTP {resp.status_code}")

# temperature 범위 초과
resp = requests.post(f"{API_BASE}/chat",
    json={"messages": [{"role": "user", "content": "테스트"}], "temperature": 5.0},
    headers={"X-API-Key": VALID_KEY})
print(f"  temperature 초과 → HTTP {resp.status_code}")

# max_new_tokens 범위 초과
resp = requests.post(f"{API_BASE}/chat",
    json={"messages": [{"role": "user", "content": "테스트"}], "max_new_tokens": 1000},
    headers={"X-API-Key": VALID_KEY})
print(f"  max_tokens 초과  → HTTP {resp.status_code}")

# 정상 요청
resp = requests.post(f"{API_BASE}/chat",
    json={"messages": [{"role": "user", "content": "테스트"}]},
    headers={"X-API-Key": VALID_KEY})
print(f"  정상 요청        → HTTP {resp.status_code}")