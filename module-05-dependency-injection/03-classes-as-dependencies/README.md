# Lesson 03 — Classes as Dependencies

## Why Classes?

Classes are useful when your dependency needs:
- Multiple related parameters
- State management
- Methods for different operations

```python
from fastapi import Depends, FastAPI, Query

app = FastAPI()

class Pagination:
    def __init__(
        self,
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=20, ge=1, le=100),
    ):
        self.page = page
        self.per_page = per_page
        self.skip = (page - 1) * per_page

    @property
    def limit(self) -> int:
        return self.per_page

@app.get("/items")
async def list_items(pagination: Pagination = Depends()):
    """
    Note: Depends() with no arguments uses the type hint.
    FastAPI creates Pagination(page=..., per_page=...) automatically.
    """
    return {
        "page": pagination.page,
        "per_page": pagination.per_page,
        "skip": pagination.skip,
        "limit": pagination.limit,
    }
```

### `Depends()` vs `Depends(ClassName)`

```python
# These are equivalent:
async def endpoint(pagination: Pagination = Depends(Pagination)):
    ...

async def endpoint(pagination: Pagination = Depends()):
    ...  # ← Shorthand — uses type hint
```

---

## Parameterized Dependencies

Create dependencies that accept configuration:

```python
class RoleChecker:
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: dict = Depends(get_current_user)):
        if user["role"] not in self.allowed_roles:
            raise HTTPException(status_code=403, detail="Access denied")
        return user

# Create instances for different permission levels
allow_admin = RoleChecker(allowed_roles=["admin"])
allow_editor = RoleChecker(allowed_roles=["admin", "editor"])
allow_any = RoleChecker(allowed_roles=["admin", "editor", "viewer"])

@app.get("/admin", dependencies=[Depends(allow_admin)])
async def admin_only():
    return {"message": "Admin area"}

@app.get("/edit", dependencies=[Depends(allow_editor)])
async def editor_area():
    return {"message": "Editor area"}
```

---

## Key Takeaways

1. **Classes as deps provide structure** — group related params and logic
2. **`Depends()` shorthand** uses the type hint for the class
3. **`__call__` makes instances callable** — enables parameterized deps
4. **Parameterized deps** = create factory instances for different configs

---

> **Next Lesson**: [Global & Router Dependencies →](../04-global-router-dependencies/)
