"""
╔══════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 1 - NGÀY 2: Collections & Comprehensions ║
║  List, Dict, Set, Tuple — Trái tim của Python            ║
╚══════════════════════════════════════════════════════════╝

Mục tiêu hôm nay:
  ✅ Thành thạo List, Dict, Set, Tuple
  ✅ Viết List/Dict Comprehensions (Pythonic!)
  ✅ Hiểu khi nào dùng cái nào
  ✅ Áp dụng vào xử lý data AI (messages, embeddings, results)

Thời gian: ~90 phút

Tại sao quan trọng với AI Engineer?
  - LLM API trả về dict (JSON)
  - Danh sách messages là list[dict]
  - Embeddings là list[float]
  - Batch processing dùng comprehensions liên tục
"""

# ============================================================
# PHẦN 1: LIST — Ordered, Mutable, Allow Duplicates
# ============================================================
print("=" * 50)
print("PHẦN 1: LIST")
print("=" * 50)

# Tạo list
fruits = ["apple", "banana", "cherry", "apple"]  # duplicate OK
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]  # Python cho phép mix types

# --- Indexing & Slicing ---
print(fruits[0])      # "apple"      — first
print(fruits[-1])     # "apple"      — last
print(fruits[1:3])    # ["banana", "cherry"]  — slicing [start:end] (end excluded)
print(fruits[:2])     # ["apple", "banana"]   — từ đầu đến index 2
print(fruits[::2])    # ["apple", "cherry"]   — mỗi 2 phần tử (step=2)
print(fruits[::-1])   # reverse list!

# --- Thêm / Xóa ---
fruits.append("mango")         # thêm vào cuối
fruits.insert(1, "avocado")    # thêm vào vị trí index 1
fruits.extend(["kiwi", "lime"])# nối list khác vào cuối

fruits.remove("banana")         # xóa theo value (xóa lần đầu tiên gặp)
popped = fruits.pop()           # xóa và trả về phần tử cuối
popped_at = fruits.pop(0)       # xóa tại index 0

# --- Tìm kiếm ---
print("cherry" in fruits)       # True/False
print(fruits.index("cherry"))   # vị trí index
print(fruits.count("apple"))    # đếm số lần xuất hiện

# --- Sắp xếp ---
nums = [3, 1, 4, 1, 5, 9, 2, 6]
nums.sort()                      # sort in-place (thay đổi list gốc)
print(nums)

sorted_nums = sorted(nums)       # trả về list mới, giữ nguyên gốc
sorted_desc = sorted(nums, reverse=True)

# Sort theo tiêu chí tùy chỉnh
words = ["banana", "apple", "cherry", "kiwi"]
words.sort(key=len)              # sort theo độ dài
print(words)  # ['kiwi', 'apple', 'banana', 'cherry']

# ============================================================
# PHẦN 2: DICT — Key-Value, Ordered (Python 3.7+), Mutable
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 2: DICT")
print("=" * 50)

# Dict trong AI — cực kỳ phổ biến!
# Mọi API response đều là dict (JSON parsed)

# LLM message format
message = {
    "role": "user",
    "content": "What is machine learning?",
    "tokens": 6
}

# Truy cập
print(message["role"])              # "user" — lỗi nếu key không tồn tại
print(message.get("role"))          # "user" — an toàn hơn
print(message.get("model", "gpt-4o"))  # "gpt-4o" — default nếu không có key

# Thêm / Sửa / Xóa
message["timestamp"] = "2026-11-09"  # thêm key mới
message["tokens"] = 10               # cập nhật giá trị
del message["timestamp"]             # xóa key

# --- Duyệt Dict ---
for key in message:
    print(key)

for key, value in message.items():
    print(f"{key}: {value}")

# Chỉ keys hoặc values
print(list(message.keys()))
print(list(message.values()))

# --- Merge Dict (Python 3.9+) ---
defaults = {"temperature": 0.7, "max_tokens": 1000, "model": "gpt-4o"}
user_config = {"temperature": 0.3, "model": "gpt-4o-mini"}

# user_config ghi đè defaults
final_config = {**defaults, **user_config}
# Hoặc Python 3.9+: final_config = defaults | user_config
print(final_config)

# --- Nested Dict (rất phổ biến trong AI responses) ---
api_response = {
    "id": "chatcmpl-123",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Machine learning is..."
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 15,
        "completion_tokens": 50,
        "total_tokens": 65
    }
}

# Truy cập nested
content = api_response["choices"][0]["message"]["content"]
total_tokens = api_response["usage"]["total_tokens"]
print(f"Response: {content}")
print(f"Tokens used: {total_tokens}")

