# Lesson 04 — API Versioning

## Why Version Your API?

When you need to make **breaking changes**, versioning lets you:
- Keep old clients working on v1
- Roll out new features on v2
- Gradually migrate users

---

## URL Path Versioning (Recommended)

The simplest and most common approach:

```python
from fastapi import APIRouter, FastAPI

app = FastAPI()

# V1 Router
v1_router = APIRouter(prefix="/api/v1")

@v1_router.get("/users")
async def get_users_v1():
    return [{"id": 1, "name": "Alice"}]  # Simple response

# V2 Router (enhanced)
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/users")
async def get_users_v2():
    return {
        "data": [{"id": 1, "name": "Alice", "email": "alice@test.com"}],
        "total": 1,
        "page": 1,
    }  # Richer response with pagination

app.include_router(v1_router, tags=["V1"])
app.include_router(v2_router, tags=["V2"])
```

```
GET /api/v1/users → Simple list
GET /api/v2/users → Paginated response with more fields
```

---

## Header Versioning

```python
from fastapi import Header

@app.get("/users")
async def get_users(api_version: str = Header(default="1", alias="X-API-Version")):
    if api_version == "2":
        return {"data": [...], "total": 1}
    return [...]  # Default v1 response
```

---

## Deprecation Strategy

```python
import warnings
from datetime import date

# Deprecation warning in v1
@v1_router.get("/users", deprecated=True)
async def get_users_v1():
    """
    ⚠️ **Deprecated** — will be removed on 2025-06-01.

    Use `GET /api/v2/users` instead.
    """
    return [{"id": 1, "name": "Alice"}]
```

---

## Versioning Best Practices

| Practice | Description |
|----------|-------------|
| Start with v1 | Even if you don't plan v2 yet |
| Keep v1 working | Don't break existing clients |
| Set deprecation dates | Give clients time to migrate |
| Document changes | Changelog between versions |
| Only version on breaking changes | Don't version for additions |

---

> **Next Lesson**: [Deployment Options →](../05-deployment-options/)
