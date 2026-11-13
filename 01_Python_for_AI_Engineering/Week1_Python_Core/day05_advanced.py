"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 1 - NGÀY 5: Python Advanced Patterns         ║
║  Exceptions, Context Managers & Generators (Streaming)       ║
╚══════════════════════════════════════════════════════════════╝

Mục tiêu hôm nay:
  ✅ Custom Exceptions cho AI Service (LLMRateLimit, InvalidPrompt...)
  ✅ Context Managers (`with` statement) tự custom với contextlib
  ✅ Generators & `yield` — Bí mật đằng sau Token Streaming của LLM
  ✅ Viết Mock Streaming Response giống hệt OpenAI/Gemini API

Thời gian: ~60-75 phút
"""

# ============================================================
# PHẦN 1: ERROR HANDLING & CUSTOM EXCEPTIONS
# ============================================================
print("=" * 50)
print("PHẦN 1: ERROR HANDLING")
print("=" * 50)

# Trong Java: class LLMException extends Exception { ... }
# Trong Python: class LLMError(Exception): pass

class LLMBaseError(Exception):
    """Base exception cho toàn bộ hệ thống AI."""
    def __init__(self, message: str, model: str):
        super().__init__(message)
        self.model = model

class RateLimitError(LLMBaseError):
    """Bắn ra khi dính 429 Too Many Requests."""
    def __init__(self, model: str, retry_after: int = 5):
        super().__init__(f"Model {model} bị rate limit. Thử lại sau {retry_after}s.", model)
        self.retry_after = retry_after

class OutputParseError(LLMBaseError):
    """Bắn ra khi LLM trả về JSON không đúng format."""
    pass

# Try - Except - Else - Finally
def call_mock_llm(prompt: str, fail_type: str = None):
    try:
        if fail_type == "rate_limit":
            raise RateLimitError("gpt-4o", retry_after=10)
        elif fail_type == "parse":
            raise OutputParseError("Model không trả về JSON hợp lệ", "gpt-4o")
        
        response = f"Success response cho prompt: {prompt}"
        return response
    except RateLimitError as e:
        print(f"⚠️ [Handle RateLimit]: Chờ {e.retry_after} giây trước khi retry...")
        return None
    except OutputParseError as e:
        print(f"❌ [Handle ParseError]: {e}")
        return "{}"
    except Exception as e:
        print(f"🚨 [Unknown Error]: {e}")
        raise
    else:
        # Chạy khi try KHÔNG có exception
        print("🎉 Gọi LLM thành công mỹ mãn!")
    finally:
        # Luôn luôn chạy (dùng để đóng connection, log metrics)
        print("📝 Đã đóng session gọi API.")

print("--- Test Rate Limit ---")
call_mock_llm("Explain AI", fail_type="rate_limit")
print("\n--- Test Success ---")
call_mock_llm("Explain Python")


# ============================================================
# PHẦN 2: CONTEXT MANAGERS (`with` statement)
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 2: CONTEXT MANAGERS")
print("=" * 50)

# Java dùng: try (Resource r = new Resource()) { ... }
# Python dùng: with open(...) as f:

# Cách 1: Tạo bằng Class với __enter__ và __exit__
class TimerContext:
    import time
    def __init__(self, task_name: str):
        self.task_name = task_name

    def __enter__(self):
        import time
        self.start_time = time.time()
        print(f"⏳ Bắt đầu task: {self.task_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        elapsed = time.time() - self.start_time
        print(f"✅ Task [{self.task_name}] hoàn tất trong: {elapsed:.4f}s")
        # return True nếu muốn nuốt Exception, return False để raise tiếp
        return False

import time

with TimerContext("Embedding generation"):
    time.sleep(0.1)
    print("  Đang chạy model embedding...")

# Cách 2: Dùng @contextmanager (Cách Pythonic và hay dùng nhất)
from contextlib import contextmanager

@contextmanager
def temporary_api_key(temp_key: str):
    """Tạm thời set API key, sau đó restore lại key cũ."""
    global CURRENT_API_KEY
    old_key = CURRENT_API_KEY
    CURRENT_API_KEY = temp_key
    print(f"🔑 Switched key sang: {CURRENT_API_KEY}")
    try:
        yield CURRENT_API_KEY  # Trả giá trị ra ngoài block `with`
    finally:
        CURRENT_API_KEY = old_key
        print(f"🔙 Reverted key về: {CURRENT_API_KEY}")

CURRENT_API_KEY = "key-goc-production"

with temporary_api_key("key-tam-thoi-test") as active_key:
    print(f"  👉 Trong with block: {active_key}")

print(f"Sau with block: {CURRENT_API_KEY}")


# ============================================================
# PHẦN 3: GENERATORS & YIELD — BÍ MẬT STREAMING TOKEN ⭐
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 3: GENERATORS & STREAMING")
print("=" * 50)

"""
Khi ChatGPT/Gemini trả về câu trả lời dài:
Nếu chờ gen hết 1000 tokens mới return: User đợi 10s (màn hình đơ).
Dùng Streaming (Generator): Gen được từ nào, 'yield' từ đó ngay lập tức!
"""

# Hàm thường (return 1 lần hết cả list, tốn RAM)
def normal_read():
    return ["Token 1", "Token 2", "Token 3"]

# Generator Function (dùng từ khóa `yield`)
def stream_llm_response(full_text: str):
    words = full_text.split()
    for word in words:
        time.sleep(0.05)  # giả lập độ trễ gen token
        yield word + " "

# Khi gọi stream_llm_response, code CHƯA CHẠY NGAY mà trả về generator object
gen = stream_llm_response("Xin chào! Tôi là AI Engineer mentor của bạn.")
print(f"Generator object: {gen}")

# Lấy từng token ra bằng vòng lặp for:
print("Streaming output: ", end="", flush=True)
for token in gen:
    print(token, end="", flush=True)
print("\n")

# Hoặc lấy thủ công bằng next():
def simple_token_stream():
    yield "Hello"
    yield "World"
    yield "from AI"

stream = simple_token_stream()
print(next(stream))  # "Hello"
print(next(stream))  # "World"
print(next(stream))  # "from AI"
# next(stream) nữa sẽ raise StopIteration


# ============================================================
# PHẦN 4: GENERATOR EXPRESSION (Tiết kiệm bộ nhớ)
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 4: GENERATOR EXPRESSION")
print("=" * 50)

# List comprehension dùng ngoặc vuông [ ] -> Tạo toàn bộ list vào RAM ngay lập tức
list_data = [x ** 2 for x in range(1000000)]  # Tốn ~8MB RAM

# Generator expression dùng ngoặc tròn ( ) -> Tính toán on-the-fly (lười - lazy evaluation)
gen_data = (x ** 2 for x in range(1000000))   # Chỉ tốn ~100 bytes RAM

import sys
print(f"Kích thước List: {sys.getsizeof(list_data)} bytes")
print(f"Kích thước Gen:  {sys.getsizeof(gen_data)} bytes")


# ============================================================
# 🏋️ BÀI TẬP THỰC HÀNH (3 Bài tinh gọn, thực chiến)
# ============================================================
print("\n" + "=" * 50)
print("BÀI TẬP THỰC HÀNH")
print("=" * 50)

"""
Bài 1: Viết Generator `chunk_streamer(text: str, chunk_size: int = 4)`
       - Nhận vào một văn bản dài.
       - Chia văn bản thành các chunk có độ dài bằng `chunk_size` ký tự.
       - Dùng `yield` để bắn từng chunk ra ngoài.
       
       Ví dụ: chunk_streamer("abcdefghij", chunk_size=3)
       -> Yield lần 1: "abc"
       -> Yield lần 2: "def"
       -> Yield lần 3: "ghi"
       -> Yield lần 4: "j"
