# Lesson 04 — Path Operations

## What Are Path Operations?

In FastAPI, a **path operation** is the combination of:
1. An **HTTP method** (GET, POST, PUT, DELETE, PATCH)
2. A **URL path** (`/users`, `/items/{id}`)
3. A **Python function** that handles the request

```python
@app.get("/users")      # ← Path operation decorator (method + path)
async def get_users():   # ← Path operation function
    return [...]
```

The term "operation" comes from the OpenAPI specification. In other frameworks, these are called "routes" or "views".

---

## The Five Main Decorators

### `@app.get()` — Read Data

```python
@app.get("/items")
async def list_items():
    """GET requests retrieve data without modifying it."""
    return [
        {"id": 1, "name": "Laptop", "price": 999.99},
        {"id": 2, "name": "Phone", "price": 699.99},
    ]

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """GET a single item by its ID."""
    return {"id": item_id, "name": "Laptop", "price": 999.99}
```

### `@app.post()` — Create Data

```python
from pydantic import BaseModel

class ItemCreate(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.post("/items", status_code=201)
async def create_item(item: ItemCreate):
    """POST creates a new resource."""
    return {"id": 1, **item.model_dump()}
```

### `@app.put()` — Replace Data (Full Update)

```python
class ItemUpdate(BaseModel):
    name: str
    price: float
    description: str | None = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemUpdate):
    """PUT replaces the entire resource."""
    return {"id": item_id, **item.model_dump()}
```

### `@app.patch()` — Modify Data (Partial Update)

```python
class ItemPatch(BaseModel):
    name: str | None = None
    price: float | None = None
    description: str | None = None

@app.patch("/items/{item_id}")
async def patch_item(item_id: int, item: ItemPatch):
    """PATCH modifies only the provided fields."""
    # Only update fields that were actually sent
    update_data = item.model_dump(exclude_unset=True)
    return {"id": item_id, "updated_fields": update_data}
```

### `@app.delete()` — Remove Data

```python
@app.delete("/items/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """DELETE removes the resource."""
    # 204 No Content — nothing to return
    return None
```

---

## PUT vs PATCH — What's the Difference?

This is a common source of confusion. Here's a clear example:

### Original Resource
```json
{
    "id": 1,
    "name": "Laptop",
    "price": 999.99,
    "description": "A powerful laptop",
    "in_stock": true
}
```

### PUT — Replace Everything
```json
PUT /items/1
{
    "name": "Gaming Laptop",
    "price": 1499.99,
    "description": "A gaming laptop",
    "in_stock": true
}
```
You must send **ALL fields**. Any missing field would be set to null/default.

### PATCH — Update Specific Fields
```json
PATCH /items/1
{
    "price": 1499.99
}
```
Only the `price` field is updated. Everything else stays the same.

| Aspect | PUT | PATCH |
|--------|-----|-------|
| What to send | All fields | Only changed fields |
| Missing fields | Reset to default | Stay unchanged |
| Idempotent | ✅ Yes | ❌ Not guaranteed |
| Use case | Full replacement | Partial update |

---

## Path Operation Order Matters!

FastAPI evaluates paths **in order of definition**. This can cause unexpected behavior:

```python
# ❌ WRONG ORDER — "/users/me" never matches!

@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}

@app.get("/users/me")      # ← This never runs!
async def get_current_user():  # Because "me" is captured as user_id above
    return {"user": "current"}
```

```python
# ✅ CORRECT ORDER — Fixed paths first!

@app.get("/users/me")
async def get_current_user():
    return {"user": "current"}

@app.get("/users/{user_id}")  # ← This only runs if path isn't "me"
async def get_user(user_id: str):
    return {"user_id": user_id}
```

> **Rule**: Define **fixed paths** before **parameterized paths** for the same route prefix.

---

## Decorator Parameters

Path operation decorators accept several useful parameters:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post(
    "/items",
    status_code=201,                    # Default response status code
    tags=["Items"],                      # Group in docs
    summary="Create a new item",         # Short summary in docs
    description="Create a new item with a name and price.",  # Override docstring
    response_description="The created item",  # Describe the response
    response_model=Item,                 # Response schema (covered in Module 04)
    deprecated=False,                    # Mark as deprecated
)
async def create_item(item: Item):
    return item
```

### All Decorator Parameters:

| Parameter | Type | Purpose |
|-----------|------|---------|
| `status_code` | int | Default HTTP status code for response |
| `tags` | list[str] | Grouping in documentation |
| `summary` | str | Short description in docs |
| `description` | str | Detailed description (overrides docstring) |
| `response_description` | str | Description of the response |
| `response_model` | type | Pydantic model for response validation |
| `deprecated` | bool | Mark endpoint as deprecated |
| `include_in_schema` | bool | Include in OpenAPI schema |
| `responses` | dict | Additional response schemas |

---

## Multiple Methods for Same Path

You can define different methods for the same path:

```python
# All of these are different path operations sharing the "/items" path

@app.get("/items")
async def list_items():
    """List all items."""
    return [{"id": 1, "name": "Widget"}]

@app.post("/items")
async def create_item(item: Item):
    """Create a new item."""
    return {"id": 1, **item.model_dump()}
```

```python
# Same for /items/{item_id}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"id": item_id}

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"id": item_id, **item.model_dump()}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return None
```

---

## Key Takeaways

1. **Each HTTP method has its own decorator** — `@app.get()`, `@app.post()`, etc.
2. **Path operations = method + path + function** — the three parts of an endpoint
3. **Use the right method** — GET for reading, POST for creating, PUT for replacing, PATCH for updating, DELETE for removing
4. **Order matters** — fixed paths before parameterized paths
5. **PUT replaces, PATCH modifies** — understand the difference
6. **Decorators have many options** — status codes, tags, summaries, etc.

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Using GET for creation | Violates HTTP semantics | Use POST |
| Wrong path order | Fixed paths shadow dynamic ones | Put fixed paths first |
| Not setting status_code for POST | Returns 200 instead of 201 | Add `status_code=201` |
| Using PUT when you mean PATCH | Requires all fields | Use PATCH for partial updates |

---

## Practice Exercises

1. Create a complete CRUD API for a "Book" resource with GET (all), GET (one), POST, PUT, PATCH, and DELETE endpoints.
2. Add a fixed path `/books/bestsellers` before `/books/{book_id}` and verify it works.
3. Add proper tags and summaries to all endpoints.

---

> **Next Module**: [Module 03 — Request Handling →](../../module-03-request-handling/)
