"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 2 - NGÀY 2: Advanced NumPy & Cosine Sim      ║
║  Indexing, Slicing & Cosine Similarity (Trái tim của RAG)    ║
╚══════════════════════════════════════════════════════════════╝
"""

import numpy as np

print("=" * 50)
print("1. INDEXING & BOOLEAN MASKING")
print("=" * 50)

scores = np.array([0.92, 0.45, 0.78, 0.33, 0.89, 0.65])

# Boolean indexing (Lọc vector theo điều kiện)
high_scores = scores[scores >= 0.7]
print(f"Scores >= 0.7: {high_scores}")

# Lấy index của các phần tử thỏa mãn
top_indices = np.where(scores >= 0.7)[0]
print(f"Vị trí các phần tử >= 0.7: {top_indices}")

# Sắp xếp và lấy Top-K (dùng argsort)
# argsort trả về mảng các index đã sắp xếp từ bé đến lớn
sorted_indices = np.argsort(scores)[::-1]  # đảo ngược để lớn -> bé
print(f"Top 3 indices: {sorted_indices[:3]}")
print(f"Top 3 scores: {scores[sorted_indices[:3]]}")


print("\n" + "=" * 50)
print("2. COSINE SIMILARITY — THUẬT TOÁN TÌM KIẾM CỦA VECTOR DB")
print("=" * 50)

"""
Công thức Cosine Similarity:
            A . B
cos(A, B) = -------------
            ||A|| * ||B||

- Bằng 1: Hai vector hoàn toàn cùng hướng (nội dung giống hệt).
- Bằng 0: Vuông góc (không liên quan).
- Bằng -1: Ngược hướng hoàn toàn.
"""

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return float(dot_product / (norm_v1 * norm_v2))

# Giả lập 3 vector embedding 5 chiều:
doc1_emb = np.array([0.8, 0.2, 0.1, 0.05, 0.1])   # Ví dụ về "Python Programming"
doc2_emb = np.array([0.75, 0.25, 0.08, 0.04, 0.12])# Ví dụ về "FastAPI Backend"
doc3_emb = np.array([0.05, 0.1, 0.9, 0.8, 0.7])   # Ví dụ về "Nấu ăn ẩm thực"

query_emb = np.array([0.7, 0.3, 0.1, 0.0, 0.05])  # User hỏi: "Cách viết web app bằng Python"

sim_1 = cosine_similarity(query_emb, doc1_emb)
sim_2 = cosine_similarity(query_emb, doc2_emb)
sim_3 = cosine_similarity(query_emb, doc3_emb)

print(f"Độ tương đồng với Doc 1 (Python):  {sim_1:.4f}")
print(f"Độ tương đồng với Doc 2 (FastAPI): {sim_2:.4f}")
print(f"Độ tương đồng với Doc 3 (Nấu ăn):  {sim_3:.4f}")

# Doc 1 và Doc 2 sẽ có độ tương đồng vượt trội so với Doc 3!

