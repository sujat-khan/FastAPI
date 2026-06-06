# Lesson 01 — Response Models

## Why Response Models?

Response models let you:
1. **Filter output** — hide sensitive fields like passwords
2. **Validate responses** — ensure your API returns correct data
3. **Document responses** — auto-generate response schemas in docs
4. **Transform data** — convert database models to API-friendly format

---

## Basic `response_model`

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str
    password: str     # Sensitive!

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    # No password field — it's filtered out!

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    """
    Even though we return a dict with 'password',
    FastAPI filters it out based on UserResponse.
    """
    return {
        "id": 1,
        "name": user.name,
        "email": user.email,
        "password": user.password,  # ← This won't appear in response!
    }
```

Response:
```json
{
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com"
}
```
Note: `password` is **not** in the response even though we returned it!

---

## Separate Input and Output Models

A common pattern is having different models for different operations:

```python
class UserBase(BaseModel):
    """Shared fields."""
    name: str
    email: str

class UserCreate(UserBase):
    """For creating — includes password."""
    password: str

class UserUpdate(UserBase):
    """For updating — all fields optional."""
    name: str | None = None
    email: str | None = None

class UserResponse(UserBase):
    """For responses — includes id, excludes password."""
    id: int
    is_active: bool
    created_at: str

class UserListResponse(BaseModel):
    """For list responses — includes pagination."""
    users: list[UserResponse]
    total: int
    page: int
    per_page: int
```

---

## `response_model_exclude_unset`

Only include fields that were explicitly set (useful for PATCH responses):

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 10.5

@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def get_item(item_id: int):
    return {"name": "Laptop", "price": 999.99}
    # Response: {"name": "Laptop", "price": 999.99}
    # description and tax are excluded because they weren't set
```

---

## `response_model_include` and `response_model_exclude`

Explicitly include or exclude fields:

```python
class User(BaseModel):
    id: int
    name: str
    email: str
    password_hash: str
    internal_notes: str

# Only include specific fields
@app.get("/users/{user_id}", response_model=User, response_model_include={"id", "name", "email"})
async def get_user(user_id: int):
    return {...}

# Exclude specific fields
@app.get("/users/{user_id}/public", response_model=User, response_model_exclude={"password_hash", "internal_notes"})
async def get_user_public(user_id: int):
    return {...}
```

> **Best Practice**: Prefer separate models over include/exclude. It's clearer and less error-prone.

---

## Return Type Annotations (FastAPI 0.100+)

Modern FastAPI supports return type annotations as an alternative to `response_model`:

```python
@app.get("/users/{user_id}")
async def get_user(user_id: int) -> UserResponse:
    """Return type annotation serves as response_model."""
    return UserResponse(id=user_id, name="Alice", email="alice@test.com", is_active=True, created_at="2025-01-01")

@app.get("/users")
async def list_users() -> list[UserResponse]:
    """Return type can be a list too."""
    return [...]
```

### `response_model` vs Return Type

| Feature | `response_model=` | Return type `->` |
|---------|-------------------|------------------|
| Filtering | ✅ Filters extra fields | ✅ Filters extra fields |
| Validation | ✅ Yes | ✅ Yes |
| Documentation | ✅ Yes | ✅ Yes |
| Override | Higher priority | Lower priority |
| Flexibility | Can differ from return | Must match return |

---

## Key Takeaways

1. **Response models filter sensitive data** — passwords, internal fields
2. **Use separate models** for create/update/response — cleaner design
3. **Return type annotations work too** — modern alternative to `response_model`
4. **`exclude_unset` is useful for PATCH** — only show changed fields
5. **Model inheritance reduces duplication** — share common fields via base models

---

> **Next Lesson**: [Status Codes →](../02-status-codes/)
