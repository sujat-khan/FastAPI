# Lesson 05 — Yield Dependencies

## Setup and Teardown Pattern

`yield` dependencies let you run code **before** and **after** the endpoint:

```python
from fastapi import Depends, FastAPI

app = FastAPI()

def get_db():
    db = DatabaseSession()    # SETUP: Create connection
    try:
        yield db              # INJECT: Pass to endpoint
    finally:
        db.close()            # TEARDOWN: Always clean up

@app.get("/items")
async def list_items(db = Depends(get_db)):
    # 'db' is the yielded database session
    return db.query("SELECT * FROM items")
    # After this returns, db.close() runs automatically!
```

### Execution Flow:

```
Request arrives
    ↓
get_db(): db = DatabaseSession()     ← SETUP
    ↓
yield db                              ← INJECT into endpoint
    ↓
list_items(db) runs                   ← ENDPOINT
    ↓
db.close()                            ← TEARDOWN (always runs!)
    ↓
Response sent
```

---

## Real-World: Database Session Management

This is the most common use case (covered in depth in Module 06):

```python
from sqlalchemy.orm import Session

def get_db():
    """Provide a database session, auto-close after request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    # Session is automatically closed after response!
```

---

## Async Yield Dependencies

```python
async def get_async_db():
    db = await AsyncDatabaseSession.create()
    try:
        yield db
    finally:
        await db.close()
```

---

## Error Handling in Yield Dependencies

The `finally` block ensures cleanup even if the endpoint raises an exception:

```python
def get_db():
    db = DatabaseSession()
    try:
        yield db
    except Exception:
        db.rollback()     # Rollback on error
        raise             # Re-raise the exception
    finally:
        db.close()        # Always close
```

---

## Key Takeaways

1. **`yield` = setup + teardown** — code before yield runs first, after yield runs last
2. **`finally` ensures cleanup** — even if the endpoint raises an error
3. **Most common for DB sessions** — open before, close after
4. **Works with async** — use `async def` and `await` for async resources
5. **Exception handling works** — catch errors, rollback, then re-raise

---

> **Next Module**: [Module 06 — Database Integration →](../../module-06-database/)
