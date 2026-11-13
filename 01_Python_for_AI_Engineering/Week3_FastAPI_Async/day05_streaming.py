"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 3 - NGÀY 5: Streaming Response (SSE)         ║
║  Server-Sent Events (SSE) để Stream Token về Frontend        ║
╚══════════════════════════════════════════════════════════════╝

Đây là cách ChatGPT stream từng từ về trình duyệt:
Dùng giao thức text/event-stream (SSE) kết hợp với Async Generator.
"""

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI(title="AI Streaming Service")

async def token_generator(prompt: str):
    full_answer = f"Đây là câu trả lời streaming chi tiết cho câu hỏi: '{prompt}'. Từng từ bay ra một cách mượt mà như ChatGPT!"
    words = full_answer.split()
    
    for word in words:
        await asyncio.sleep(0.08)  # giả lập thời gian model generate từng token
        # Format chuẩn SSE: data: <nội dung>\n\n
        yield f"data: {word} \n\n"
    
    yield "data: [DONE]\n\n"

@app.get("/api/chat/stream")
async def stream_chat(prompt: str = "Giới thiệu bản thân"):
    return StreamingResponse(
        token_generator(prompt),
        media_type="text/event-stream"
    )

