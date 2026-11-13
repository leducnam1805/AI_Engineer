"""
╔══════════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 2 - NGÀY 5: Pydantic v2                      ║
║  Data Validation, Schema & Structured Output cho LLM         ║
╚══════════════════════════════════════════════════════════════╝

Tại sao Pydantic là thư viện QUAN TRỌNG NHẤT của AI Engineer?
- FastAPI dùng Pydantic để validate Request Body từ Frontend/Client.
- OpenAI / Gemini Function Calling & Structured Outputs bắt buộc định nghĩa Schema bằng Pydantic.
- Giúp parse chuỗi JSON từ LLM thành object Python có kiểm tra kiểu an toàn (Type Safety).
"""

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import List, Optional
from enum import Enum

print("=" * 50)
print("1. PYDANTIC MODEL CƠ BẢN")
print("=" * 50)

class RoleEnum(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    role: RoleEnum
    content: str = Field(..., min_length=1, description="Nội dung tin nhắn")
    tokens: Optional[int] = Field(default=None, ge=0)

# Khởi tạo hợp lệ
msg = ChatMessage(role=RoleEnum.USER, content="Xin chào AI!")
print(f"Message Valid: {msg}")
print(f"Serialize sang JSON: {msg.model_dump_json()}")

# Thử truyền dữ liệu sai -> Pydantic tự động báo lỗi chi tiết
from pydantic import ValidationError
try:
    invalid_msg = ChatMessage(role="admin", content="")  # role sai, content rỗng
except ValidationError as e:
    print(f"\n❌ Bắt lỗi Validation tự động:\n{e}")


print("\n" + "=" * 50)
print("2. STRUCTURED OUTPUT CHO LLM (VD: Trích xuất thông tin CV)")
print("=" * 50)

class CandidateSkill(BaseModel):
    name: str
    years_of_experience: float
    level: str = Field(description="Junior, Middle, Senior")

class CandidateProfile(BaseModel):
    full_name: str
    email: EmailStr
    current_title: str
    skills: List[CandidateSkill]
    estimated_salary_k: Optional[float] = None

    @field_validator("estimated_salary_k")
    @classmethod
    def validate_salary(cls, v):
        if v is not None and v < 0:
            raise ValueError("Lương không thể âm!")
        return v

# Giả sử LLM trả về chuỗi JSON raw sau:
raw_llm_json = """
{
    "full_name": "Nguyen Van A",
    "email": "nguyenvana@gmail.com",
    "current_title": "Senior Java Developer",
    "skills": [
        {"name": "Java", "years_of_experience": 5.0, "level": "Senior"},
        {"name": "Docker", "years_of_experience": 3.0, "level": "Middle"},
        {"name": "Python", "years_of_experience": 0.5, "level": "Junior"}
    ],
    "estimated_salary_k": 3.5
}
"""

# Parse JSON thành Object có type an toàn 100%:
profile = CandidateProfile.model_validate_json(raw_llm_json)
print(f"Họ tên ứng viên: {profile.full_name}")
print(f"Email: {profile.email}")
print(f"Số kỹ năng: {len(profile.skills)}")
for s in profile.skills:
    print(f"  - {s.name}: {s.years_of_experience} năm ({s.level})")

