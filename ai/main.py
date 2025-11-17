# ai/main.py ← 이 코드로 완전히 교체 (Railway 100% 호환 버전)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from supabase import create_client
import os
import json
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase 연결
supabase = create_client(
    os.getenv("VITE_SUPABASE_URL"),
    os.getenv("VITE_SUPABASE_ANON_KEY")
)

# OpenAI 연결
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Question(BaseModel):
    question: str

# 임베딩 생성
def get_embedding(text: str):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# DB 초기화
@app.get("/init-db")
async def init_db():
    try:
        with open("../data/qa.json", "r", encoding="utf-8") as f:
            qa_list = json.load(f)

        supabase.table("embeddings").delete().neq("id", 0).execute()

        for item in qa_list:
            emb = get_embedding(item["question"])
            supabase.table("embeddings").insert({
                "question": item["question"],
                "answer": item["answer"],
                "embedding": emb
            }).execute()

        return {"status": "초기화 완료!", "count": len(qa_list)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 질문 처리
@app.post("/ask")
async def ask(q: Question):
    try:
        emb = get_embedding(q.question)
        result = supabase.rpc("match_embeddings", {
            "query_embedding": emb,
            "match_threshold": 0.72,   # ← 더 자연스럽게 매칭되도록 0.72 추천
            "match_count": 1
        }).execute()

        if result.data and len(result.data) > 0:
            return {"answer": result.data[0]["answer"]}
        else:
            return {"answer": "죄송합니다. 해당 질문에 대한 답변을 찾을 수 없습니다."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 루트 엔드포인트
@app.get("/")
async def root():
    return {"message": "Perso.ai 챗봇 백엔드 정상 작동 중 (OpenAI + Railway)"}