# Lesson 01 — Installation & Setup

## Installing FastAPI

FastAPI requires two main packages:
1. **`fastapi`** — The framework itself
2. **`uvicorn`** — An ASGI server to run your app (like a web server for async Python)

### Quick Install

```bash
# Create a project directory
mkdir my-fastapi-app
cd my-fastapi-app

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install FastAPI with all optional dependencies
pip install "fastapi[standard]"
```

### What Does `fastapi[standard]` Include?

| Package | Purpose |
|---------|---------|
| `fastapi` | The core framework |
| `uvicorn` | ASGI server to run the app |
| `httpx` | Async HTTP client (for testing) |
| `jinja2` | Template engine (for HTML responses) |
| `python-multipart` | Form data & file upload support |
| `email-validator` | Email field validation in Pydantic |

### Minimal Install

If you want just the essentials:

```bash
pip install fastapi uvicorn
```

---

## What is ASGI?

**ASGI (Asynchronous Server Gateway Interface)** is the async successor to WSGI. It's the interface between your Python app and the web server.

```
Client Request → Uvicorn (ASGI Server) → FastAPI (ASGI Application) → Your Code
                                        ↓
Client Response ← Uvicorn ← FastAPI ← Your Code
```

| Term | What It Is | Example |
|------|-----------|---------|
| **WSGI** | Sync interface (old) | Gunicorn + Flask |
| **ASGI** | Async interface (modern) | Uvicorn + FastAPI |
| **Uvicorn** | ASGI server | Like Gunicorn but for async |

> **Why Uvicorn?** It's built on `uvloop` (a fast event loop) and `httptools` (fast HTTP parser), making it one of the fastest Python web servers.

---

## Project Structure

For a simple project, start with this structure:

```
my-fastapi-app/
├── venv/              ← Virtual environment (don't commit to git)
├── main.py            ← Your FastAPI application
├── requirements.txt   ← Dependencies
└── .gitignore         ← Git ignore file
```

### `requirements.txt`

```
fastapi[standard]>=0.115.0
```

Generate it automatically:
```bash
pip freeze > requirements.txt
```

### `.gitignore`

```
venv/
__pycache__/
*.pyc
.env
```

---

## For Larger Projects (Preview)

As your app grows, you'll organize it like this (covered in Module 08):

```
my-fastapi-app/
├── app/
│   ├── __init__.py
│   ├── main.py          ← FastAPI app instance
│   ├── config.py        ← Settings & configuration
│   ├── models/          ← Database models
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/         ← Pydantic schemas
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/         ← API route handlers
│   │   ├── __init__.py
│   │   └── users.py
│   ├── services/        ← Business logic
│   │   └── user_service.py
│   └── dependencies.py  ← Shared dependencies
├── tests/
│   └── test_users.py
├── requirements.txt
└── .env
```

> Don't worry about this structure now — we'll build up to it gradually!

---

## Verifying Your Installation

Create a simple test file to make sure everything works:

```python
# test_install.py
import fastapi
import uvicorn
import pydantic

print(f"FastAPI version: {fastapi.__version__}")
print(f"Pydantic version: {pydantic.__version__}")
print("✅ All packages installed correctly!")
```

Run it:
```bash
python test_install.py
```

Expected output:
```
FastAPI version: 0.115.x
Pydantic version: 2.x.x
✅ All packages installed correctly!
```

---

## Key Takeaways

1. **Always use a virtual environment** — keeps your project dependencies isolated
2. **`fastapi[standard]` is the recommended install** — includes everything you need
3. **Uvicorn is the ASGI server** — it runs your FastAPI app
4. **Start simple** — begin with a single `main.py`, organize later
5. **Use `requirements.txt`** — track your dependencies for reproducibility

---

> **Next Lesson**: [Hello World API →](../02-hello-world/)
