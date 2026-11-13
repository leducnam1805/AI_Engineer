# Multi-stage Dockerfile tối ưu kích thước cho FastAPI AI Service
FROM python:3.11-slim as builder

WORKDIR /app

# Cài đặt công cụ uv để cài thư viện siêu tốc
RUN pip install --no-cache-dir uv

COPY pyproject.toml requirements.txt* ./

# Cài đặt dependencies vào virtualenv
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install --no-cache -r requirements.txt || true

# Runner Stage: Chỉ chứa runtime thực thi, loại bỏ rác build
FROM python:3.11-slim as runner

WORKDIR /app

# Copy môi trường Python từ builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy source code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

