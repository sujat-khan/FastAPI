# Lesson 02 — Query Parameters

## What Are Query Parameters?

Query parameters are **key-value pairs appended to the URL** after the `?` symbol. Multiple parameters are separated by `&`.

```
GET /items?skip=0&limit=10&search=laptop
           └─────────────────────────┘
                Query Parameters
```

In FastAPI, any function parameter that is **NOT in the path template** is automatically treated as a query parameter.

---

## Basic Query Parameters

```python
from fastapi import FastAPI

app = FastAPI()

# Fake database
items_db = [
    {"id": i, "name": f"Item {i}", "price": i * 10.0}
    for i in range(1, 51)
]

@app.get("/items")
async def list_items(skip: int = 0, limit: int = 10):
    """
    'skip' and 'limit' are NOT in the path → query parameters.
    Both have default values → they're optional.
    """
    return items_db[skip : skip + limit]

# GET /items             → First 10 items (defaults: skip=0, limit=10)
# GET /items?skip=20     → Items 21-30 (skip=20, limit=10)
# GET /items?limit=5     → First 5 items (skip=0, limit=5)
# GET /items?skip=10&limit=5 → Items 11-15
```

---

## Required vs Optional Query Parameters

```python
# ❌ REQUIRED — No default value
@app.get("/search")
async def search(q: str):
    """'q' has no default → it's required."""
    return {"query": q}

# GET /search?q=laptop  → ✅ {"query": "laptop"}
# GET /search           → ❌ 422 error — 'q' is required

# ✅ OPTIONAL — Has a default value
@app.get("/search2")
async def search2(q: str = ""):
    """'q' has a default → it's optional."""
    return {"query": q}

# GET /search2?q=laptop → {"query": "laptop"}
# GET /search2           → {"query": ""}

# ✅ OPTIONAL (can be None)
@app.get("/search3")
async def search3(q: str | None = None):
    """'q' defaults to None → optional."""
    if q:
        return {"query": q}
    return {"message": "No search query provided"}

# GET /search3?q=laptop → {"query": "laptop"}
# GET /search3           → {"message": "No search query provided"}
```

### The Rule:

| Definition | Required? | Default |
|-----------|-----------|---------|
| `param: str` | ✅ Required | No default |
| `param: str = "value"` | ❌ Optional | `"value"` |
| `param: str \| None = None` | ❌ Optional | `None` |

---

## Type Conversion

FastAPI automatically converts query parameters to the declared type:

```python
@app.get("/items")
async def filter_items(
    min_price: float = 0,
    max_price: float = 1000,
    in_stock: bool = True,
    category: str | None = None,
):
    return {
        "min_price": min_price,
        "max_price": max_price,
        "in_stock": in_stock,
        "category": category,
    }

# GET /items?min_price=10.5&max_price=100&in_stock=false&category=electronics
# → All values are properly typed!
```

### Boolean Conversion

FastAPI accepts many boolean representations:

```python
# All of these are True:
# ?active=true, ?active=True, ?active=1, ?active=yes, ?active=on

# All of these are False:
# ?active=false, ?active=False, ?active=0, ?active=no, ?active=off
```

---

## The `Query()` Function — Advanced Validation

`Query()` gives you fine-grained control over query parameters:

```python
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items")
async def search_items(
    q: str = Query(
        default=None,
        min_length=3,
        max_length=50,
        pattern="^[a-zA-Z0-9 ]+$",
        title="Search Query",
        description="Search for items by name. Alphanumeric only, 3-50 chars.",
        examples=["laptop", "wireless mouse"],
    ),
    skip: int = Query(default=0, ge=0, description="Number of items to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Max items to return"),
):
    return {"query": q, "skip": skip, "limit": limit}
```

### Available `Query()` Parameters:

| Parameter | Type | Purpose |
|-----------|------|---------|
| `default` | any | Default value |
| `min_length` | int | Min string length |
| `max_length` | int | Max string length |
| `pattern` | str | Regex pattern |
| `ge`, `gt`, `le`, `lt` | number | Numeric constraints |
| `title` | str | Title in docs |
| `description` | str | Description in docs |
| `examples` | list | Example values |
| `deprecated` | bool | Mark as deprecated |
| `alias` | str | Alternative name in URL |
| `include_in_schema` | bool | Show in OpenAPI docs |

