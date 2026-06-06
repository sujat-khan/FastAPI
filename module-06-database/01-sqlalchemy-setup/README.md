# Lesson 01 — SQLAlchemy Setup

## What is SQLAlchemy?

**SQLAlchemy** is Python's most popular SQL toolkit and ORM (Object-Relational Mapper). It lets you interact with databases using Python classes instead of raw SQL.

```
Python Class (User) ←→ SQLAlchemy ORM ←→ Database Table (users)
```

---

## Installation

```bash
pip install sqlalchemy
# SQLite comes built-in with Python — no extra driver needed!

# For PostgreSQL (optional):
# pip install psycopg2-binary
```

---

## Setting Up the Database Connection

Create a `database.py` file — this is the standard pattern:

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Database URL
# SQLite (file-based):
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

# PostgreSQL (if you prefer):
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

# Create the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Only needed for SQLite
    echo=True,  # Log SQL queries (disable in production)
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
class Base(DeclarativeBase):
    pass
```

### Key Components:

| Component | Purpose |
|-----------|---------|
| `engine` | Manages the database connection pool |
| `SessionLocal` | Factory that creates database sessions |
| `Base` | Parent class for all your ORM models |

### Database URL Formats:

| Database | URL Format |
|----------|-----------|
| SQLite (file) | `sqlite:///./app.db` |
| SQLite (memory) | `sqlite:///:memory:` |
| PostgreSQL | `postgresql://user:pass@host:5432/dbname` |
| MySQL | `mysql://user:pass@host:3306/dbname` |

---

## Creating Database Models

```python
# models.py
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
```

---

## Database Session Dependency

```python
# dependencies.py
from database import SessionLocal

def get_db():
    """Provide a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## Putting It All Together

```python
# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base
from dependencies import get_db
import models

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/users")
def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users
```

---

## Key Takeaways

1. **`database.py`** contains engine, session factory, and Base
2. **Models define table structure** using Python classes
3. **`get_db()` yield dependency** manages session lifecycle
4. **`Base.metadata.create_all()`** creates tables (for development)
5. **SQLite is great for learning** — no setup required

---

> **Next Lesson**: [Models & Schemas →](../02-models-and-schemas/)
