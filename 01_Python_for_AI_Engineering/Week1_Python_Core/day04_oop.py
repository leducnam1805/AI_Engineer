"""
╔══════════════════════════════════════════════════════════╗
║  THÁNG 1 - TUẦN 1 - NGÀY 4: OOP trong Python            ║
║  Class, Inheritance, Dunder Methods, Dataclass           ║
╚══════════════════════════════════════════════════════════╝

Mục tiêu hôm nay:
  ✅ Python OOP so với Java OOP — điểm giống và khác
  ✅ Dunder methods (__str__, __repr__, __len__, __call__...)
  ✅ Dataclass — cách hiện đại thay thế boilerplate
  ✅ Abstract class & Protocol (duck typing)
  ✅ Build LLM Client class thực tế

Thời gian: ~90 phút

Tại sao quan trọng với AI Engineer?
  - LangChain, LlamaIndex đều dùng class hierarchy
  - Pydantic BaseModel là OOP
  - Viết LLM client, RAG pipeline đều cần OOP
  - Hiểu OOP để đọc được source code của AI libraries
"""

# ============================================================
# PHẦN 1: CLASS CƠ BẢN — Python vs Java
# ============================================================
print("=" * 50)
print("PHẦN 1: CLASS CƠ BẢN")
print("=" * 50)

"""
Java:
  public class LLMConfig {
      private String model;
      private double temperature;
      
      public LLMConfig(String model, double temperature) {
          this.model = model;
          this.temperature = temperature;
      }
      public String getModel() { return model; }
  }

Python: Không có private/public thực sự, dùng convention _underscore
"""

class LLMConfig:
    # Class variable — dùng chung cho tất cả instances
    SUPPORTED_MODELS = ["gpt-4o", "gpt-4o-mini", "gemini-1.5-flash"]
    
    def __init__(self, model: str, temperature: float = 0.7, max_tokens: int = 1000):
        """Constructor — tương tự Java constructor."""
        # Instance variables
        self.model = model              # public
        self.temperature = temperature  # public
        self._max_tokens = max_tokens   # protected (convention)
        self.__api_key = None           # private (name mangling)
    
    def set_api_key(self, key: str) -> None:
        """Setter cho private attribute."""
        self.__api_key = key
    
    def is_valid(self) -> bool:
        return self.model in self.SUPPORTED_MODELS and 0 <= self.temperature <= 2
    
    # Tương đương toString() trong Java
    def __repr__(self) -> str:
        return f"LLMConfig(model='{self.model}', temperature={self.temperature})"
    
    def __str__(self) -> str:
        return f"Config: {self.model} (temp={self.temperature})"


# Khởi tạo
config = LLMConfig("gpt-4o", temperature=0.3)
print(repr(config))    # gọi __repr__
print(str(config))     # gọi __str__
print(config)          # cũng gọi __str__
print(config.is_valid())
print(LLMConfig.SUPPORTED_MODELS)  # class variable

# ============================================================
# PHẦN 2: DUNDER METHODS ⭐ (Magic Methods)
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 2: DUNDER METHODS")
print("=" * 50)

class ChatHistory:
    """Quản lý lịch sử chat với LLM."""
    
    def __init__(self):
        self._messages: list[dict] = []
    
    def add(self, role: str, content: str) -> None:
        self._messages.append({"role": role, "content": content})
    
    # len(history) → trả về số messages
    def __len__(self) -> int:
        return len(self._messages)
    
    # history[0] → truy cập theo index
    def __getitem__(self, index: int) -> dict:
        return self._messages[index]
    
    # for msg in history → iterate
    def __iter__(self):
        return iter(self._messages)
    
    # "user" in history → check membership
    def __contains__(self, role: str) -> bool:
        return any(m["role"] == role for m in self._messages)
    
    # history1 + history2 → merge
    def __add__(self, other: "ChatHistory") -> "ChatHistory":
        new = ChatHistory()
        new._messages = self._messages + other._messages
        return new
    
    # bool(history) → True nếu có messages
    def __bool__(self) -> bool:
        return len(self._messages) > 0
    
    def __repr__(self) -> str:
        return f"ChatHistory({len(self)} messages)"


