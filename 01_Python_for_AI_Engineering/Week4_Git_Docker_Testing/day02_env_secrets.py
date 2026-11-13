"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 4 - NGÀY 2: Environment Variables & Secrets ║
║  Quản lý API Key an toàn với python-dotenv & Pydantic Setting║
╚══════════════════════════════════════════════════════════════╝
"""

import os
from pydantic import BaseModel, Field

# Cách 1: Đọc trực tiếp từ os.environ (truyền qua Docker hoặc .env)
api_key = os.getenv("OPENAI_API_KEY", "mock-default-key-for-dev")
print(f"Current API Key: {api_key[:4]}****")

# Cách 2: Quản lý config tập trung bằng class Settings
class AppSettings(BaseModel):
    app_env: str = Field(default="development")
    openai_api_key: str = Field(default="mock-key")
    gemini_api_key: str = Field(default="mock-gemini-key")
    max_retries: int = 3
    timeout_seconds: float = 30.0

settings = AppSettings()
print(f"Môi trường ứng dụng: {settings.app_env}")
print(f"Max retries: {settings.max_retries}")

