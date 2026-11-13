"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 3 - NGÀY 2: FastAPI Routing & Request Params ║
║  Cách tạo REST API hiện đại với FastAPI                      ║
╚══════════════════════════════════════════════════════════════╝

So sánh với Spring Boot trong Java:
- @RestController + @RequestMapping <-> FastAPI()
- @GetMapping("/path/{id}")         <-> @app.get("/path/{id}")
- Swagger UI tự động (/docs)        <-> Tích hợp sẵn 100% không cần cấu hình thêm
"""

from fastapi import FastAPI, Query, Path

app = FastAPI(
    title="AI Core API Service",
    description="Service xử lý tác vụ AI & LLM Inference",
    version="1.0.0"
)

# GET: Healthcheck endpoint
@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "service": "ai-backend", "version": "1.0.0"}

# GET với Path Parameter và Query Parameter
@app.get("/api/models/{model_id}", tags=["Models"])
async def get_model_info(
    model_id: str = Path(..., description="Tên mô hình AI, vd: gpt-4o, gemini-flash"),
    include_pricing: bool = Query(default=True, description="Kèm theo giá hay không")
):
    info = {
        "model_id": model_id,
        "is_available": True,
        "context_window": 128000
    }
    if include_pricing:
        info["price_per_1m"] = 0.15
    return info

# Hướng dẫn chạy:
# uv run uvicorn day02_fastapi_basics:app --reload

