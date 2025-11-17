## 사용 기술 스택
- Frontend: React + TypeScript + Vite
- Backend + AI: Supabase + FastAPI (Python)
- Vector DB: pgvector
- Embedding 모델: OpenAI text-embedding-3-small
- 배포: Vercel (프론트) + Railway (백엔드)

## 벡터 DB 및 임베딩 방식
- 모든 질문-답변 쌍을 OpenAI text-embedding-3-small로 벡터화
- Supabase pgvector에 저장 
- 사용자 질문도 동일 모델로 벡터화 → 코사인 유사도 검색

## 정확도 향상 전략
1. LLM은 답변 생성에 전혀 관여하지 않음 → 오직 임베딩 생성만 담당
2. Top-1 매칭된 원본 텍스트만 100% 그대로 반환
3. 유사도 임계값 0.72 적용 → 데이터셋 외 질문은 정중히 거부
4. 결과 → 할루시네이션 완전 차단 + 사실 기반 답변만 제공