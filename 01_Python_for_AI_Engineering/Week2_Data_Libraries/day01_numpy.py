"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 2 - NGÀY 1: NumPy Foundations                ║
║  Arrays, Vector Operations, Broadcasting                     ║
╚══════════════════════════════════════════════════════════════╝

Tại sao AI Engineer cần NumPy?
- Mọi dữ liệu hình ảnh, âm thanh, text embeddings đều biểu diễn dưới dạng Vector / Ma trận.
- NumPy tính toán bằng C, nhanh hơn vòng lặp Python thuần gấp 50-100 lần.
"""

import numpy as np

print("=" * 50)
print("1. KHỞI TẠO NUMPY ARRAY")
print("=" * 50)

# 1D Array (Vector) - Ví dụ: 1 vector embedding của 1 từ
vec = np.array([0.15, -0.42, 0.88, 0.05])
print(f"Vector: {vec}")
print(f"Shape: {vec.shape}, Dtype: {vec.dtype}")

# 2D Array (Matrix) - Ví dụ: 3 documents, mỗi doc có 4 chiều embedding
matrix = np.array([
    [0.1, 0.2, 0.3, 0.4],
    [0.5, 0.6, 0.7, 0.8],
    [0.9, 1.0, 1.1, 1.2]
])
print(f"\nMatrix 3x4:\n{matrix}")
print(f"Shape: {matrix.shape}")

# Các hàm sinh mảng thông dụng
zeros = np.zeros((2, 3))        # Mảng toàn số 0
ones = np.ones((3, 3))          # Mảng toàn số 1
random_embeds = np.random.randn(2, 4)  # Phân phối chuẩn Gaussian N(0, 1)
print(f"\nRandom Embeddings:\n{random_embeds}")

print("\n" + "=" * 50)
print("2. VECTORIZED OPERATIONS (KHÔNG DÙNG FOR LOOP)")
print("=" * 50)

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

# Cộng, trừ, nhân từng phần tử (Element-wise)
print(f"a + b = {a + b}")
print(f"a * b = {a * b}")
print(f"a ** 2 = {a ** 2}")

# So sánh tốc độ: Vectorization vs Pure Python Loop
import time
large_arr = np.random.randn(1_000_000)

# Cách NumPy
start = time.perf_counter()
res_np = large_arr * 2.5 + 1.0
t_np = time.perf_counter() - start

# Cách Python thuần
large_list = list(large_arr)
start = time.perf_counter()
res_py = [x * 2.5 + 1.0 for x in large_list]
t_py = time.perf_counter() - start

print(f"\n⏱️  Thời gian NumPy: {t_np*1000:.2f}ms")
print(f"⏱️  Thời gian Python Loop: {t_py*1000:.2f}ms (NumPy nhanh hơn ~{t_py/t_np:.1f} lần!)")

print("\n" + "=" * 50)
print("3. BROADCASTING (Cơ chế khớp chiều tự động)")
print("=" * 50)

# Cộng 1 vector (1, 4) vào ma trận (3, 4)
bias = np.array([1, 10, 100, 1000])
res_broadcast = matrix + bias
print(f"Matrix gốc:\n{matrix}")
print(f"Sau khi cộng bias:\n{res_broadcast}")

# BÀI TẬP:
# Viết hàm normalize_vector(v: np.ndarray) -> np.ndarray
# Chuẩn hóa vector theo L2 Norm: v / ||v|| (dùng np.linalg.norm)