"""
def chunk_streamer(text: str, chunk_size: int = 4):
    pass  # TODO: Dùng vòng lặp và slicing + yield


"""
Bài 2: Viết Context Manager `@contextmanager def mock_llm_session(session_id: str)`
       - Trước khi vào with: in ra "🔵 [Session {session_id}] Bắt đầu phiên hội thoại."
       - Trả về đối tượng dict: `{"session_id": session_id, "messages": []}`
       - Trong with: cho phép người dùng append tin nhắn vào danh sách `messages`.
       - Sau khi thoát with (kể cả có lỗi hay không): in ra "🔴 [Session {session_id}] Đóng phiên. Tổng tin nhắn: {len}"
"""
@contextmanager
def mock_llm_session(session_id: str):
    pass  # TODO: Implement với try...finally


"""
Bài 3: Xây dựng Custom Exception `ContentFilterBlockError`
       và hàm `safe_generate(prompt: str)`:
       - Nếu prompt chứa các từ cấm: "hack", "bypass", "leak"
         -> raise ContentFilterBlockError(f"Prompt bị chặn do vi phạm chính sách: {prompt}")
       - Nếu hợp lệ: trả về f"Phản hồi an toàn cho: {prompt}"
       - Viết code gọi thử hàm và try-except bắt đúng ngoại lệ ContentFilterBlockError.
"""
# TODO: Implement class ContentFilterBlockError & safe_generate function


print("\n✅ Ngày 5 đã sẵn sàng! Chạy thử và làm 3 bài tập nhé.")

