# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일에서 환경 변수 로드
load_dotenv()

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI 클라이언트 초기화
client = OpenAI(
    api_key=os.getenv("UPSTAGE_API_KEY"),
    base_url="https://api.upstage.ai/v1"
)

# 대화 기록을 저장할 딕셔너리
conversation_history = {}

class ChatRequest(BaseModel):
    message: str
    car_model: str

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat: ChatRequest):
    user_message = chat.message
    car_model = chat.car_model

    if not car_model:
        return {"response": "차종을 먼저 선택해주세요."}

    # 세션 ID나 사용자 ID를 기반으로 대화 기록을 가져옴 (여기서는 car_model을 키로 사용)
    if car_model not in conversation_history:
        conversation_history[car_model] = [
            {"role": "system", "content": f"당신은 {car_model}에 대한 전문 자동차 상담원입니다. 한국어로 답변해주세요. {car_model}에 대한 질문에 상세하고 정확하게 답변해주십시오."}
        ]
    
    # 현재 사용자 메시지를 대화 기록에 추가
    conversation_history[car_model].append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="solar-pro",
            messages=conversation_history[car_model]
        )
        assistant_response = response.choices[0].message.content
        
        # 어시스턴트의 응답을 대화 기록에 추가
        conversation_history[car_model].append({"role": "assistant", "content": assistant_response})
        
        return {"response": assistant_response}

    except Exception as e:
        return {"response": f"An error occurred: {str(e)}"}
