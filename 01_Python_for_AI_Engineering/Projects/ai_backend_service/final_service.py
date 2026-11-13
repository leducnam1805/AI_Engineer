"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - DELIVERABLE DỰ ÁN CUỐI THÁNG 1                    ║
║  AI BACKEND SERVICE HOÀN CHỈNH (FastAPI + Pydantic + Docker) ║
╚══════════════════════════════════════════════════════════════╝

Cấu trúc:
- REST API đầy đủ
- Healthcheck endpoint
- Chat Completion endpoint
- Text Summarization endpoint
- SSE Token Streaming
- Error handling chuẩn HTTP Status
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import asyncio
from typing import List, Optional

app = FastAPI(
    title="Enterprise AI Backend Service",
    description="Deliverable Tháng 1 - Xây dựng hệ thống phục vụ suy luận AI chuẩn Production",
    version="1.0.0"
)

# --- MODELS ---
class ChatInput(BaseModel):
    prompt: str = Field(..., min_length=1, example="Hãy giải thích RAG là gì?")
    model: str = Field(default="gemini-1.5-flash")
    stream: bool = Field(default=False)

class SummarizeInput(BaseModel):
    document: str = Field(..., min_length=20, example="Đoạn văn bản dài cần tóm tắt...")
    max_length: int = Field(default=100)

class StandardResponse(BaseModel):
    status: str
    result: str
    tokens_used: int

# --- ROUTES ---
@app.get("/health", tags=["Monitoring"])
async def health():
    return {"status": "HEALTHY", "version": "1.0.0"}

@app.post("/api/chat", response_model=StandardResponse, tags=["AI Core"])
async def chat_endpoint(payload: ChatInput):
    if payload.stream:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Với streaming, vui lòng gọi GET /api/chat/stream"
        )
    # Giả lập xử lý model
    await asyncio.sleep(0.3)
    return StandardResponse(
        status="success",
        result=f"[{payload.model}]: Phản hồi hoàn chỉnh cho '{payload.prompt}'",
        tokens_used=len(payload.prompt.split()) + 30
    )

@app.post("/api/summarize", response_model=StandardResponse, tags=["AI Core"])
async def summarize_endpoint(payload: SummarizeInput):
    await asyncio.sleep(0.4)
    words = payload.document.split()
    summary = " ".join(words[:15]) + "..."
    return StandardResponse(
        status="success",
        result=f"Bản tóm tắt: {summary}",
        tokens_used=len(words)
    )

@app.get("/api/chat/stream", tags=["AI Core"])
async def chat_stream_endpoint(prompt: str):
    async def event_generator():
        mock_tokens = f"Dữ liệu streaming cho câu hỏi: '{prompt}' từ AI Backend Service.".split()
        for t in mock_tokens:
            await asyncio.sleep(0.08)
            yield f"data: {t} \n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

# Chạy app:
# uv run uvicorn final_service:app --reload --port 8000