history = ChatHistory()
print(f"Empty: {bool(history)}")     # False

history.add("user", "Hello!")
history.add("assistant", "Hi there!")
history.add("user", "Tell me about Python")

print(f"Length: {len(history)}")     # 3
print(f"First: {history[0]}")        # dict
print(f"Has user: {'user' in history}")  # True

for msg in history:
    print(f"  [{msg['role']}]: {msg['content']}")

# ============================================================
# PHẦN 3: INHERITANCE
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 3: INHERITANCE")
print("=" * 50)

class BaseLLMClient:
    """Base class cho tất cả LLM clients."""
    
    def __init__(self, model: str, api_key: str):
        self.model = model
        self._api_key = api_key
        self._call_count = 0
    
    def complete(self, prompt: str) -> str:
        """Template method — subclass phải implement."""
        raise NotImplementedError("Subclass must implement complete()")
    
    def chat(self, messages: list[dict]) -> str:
        """Template method — subclass phải implement."""
        raise NotImplementedError("Subclass must implement chat()")
    
    def get_stats(self) -> dict:
        """Shared method — dùng chung cho tất cả subclasses."""
        return {"model": self.model, "total_calls": self._call_count}
    
    def _increment_counter(self):
        self._call_count += 1


class OpenAIClient(BaseLLMClient):
    """OpenAI-specific client."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        super().__init__(model, api_key)   # gọi parent __init__
        self.organization = None
    
    def complete(self, prompt: str) -> str:
        self._increment_counter()
        # Thực tế: gọi openai.chat.completions.create(...)
        return f"[OpenAI/{self.model}]: Response to '{prompt[:30]}'"
    
    def chat(self, messages: list[dict]) -> str:
        self._increment_counter()
        last_msg = messages[-1]["content"]
        return f"[OpenAI/{self.model}]: Chat response to '{last_msg[:30]}'"


class GeminiClient(BaseLLMClient):
    """Google Gemini-specific client."""
    
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash"):
        super().__init__(model, api_key)
        self.safety_settings = {}
    
    def complete(self, prompt: str) -> str:
        self._increment_counter()
        return f"[Gemini/{self.model}]: Response to '{prompt[:30]}'"
    
    def chat(self, messages: list[dict]) -> str:
        self._increment_counter()
        last_msg = messages[-1]["content"]
        return f"[Gemini/{self.model}]: Chat response to '{last_msg[:30]}'"
    
    def set_safety(self, category: str, level: str) -> None:
        """Gemini-specific method."""
        self.safety_settings[category] = level


# Dùng polymorphism — đây là điểm mạnh của OOP!
clients: list[BaseLLMClient] = [
    OpenAIClient("sk-..."),
    GeminiClient("AIza..."),
]

for client in clients:
    response = client.complete("What is AI?")  # gọi đúng implementation
    print(response)
    print(f"Stats: {client.get_stats()}")

# isinstance check
print(isinstance(clients[0], BaseLLMClient))   # True
print(isinstance(clients[0], OpenAIClient))    # True
print(isinstance(clients[0], GeminiClient))    # False

# ============================================================
# PHẦN 4: DATACLASS ⭐ (Python hiện đại — ít boilerplate hơn)
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 4: DATACLASS")
print("=" * 50)

from dataclasses import dataclass, field
from typing import Optional

# Thay vì viết __init__, __repr__, __eq__ thủ công:
@dataclass
class Message:
    role: str
    content: str
    tokens: int = 0
    model: Optional[str] = None
    # field(default_factory=...) cho mutable defaults
    metadata: dict = field(default_factory=dict)
    
    # Vẫn có thể thêm methods
    def is_user_message(self) -> bool:
        return self.role == "user"
    
    def word_count(self) -> int:
        return len(self.content.split())


@dataclass
class ChatRequest:
    messages: list[Message]
    model: str = "gpt-4o"
    temperature: float = 0.7
    max_tokens: int = 1000
    stream: bool = False


# Dùng dataclass
msg = Message(role="user", content="What is machine learning?", tokens=6)
print(msg)               # auto __repr__
print(msg.is_user_message())
print(msg.word_count())

msg2 = Message(role="user", content="What is machine learning?", tokens=6)
print(msg == msg2)       # auto __eq__ — True!

request = ChatRequest(
    messages=[msg],
    temperature=0.3
)
print(request)

# @dataclass(frozen=True) — immutable như Java record
@dataclass(frozen=True)
class ModelInfo:
    name: str
    context_window: int
    cost_per_1m_tokens: float
    
    def is_affordable(self, budget: float) -> bool:
        return self.cost_per_1m_tokens <= budget

gpt4o = ModelInfo("gpt-4o", 128000, 5.0)
# gpt4o.name = "changed"  # ❌ FrozenInstanceError!
print(gpt4o.is_affordable(10.0))  # True

# ============================================================
# PHẦN 5: PROPERTY (Getter/Setter Pythonic)
# ============================================================
print("\n" + "=" * 50)
print("PHẦN 5: PROPERTY")
print("=" * 50)

class LLMSession:
    def __init__(self, model: str):
        self._model = model
        self._temperature = 0.7
        self._message_count = 0
    
    @property
    def temperature(self) -> float:
        """Getter — truy cập như attribute bình thường."""
        return self._temperature
    
    @temperature.setter
    def temperature(self, value: float) -> None:
        """Setter với validation."""
        if not 0.0 <= value <= 2.0:
            raise ValueError(f"Temperature must be 0-2, got {value}")
        self._temperature = value
    
    @property
    def model(self) -> str:
        return self._model
    
    # Read-only property (không có setter)
    @property
    def message_count(self) -> int:
        return self._message_count


session = LLMSession("gpt-4o")
print(session.temperature)       # gọi getter → 0.7
session.temperature = 0.3        # gọi setter
print(session.temperature)       # 0.3

try:
    session.temperature = 5.0   # ❌ ValueError
except ValueError as e:
    print(f"Error: {e}")

# ============================================================
# 🏋️ BÀI TẬP THỰC HÀNH
# ============================================================
print("\n" + "=" * 50)
print("BÀI TẬP")
print("=" * 50)

"""
Bài 1: Tạo dataclass TokenUsage để track chi phí API:
       - Fields: prompt_tokens, completion_tokens, model, cost_per_1m
       - Property: total_tokens (computed)
       - Method: calculate_cost() → float (tính chi phí thực tế)
       - Method: __str__ → "Used X tokens, cost $Y"
       
       Ví dụ: 
       usage = TokenUsage(500, 300, "gpt-4o", 5.0)
       print(usage.total_tokens)   # 800
       print(usage.calculate_cost()) # 0.004  (800/1_000_000 * 5.0)
"""
# TODO: Implement TokenUsage dataclass

"""
Bài 2: Tạo class ConversationManager quản lý chat session:
       - __init__(self, llm_client: BaseLLMClient, system_prompt: str = "")
       - add_user_message(content: str) → tự gọi llm_client.chat() và lưu response
       - history property → trả về list[Message] 
       - clear() → xóa lịch sử
       - __len__ → số turns (1 turn = 1 user + 1 assistant)
       - __str__ → format đẹp toàn bộ conversation
"""
# TODO: Implement ConversationManager

"""
Bài 3 (Challenge): Implement LLMClientPool — load balancing giữa nhiều clients:
       - __init__(clients: list[BaseLLMClient])
       - complete(prompt: str) → tự chọn client ít được dùng nhất (round-robin)
       - get_stats() → stats của tất cả clients
       - Dùng __call__ để có thể gọi trực tiếp: pool("What is AI?")
"""
# TODO: Implement LLMClientPool

print("\n✅ Ngày 4: OOP xong! Key takeaway:")
print("  - Dataclass > viết __init__ thủ công trong hầu hết trường hợp")
print("  - Dunder methods giúp class hoạt động tự nhiên với Python syntax")
print("  - Inheritance để share logic, không copy-paste code")

