"""
╔══════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 1 - NGÀY 3: Functions & Decorators      ║
║  *args, **kwargs, Closures, Decorators                   ║
╚══════════════════════════════════════════════════════════╝

Mục tiêu hôm nay:
  ✅ Hiểu *args và **kwargs (dùng mọi nơi trong AI libraries)
  ✅ First-class functions & closures
  ✅ Decorators — cách LangChain, FastAPI hoạt động bên trong
  ✅ Viết decorator thực tế: retry, timing, caching

Thời gian: ~90 phút

Tại sao quan trọng với AI Engineer?
  - FastAPI dùng @app.get(), @app.post() — đó là decorators
  - LangChain dùng @tool, @chain
  - Retry decorator cực kỳ cần khi gọi LLM API (rate limits!)
  - Caching decorator tiết kiệm tiền API
"""

# ============================================================
# PHẦN 1: FUNCTION NÂNG CAO
# ============================================================
print("=" * 50)
print("PHẦN 1: FUNCTION NÂNG CAO")
print("=" * 50)

# --- Default arguments ---
def create_chat_message(content: str, role: str = "user", model: str = "gpt-4o") -> dict:
    return {"role": role, "content": content, "model": model}

msg1 = create_chat_message("Hello!")                        # dùng defaults
msg2 = create_chat_message("Hi", role="assistant")          # override 1 arg
msg3 = create_chat_message("Test", "system", "gemini")      # override all
print(msg1)
print(msg2)

# ⚠️ NGUY HIỂM: Mutable default argument — lỗi phổ biến!
# BAD (bug kinh điển của Python):
def add_message_bad(content: str, history: list = []):  # list tạo 1 lần duy nhất!
    history.append(content)
    return history

# GOOD:
def add_message_good(content: str, history: list | None = None) -> list:
    if history is None:
        history = []  # tạo list mới mỗi lần
    history.append(content)
    return history

# --- Keyword-only arguments (sau *) ---
def call_llm(prompt: str, *, temperature: float = 0.7, max_tokens: int = 1000):
    """Dấu * bắt buộc các arg sau phải dùng keyword khi gọi."""
    return f"Calling LLM: temp={temperature}, max={max_tokens}"

# call_llm("Hello", 0.5)       # ❌ Error!
result = call_llm("Hello", temperature=0.5)   # ✅ phải dùng keyword
print(result)

# ============================================================
# PHẦN 2: *ARGS và **KWARGS
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 2: *ARGS và **KWARGS")
print("=" * 50)

# *args — nhận bất kỳ số lượng positional arguments
def sum_all(*args: float) -> float:
    """args là 1 tuple bên trong function."""
    print(f"args type: {type(args)}, value: {args}")
    return sum(args)

print(sum_all(1, 2, 3))           # 6
print(sum_all(1, 2, 3, 4, 5))     # 15

# **kwargs — nhận bất kỳ số lượng keyword arguments
def configure_model(**kwargs) -> dict:
    """kwargs là 1 dict bên trong function."""
    print(f"kwargs: {kwargs}")
    defaults = {"temperature": 0.7, "max_tokens": 1000, "model": "gpt-4o"}
    return {**defaults, **kwargs}  # merge, kwargs ghi đè defaults

config = configure_model(temperature=0.3, model="gemini-1.5-flash", stream=True)
print(config)

# Kết hợp cả 3:
def flexible_function(required_arg: str, *args, **kwargs):
    print(f"Required: {required_arg}")
    print(f"Extra args: {args}")
    print(f"Extra kwargs: {kwargs}")

flexible_function("hello", "world", "python", key1="val1", key2="val2")

# --- Unpacking khi gọi hàm (rất phổ biến!) ---
def create_embedding(text: str, model: str, dimension: int) -> dict:
    return {"text": text, "model": model, "dimension": dimension}

# Thay vì:
params = {"text": "Hello world", "model": "text-embedding-3-small", "dimension": 1536}
# create_embedding(params["text"], params["model"], params["dimension"])  # dài dòng

