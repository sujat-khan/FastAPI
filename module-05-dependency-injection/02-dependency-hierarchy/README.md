# Lesson 02 — Dependency Hierarchy

## Chained Dependencies

Dependencies can depend on other dependencies, creating a chain:

```python
from fastapi import Depends, Header, HTTPException, FastAPI

app = FastAPI()

# Level 1: Extract token from header
def get_token(authorization: str = Header()):
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid auth scheme")
    return token

# Level 2: Validate token and get user (depends on Level 1)
def get_current_user(token: str = Depends(get_token)):
    if token != "valid-token-123":
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"id": 1, "name": "Alice", "role": "admin"}

# Level 3: Check admin role (depends on Level 2)
def require_admin(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    return user

# Endpoint uses Level 3, which triggers the full chain
@app.get("/admin/dashboard")
async def admin_dashboard(admin: dict = Depends(require_admin)):
    return {"message": f"Welcome, {admin['name']}!"}
```

```
Request arrives
    ↓
get_token(authorization=Header)     ← Level 1
    ↓ returns token
get_current_user(token)             ← Level 2
    ↓ returns user dict
require_admin(user)                 ← Level 3
    ↓ returns admin dict
admin_dashboard(admin)              ← Endpoint
    ↓ returns response
```

---

## Shared Dependencies (Caching)

If the same dependency is used multiple times in one request, FastAPI **caches** the result:

```python
def get_db():
    print("Creating DB connection")  # Only printed ONCE per request
    return FakeDB()

@app.get("/items")
async def list_items(
    db1 = Depends(get_db),
    db2 = Depends(get_db),  # Same instance as db1!
):
    # db1 is db2 → True (same object)
    return {"same_instance": db1 is db2}
```

To disable caching and always create new instances:
```python
@app.get("/items")
async def list_items(
    db = Depends(get_db, use_cache=False),  # Always creates new
):
    return {}
```

---

## Key Takeaways

1. **Dependencies can chain** — each level depends on the previous
2. **Results are cached per-request** — same dependency = same result
3. **Chains stop early on errors** — if any dep raises, the chain stops
4. **Use `use_cache=False`** to disable caching when needed

---

> **Next Lesson**: [Classes as Dependencies →](../03-classes-as-dependencies/)
