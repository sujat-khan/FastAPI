# Lesson 02 — Models & Schemas

## ORM Models vs Pydantic Schemas

This is a critical distinction in FastAPI applications:

| | SQLAlchemy Model | Pydantic Schema |
|--|-----------------|-----------------|
| **Purpose** | Database table structure | API data validation |
| **Lives in** | `models.py` | `schemas.py` |
| **Inherits from** | `Base` (DeclarativeBase) | `BaseModel` |
| **Talks to** | Database | API clients |
| **Validates** | DB constraints | Request/response data |

```
Client → Pydantic Schema (validates) → SQLAlchemy Model (stores) → Database
Client ← Pydantic Schema (formats)  ← SQLAlchemy Model (reads)  ← Database
```

---

## Side-by-Side Comparison

### SQLAlchemy Model (Database)
```python
# models.py — HOW data is stored
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
```

### Pydantic Schemas (API)
```python
# schemas.py — HOW data flows in/out of the API
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    """Shared fields."""
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

class UserCreate(UserBase):
    """Client sends this to create a user."""
    password: str = Field(min_length=8)

class UserResponse(UserBase):
    """API sends this back to the client."""
    id: int
    is_active: bool

    model_config = {"from_attributes": True}

class UserUpdate(BaseModel):
    """Client sends this for partial updates."""
    name: str | None = None
    email: EmailStr | None = None
```

### `from_attributes = True`

This is essential! It tells Pydantic to read data from ORM objects:

```python
# Without from_attributes:
user_orm = db.query(User).first()
UserResponse.model_validate(user_orm)  # ❌ Error!

# With from_attributes:
class UserResponse(BaseModel):
    model_config = {"from_attributes": True}

UserResponse.model_validate(user_orm)  # ✅ Works!
```

---

## The Complete Flow

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

@app.post("/users", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 1. Pydantic validates the input (UserCreate)
    # 2. Create ORM model from validated data
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    # 3. Save to database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # 4. Pydantic formats the response (UserResponse)
    #    password is NOT in response because UserResponse doesn't have it!
    return db_user
```

---

## Key Takeaways

1. **Models = database**, **Schemas = API** — keep them separate
2. **Multiple schemas per model** — Create, Update, Response, List
3. **`from_attributes = True`** — required to convert ORM → Pydantic
4. **Schemas filter sensitive data** — passwords never in responses
5. **BaseModel inheritance** — share common fields, reduce duplication

---

> **Next Lesson**: [CRUD Operations →](../03-crud-operations/)
