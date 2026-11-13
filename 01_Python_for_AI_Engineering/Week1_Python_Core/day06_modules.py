"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 1 - NGÀY 6: Modules, Packages & UV Setup     ║
║  Cách tổ chức Codebase chuẩn Production cho AI Projects      ║
╚══════════════════════════════════════════════════════════════╝

Mục tiêu hôm nay:
  ✅ Phân biệt Module vs Package vs Script
  ✅ Cơ chế import của Python (sys.path, absolute vs relative import)
  ✅ File bí mật `__init__.py` và `if __name__ == "__main__":`
  ✅ Quản lý dependency thời đại mới với `uv` & `pyproject.toml`

Thời gian: ~60 phút
"""

# ============================================================
# PHẦN 1: MODULE vs PACKAGE
# ============================================================
print("=" * 50)
print("PHẦN 1: MODULE vs PACKAGE TRONG PYTHON")
print("=" * 50)

"""
Ánh xạ cho Java Dev:
- 1 file `.py`               = 1 Module  (tương tự 1 class hoặc 1 source file)
- 1 thư mục chứa các file .py = 1 Package (tương tự package trong Java)
- File `__init__.py`         = Đánh dấu thư mục đó là Python package 
                               (và chứa logic init khi package được import)

Cấu trúc dự án AI chuẩn:
my_ai_app/
├── pyproject.toml         # Giống pom.xml
├── .env                   # Chứa API_KEY (KHÔNG commit lên Git)
└── src/
    └── ai_service/        # Package chính
        ├── __init__.py    # Expose các class/function public
        ├── core/          # Sub-package
        │   ├── __init__.py
        │   └── llm.py     # Module
        └── utils/
            ├── __init__.py
            └── logger.py
"""

# ============================================================
# PHẦN 2: CÁC CÁCH IMPORT
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 2: CÁCH IMPORT")
print("=" * 50)

# 1. Import cả module
import math
print(f"PI: {math.pi}")

# 2. Import cụ thể class/hàm/biến
from datetime import datetime
print(f"Hôm nay: {datetime.now().strftime('%Y-%m-%d')}")

# 3. Import với Alias (rất hay gặp trong AI: np, pd, plt)
import os as operating_system
print(f"Current Dir: {operating_system.getcwd()}")

# 4. Kiểm tra sys.path - Nơi Python tìm kiếm modules
import sys
print(f"Python đang tìm module ở các thư mục đầu tiên:")
for path in sys.path[:3]:
    print(f"  📂 {path}")


# ============================================================
# PHẦN 3: `if __name__ == "__main__":` LÀ GÌ?
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 3: TẠI SAO PHẢI CÓ if __name__ == '__main__':")
print("=" * 50)

"""
Trong Java: Cần hàm public static void main(String[] args) để chạy.
Trong Python: Chạy từ trên xuống dưới. 

Khi bạn chạy trực tiếp file: `__name__` sẽ có giá trị là `"__main__"`.
Khi file này được file KHÁC import: `__name__` sẽ là TÊN CỦA FILE (module name).

Tác dụng:
- Giúp bạn vừa có thể import hàm từ file này sang file khác (không bị chạy code test).
- Vừa có thể chạy độc lập file này để debug.
"""

def helper_function():
    return "Tôi là hàm tiện ích hỗ trợ AI!"

if __name__ == "__main__":
    print("🚀 File này đang được CHẠY TRỰC TIẾP!")
    print(f"Test hàm: {helper_function()}")
else:
    print(f"📦 File này đang được IMPORT bởi một module khác! __name__ = {__name__}")


# ============================================================
# PHẦN 4: HIỆN ĐẠI HÓA VỚI `uv` (Thay thế pip, venv cổ điển)
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 4: PACKAGE MANAGEMENT VỚI UV")
print("=" * 50)

"""
Tại sao là UV thay vì PIP?
- Pip truyền thống: Cài thư viện chậm, giải quyết conflict phụ thuộc rất khổ.
- UV (bởi Astral - viết bằng Rust):
  + Cực nhanh (gấp 10-100 lần pip).
  + Tự quản lý virtualenv (.venv).
  + Tạo file lock (uv.lock) chuẩn deterministic như package-lock.json / pom.xml.

CÁC LỆNH UV CẦN NHỚ:
1. uv init my-project          # Khởi tạo project mới với pyproject.toml
2. uv add fastapi httpx openai # Cài package và tự lưu vào pyproject.toml
3. uv add --dev pytest ruff    # Cài package chỉ dùng cho môi trường dev
4. uv run python main.py       # Chạy script trong virtualenv của project
5. uv sync                     # Đồng bộ toàn bộ package từ file lock (cho máy mới)
"""


# ============================================================
# 🏋️ BÀI TẬP THỰC HÀNH DAY 6 (Xây dựng Mini Package)
# ============================================================
print("\n" + "=" * 50)
print("BÀI TẬP THỰC HÀNH DAY 6")
print("=" * 50)

"""
Mục tiêu: Tự tạo một cấu trúc package chuẩn trong thư mục Day 6 và import nó.

Cấu trúc bạn sẽ tạo bằng tay hoặc bằng code:
Week1_Python_Core/
└── ai_toolkit/               <-- Tạo folder này
    ├── __init__.py           <-- File rỗng hoặc expose module
    ├── prompt_cleaner.py     <-- Chứa hàm clean_prompt(text: str) -> str
    └── token_counter.py      <-- Chứa hàm count_mock_tokens(text: str) -> int

Yêu cầu:
Bài 1: Viết module `prompt_cleaner.py` với hàm `clean_prompt(text: str) -> str`:
       - Loại bỏ khoảng trắng thừa ở 2 đầu.
       - Thay thế nhiều dấu cách liên tiếp thành 1 dấu cách duy nhất.

Bài 2: Viết module `token_counter.py` với hàm `count_mock_tokens(text: str) -> int`:
       - Quy ước đơn giản: 1 từ = 1.3 token (làm tròn lên `math.ceil`).

Bài 3: Trong file `day06_modules.py` này, viết code import 2 hàm trên từ package `ai_toolkit`
       và gọi thử với chuỗi:
       sample = "   AI   Engineer     Roadmap   2026   "
       In ra prompt sau khi clean và số token ước lượng!
"""

# TODO: Viết code test Bài 3 ở đây sau khi đã tạo package ai_toolkit:
# from ai_toolkit.prompt_cleaner import clean_prompt
# from ai_toolkit.token_counter import count_mock_tokens


print("\n✅ Ngày 6 đã hoàn thành phần lý thuyết! Hãy tạo thư mục ai_toolkit và hoàn thành bài tập nhé.")