---

## Required Query Params with `Query()`

```python
from fastapi import Query

# Using ... (Ellipsis) to mark as required
@app.get("/search")
async def search(
    q: str = Query(
        ...,  # ← Ellipsis means REQUIRED
        min_length=1,
        description="Search query (required)",
    ),
):
    return {"query": q}

# Or simply don't provide a default:
@app.get("/search2")
async def search2(
    q: str = Query(min_length=1),  # No default → required
):
    return {"query": q}
```

---

## List Query Parameters

Accept multiple values for the same parameter:

```python
from fastapi import Query

@app.get("/items")
async def filter_items(
    tags: list[str] = Query(default=[], description="Filter by tags"),
):
    """
    Accept multiple values: ?tags=electronics&tags=sale

    This captures a list of strings from repeated query parameters.
    """
    return {"tags": tags}

# GET /items?tags=electronics&tags=sale
# → {"tags": ["electronics", "sale"]}

# GET /items?tags=books
# → {"tags": ["books"]}

# GET /items
# → {"tags": []}
```

---

## Combining Path and Query Parameters

FastAPI automatically distinguishes between them:

```python
@app.get("/users/{user_id}/items")
async def get_user_items(
    user_id: int,                           # ← Path parameter (in URL template)
    skip: int = 0,                          # ← Query parameter (not in template)
    limit: int = 10,                        # ← Query parameter
    sort_by: str | None = None,             # ← Query parameter
):
    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
    }

# GET /users/42/items?skip=5&limit=20&sort_by=price
```

### How FastAPI Decides:

```
Function parameter name matches {path_param}?
├── YES → It's a Path Parameter
└── NO → It's a Query Parameter
```

---

## Query Parameter Aliases

Use aliases when the URL parameter name differs from the Python variable name:

```python
@app.get("/items")
async def list_items(
    item_query: str | None = Query(
        default=None,
        alias="item-query",  # URL uses 'item-query', code uses 'item_query'
    ),
):
    return {"item_query": item_query}

# GET /items?item-query=laptop
# → {"item_query": "laptop"}
# Note: use 'item-query' in URL, 'item_query' in Python code
```

This is useful because URL conventions often use hyphens, but Python requires underscores.

---

## Real-World Example: Pagination & Filtering

```python
from fastapi import FastAPI, Query
from enum import Enum

app = FastAPI()

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

@app.get("/products")
async def list_products(
    # Pagination
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=20, ge=1, le=100, description="Items per page"),
    # Filtering
    category: str | None = Query(default=None, description="Filter by category"),
    min_price: float = Query(default=0, ge=0, description="Minimum price"),
    max_price: float = Query(default=99999, ge=0, description="Maximum price"),
    in_stock: bool = Query(default=True, description="Only show in-stock items"),
    # Sorting
    sort_by: str = Query(default="name", description="Sort field"),
    order: SortOrder = Query(default=SortOrder.asc, description="Sort order"),
    # Search
    q: str | None = Query(
        default=None,
        min_length=2,
        max_length=100,
        description="Search query",
    ),
):
    """
    List products with pagination, filtering, sorting, and search.

    This is a realistic endpoint showing common query parameter patterns.
    """
    return {
        "pagination": {"page": page, "per_page": per_page},
        "filters": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "in_stock": in_stock,
        },
        "sorting": {"sort_by": sort_by, "order": order.value},
        "search": q,
    }
```

---

## Key Takeaways

1. **Query params are auto-detected** — any param not in the path template is a query param
2. **Defaults make them optional** — no default = required, with default = optional
3. **Type validation is automatic** — wrong types get `422` errors
4. **`Query()` adds validation** — min/max length, regex, numeric constraints
5. **Lists work with repeated params** — `?tag=a&tag=b` → `["a", "b"]`
6. **Use aliases for hyphens** — URL uses `item-query`, code uses `item_query`

---

> **Next Lesson**: [Request Body →](../03-request-body/)
