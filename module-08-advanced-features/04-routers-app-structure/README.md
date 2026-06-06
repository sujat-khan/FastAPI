# Lesson 04 — Routers & Application Structure

## Why Routers?

As your app grows, putting everything in one file becomes unmanageable. `APIRouter` lets you split your app into modules.

---

## Basic Router Usage

```python
# routers/users.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def list_users():
    return [{"id": 1, "name": "Alice"}]

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"id": user_id, "name": "Alice"}

@router.post("/", status_code=201)
async def create_user():
    return {"id": 1, "name": "Alice"}
```

```python
# main.py
from fastapi import FastAPI
from routers import users, items

app = FastAPI(title="My API")

# Include routers
app.include_router(users.router)
app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Welcome!"}
```

---

## Recommended Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              ← FastAPI app, include routers
│   ├── config.py             ← Settings (env vars, constants)
│   ├── database.py           ← DB engine, session, Base
│   ├── dependencies.py       ← Shared dependencies
│   │
│   ├── models/               ← SQLAlchemy models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   │
│   ├── schemas/              ← Pydantic schemas
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   │
│   ├── routers/              ← API route handlers
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   │
│   ├── services/             ← Business logic / CRUD
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── item_service.py
│   │
│   └── utils/                ← Utilities
│       ├── __init__.py
│       └── security.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   └── test_items.py
│
├── alembic/                  ← Migrations
├── requirements.txt
├── .env
└── .gitignore
```

---

## Router Configuration Options

```python
router = APIRouter(
    prefix="/api/v1/users",          # URL prefix for all routes
    tags=["Users"],                   # Tag for documentation grouping
    dependencies=[Depends(verify_token)],  # Auth for all routes
    responses={                       # Default responses
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
    },
)
```

---

## Including Router with Override

```python
# Override prefix and tags when including
app.include_router(
    users.router,
    prefix="/api/v2/users",    # Override the router's prefix
    tags=["Users V2"],         # Override tags
)
```

---

## Key Takeaways

1. **`APIRouter` splits your app** into focused modules
2. **`prefix` adds URL prefix** to all routes in the router
3. **`tags` groups in docs** — keeps Swagger UI organized
4. **Follow the standard structure** — models, schemas, routers, services
5. **`include_router()`** assembles all pieces in main.py

---

> **Next Lesson**: [Lifespan Events →](../05-lifespan-events/)
