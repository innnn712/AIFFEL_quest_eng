# notebooks/test4.py
import requests, time
from concurrent.futures import ThreadPoolExecutor, as_completed

API_BASE = "http://localhost:8000"
VALID_KEY = "test-key-001"

def send_chat(i):
    start = time.time()
    resp = requests.post(
        f"{API_BASE}/chat",
        json={
            "messages": [{"role": "user", "content": f"질문 {i}번입니다"}],
            "max_new_tokens": 10,
        },
        headers={"X-API-Key": VALID_KEY},
        timeout=60,
    )
    return {
        "id": i + 1,
        "elapsed": round(time.time() - start, 1),
        "status": resp.status_code,
    }

print("=" * 50)
print("  테스트 4: 동시 요청 (4개)")
print("=" * 50)
start = time.time()
with ThreadPoolExecutor(max_workers=4) as ex:
    futures = [ex.submit(send_chat, i) for i in range(4)]
    results = [f.result() for f in as_completed(futures)]
total = round(time.time() - start, 1)

for r in sorted(results, key=lambda x: x["id"]):
    print(f"  요청 #{r['id']}: {r['elapsed']}초 (HTTP {r['status']})")
print(f"  전체: {total}초")