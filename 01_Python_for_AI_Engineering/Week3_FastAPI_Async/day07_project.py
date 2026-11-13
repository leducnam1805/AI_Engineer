"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 3 - NGÀY 7: Mini-Project FastAPI AI Server   ║
║  Dự Án: Full FastAPI Proxy Service tích hợp Mock/Real LLM    ║
╚══════════════════════════════════════════════════════════════╝
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
import asyncio
import time

app = FastAPI(title="Mini AI Gateway Service", version="1.0.0")

class PromptInput(BaseModel):
    prompt: str = Field(..., min_length=2)
    stream: bool = False

@app.post("/api/generate")
async def generate_text(payload: PromptInput):
    if not payload.stream:
        # Giả lập xử lý thường
        await asyncio.sleep(0.5)
        return {
            "prompt": payload.prompt,
            "response": f"Đây là câu trả lời được xử lý bởi AI Backend cho: {payload.prompt}",
            "status": "success"
        }
    
    # Xử lý streaming nếu stream=True
    async def sse_event_stream():
        tokens = f"Câu trả lời streaming cho: {payload.prompt}".split()
        for t in tokens:
            await asyncio.sleep(0.06)
            yield f"data: {t} \n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(sse_event_stream(), media_type="text/event-stream")

# Hướng dẫn chạy và test Swagger UI:
# uv run uvicorn day07_project:app --reload
# Truy cập: http://127.0.0.1:8000/docs

