# Lesson 01 — Path Parameters

## What Are Path Parameters?

Path parameters are **dynamic parts of the URL path** that capture values from the URL. They're enclosed in curly braces `{}` in the path template.

```
GET /users/42         ← 42 is the path parameter value
GET /users/{user_id}  ← user_id is the path parameter name
```

---

## Basic Path Parameters

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """FastAPI extracts 'user_id' from the URL and converts it to int."""
    return {"user_id": user_id}

# GET /users/42     → {"user_id": 42}
# GET /users/abc    → 422 Validation Error (not an int!)
```

### How It Works:

1. FastAPI sees `{user_id}` in the path template
2. It finds a function parameter with the same name: `user_id`
3. It reads the type hint: `int`
4. It extracts the value from the URL and **validates/converts** it to `int`
5. If conversion fails → automatic `422 Unprocessable Entity` error

---

## Type Validation

FastAPI automatically validates path parameters based on type hints:

```python
# Integer parameter
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {"item_id": item_id}
# /items/5     → ✅ {"item_id": 5}
# /items/abc   → ❌ 422 error

# Float parameter
@app.get("/prices/{amount}")
async def get_price(amount: float):
    return {"amount": amount}
# /prices/19.99  → ✅ {"amount": 19.99}
# /prices/abc    → ❌ 422 error

# String parameter (default, accepts anything)
@app.get("/greet/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}
# /greet/alice  → ✅ {"message": "Hello, alice!"}
# /greet/123    → ✅ {"message": "Hello, 123!"}  (123 as string)

# Boolean parameter
@app.get("/feature/{enabled}")
async def feature(enabled: bool):
    return {"enabled": enabled}
# /feature/true   → ✅ {"enabled": true}
# /feature/1      → ✅ {"enabled": true}
# /feature/yes    → ✅ {"enabled": true}
# /feature/false  → ✅ {"enabled": false}
# /feature/0      → ✅ {"enabled": false}
```

---

## Multiple Path Parameters

```python
@app.get("/users/{user_id}/posts/{post_id}")
async def get_user_post(user_id: int, post_id: int):
    return {
        "user_id": user_id,
        "post_id": post_id
    }
# GET /users/42/posts/7 → {"user_id": 42, "post_id": 7}
```

---

## Predefined Values with Enum

Use Python's `Enum` to restrict path parameters to specific values:

```python
from enum import Enum
from fastapi import FastAPI

app = FastAPI()

class ModelName(str, Enum):
    """Allowed ML model names."""
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """Only accepts: alexnet, resnet, or lenet."""

    if model_name is ModelName.alexnet:
        return {"model": model_name.value, "message": "Deep Learning FTW!"}

    if model_name is ModelName.resnet:
        return {"model": model_name.value, "message": "Residual Networks"}

    return {"model": model_name.value, "message": "Classic architecture"}

# GET /models/alexnet  → ✅ {"model": "alexnet", "message": "Deep Learning FTW!"}
# GET /models/vgg      → ❌ 422 error — not a valid option
```

In Swagger UI, the enum values appear as a **dropdown**, making it clear which values are valid.

---

## The `Path()` Function — Advanced Validation

`Path()` gives you more control over path parameters:

```python
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(
        title="Item ID",
        description="The unique identifier of the item to retrieve",
        ge=1,           # Greater than or equal to 1
        le=10000,       # Less than or equal to 10000
        examples=[42],
    )
):
    return {"item_id": item_id}

# GET /items/42     → ✅ {"item_id": 42}
# GET /items/0      → ❌ 422 error (must be >= 1)
# GET /items/99999  → ❌ 422 error (must be <= 10000)
```

### Available `Path()` Constraints:

| Parameter | Type | Purpose |
|-----------|------|---------|
| `title` | str | Title in docs |
| `description` | str | Description in docs |
| `ge` | number | Greater than or equal to |
| `gt` | number | Greater than |
| `le` | number | Less than or equal to |
| `lt` | number | Less than |
| `examples` | list | Example values for docs |
| `deprecated` | bool | Mark as deprecated |
| `alias` | str | Alternative parameter name |

---

## Path Parameters with File Paths

If you need to capture a **file path** in the URL (containing `/`), use `:path`:

```python
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """Captures everything after /files/ including slashes."""
    return {"file_path": file_path}

# GET /files/documents/report.pdf
# → {"file_path": "documents/report.pdf"}

# GET /files/images/2025/photo.jpg
# → {"file_path": "images/2025/photo.jpg"}
```

---

## Path Parameter Order — Important!

Remember from Module 02: **Fixed paths must come before parameterized paths!**

```python
# ✅ CORRECT ORDER
@app.get("/users/me")
async def get_current_user():
    return {"user": "current_user"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# ❌ WRONG ORDER — /users/me would try to convert "me" to int → 422 error
```

---

## Combining Path and Query Parameters

Path and query parameters can be used together:

```python
@app.get("/users/{user_id}/posts")
async def get_user_posts(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
):
    """
    Path parameter: user_id (from URL)
    Query parameters: skip, limit (from ?skip=0&limit=10)
    """
    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit,
    }

# GET /users/42/posts?skip=5&limit=20
# → {"user_id": 42, "skip": 5, "limit": 20}
```

FastAPI knows the difference:
- **In the path template** (`{user_id}`) → path parameter
- **Not in the path template** (`skip`, `limit`) → query parameter

---

## Key Takeaways

1. **Path parameters capture URL segments** — defined with `{param_name}` in the path
2. **Type hints validate automatically** — wrong types get a `422` error
3. **Use Enums for restricted values** — shows dropdown in docs
4. **`Path()` adds validation** — min/max, descriptions, examples
5. **Order matters** — fixed paths before parameterized paths
6. **`:path` suffix captures slashes** — for file path parameters

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| No type hint on path param | No validation | Always add type hints |
| Wrong path order | Fixed paths never match | Define fixed paths first |
| Using `str` when you need `int` | Accepts anything | Use appropriate type |
| Spaces in path parameter names | Invalid | Use underscores: `user_id` |

---

> **Next Lesson**: [Query Parameters →](../02-query-parameters/)
