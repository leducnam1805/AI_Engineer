"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 1 - NGÀY 7: Mini-Project Tổng Kết Tuần 1    ║
║  Dự Án: AI Prompt Engineering & API Inspection CLI Tool      ║
╚══════════════════════════════════════════════════════════════╝

Mục tiêu dự án:
  Áp dụng toàn bộ kiến thức Tuần 1:
  - OOP & Dataclass (Message, PromptRequest, LLMResponse)
  - Decorator (@timer, @retry, @validate_prompt)
  - Context Manager (đo tài nguyên/thời gian)
  - Generator (stream mock output)
  - Custom Exceptions (InvalidPromptError, APIConnectionError)
  - Xử lý Dict/List Comprehension

Mô tả bài toán:
  Xây dựng một CLI Tool mô phỏng LLM API Client có tính năng:
  1. Validate prompt người dùng nhập vào.
  2. Retry nếu gặp sự cố mạng (simulate random fail).
  3. Đo thời gian phản hồi bằng decorator.
  4. Trả về token streaming ra màn hình terminal.
  5. Thống kê chi phí & tokens dùng dataclass.
"""

import time
import random
import functools
from dataclasses import dataclass, field
from datetime import datetime
from typing import Generator, List, Dict, Optional


# ============================================================
# 1. CUSTOM EXCEPTIONS
# ============================================================
class CLIError(Exception):
    pass

class EmptyPromptError(CLIError):
    pass

class MockAPIConnectionError(CLIError):
    pass


# ============================================================
# 2. DATA MODELS (DATACLASS)
# ============================================================
@dataclass
class UsageStats:
    prompt_tokens: int
    completion_tokens: int
    model: str
    cost_per_1m_tokens: float = 0.15  # gpt-4o-mini price

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    @property
    def cost_usd(self) -> float:
        return (self.total_tokens / 1_000_000) * self.cost_per_1m_tokens


@dataclass
class ChatTurn:
    role: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))


# ============================================================
# 3. DECORATORS
# ============================================================
def timer_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"\n⏱️  [Latency]: {elapsed * 1000:.2f}ms")
        return result
    return wrapper


def retry_on_failure(max_retries: int = 3, delay: float = 0.5):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_err = None
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except MockAPIConnectionError as e:
                    last_err = e
                    print(f"⚠️  Thử lại lần {attempt}/{max_retries} do: {e}")
                    time.sleep(delay)
            raise last_err
        return wrapper
    return decorator


# ============================================================
# 4. MOCK LLM SERVICE ENGINE
# ============================================================
class MockLLMService:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.history: List[ChatTurn] = []

    def validate_prompt(self, prompt: str) -> None:
        if not prompt or not prompt.strip():
            raise EmptyPromptError("Prompt không được để trống!")

    @retry_on_failure(max_retries=3, delay=0.2)
    def call_api(self, prompt: str) -> str:
        # Giả lập 20% khả năng timeout/ngắt mạng
        if random.random() < 0.2:
            raise MockAPIConnectionError("Socket timeout kết nối API!")
        
        # Giả lập câu trả lời từ AI
        responses = [
            f"Về câu hỏi '{prompt}', Python là một ngôn ngữ tuyệt vời cho AI Engineer.",
            f"Để giải quyết vấn đề '{prompt}', bạn nên kết hợp Vector Database và RAG.",
            f"Phân tích '{prompt}': Hãy bắt đầu với việc chuẩn bị dữ liệu và mô hình nhỏ.",
        ]
        return random.choice(responses)

    def stream_tokens(self, response_text: str) -> Generator[str, None, None]:
        tokens = response_text.split()
        for token in tokens:
            time.sleep(0.04)  # mô phỏng streaming từng token
            yield token + " "

    @timer_decorator
    def chat(self, user_prompt: str) -> UsageStats:
        self.validate_prompt(user_prompt)
        
        # Lưu lịch sử chat
        self.history.append(ChatTurn(role="user", content=user_prompt))
        
        # Gọi API sinh text
        full_text = self.call_api(user_prompt)
        
        # Stream ra màn hình
        print(f"🤖 [{self.model}]: ", end="", flush=True)
        for token in self.stream_tokens(full_text):
            print(token, end="", flush=True)
        print()

        self.history.append(ChatTurn(role="assistant", content=full_text))

        # Ước lượng tokens
        p_tokens = len(user_prompt.split()) * 2
        c_tokens = len(full_text.split()) * 2
        return UsageStats(p_tokens, c_tokens, self.model)


# ============================================================
# 5. MAIN CLI INTERACTION LOOP
# ============================================================
def main():
    print("=" * 60)
    print("🚀 CHÀO MỪNG ĐẾN VỚI AI ASSISTANT CLI - WEEK 1 MINI PROJECT")
    print("Gõ 'exit' hoặc 'quit' để thoát.")
    print("=" * 60)

    service = MockLLMService(model="gemini-1.5-flash")
    total_cost = 0.0

    # Test tự động 1 câu trước:
    sample_prompt = "Lộ trình học AI Engineer trong 6 tháng"
    print(f"\n[Test Case Tự Động]: Hỏi '{sample_prompt}'")
    stats = service.chat(sample_prompt)
    print(f"📊 Tokens: {stats.total_tokens} | Chi phí: ${stats.cost_usd:.6f}")
    total_cost += stats.cost_usd

    print("\n✅ Project Day 7 mẫu đã chạy xong! Bạn có thể chỉnh sửa và mở rộng thêm.")


if __name__ == "__main__":
    main()

