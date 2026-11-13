# Git Best Practices cho AI & Data Projects

## 1. Không bao giờ commit Secrets & API Keys
Luôn có file `.env` và `.gitignore`.

Ví dụ `.gitignore` chuẩn cho AI Project:
```gitignore
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C environments
.venv/
env/
venv/

# Environment Variables (Chứa OpenAI Key, Gemini Key, DB Password)
.env
.env.local
.env.*.local

# Data & Model weights (Không commit file nặng lên git!)
*.csv
*.parquet
*.pt
*.bin
*.onnx
models/
data/

# IDE
.vscode/
.idea/
```

## 2. Quản lý Git Branching
- `main`: Code production đã test qua CI/CD
- `dev`: Code tích hợp
- `feature/rag-pipeline`: Nhánh phát triển tính năng mới

