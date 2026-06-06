# Lesson 03 — CRUD Operations

## Complete CRUD with SQLAlchemy + FastAPI

This lesson builds a complete, working CRUD API.

---

## Project Structure

```
crud-example/
├── main.py           ← FastAPI app
├── database.py       ← DB connection
├── models.py         ← SQLAlchemy models
├── schemas.py        ← Pydantic schemas
├── crud.py           ← Database operations
└── requirements.txt
```

---

## The CRUD Service Layer

Separate database operations into a `crud.py` file for clean code:

```python
# crud.py
from sqlalchemy.orm import Session
import models
import schemas

# CREATE
def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=f"hashed_{user.password}",  # Use real hashing!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# READ (single)
def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()

# READ (by email)
def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()

# READ (list with pagination)
def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

# UPDATE
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> models.User | None:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.commit()
    db.refresh(db_user)
    return db_user

# DELETE
def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True
```

---

## The API Endpoints

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine, Base, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI(title="CRUD Example API")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users", response_model=schemas.UserResponse, status_code=201)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check for duplicate email
    existing = crud.get_user_by_email(db, email=user.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users", response_model=list[schemas.UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db, skip=skip, limit=limit)

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = crud.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None
```

---

## Common Query Patterns

```python
from sqlalchemy import or_, and_, desc

# Search
def search_users(db: Session, query: str):
    return db.query(models.User).filter(
        or_(
            models.User.name.ilike(f"%{query}%"),
            models.User.email.ilike(f"%{query}%"),
        )
    ).all()

# Filter and sort
def get_active_users(db: Session):
    return db.query(models.User).filter(
        models.User.is_active == True
    ).order_by(desc(models.User.created_at)).all()

# Count
def count_users(db: Session) -> int:
    return db.query(models.User).count()
```

---

## Key Takeaways

1. **Separate CRUD into `crud.py`** — keeps endpoints clean
2. **Always check for duplicates** before creating (email uniqueness)
3. **Use `exclude_unset=True`** for PATCH operations
4. **Return 404 for missing resources** — don't return None
5. **Use `db.refresh()`** after commit to get auto-generated values (id, timestamps)

---

> **Next Lesson**: [Relationships →](../04-relationships/)
