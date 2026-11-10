# 🐍 Tháng 1: Python for AI Engineering

> **Mục tiêu**: Thành thạo Python theo hướng AI Engineering — không học như beginner mà học như dev 5 năm đang switch stack.

---

## 🎯 Deliverable Cuối Tháng
**Xây dựng AI Backend Service** bao gồm:
- REST API bằng FastAPI
- Gọi LLM API (Gemini / OpenAI)
- Xử lý dữ liệu với Pandas/NumPy
- Containerize bằng Docker
- Unit tests

---

## 📅 Kế Hoạch 4 Tuần

### ✅ Tuần 1 — Python Core (Góc nhìn từ Java Dev)

**Mục tiêu**: Viết Python tự nhiên như Java trong 7 ngày.

| Ngày | Chủ đề | File thực hành |
|------|--------|---------------|
| 1 | Syntax cơ bản, types, f-strings | `Week1_Python_Core/day01_basics.py` |
| 2 | List, Dict, Set, Tuple & Comprehensions | `Week1_Python_Core/day02_collections.py` |
| 3 | Functions, `*args`, `**kwargs`, Decorators | `Week1_Python_Core/day03_functions.py` |
| 4 | OOP: Class, Inheritance, Dunder methods | `Week1_Python_Core/day04_oop.py` |
| 5 | Error handling, Context managers, Generators | `Week1_Python_Core/day05_advanced.py` |
| 6 | Modules, Packages, `__init__.py`, `uv` setup | `Week1_Python_Core/day06_modules.py` |
| 7 | **Mini Project**: Script gọi REST API + xử lý JSON | `Week1_Python_Core/day07_project.py` |

**Tài nguyên**:
- [LearnXinYMinutes Python](https://learnxinyminutes.com/docs/python/) — 30 phút đọc xong
- [Python cho Java devs](https://realpython.com/python-vs-java/) — so sánh trực tiếp

---

### ✅ Tuần 2 — Data Libraries (NumPy, Pandas, Pydantic)

**Mục tiêu**: Xử lý dữ liệu và validate dữ liệu — nền tảng của mọi AI app.

| Ngày | Chủ đề | File thực hành |
|------|--------|---------------|
| 1 | NumPy: arrays, operations, broadcasting | `Week2_Data_Libraries/day01_numpy.py` |
| 2 | NumPy: indexing, slicing, linear algebra | `Week2_Data_Libraries/day02_numpy_advanced.py` |
| 3 | Pandas: Series, DataFrame, read/write CSV | `Week2_Data_Libraries/day03_pandas_basics.py` |
| 4 | Pandas: filtering, groupby, merge, handling nulls | `Week2_Data_Libraries/day04_pandas_advanced.py` |
| 5 | Pydantic v2: Models, validation, settings | `Week2_Data_Libraries/day05_pydantic.py` |
| 6 | Matplotlib/Seaborn: basic visualization | `Week2_Data_Libraries/day06_visualization.py` |
| 7 | **Mini Project**: Phân tích dataset thực tế (CSV) | `Week2_Data_Libraries/day07_project.py` |

**Tài nguyên**:
- [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html)
- [Pandas in 10 minutes](https://pandas.pydata.org/docs/user_guide/10min.html)
- [Pydantic docs](https://docs.pydantic.dev/)

---

### ✅ Tuần 3 — FastAPI & AsyncIO

**Mục tiêu**: Xây dựng AI backend service — đây là skill core nhất của AI Engineer.

| Ngày | Chủ đề | File thực hành |
|------|--------|---------------|
| 1 | AsyncIO: `async/await`, event loop, tasks | `Week3_FastAPI_Async/day01_asyncio.py` |
| 2 | FastAPI: routing, path params, query params | `Week3_FastAPI_Async/day02_fastapi_basics.py` |
| 3 | FastAPI: request body (Pydantic), response models | `Week3_FastAPI_Async/day03_fastapi_models.py` |
| 4 | FastAPI: middleware, CORS, error handling | `Week3_FastAPI_Async/day04_fastapi_advanced.py` |
| 5 | FastAPI: Streaming responses (SSE) | `Week3_FastAPI_Async/day05_streaming.py` |
| 6 | `httpx` async HTTP client, gọi external APIs | `Week3_FastAPI_Async/day06_http_client.py` |
| 7 | **Mini Project**: API nhận text → gọi Gemini API → trả kết quả | `Week3_FastAPI_Async/day07_project.py` |

**Tài nguyên**:
- [FastAPI official docs](https://fastapi.tiangolo.com/) — cực kỳ tốt
- [AsyncIO explained](https://realpython.com/async-io-python/)

---

### ✅ Tuần 4 — Git, Docker, Testing

**Mục tiêu**: Áp dụng engineering practices vào AI project (bạn đã biết nhiều phần này).

| Ngày | Chủ đề | File thực hành |
|------|--------|---------------|
| 1 | Git flow cho AI project: `.gitignore` (secrets!), branching | `Week4_Git_Docker_Testing/day01_git.md` |
| 2 | `python-dotenv` + quản lý API keys an toàn | `Week4_Git_Docker_Testing/day02_env_secrets.py` |
| 3 | Docker: Dockerfile cho Python/FastAPI app | `Week4_Git_Docker_Testing/day03_docker/` |
| 4 | Docker Compose: app + dependencies | `Week4_Git_Docker_Testing/day04_compose/` |
| 5 | Testing: `pytest` basics, fixtures, mocking LLM calls | `Week4_Git_Docker_Testing/day05_testing.py` |
| 6 | Logging: `structlog`, monitoring cơ bản | `Week4_Git_Docker_Testing/day06_logging.py` |
| 7 | **DELIVERABLE**: Kết hợp tất cả → AI Backend Service hoàn chỉnh | `Projects/ai_backend_service/` |

---

## 🏗️ Deliverable: AI Backend Service

```
Projects/ai_backend_service/
├── app/
│   ├── main.py          # FastAPI app
│   ├── routes/
│   │   └── ai.py        # AI endpoints
│   ├── services/
│   │   └── llm.py       # Gemini/OpenAI service
│   └── models/
│       └── schemas.py   # Pydantic models
├── tests/
│   └── test_ai.py
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── requirements.txt
└── README.md
```

**Endpoints cần có**:
- `POST /api/chat` — gửi message, nhận AI response
- `POST /api/summarize` — tóm tắt văn bản
- `GET /api/health` — health check

---

## 📝 Notes Template

Trong thư mục `Notes/`, ghi lại:
- Concepts khó hiểu và cách bạn hiểu nó
- Lỗi gặp phải và cách fix
- Khám phá thú vị

---

## ✅ Checklist Hoàn Thành Tháng 1

- [ ] Tuần 1: Python Core — viết code Python tự nhiên
- [ ] Tuần 2: Data Libraries — xử lý dữ liệu với NumPy/Pandas/Pydantic
- [ ] Tuần 3: FastAPI & Async — build REST API có streaming
- [ ] Tuần 4: DevOps basics — Docker, testing, logging
- [ ] **Deliverable**: AI Backend Service chạy được trong Docker

