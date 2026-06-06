# Lesson 01 — What Are Dependencies

## The Problem Dependencies Solve

Without DI, you repeat common logic everywhere:

```python
# ❌ WITHOUT DEPENDENCY INJECTION — repetition everywhere
@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    if limit > 100: limit = 100  # Same validation repeated
    return items_db[skip : skip + limit]

@app.get("/users")
async def list_users(skip: int = 0, limit: int = 10):
    if limit > 100: limit = 100  # Same validation repeated!
    return users_db[skip : skip + limit]
```

With DI, you extract common logic into a reusable function:

```python
# ✅ WITH DEPENDENCY INJECTION — DRY code
from fastapi import Depends

def common_pagination(skip: int = 0, limit: int = 10):
    if limit > 100:
        limit = 100
    return {"skip": skip, "limit": limit}

@app.get("/items")
async def list_items(pagination: dict = Depends(common_pagination)):
    return items_db[pagination["skip"] : pagination["skip"] + pagination["limit"]]

@app.get("/users")
async def list_users(pagination: dict = Depends(common_pagination)):
    return users_db[pagination["skip"] : pagination["skip"] + pagination["limit"]]
```

---

## How `Depends()` Works

```python
from fastapi import Depends, FastAPI

app = FastAPI()

# 1. Define a dependency function
def get_db():
    """This function IS the dependency."""
    db = FakeDatabase()
    return db

# 2. Use it with Depends()
@app.get("/items")
async def list_items(db = Depends(get_db)):
    """FastAPI calls get_db() and injects the result as 'db'."""
    return db.get_all_items()
```

### What happens under the hood:

```
Client sends GET /items
    ↓
FastAPI sees Depends(get_db)
    ↓
FastAPI calls get_db()
    ↓
Result is passed to list_items(db=result)
    ↓
list_items() runs and returns response
```

---

## Dependencies Can Have Their Own Parameters

Dependencies are regular functions — they can have parameters too:

```python
from fastapi import Depends, Header, HTTPException

async def verify_api_key(x_api_key: str = Header()):
    """A dependency that reads a header and validates it."""
    if x_api_key != "secret-api-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return x_api_key

@app.get("/protected")
async def protected_route(api_key: str = Depends(verify_api_key)):
    """This endpoint requires a valid API key."""
    return {"message": "Access granted", "key": api_key}
```

---

## Async Dependencies

Dependencies can be `async` or sync — FastAPI handles both:

```python
# Sync dependency
def get_settings():
    return {"app_name": "My API", "debug": True}

# Async dependency
async def get_current_user():
    # Could be an async database call
    return {"id": 1, "name": "Alice"}

@app.get("/dashboard")
async def dashboard(
    settings = Depends(get_settings),
    user = Depends(get_current_user),
):
    return {"settings": settings, "user": user}
```

---

## Multiple Dependencies

An endpoint can have any number of dependencies:

```python
def verify_token(token: str = Header()):
    if token != "valid-token":
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

def get_current_user(token: str = Depends(verify_token)):
    return {"id": 1, "name": "Alice", "token": token}

def check_permissions(user: dict = Depends(get_current_user)):
    if user["name"] != "Alice":
        raise HTTPException(status_code=403, detail="Not authorized")
    return user

@app.get("/admin")
async def admin_panel(user: dict = Depends(check_permissions)):
    return {"message": f"Welcome admin {user['name']}!"}
```

---

## Key Takeaways

1. **Dependencies = reusable logic** — extract common patterns into functions
2. **`Depends()` injects function results** — FastAPI calls the function for you
3. **Dependencies can raise exceptions** — for validation, auth, etc.
4. **Dependencies can depend on other dependencies** — creating chains
5. **Both sync and async work** — FastAPI handles both

---

> **Next Lesson**: [Dependency Hierarchy →](../02-dependency-hierarchy/)
