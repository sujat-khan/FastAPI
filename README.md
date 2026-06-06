# 🚀 FastAPI — Complete Python Course (Beginner to Master)

Welcome to the **FastAPI Complete Course**! This hands-on course takes you from zero to building production-ready APIs with FastAPI, Python's modern, high-performance web framework.

---

## 📋 Prerequisites

- **Python 3.10+** installed
- Basic Python knowledge (variables, functions, classes, lists, dictionaries)
- A code editor (VS Code recommended)
- Familiarity with the terminal/command line

---

## 🗂️ Course Modules

| # | Module | Description | Status |
|---|--------|-------------|--------|
| 01 | [Python & Web Fundamentals](./module-01-fundamentals/) | HTTP, REST, async/await, type hints | 📖 |
| 02 | [Getting Started with FastAPI](./module-02-getting-started/) | Installation, first app, Swagger docs | 📖 |
| 03 | [Request Handling](./module-03-request-handling/) | Path params, query params, body, files | 📖 |
| 04 | [Response & Validation](./module-04-response-validation/) | Pydantic, status codes, error handling | 📖 |
| 05 | [Dependency Injection](./module-05-dependency-injection/) | DI system, `Depends()`, yield deps | 📖 |
| 06 | [Database Integration](./module-06-database/) | SQLAlchemy, CRUD, Alembic, SQLModel | 📖 |
| 07 | [Authentication & Security](./module-07-authentication/) | JWT, OAuth2, password hashing | 📖 |
| 08 | [Advanced Features](./module-08-advanced-features/) | Middleware, WebSockets, routers, lifespan | 📖 |
| 09 | [Testing & Debugging](./module-09-testing/) | TestClient, async tests, mocking | 📖 |
| 10 | [Production & Deployment](./module-10-production/) | Docker, performance, deployment | 📖 |

---

## 🛠️ How to Use This Course

### 1. Read the Notes
Each lesson has a `README.md` with detailed explanations, theory, and diagrams.

### 2. Run the Code
```bash
# Navigate to any lesson folder
cd module-02-getting-started/02-hello-world

# Install dependencies (if requirements.txt exists)
pip install -r requirements.txt

# Run the example
uvicorn main:app --reload
```

### 3. Experiment
Each lesson includes practice exercises. Modify the code, break things, and learn!

### 4. Check the Docs
FastAPI auto-generates interactive API docs:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 📦 Quick Setup

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install FastAPI + Uvicorn
pip install fastapi uvicorn[standard]
```

---

## 🎯 What You'll Build

By the end of this course, you'll have built:
- ✅ RESTful CRUD APIs
- ✅ Authenticated APIs with JWT tokens
- ✅ Database-backed applications with SQLAlchemy
- ✅ Real-time WebSocket applications
- ✅ Fully tested, production-ready FastAPI applications
- ✅ Dockerized deployments

---

## 📚 Resources

- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- [Uvicorn Docs](https://www.uvicorn.org/)

---

> **Tip**: Start with Module 01 if you're new to web APIs, or jump to Module 02 if you already know HTTP/REST basics.

Happy coding! 🐍⚡