# Pythonic — unpack dict thành kwargs:
embedding = create_embedding(**params)
print(embedding)

# Unpack list thành args:
def add(a, b, c):
    return a + b + c

numbers = [1, 2, 3]
result = add(*numbers)   # tương đương add(1, 2, 3)
print(result)

# ============================================================
# PHẦN 3: FIRST-CLASS FUNCTIONS & CLOSURES
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 3: FIRST-CLASS FUNCTIONS")
print("=" * 50)

# Trong Python, function là object — có thể truyền, return, gán vào biến

# 1. Gán function vào biến
def greet(name: str) -> str:
    return f"Hello, {name}!"

say_hello = greet          # không có () → không gọi, chỉ gán reference
print(say_hello("Alice"))  # gọi qua biến mới

# 2. Truyền function như argument (Higher-order functions)
def apply_to_all(func, items: list) -> list:
    return [func(item) for item in items]

names = ["alice", "bob", "charlie"]
upper_names = apply_to_all(str.upper, names)
print(upper_names)

# Với lambda:
prices = [10.5, 25.0, 7.3, 50.1]
discounted = apply_to_all(lambda p: p * 0.9, prices)
print([f"${p:.2f}" for p in discounted])

# 3. Closures — function nhớ environment khi được tạo
def make_llm_caller(model: str, temperature: float = 0.7):
    """Factory function — tạo ra function chuyên dụng cho từng model."""
    
    def call(prompt: str) -> str:
        # Closure nhớ model và temperature từ outer function
        return f"[{model}] (temp={temperature}): Responding to '{prompt}'"
    
    return call  # trả về function, không gọi nó

# Tạo các "specialized callers"
gpt4_caller = make_llm_caller("gpt-4o", temperature=0.3)
gemini_caller = make_llm_caller("gemini-1.5-flash", temperature=0.9)

print(gpt4_caller("What is AI?"))
print(gemini_caller("Tell me a joke"))

# ============================================================
# PHẦN 4: DECORATORS ⭐ (Trái tim của FastAPI, LangChain)
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 4: DECORATORS")
print("=" * 50)

"""
Decorator là function nhận 1 function, trả về 1 function mới.
Syntax @decorator là syntactic sugar cho: func = decorator(func)
"""

import time
import functools

