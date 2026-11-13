"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 3 - NGÀY 3: Pydantic Request & Response Body ║
║  Định nghĩa DTO (Data Transfer Objects) chuẩn chỉnh          ║
╚══════════════════════════════════════════════════════════════╝
"""

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Chat Completion API")

# --- DTO / Schemas ---
class MessageDTO(BaseModel):
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)

class ChatCompletionRequest(BaseModel):
    model: str = Field(default="gpt-4o-mini")
    messages: List[MessageDTO] = Field(..., min_items=1)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=1000, gt=0)

class ChatCompletionResponse(BaseModel):
    id: str
    model: str
    reply: str
    total_tokens: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

# --- Endpoint POST ---
@app.post(
    "/v1/chat/completions",
    response_model=ChatCompletionResponse,
    status_code=status.HTTP_200_OK,
    tags=["Chat"]
)
async def create_chat_completion(request: ChatCompletionRequest):
    last_user_msg = request.messages[-1].content
    
    # Mock xử lý LLM
    mock_reply = f"AI phản hồi cho câu hỏi: '{last_user_msg}' bằng model {request.model}"
    
    return ChatCompletionResponse(
        id="chatcmpl-mock-12345",
        model=request.model,
        reply=mock_reply,
        total_tokens=len(last_user_msg.split()) + 25
    )

