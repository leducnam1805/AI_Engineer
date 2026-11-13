"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 2 - NGÀY 6: Data Visualization Basics        ║
║  Vẽ Biểu Đồ Hiệu Năng & Chi Phí AI                           ║
╚══════════════════════════════════════════════════════════════╝
"""

# Day 6 tập trung vào cách export chart hoặc hiển thị phân phối tokens/latency
# Thường dùng Matplotlib hoặc xuất báo cáo dạng text/json nếu chạy server headless.

def draw_ascii_bar_chart(data: dict):
    """Vẽ biểu đồ Bar Chart dạng ASCII ngay trong Terminal (rất tiện khi dev/debug trên server)."""
    print("\n📊 BIỂU ĐỒ TỔNG SỐ TOKEN THEO MODEL:")
    max_val = max(data.values()) if data else 1
    for label, val in data.items():
        bar_len = int((val / max_val) * 30)
        bar = "█" * bar_len
        print(f"{label.ljust(18)} | {bar} {val}")

mock_data = {
    "gpt-4o": 45000,
    "gemini-1.5-pro": 32000,
    "gpt-4o-mini": 128000,
    "claude-3-5-sonnet": 15000
}

draw_ascii_bar_chart(mock_data)

