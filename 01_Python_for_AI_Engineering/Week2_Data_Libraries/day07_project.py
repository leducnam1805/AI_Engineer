"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 2 - NGÀY 7: Mini-Project Xử Lý Dữ Liệu AI   ║
║  Dự Án: AI Evaluation Dataset Analyzer & Schema Validator    ║
╚══════════════════════════════════════════════════════════════╝

Mục tiêu dự án:
  - Đọc file logs giả lập các câu hỏi/trả lời của LLM.
  - Dùng Pydantic validate từng bản ghi đánh giá (accuracy, latency, cost).
  - Dùng Pandas tổng hợp và xuất báo cáo:
    + Model nào có latency thấp nhất?
    + Model nào tốn ít chi phí nhất trên mỗi 1000 tokens?
    + Tỷ lệ lỗi (Error rate) của hệ thống.
"""

import pandas as pd
from pydantic import BaseModel, Field
from typing import List

class EvaluationRecord(BaseModel):
    eval_id: str
    model: str
    prompt_tokens: int = Field(..., ge=0)
    completion_tokens: int = Field(..., ge=0)
    latency_ms: float = Field(..., ge=0)
    is_hallucination: bool
    ground_truth_score: float = Field(..., ge=0.0, le=1.0)

# Dataset mẫu
records_raw = [
    {"eval_id": "e1", "model": "gpt-4o", "prompt_tokens": 100, "completion_tokens": 200, "latency_ms": 650.0, "is_hallucination": False, "ground_truth_score": 0.95},
    {"eval_id": "e2", "model": "gemini-flash", "prompt_tokens": 120, "completion_tokens": 180, "latency_ms": 250.0, "is_hallucination": False, "ground_truth_score": 0.88},
    {"eval_id": "e3", "model": "gpt-4o-mini", "prompt_tokens": 90, "completion_tokens": 150, "latency_ms": 320.0, "is_hallucination": True, "ground_truth_score": 0.40},
    {"eval_id": "e4", "model": "gemini-flash", "prompt_tokens": 300, "completion_tokens": 400, "latency_ms": 410.0, "is_hallucination": False, "ground_truth_score": 0.91},
]

# 1. Validate bằng Pydantic
valid_records = [EvaluationRecord(**r) for r in records_raw]

# 2. Chuyển sang Pandas DataFrame
df = pd.DataFrame([r.model_dump() for r in valid_records])

print("=" * 60)
print("📊 BÁO CÁO ĐÁNH GIÁ CHẤT LƯỢNG MÔ HÌNH (EVALUATION REPORT)")
print("=" * 60)

report = df.groupby("model").agg(
    avg_latency=("latency_ms", "mean"),
    avg_quality=("ground_truth_score", "mean"),
    hallucination_count=("is_hallucination", "sum"),
    total_evals=("eval_id", "count")
).reset_index()

print(report.to_string(index=False))
print("\n✅ Hoàn thành Mini-Project Tuần 2!")

