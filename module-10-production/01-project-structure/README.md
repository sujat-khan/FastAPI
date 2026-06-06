# Lesson 01 — Project Structure Best Practices

## Production-Ready Project Structure

```
my-fastapi-app/
│
├── app/                          ← Application package
│   ├── __init__.py
│   ├── main.py                   ← App entry point
│   ├── config.py                 ← Settings management
│   │
│   ├── api/                      ← API layer
│   │   ├── __init__.py
│   │   ├── deps.py               ← Shared dependencies
│   │   └── v1/                   ← API version 1
│   │       ├── __init__.py
│   │       ├── router.py         ← Assembles all v1 routes
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── users.py
│   │           ├── items.py
│   │           └── auth.py
│   │
│   ├── core/                     ← Core utilities
│   │   ├── __init__.py
│   │   ├── security.py           ← JWT, password hashing
│   │   └── exceptions.py         ← Custom exceptions
│   │
│   ├── db/                       ← Database layer
│   │   ├── __init__.py
│   │   ├── session.py            ← Engine, session factory
│   │   └── base.py               ← Import all models here
│   │
│   ├── models/                   ← SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   │
│   ├── schemas/                  ← Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   │
│   └── services/                 ← Business logic
│       ├── __init__.py
│       ├── user_service.py
│       └── item_service.py
│
├── tests/                        ← Test suite
│   ├── __init__.py
│   ├── conftest.py               ← Shared fixtures
│   ├── test_users.py
│   └── test_items.py
│
├── alembic/                      ← Database migrations
│   ├── versions/
│   └── env.py
│
├── .env                          ← Environment variables (NOT committed)
├── .env.example                  ← Example env file (committed)
├── .gitignore
├── alembic.ini
├── Dockerfile
├── docker-compose.yml
├── requirements.txt              ← Production dependencies
├── requirements-dev.txt          ← Dev dependencies (pytest, etc.)
├── pyproject.toml                ← Project metadata
└── README.md
```

---

## Configuration Management

Use Pydantic's `BaseSettings` to manage environment variables:

```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App
    app_name: str = "My FastAPI App"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # Database
    database_url: str = "sqlite:///./app.db"

    # Auth
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # CORS
    allowed_origins: list[str] = ["http://localhost:3000"]

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }

@lru_cache
def get_settings() -> Settings:
    """Cache settings to avoid reading .env on every request."""
    return Settings()
```

### `.env` File:
```env
APP_NAME=My Production API
DEBUG=false
DATABASE_URL=postgresql://user:pass@db:5432/myapp
SECRET_KEY=super-secret-production-key-change-this
ALLOWED_ORIGINS=["https://myapp.com","https://www.myapp.com"]
```

### Using Settings:
```python
from app.config import get_settings

settings = get_settings()
print(settings.database_url)
print(settings.secret_key)
```

---

## Key Principles

| Principle | Description |
|-----------|-------------|
| **Separation of Concerns** | Each file/folder has one responsibility |
| **12-Factor App** | Config in env vars, not code |
| **Dependency Injection** | Makes testing easy |
| **Layered Architecture** | API → Service → Model → DB |
| **Version Your API** | `/api/v1/`, `/api/v2/` |

---

> **Next Lesson**: [Dockerizing FastAPI →](../02-dockerizing-fastapi/)
