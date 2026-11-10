"""
╔══════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 1 - NGÀY 1: Python Core Basics           ║
║  Dành cho: Java/React dev đang học Python                ║
╚══════════════════════════════════════════════════════════╝

Mục tiêu hôm nay:
  ✅ Hiểu sự khác biệt Python vs Java
  ✅ Nắm vững kiểu dữ liệu và cú pháp cơ bản
  ✅ Viết code Python "Pythonic" (không phải code Java bằng Python)

Thời gian: ~90 phút
"""

# ============================================================
# PHẦN 1: KHÁC BIỆT CỐT LÕI PYTHON vs JAVA
# ============================================================

# Java:  String name = "Nguyen Van A";
# Python: (không cần khai báo kiểu)
name = "Nguyen Van A"
age = 25
height = 1.75
is_engineer = True

print(type(name))       # <class 'str'>
print(type(age))        # <class 'int'>
print(type(height))     # <class 'float'>
print(type(is_engineer))# <class 'bool'>

# ============================================================
# PHẦN 2: F-STRINGS (cực kỳ dùng nhiều trong AI apps)
# ============================================================

# Java: String.format("Hello, %s! You are %d years old.", name, age)
# Python:
greeting = f"Hello, {name}! You are {age} years old."
print(greeting)

# F-string với expression
print(f"Height in cm: {height * 100:.1f}cm")  # format 1 chữ số thập phân
print(f"Name length: {len(name)}")
print(f"Upper: {name.upper()}")

# Multi-line f-string (hay dùng để build prompts cho LLM!)
prompt = f"""
You are an AI assistant.
User name: {name}
User age: {age}
Please greet the user professionally.
"""
print(prompt)

# ============================================================
# PHẦN 3: CONDITIONAL (không có dấu {}, dùng indent)
# ============================================================

# Java:
# if (age >= 18) { ... } else { ... }

# Python:
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")

# Ternary - Python style
status = "adult" if age >= 18 else "minor"
print(f"Status: {status}")

# ============================================================
# PHẦN 4: LOOPS
# ============================================================

# --- For loop ---
# Java: for (int i = 0; i < 5; i++) { ... }
# Python:
for i in range(5):
    print(f"Index: {i}")

# Duyệt list trực tiếp (Pythonic!)
languages = ["Python", "Java", "JavaScript", "Go"]
for lang in languages:
    print(f"- {lang}")

# enumerate() khi cần cả index lẫn value
for index, lang in enumerate(languages):
    print(f"{index + 1}. {lang}")

# --- While loop ---
count = 0
while count < 3:
    print(f"Count: {count}")
    count += 1  # Python không có count++

# ============================================================
# PHẦN 5: STRINGS - QUAN TRỌNG VỚI AI (xử lý text nhiều)
# ============================================================

text = "  Hello, World! This is Python.  "

print(text.strip())          # Bỏ whitespace hai đầu
print(text.lower())          # chuyển thường
print(text.upper())          # chuyển hoa
print(text.replace("Python", "AI"))
print(text.split(" "))       # tách thành list
print("Python" in text)      # kiểm tra substring → True/False

# Join list thành string
words = ["AI", "Engineer", "Roadmap"]
sentence = " ".join(words)
print(sentence)  # "AI Engineer Roadmap"

# Multi-line string (dùng nhiều khi viết prompts!)
system_prompt = """
You are a helpful AI assistant specialized in coding.
Always provide clear, concise answers with code examples.
Use Vietnamese when the user writes in Vietnamese.
"""
print(system_prompt.strip())

# ============================================================
# PHẦN 6: NONE (tương tự null trong Java)
# ============================================================

result = None
print(result is None)      # True (dùng "is None" thay vì "== None")
print(result is not None)  # False

# Optional value pattern (rất phổ biến trong AI code)
def get_user(user_id: int):
    if user_id == 1:
        return "Nguyen Van A"
    return None  # Không tìm thấy

user = get_user(1)
if user is not None:
    print(f"Found: {user}")
else:
    print("User not found")

# ============================================================
# PHẦN 7: TYPE HINTS (quan trọng trong production AI code!)
# ============================================================
# Python hiện đại dùng type hints như Java nhưng optional

def calculate_bmi(weight: float, height: float) -> float:
    """Tính chỉ số BMI.
    
    Args:
        weight: Cân nặng (kg)
        height: Chiều cao (m)
    
    Returns:
        Chỉ số BMI
    """
    return weight / (height ** 2)

bmi = calculate_bmi(70, 1.75)
print(f"BMI: {bmi:.2f}")

# ============================================================
# 🏋️ BÀI TẬP THỰC HÀNH
# ============================================================
"""
TODO: Làm các bài tập sau (xóa "pass" và viết code)

Bài 1: Viết function nhận tên và tuổi, trả về greeting string
       dùng f-string. Ví dụ: "Xin chào Minh! Bạn 28 tuổi."
"""
def create_greeting(name: str, age: int) -> str:
    return f"Xin chào {name}! Bạn {age} tuổi."

"""
Bài 2: Viết function nhận list các số, trả về tổng và trung bình.
       Dùng built-in sum() và len()
"""
# numbers = [10, 20, 30, 40, 50]
def calculate_stats(numbers: list) -> dict:
    total = sum(numbers)
    count = len(numbers)
    average = total / count if count > 0 else 0
    return {"sum": total, "average": average, "count": count}

"""
Bài 3: Viết function kiểm tra xem 1 string có phải là 
       "positive prompt" không (chứa các từ: "help", "explain", "show")
"""
def is_positive_prompt(text: str) -> bool:
    text = text.lower()
    if "help" in text or "explain" in text or "show" in text:
        return True
    else:
        return False

"""
Bài 4 (Challenge): Viết function nhận 1 đoạn text dài,
       trả về dict thống kê: số từ, số câu, số ký tự
"""
def analyze_text(text: str) -> dict:
    so_tu = text.split()
    so_cau = text.count(".") + text.count("?") + text.count("!")
    so_ky_tu = len(text)

    return {"so tu": so_tu, "so cau": so_cau, "so ky tu": so_ky_tu}

# Test your functions:
# print(create_greeting("Minh", 28))
# print(calculate_stats([1, 2, 3, 4, 5]))
# print(is_positive_prompt("Can you help me?"))
# print(analyze_text("Hello world. How are you? I am fine."))

print("\n✅ Ngày 1 hoàn thành! Hãy làm các bài tập trên trước khi sang Ngày 2.")

