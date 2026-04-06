# notebooks/test2.py
import requests

API_BASE = "http://localhost:8000"
VALID_KEY = "test-key-001"

print("=" * 50)
print("  테스트 2: 멀티턴 대화")
print("=" * 50)

messages = []
turns = ["안녕하세요!", "오늘 뭐 하면 좋을까?", "맛있는 거 추천해줘"]

for user_msg in turns:
    messages.append({"role": "user", "content": user_msg})
    resp = requests.post(f"{API_BASE}/chat",
        json={"messages": messages, "max_new_tokens": 50},
        headers={"X-API-Key": VALID_KEY})
    result = resp.json()
    bot_msg = result["response"]
    messages.append({"role": "bot", "content": bot_msg})
    print(f"  사용자: {user_msg}")
    print(f"  봇:    {bot_msg[:60]}")
    print()

print(f"  총 대화 턴: {len(messages) // 2}")