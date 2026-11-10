# Python for AI Engineering - Quick Reference
# Dành cho Java/React developer

## Python vs Java - So sánh nhanh

| Khái niệm | Java | Python |
|-----------|------|--------|
| Khai báo biến | `String name = "A";` | `name = "A"` |
| In ra màn hình | `System.out.println(x)` | `print(x)` |
| String format | `String.format("%s %d", a, b)` | `f"{a} {b}"` |
| Null check | `if (x != null)` | `if x is not None` |
| Ternary | `x > 0 ? "pos" : "neg"` | `"pos" if x > 0 else "neg"` |
| For loop | `for (int i=0; i<n; i++)` | `for i in range(n)` |
| Array/List | `List<String> list = new ArrayList<>()` | `list = []` |
| Dictionary | `Map<String, Object> map = new HashMap<>()` | `d = {}` |
| Lambda | `x -> x * 2` | `lambda x: x * 2` |
| Try/Catch | `try { } catch (Exception e) { }` | `try: ... except Exception as e:` |
| Class | `public class Foo { }` | `class Foo:` |
| Extends | `class B extends A` | `class B(A):` |
| Interface | `implements Runnable` | Duck typing / ABC |
| Void method | `void doSomething()` | `def do_something() -> None:` |
| Return type | `String getName()` | `def get_name() -> str:` |
| Const | `final String NAME = "A"` | `NAME = "A"` (convention: UPPER_CASE) |

## Tools

| Công cụ | Mô tả | Tương đương Java |
|---------|-------|-----------------|
| `uv` | Package manager (nhanh nhất) | Maven/Gradle |
| `pip` | Package installer | mvn install |
| `venv` | Virtual environment | Classpath isolation |
| `pytest` | Testing | JUnit |
| `ruff` | Linter + formatter | Checkstyle + Spotless |
| `mypy` | Type checker | Compiler type checking |

## Setup môi trường (chạy 1 lần)

```bash
# Cài uv
pip install uv

# Tạo project mới
uv init my_project
cd my_project

# Thêm thư viện
uv add fastapi httpx pydantic python-dotenv

# Chạy script
uv run python main.py
```

## Các kiểu dữ liệu quan trọng trong AI

```python
# String - xử lý prompt, text
prompt: str = "Tell me about AI"

# List - batch của items
documents: list[str] = ["doc1", "doc2"]
embeddings: list[float] = [0.1, 0.2, 0.9]

# Dict - JSON response từ LLM API
response: dict = {"role": "assistant", "content": "..."}

# Optional - value có thể là None
user_id: int | None = None

# Pydantic Model - structured data (cực kỳ quan trọng!)
from pydantic import BaseModel
class ChatMessage(BaseModel):
    role: str
    content: str
```