# ============================================================
# PHẦN 3: SET — Unique values, Unordered, Fast lookup
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 3: SET")
print("=" * 50)

# Dùng khi cần unique values
tags = {"python", "ai", "ml", "python", "ai"}  # duplicates bị loại
print(tags)  # {'ml', 'python', 'ai'} — thứ tự không xác định

tags.add("deep-learning")
tags.discard("ml")  # xóa, không lỗi nếu không tồn tại

# Set operations — rất hữu ích khi xử lý categories, labels
set_a = {"python", "java", "go"}
set_b = {"python", "rust", "go"}

print(set_a & set_b)   # intersection: {'python', 'go'}
print(set_a | set_b)   # union: {'python', 'java', 'go', 'rust'}
print(set_a - set_b)   # difference: {'java'}
print(set_a ^ set_b)   # symmetric diff: {'java', 'rust'}

# Dùng set để dedup list
documents = ["doc1", "doc2", "doc1", "doc3", "doc2"]
unique_docs = list(set(documents))
print(f"Unique: {unique_docs}")

# ============================================================
# PHẦN 4: TUPLE — Ordered, IMMUTABLE
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 4: TUPLE")
print("=" * 50)

# Dùng khi data không nên thay đổi
point = (10.5, 20.3)         # coordinates
rgb = (255, 128, 0)           # color
model_config = ("gpt-4o", 0.7, 1000)  # (model, temp, max_tokens)

# Unpacking — cực kỳ Pythonic!
x, y = point
r, g, b = rgb
model_name, temperature, max_tokens = model_config

print(f"Point: ({x}, {y})")
print(f"Model: {model_name}, temp={temperature}")

# Swap variables (không cần temp variable!)
a, b = 10, 20
a, b = b, a   # swap!
print(f"a={a}, b={b}")  # a=20, b=10

# Function trả về nhiều giá trị — thực ra là tuple
def get_model_info():
    return "gpt-4o", 0.7, 128000  # returns tuple

name, temp, ctx_window = get_model_info()

# ============================================================
# PHẦN 5: LIST COMPREHENSIONS ⭐ (Pythonic & cực kỳ quan trọng)
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 5: LIST COMPREHENSIONS")
print("=" * 50)

# Syntax: [expression for item in iterable if condition]

# Thay vì:
squares_loop = []
for n in range(1, 6):
    squares_loop.append(n ** 2)

# Viết Pythonic:
squares = [n ** 2 for n in range(1, 6)]
print(squares)  # [1, 4, 9, 16, 25]

# Với điều kiện (filter)
even_squares = [n ** 2 for n in range(1, 11) if n % 2 == 0]
print(even_squares)  # [4, 16, 36, 64, 100]

# --- Ứng dụng thực tế trong AI ---

# 1. Extract content từ list of messages
messages = [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"},
    {"role": "user", "content": "How are you?"},
]
user_messages = [m["content"] for m in messages if m["role"] == "user"]
print(f"User messages: {user_messages}")

# 2. Normalize embeddings (ví dụ)
raw_scores = [0.9, 0.3, 0.7, 0.1, 0.5]
threshold = 0.5
high_scores = [score for score in raw_scores if score >= threshold]
print(f"High scores: {high_scores}")

# 3. Batch processing prompts
topics = ["python", "machine learning", "neural networks"]
prompts = [f"Explain {topic} in simple terms" for topic in topics]
for p in prompts:
    print(f"  → {p}")

# 4. Flatten nested list
nested = [[1, 2, 3], [4, 5], [6, 7, 8, 9]]
flat = [item for sublist in nested for item in sublist]
print(f"Flat: {flat}")  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# ============================================================
# PHẦN 6: DICT COMPREHENSIONS
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 6: DICT COMPREHENSIONS")
print("=" * 50)

# {key: value for item in iterable if condition}

# Đảo ngược dict
original = {"a": 1, "b": 2, "c": 3}
reversed_dict = {v: k for k, v in original.items()}
print(reversed_dict)  # {1: 'a', 2: 'b', 3: 'c'}

# Ứng dụng: tạo lookup table từ list
model_costs = [
    ("gpt-4o", 5.0),
    ("gpt-4o-mini", 0.15),
    ("gemini-1.5-pro", 1.25),
    ("claude-3-5-sonnet", 3.0),
]
cost_lookup = {name: cost for name, cost in model_costs}
print(cost_lookup)
print(f"GPT-4o cost: ${cost_lookup['gpt-4o']}/1M tokens")