# --- Decorator cơ bản ---
def simple_logger(func):
    """Decorator: log tên function khi được gọi."""
    @functools.wraps(func)   # giữ metadata của func gốc (name, docstring)
    def wrapper(*args, **kwargs):
        print(f"📞 Calling: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"✅ Done: {func.__name__}")
        return result
    return wrapper

@simple_logger
def process_text(text: str) -> str:
    return text.upper()

# Tương đương: process_text = simple_logger(process_text)
output = process_text("hello world")
print(output)

# --- Timing decorator (rất hữu ích khi optimize AI app) ---
def timer(func):
    """Đo thời gian thực thi của function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"⏱️  {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def simulate_llm_call(prompt: str) -> str:
    """Giả lập gọi LLM API (mất 0.1s)."""
    time.sleep(0.1)
    return f"Response to: {prompt}"

response = simulate_llm_call("What is machine learning?")
print(response)

# --- Decorator có tham số (Decorator Factory) ---
def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Decorator retry — cực kỳ cần thiết khi gọi LLM API!
    LLM APIs thường bị rate limit → cần retry tự động.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"⚠️  Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt < max_attempts:
                        time.sleep(delay)
            raise last_error  # re-raise sau khi hết attempts
        return wrapper
    return decorator

# Giả lập API hay bị lỗi
import random

@retry(max_attempts=3, delay=0.1)
def unreliable_api_call(prompt: str) -> str:
    """API này 60% thất bại."""
    if random.random() < 0.6:
        raise ConnectionError("API rate limit exceeded!")
    return f"Success: {prompt}"

# Thử gọi:
try:
    result = unreliable_api_call("Hello AI!")
    print(f"Result: {result}")
except ConnectionError as e:
    print(f"All retries failed: {e}")

# --- Stacking decorators ---
@timer
@retry(max_attempts=2, delay=0.05)
@simple_logger
def complex_operation(text: str) -> str:
    """Nhiều decorators — thứ tự áp dụng từ dưới lên."""
    time.sleep(0.05)
    return text.strip().lower()

# Thứ tự: simple_logger → retry → timer (wrap từ trong ra ngoài)

# ============================================================
# PHẦN 5: DECORATOR THỰC TẾ — CACHING (Tiết kiệm tiền API!)
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 5: CACHING DECORATOR")
print("=" * 50)

from functools import lru_cache

# lru_cache — Python built-in, cache kết quả của function
@lru_cache(maxsize=128)
def expensive_embedding(text: str) -> tuple:
    """Giả lập tạo embedding (tốn tiền API, cần cache!)."""
    print(f"  🔄 Computing embedding for: '{text[:30]}...'")
    time.sleep(0.1)  # simulate API call
    # Trả về tuple (không phải list) vì lru_cache cần hashable args
    return tuple([hash(text) % 100 / 100 for _ in range(5)])

print("First call (no cache):")
e1 = expensive_embedding("What is machine learning?")
print(f"Embedding: {e1}")

print("\nSecond call (cached — instant!):")
e2 = expensive_embedding("What is machine learning?")  # same input → cached
print(f"Embedding: {e2}")

print("\nDifferent input (no cache):")
e3 = expensive_embedding("How does Python work?")

print(f"\nCache info: {expensive_embedding.cache_info()}")

# ============================================================
# PHẦN 6: LAMBDA FUNCTIONS
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 6: LAMBDA")
print("=" * 50)

# Lambda: anonymous function ngắn gọn, 1 expression
# Syntax: lambda args: expression

double = lambda x: x * 2
add = lambda x, y: x + y
greet_fn = lambda name, greeting="Hello": f"{greeting}, {name}!"

print(double(5))
print(add(3, 4))
print(greet_fn("Alice"))
print(greet_fn("Bob", greeting="Hi"))

# Dùng nhiều nhất với sort, map, filter, max, min
messages = [
    {"role": "user", "content": "Hello", "tokens": 5},
    {"role": "assistant", "content": "Hi there! How can I help you?", "tokens": 30},
    {"role": "user", "content": "Tell me about Python", "tokens": 15},
]

# Sort theo số tokens
sorted_by_tokens = sorted(messages, key=lambda m: m["tokens"])
sorted_by_tokens_desc = sorted(messages, key=lambda m: m["tokens"], reverse=True)

# Tìm message nhiều token nhất
longest_msg = max(messages, key=lambda m: m["tokens"])
print(f"Longest: [{longest_msg['role']}] {longest_msg['content']}")

# ============================================================
# 🏋️ BÀI TẬP THỰC HÀNH
# ============================================================
print("\n" + "=" * 50)
print("BÀI TẬP")
print("=" * 50)

"""
Bài 1: Viết decorator @validate_prompt
       - Kiểm tra nếu prompt rỗng → raise ValueError("Prompt cannot be empty")  
       - Kiểm tra nếu prompt quá dài (> 1000 chars) → raise ValueError("Prompt too long")
       - Nếu OK → gọi function bình thường
       - In ra: "✅ Prompt validated: {len} chars"
"""
import functools

def validate_prompt(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # Bước 1: Lấy prompt
        prompt = args[0]

        # Bước 2: Kiểm tra prompt rỗng
        if not prompt:
            raise ValueError("Prompt cannot be empty")

        # Bước 3: Kiểm tra độ dài
        if len(prompt) > 1000:
            raise ValueError("Prompt too long")

        # Bước 4: In thông báo
        print(f"✅ Prompt validated: {len(prompt)} chars")

        # Bước 5: Gọi function gốc
        return func(*args, **kwargs)

    return wrapper

@validate_prompt
def send_to_llm(prompt: str) -> str:
    return f"LLM Response to: {prompt[:50]}"

# Test:
# print(send_to_llm("What is AI?"))          # ✅ OK
# print(send_to_llm(""))                      # ❌ ValueError
# print(send_to_llm("x" * 1001))             # ❌ ValueError

"""
Bài 2: Viết function make_prompt_template(template: str)
       - Nhận template string có placeholders như "{topic}" và "{language}"
       - Trả về 1 function mà khi gọi với keyword args sẽ fill vào template
       - Dùng closure
       
       Ví dụ:
       explain_template = make_prompt_template("Explain {topic} in {language}")
       prompt = explain_template(topic="Python", language="Vietnamese")
       # → "Explain Python in Vietnamese"
"""
def make_prompt_template(template: str):
    def prompt_builder(**kwargs):
        return template.format(**kwargs)
    return prompt_builder

"""
Bài 3: Viết decorator @rate_limiter(calls_per_minute: int)
       - Giới hạn số lần gọi function trong 1 phút
       - Nếu vượt quá → raise Exception("Rate limit exceeded. Try again later.")
       - Dùng 1 list để track timestamps của các lần gọi
       - Hint: dùng time.time() để lấy timestamp hiện tại
"""
def rate_limiter(calls_per_minute: int):
    def decorator(func):
        call_times = []  # track timestamps
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Bước 1: Lấy thời gian hiện tại
            now = time.time()

            # Bước 2: Chỉ giữ các lần gọi trong 60 giây gần nhất
            call_times[:] = [
                timestamp
                for timestamp in call_times
                if now - timestamp < 60
            ]

            # Bước 3: Kiểm tra giới hạn
            if len(call_times) >= calls_per_minute:
                raise Exception(
                    "Rate limit exceeded. Try again later."
                )

            # Bước 4: Ghi nhận lần gọi mới
            call_times.append(now)

            # Bước 5: Gọi function gốc
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limiter(calls_per_minute=3)
def api_call(prompt: str) -> str:
    return f"Response: {prompt}"

# Test:
# for i in range(5):
#     try:
#         print(api_call(f"Message {i}"))
#     except Exception as e:
#         print(f"❌ {e}")

"""
Bài 4 (Challenge): Viết decorator @log_llm_usage
       Sau mỗi lần gọi LLM, lưu vào list:
       {
           "function": tên function,
           "input_length": độ dài input,
           "output_length": độ dài output,
           "duration_ms": thời gian thực thi (ms),
           "timestamp": thời gian hiện tại (string)
       }
       Decorator cũng expose list đó qua attribute .usage_log
"""
import functools
import time
from datetime import datetime

usage_log = []

def log_llm_usage(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        # Bước 1: Lấy input prompt
        prompt = args[0] if args else kwargs.get("prompt", "")

        # Bước 2: Đo thời gian bắt đầu
        start_time = time.time()

        # Bước 3: Gọi function gốc
        result = func(*args, **kwargs)

        # Bước 4: Đo thời gian kết thúc
        end_time = time.time()

        # Bước 5: Tính thời gian thực thi (ms)
        duration_ms = (end_time - start_time) * 1000

        # Bước 6: Tạo log
        log_entry = {
            "function": func.__name__,
            "input_length": len(prompt),
            "output_length": len(result),
            "duration_ms": round(duration_ms, 2),
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }

        # Bước 7: Lưu log
        usage_log.append(log_entry)

        # Bước 8: Trả về kết quả
        return result

    # Bước 9: Expose usage_log
    wrapper.usage_log = usage_log

    return wrapper


@log_llm_usage
def mock_llm(prompt: str) -> str:
    time.sleep(0.05)
    return f"Response to: {prompt}"


# Test
result = mock_llm("Explain Python")

print(result)
print(mock_llm.usage_log)

# Test:
# mock_llm("Hello!")
# mock_llm("What is AI?")
# print(mock_llm.usage_log)

print("\n✅ Ngày 3 hoàn thành khi bạn làm xong 4 bài tập!")
print("💡 Tip: Decorators = Middleware trong Java Spring. Cùng concept, khác syntax!")

