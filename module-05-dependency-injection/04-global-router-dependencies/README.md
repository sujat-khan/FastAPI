# Lesson 04 — Global & Router Dependencies

## Apply Dependencies to All Routes

Instead of adding dependencies to each endpoint individually, apply them globally.

### App-Level Dependencies
```python
from fastapi import Depends, FastAPI, Header, HTTPException

async def verify_api_key(x_api_key: str = Header()):
    if x_api_key != "my-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")

# Every endpoint in this app requires an API key
app = FastAPI(dependencies=[Depends(verify_api_key)])

@app.get("/items")
async def list_items():
    return [{"id": 1}]  # API key already verified!

@app.get("/users")
async def list_users():
    return [{"id": 1}]  # API key already verified!
```

### Router-Level Dependencies
```python
from fastapi import APIRouter, Depends

# All routes in this router require admin access
admin_router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
    dependencies=[Depends(require_admin)],
)

@admin_router.get("/users")
async def admin_list_users():
    return {"users": [...]}

@admin_router.delete("/users/{user_id}")
async def admin_delete_user(user_id: int):
    return {"deleted": user_id}

app.include_router(admin_router)
```

---

## Overriding Dependencies (For Testing)

```python
# Original dependency
def get_db():
    return RealDatabase()

# Override for testing
def get_test_db():
    return FakeDatabase()

app.dependency_overrides[get_db] = get_test_db

# Now all endpoints using Depends(get_db) get FakeDatabase instead!
```

This is incredibly powerful for testing (covered in Module 09).

---

## Key Takeaways

1. **App-level deps** apply to every endpoint — great for API keys, logging
2. **Router-level deps** apply to a group — great for role-based access
3. **`dependency_overrides`** lets you swap deps for testing
4. **Use `dependencies=[]`** when you don't need the return value

---

> **Next Lesson**: [Yield Dependencies →](../05-yield-dependencies/)
