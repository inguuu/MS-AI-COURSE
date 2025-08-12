from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os
import openai
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.azure_endpoint = os.getenv('AZURE_ENDPOINT')
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_version = os.getenv('OPENAI_API_VERSION')



st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("메시지를 입력하세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    messages = [
        {"role": "system", "content": "You are an AI poem generator."},
    ]
    messages.extend(st.session_state.messages[1:])  # 초기 assistant 메시지는 제외

    response = openai.chat.completions.create(
        model="dev-gpt-4.1-mini",  # Azure 포털에서 배포할 때 만든 이름
        messages=messages,
        max_tokens=1000,
        temperature=0.7,
    )
    assistant_msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})
    st.chat_message("assistant").write(assistant_msg)
