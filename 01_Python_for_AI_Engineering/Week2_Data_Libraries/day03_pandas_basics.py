"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 2 - NGÀY 3: Pandas Basics cho AI Dataset     ║
║  Series, DataFrame, Đọc & Ghi File CSV/JSON                  ║
╚══════════════════════════════════════════════════════════════╝
"""

import pandas as pd

print("=" * 50)
print("1. TẠO DATAFRAME TỪ DICT")
print("=" * 50)

# Dữ liệu log gọi LLM
data = {
    "request_id": ["req_01", "req_02", "req_03", "req_04"],
    "model": ["gpt-4o", "gpt-4o-mini", "gemini-1.5-flash", "gpt-4o"],
    "prompt_tokens": [120, 450, 80, 600],
    "completion_tokens": [250, 180, 40, 520],
    "latency_ms": [820.5, 340.2, 210.0, 1150.8],
    "status": ["SUCCESS", "SUCCESS", "RATE_LIMIT", "SUCCESS"]
}

df = pd.DataFrame(data)
print("DataFrame Log Gọi LLM:")
print(df)

print("\n" + "=" * 50)
print("2. THÔNG TIN & THỐNG KÊ NHANH")
print("=" * 50)
print(df.info())
print("\nThống kê mô tả số lượng token và latency:")
print(df.describe())

print("\n" + "=" * 50)
print("3. TẠO CỘT MỚI (FEATURE ENGINEERING CƠ BẢN)")
print("=" * 50)

# Tổng tokens
df["total_tokens"] = df["prompt_tokens"] + df["completion_tokens"]

# Phân loại độ trễ
df["is_slow"] = df["latency_ms"] > 500.0

print(df[["request_id", "model", "total_tokens", "latency_ms", "is_slow"]])

# Đọc ghi file (rất hay dùng khi lưu dataset fine-tuning)
# df.to_csv("llm_logs.csv", index=False)
# df_read = pd.read_csv("llm_logs.csv")