# Filter + transform
expensive_models = {name: cost for name, cost in cost_lookup.items() if cost > 2.0}
print(f"Expensive models: {expensive_models}")

# ============================================================
# PHẦN 7: ZIP, ENUMERATE, MAP, FILTER
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 7: BUILT-IN FUNCTIONS")
print("=" * 50)

# zip() — kết hợp 2 list thành pairs
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# zip tạo dict
score_dict = dict(zip(names, scores))
print(score_dict)

# enumerate() — loop với index (bạn đã biết từ Day 1)
for i, name in enumerate(names, start=1):  # start=1 đánh số từ 1
    print(f"{i}. {name}")

# map() — apply function lên từng element
temperatures_c = [0, 20, 37, 100]
temperatures_f = list(map(lambda c: c * 9/5 + 32, temperatures_c))
print(temperatures_f)
# Thường dùng comprehension thay vì map() cho rõ ràng hơn:
temperatures_f = [c * 9/5 + 32 for c in temperatures_c]

# filter() — lọc elements
scores_list = [45, 72, 88, 55, 93, 61, 79]
passing = list(filter(lambda s: s >= 60, scores_list))
print(passing)
# Pythonic hơn:
passing = [s for s in scores_list if s >= 60]

# ============================================================
# 🏋️ BÀI TẬP THỰC HÀNH
# ============================================================
"""
Bài 1: Cho list các LLM API responses, hãy:
       a. Extract tất cả "content" từ messages
       b. Tính tổng tokens đã dùng
       c. Lọc ra các response có finish_reason = "stop"
"""
responses = [
    {"content": "Machine learning is...", "tokens": 150, "finish_reason": "stop"},
    {"content": "Deep learning uses...", "tokens": 200, "finish_reason": "length"},
    {"content": "Neural networks...", "tokens": 180, "finish_reason": "stop"},
    {"content": "LLMs are...", "tokens": 120, "finish_reason": "stop"},
]

# a. Extract all content
all_contents = [m["content"] for m in responses]

# b. Tổng tokens
total_tokens = sum([m["tokens"] for m in responses])

# c. Filter finish_reason = "stop"
completed = [m for m in responses if m["finish_reason"] == "stop"]

"""
Bài 2: Cho dict chứa model và giá tiền,
       hãy tạo dict mới chỉ gồm các model có giá < 2.0
       và đổi đơn vị từ $/1M tokens sang đơn vị cent/1K tokens
"""
models = {
    "gpt-4o": 5.0,
    "gpt-4o-mini": 0.15,
    "gemini-1.5-flash": 0.075,
    "claude-3-haiku": 0.25,
}
# Kết quả mong muốn: {"gpt-4o-mini": 0.015, "gemini-1.5-flash": 0.0075, ...}
affordable_models = {
    key: value * 0.1
    for key, value in models.items()
    if value < 2.0
}

"""
Bài 3: Cho list câu, hãy:
       a. Tạo list các từ unique trong tất cả câu (dùng set)
       b. Đếm số từ của mỗi câu → trả về dict {câu: số_từ}
       c. Tìm câu dài nhất (nhiều từ nhất)
"""
sentences = [
    "Python is great for AI development",
    "Machine learning needs good data",
    "AI is transforming software development",
    "Python libraries make ML easier",
]

# a. Unique words
all_words = set()
for i in sentences:
    all_words.update(i.split())

# b. Word count per sentence
word_counts = {
    i: len(i.split())
    for i in sentences
}

# c. Longest sentence
longest = max(sentences, key=lambda i: len(i.split()))

"""
Bài 4 (Challenge): Viết function format_chat_history(messages)
       nhận list messages và trả về string đẹp như sau:
       
       [USER]: Hello, how are you?
       [ASSISTANT]: I'm doing well, thank you!
       [USER]: Tell me about Python
"""
def format_chat_history(messages: list[dict]) -> str:
    lines = []
    for message in messages:
        role= message["role"].upper()
        content= message["content"]
        lines.append(f"[{role}]: {content}")
        return "\n".join(lines) 

# Test:
chat = [
    {"role": "user", "content": "Hello, how are you?"},
    {"role": "assistant", "content": "I'm doing well, thank you!"},
    {"role": "user", "content": "Tell me about Python"},
]
# print(format_chat_history(chat))

print("\n✅ Đọc xong lý thuyết! Bây giờ làm 4 bài tập nhé.")
print("💡 Tip: Dùng comprehensions nhiều nhất có thể — đó là cách Pythonic!")

