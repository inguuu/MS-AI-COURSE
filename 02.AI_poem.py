import openai
from dotenv import load_dotenv
import os
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')
openai.azure_endpoint = os.getenv('AZURE_ENDPOINT')
openai.api_type = os.getenv('OPENAI_API_TYPE')
openai.api_version = os.getenv('OPENAI_API_VERSION')


while True:
    question = input("시의 주제를 입력하세요: (종료: q)")
    if question.lower() == 'q':
        break

    answer = input("시의 내용을 입력하세요: (종료: q)")
    if answer.lower() == 'q':
        break

        
    messages = [
            {"role": "system", "content": "You are a AI poem generator"},
            {"role": "user", "content": "시의 주제는 " + question},
            {"role": "user", "content": "시의 내용은 " + answer},
            {"role": "user", "content": "시의 형식은 자유롭게 작성해 주세요 " },
            {"role": "user", "content": "시의 길이는 4연 이상으로 작성해 주세요 "}
        ]

    response = openai.chat.completions.create(
                        model="dev-gpt-4.1-mini",  
                        messages=messages,
                        max_tokens= 1000,
                        temperature= 0.9,
                    )

    print(response.choices[0].message.content)