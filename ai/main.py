# ai/main.py ← 이 코드로 완전히 교체 (Gemini → OpenAI)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from supabase import create_client
import os
import json
from dotenv import load_dotenv
from mangum import Mangum

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase = create_client(
    os.getenv("VITE_SUPABASE_URL"),
    os.getenv("VITE_SUPABASE_ANON_KEY")
)

# OpenAI 클라이언트
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Question(BaseModel):
    question: str

# 임베딩 생성 함수 (OpenAI text-embedding-3-small, 1536차원)
def get_embedding(text: str):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

# DB 초기화 (최초 1회만!)
@app.get("/init-db")
async def init_db():
    try:
        with open("../data/qa.json", "r", encoding="utf-8") as f:
            qa_list = json.load(f)

        # 기존 데이터 삭제
        supabase.table("embeddings").delete().neq("id", 0).execute()

        # 새로 삽입 (차원 1536으로 변경!)
        for item in qa_list:
            emb = get_embedding(item["question"])
            supabase.table("embeddings").insert({
                "question": item["question"],
                "answer": item["answer"],
                "embedding": emb  # 1536차원 벡터
            }).execute()

        return {"status": "초기화 완료!", "count": len(qa_list)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 질문 받기
@app.post("/ask")
async def ask(q: Question):
    try:
        emb = get_embedding(q.question)
        result = supabase.rpc("match_embeddings", {
            "query_embedding": emb,
            "match_threshold": 0.78,
            "match_count": 1
        }).execute()

        if result.data and len(result.data) > 0:
            return {"answer": result.data[0]["answer"]}
        else:
            return {"answer": "죄송합니다. 해당 질문에 대한 답변을 찾을 수 없습니다."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Perso.ai 챗봇 백엔드 정상 작동 중 (OpenAI 버전)"}