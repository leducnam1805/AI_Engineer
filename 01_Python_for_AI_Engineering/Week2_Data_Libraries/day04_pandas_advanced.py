"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 2 - NGÀY 4: Pandas Advanced & Data Cleaning  ║
║  Filtering, GroupBy, Xử lý Missing Values                    ║
╚══════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import numpy as np

# Tạo dataset thực tế hơn: Log hệ thống AI production
data = {
    "user_id": ["u1", "u2", "u1", "u3", "u2", "u4", "u1"],
    "model": ["gpt-4o", "gemini-1.5-flash", "gpt-4o", "gpt-4o-mini", "gemini-1.5-flash", "gpt-4o", None],
    "cost": [0.005, 0.0001, 0.008, 0.0004, 0.0002, 0.012, 0.003],
    "rating": [5, 4, None, 5, 2, 4, 3],  # User feedback (1-5 sao)
    "feedback": ["Great answer", "Fast", None, "Perfect", "Wrong code", None, "Ok"]
}

df = pd.DataFrame(data)
print("Dataset gốc:")
print(df)

print("\n" + "=" * 50)
print("1. XỬ LÝ DỮ LIỆU THIẾU (NULL / NAN)")
print("=" * 50)

print("Số lượng giá trị null ở mỗi cột:")
print(df.isnull().sum())

# Điền giá trị mặc định cho cột model và rating
df["model"] = df["model"].fillna("unknown")
df["rating"] = df["rating"].fillna(df["rating"].mean())  # điền bằng trung bình
print("\nSau khi fillna:")
print(df[["user_id", "model", "rating"]])

print("\n" + "=" * 50)
print("2. FILTERING & QUERY")
print("=" * 50)

# Lấy các request có cost > 0.001 hoặc rating < 3
problematic_or_expensive = df[(df["cost"] > 0.001) | (df["rating"] < 3)]
print("Các request tốn tiền hoặc user không hài lòng:")
print(problematic_or_expensive)

print("\n" + "=" * 50)
print("3. GROUPBY & AGGREGATION (Báo cáo kinh doanh)")
print("=" * 50)

# Thống kê tổng tiền và rating trung bình theo từng Model
summary_by_model = df.groupby("model").agg(
    total_cost=("cost", "sum"),
    avg_rating=("rating", "mean"),
    total_requests=("user_id", "count")
).reset_index()

print("Thống kê hiệu năng & chi phí từng model:")
print(summary_by_model)

