# Lesson 06 — Async Database with SQLModel

## What is SQLModel?

**SQLModel** is a library by the creator of FastAPI (Sebastián Ramírez) that combines **SQLAlchemy** and **Pydantic** into a single model:

```
Traditional:  SQLAlchemy Model + Pydantic Schema = 2 classes
SQLModel:     SQLModel class = 1 class (both ORM + validation!)
```

---

## Installation

```bash
pip install sqlmodel aiosqlite  # aiosqlite for async SQLite
```

---

## Defining Models

```python
from sqlmodel import SQLModel, Field
from datetime import datetime

class UserBase(SQLModel):
    """Shared fields — NOT a table."""
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(unique=True, index=True)

class User(UserBase, table=True):
    """Database table model."""
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(UserBase):
    """Input schema — has password."""
    password: str = Field(min_length=8)

class UserResponse(UserBase):
    """Output schema — has id, no password."""
    id: int
    is_active: bool
```

Note: Only classes with `table=True` become database tables. Others are just Pydantic models!

---

## Async Setup

```python
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./app.db"

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session
```

---

## Async CRUD Operations

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=f"hashed_{user.password}",
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@app.get("/users", response_model=list[UserResponse])
async def list_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

---

## SQLModel vs Traditional SQLAlchemy

| Feature | SQLAlchemy + Pydantic | SQLModel |
|---------|----------------------|---------|
| Number of classes | 2 per entity | 1 per entity |
| Validation | Pydantic only | Built-in |
| ORM features | Full | Full (via SQLAlchemy) |
| Async support | Yes (with setup) | Yes (with setup) |
| Creator | Different teams | Same as FastAPI |
| Maturity | Very mature | Newer but growing |

---

## Key Takeaways

1. **SQLModel = SQLAlchemy + Pydantic in one** — less boilerplate
2. **`table=True`** makes a class a database table
3. **Async requires `aiosqlite`** (or `asyncpg` for PostgreSQL)
4. **Use `select()` with `session.execute()`** for async queries
5. **Great for new projects** — simpler mental model

---

> **Next Module**: [Module 07 — Authentication & Security →](../../module-07-authentication/)
