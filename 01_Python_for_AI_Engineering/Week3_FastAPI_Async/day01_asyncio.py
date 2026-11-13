"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 3 - NGÀY 1: AsyncIO Fundamentals             ║
║  Event Loop, async/await, Task Gathering                     ║
╚══════════════════════════════════════════════════════════════╝

Tại sao AI Service BẮT BUỘC dùng AsyncIO?
- Gọi LLM API mất từ 1s đến 10s (I/O bound).
- Nếu dùng synchronous (code đồng bộ): Server chỉ phục vụ được 1 request/lần trên 1 worker.
- Nếu dùng async/await: Server có thể xử lý hàng nghìn request đồng thời mà không bị block.
"""

import asyncio
import time

print("=" * 50)
print("1. SO SÁNH SYNC vs ASYNC KHI GỌI NHIỀU API")
print("=" * 50)

# Giả lập gọi LLM mất 1 giây
async def async_call_llm(model_name: str, delay: float = 1.0) -> str:
    print(f"  👉 Bắt đầu gọi model [{model_name}]...")
    await asyncio.sleep(delay)  # Non-blocking sleep (không làm đứng luồng)
    print(f"  ✅ Nhận phản hồi từ [{model_name}]!")
    return f"Kết quả từ {model_name}"

async def main():
    start = time.perf_counter()
    
    # Chạy 3 model đồng thời (Parallel/Concurrent) bằng asyncio.gather
    print("🚀 Gọi 3 model cùng một lúc...")
    results = await asyncio.gather(
        async_call_llm("gpt-4o", 1.2),
        async_call_llm("gemini-1.5-flash", 0.8),
        async_call_llm("claude-3-5-sonnet", 1.0)
    )
    
    elapsed = time.perf_counter() - start
    print(f"\nKết quả nhận được: {results}")
    print(f"⏱️  Tổng thời gian: {elapsed:.2f}s (Thay vì 3.0s nếu chạy tuần tự!)")

if __name__ == "__main__":
    asyncio.run(main())

