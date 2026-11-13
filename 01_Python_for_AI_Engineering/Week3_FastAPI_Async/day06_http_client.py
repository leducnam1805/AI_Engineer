"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 3 - NGÀY 6: Async HTTP Client với HTTPX     ║
║  Gọi API Bên Ngoài (OpenAI, Gemini, External Services)      ║
╚══════════════════════════════════════════════════════════════╝

Tại sao dùng `httpx` thay vì `requests`?
- `requests` chỉ hỗ trợ đồng bộ (blocking IO).
- `httpx` hỗ trợ cả async/await, HTTP/2, connection pooling, timeout rõ ràng.
"""

import httpx
import asyncio

async def fetch_external_ai_service(url: str):
    # Dùng client session với timeout quản lý chặt chẽ
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            print(f"📡 Đang gửi request tới {url}...")
            response = await client.get(url)
            print(f"✅ Status Code: {response.status_code}")
            return response.json()
        except httpx.TimeoutException:
            print("❌ Request bị quá thời gian (Timeout)!")
        except httpx.HTTPError as e:
            print(f"❌ Lỗi HTTP: {e}")

async def main():
    # Gọi test API public
    data = await fetch_external_ai_service("https://httpbin.org/json")
    print(f"Dữ liệu nhận được: {data}")

if __name__ == "__main__":
    asyncio.run(main())

