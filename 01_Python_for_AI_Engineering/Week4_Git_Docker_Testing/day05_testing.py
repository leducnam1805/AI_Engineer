"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 4 - NGÀY 5: Testing AI Services với Pytest   ║
║  Unit Test, Fixtures & Mocking LLM Calls                     ║
╚══════════════════════════════════════════════════════════════╝

Nguyên tắc vàng khi test hệ thống AI:
- KHÔNG BAO GIỜ gọi API thật (OpenAI/Gemini) trong Unit Test (tốn tiền & phụ thuộc mạng).
- Dùng unittest.mock để giả lập response.
"""

import pytest
from unittest.mock import AsyncMock, patch

def clean_text(text: str) -> str:
    return " ".join(text.strip().split())

# 1. Test cơ bản
def test_clean_text():
    raw = "   Đây là   prompt    thừa dấu cách   "
    expected = "Đây là prompt thừa dấu cách"
    assert clean_text(raw) == expected

# 2. Test Fixture (tương tự @BeforeEach trong JUnit)
@pytest.fixture
def sample_chat_payload():
    return {
        "model": "gpt-4o",
        "prompt": "Hello test"
    }

def test_chat_payload_structure(sample_chat_payload):
    assert "model" in sample_chat_payload
    assert sample_chat_payload["prompt"] == "Hello test"

# 3. Mocking LLM Call
class MockLLMService:
    async def call_model(self, prompt: str):
        # Hàm này trong thực tế gọi ra mạng
        pass

@pytest.mark.asyncio
async def test_mocked_llm_response():
    service = MockLLMService()
    # Mock hàm call_model
    service.call_model = AsyncMock(return_value="Mocked AI response")
    
    result = await service.call_model("Test prompt")
    assert result == "Mocked AI response"
    service.call_model.assert_called_once_with("Test prompt")

print("✅ File test mẫu đã sẵn sàng! Chạy bằng lệnh: uv run pytest")

