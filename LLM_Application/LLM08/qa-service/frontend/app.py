# -*- coding: utf-8 -*-
# frontend/app.py

import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = "http://localhost:8000"

st.title("한국어 QA 서비스")

# 사이드바 - API Key 입력
with st.sidebar:
    api_key = st.text_input("API Key", value="test-key-001", type="password")
    headers = {"X-API-Key": api_key}

    # 서버 상태 확인
    if st.button("서버 상태 확인"):
        try:
            res = requests.get(f"{API_URL}/health")
            if res.status_code == 200:
                st.success("서버 정상")
            else:
                st.error("서버 오류")
        except:
            st.error("서버 연결 실패")

# 지문 입력
context = st.text_area(
    "지문",
    height=150,
    placeholder="답변을 찾을 지문을 입력하세요. (최소 10자, 최대 1000자)"
)

# 질문 입력
question = st.text_input(
    "질문",
    placeholder="질문을 입력하세요. (최소 5자, 최대 150자)"
)

# 답변 찾기 버튼
if st.button("답변 찾기"):
    if not context:
        st.warning("지문을 입력해주세요.")
    elif not question:
        st.warning("질문을 입력해주세요.")
    else:
        with st.spinner("답변 찾는 중..."):
            try:
                response = requests.post(
                    f"{API_URL}/predict",
                    json={"context": context, "question": question},
                    headers=headers,
                )

                if response.status_code == 200:
                    result = response.json()

                    # 결과 출력
                    st.write("**답변:**", result["answer"])
                    st.write("**신뢰도:**", f"{result['confidence'] * 100:.2f}%")

                    # 지문에서 답변 위치 하이라이트
                    st.write("**지문에서 답변 위치:**")
                    highlighted = (
                        context[:result["start"]]
                        + f"**:orange[{result['answer']}]**"
                        + context[result["end"]:]
                    )
                    st.markdown(highlighted)

                elif response.status_code == 401:
                    st.error("API Key가 올바르지 않습니다.")
                elif response.status_code == 422:
                    st.error("입력값을 확인해주세요. (지문 최소 10자, 질문 최소 5자)")
                else:
                    st.error(f"오류 발생: {response.status_code}")

            except requests.exceptions.ConnectionError:
                st.error("서버에 연결할 수 없습니다.")