"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 3 - NGÀY 4: Middleware, CORS & Error Handling║
║  Bảo mật & Chuẩn hóa Response Lỗi                            ║
╚══════════════════════════════════════════════════════════════╝
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI(title="Production Ready AI API")

# 1. CORS Configuration (Để Frontend React kết nối được)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production: thay bằng domain Frontend ví dụ http://localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Custom Logging Middleware (Đo thời gian mọi request)
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = (time.perf_counter() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    return response

# 3. Custom Exception Handler toàn cục
class LLMQuotaExceededException(Exception):
    def __init__(self, message: str):
        self.message = message

@app.exception_handler(LLMQuotaExceededException)
async def quota_exception_handler(request: Request, exc: LLMQuotaExceededException):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"error": "QUOTA_EXCEEDED", "message": exc.message}
    )

@app.get("/test-quota")
async def test_quota():
    raise LLMQuotaExceededException("Hết hạn mức token trong tháng!")

