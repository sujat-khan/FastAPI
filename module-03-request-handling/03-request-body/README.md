# Lesson 03 — Request Body

## What Is a Request Body?

A **request body** is data sent by the client to your API in the body of the HTTP request. It's typically used with `POST`, `PUT`, and `PATCH` methods to send structured data (usually JSON).

```
POST /users HTTP/1.1
Content-Type: application/json

{                          ← This is the request body
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30
}
```

In FastAPI, you define request bodies using **Pydantic models**.

---

## Basic Request Body

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items")
async def create_item(item: Item):
    """
    FastAPI sees 'item: Item' and knows to:
    1. Read the request body as JSON
    2. Validate it against the Item model
    3. Convert it to an Item instance
    4. Pass it to this function
    """
    item_dict = item.model_dump()
    if item.tax:
        item_dict["price_with_tax"] = item.price + item.tax
    return item_dict
```

### How FastAPI Detects Body vs Query Parameters:

| Parameter Type | How FastAPI Detects It |
|---------------|----------------------|
| Path parameter | Name matches `{param}` in path template |
| Query parameter | Simple type (str, int, float, bool) NOT in path |
| Request body | Pydantic model type |

---

## Body + Path + Query Parameters Together

```python
class Item(BaseModel):
    name: str
    price: float

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,             # ← Path parameter (in URL template)
    item: Item,               # ← Request body (Pydantic model)
    q: str | None = None,     # ← Query parameter (simple type, not in path)
):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result["query"] = q
    return result

# PUT /items/42?q=urgent
# Body: {"name": "Widget", "price": 9.99}
# → {"item_id": 42, "name": "Widget", "price": 9.99, "query": "urgent"}
```

---

## Nested Models

Real-world data is often nested. Pydantic handles this naturally:

```python
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"

class SocialLinks(BaseModel):
    twitter: str | None = None
    linkedin: str | None = None
    github: str | None = None

class UserCreate(BaseModel):
    name: str
    email: str
    age: int | None = None
    address: Address                          # Nested model
    social: SocialLinks | None = None         # Optional nested model
    interests: list[str] = []                 # List of strings
    metadata: dict[str, str] = {}             # Dict of strings

@app.post("/users")
async def create_user(user: UserCreate):
    return user
```

Expected JSON body:
```json
{
    "name": "Alice",
    "email": "alice@example.com",
    "age": 30,
    "address": {
        "street": "123 Main St",
        "city": "New York",
        "state": "NY",
        "zip_code": "10001"
    },
    "social": {
        "github": "alice-dev",
        "twitter": "@alice"
    },
    "interests": ["coding", "hiking"],
    "metadata": {"source": "web", "plan": "premium"}
}
```

---

## Deeply Nested Models

```python
class Image(BaseModel):
    url: str
    width: int
    height: int

class Product(BaseModel):
    name: str
    price: float
    images: list[Image]               # List of nested models

class Order(BaseModel):
    customer_name: str
    products: list[Product]           # List of nested models (2 levels deep!)
    shipping_address: Address

@app.post("/orders")
async def create_order(order: Order):
    total = sum(p.price for p in order.products)
    return {
        "customer": order.customer_name,
        "total_products": len(order.products),
        "total_price": total,
    }
```

---

## Multiple Body Parameters

If you have multiple Pydantic model parameters, FastAPI expects them as **named keys** in the JSON:

```python
class Item(BaseModel):
    name: str
    price: float

class User(BaseModel):
    username: str
    email: str

@app.post("/orders")
async def create_order(item: Item, user: User):
    return {"item": item.model_dump(), "buyer": user.model_dump()}
```

Expected JSON body (note the keys!):
```json
{
    "item": {
        "name": "Widget",
        "price": 9.99
    },
    "user": {
        "username": "alice",
        "email": "alice@test.com"
    }
}
```

---

## The `Body()` Function

For simple types as body parameters (instead of query params), use `Body()`:

```python
from fastapi import Body

class Item(BaseModel):
    name: str
    price: float

@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item,
    importance: int = Body(
        description="Priority level for this update",
        ge=1,
        le=5,
    ),
):
    return {"item_id": item_id, "item": item.model_dump(), "importance": importance}
```

Expected JSON body:
```json
{
    "item": {
        "name": "Widget",
        "price": 9.99
    },
    "importance": 3
}
```

### `embed=True` — Force a Single Model to Have a Key

By default, a single Pydantic model parameter reads the body directly. Use `embed=True` to require a key:

```python
class Item(BaseModel):
    name: str
    price: float

# WITHOUT embed — body is the item directly
@app.post("/items")
async def create_item(item: Item):
    return item
# Body: {"name": "Widget", "price": 9.99}

# WITH embed — body has an "item" key
@app.post("/items-embedded")
async def create_item_embedded(item: Item = Body(embed=True)):
    return item
# Body: {"item": {"name": "Widget", "price": 9.99}}
```

---

## Lists as Request Body

```python
class Item(BaseModel):
    name: str
    price: float

# Accept a list of items
@app.post("/items/bulk")
async def create_items(items: list[Item]):
    return {"created": len(items), "items": items}
```

JSON body:
```json
[
    {"name": "Widget", "price": 9.99},
    {"name": "Gadget", "price": 19.99},
    {"name": "Doohickey", "price": 4.99}
]
```

---

## Model Config with Examples

Add examples to your models for better documentation:

```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float = 0

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Laptop",
                    "description": "A powerful laptop for development",
                    "price": 999.99,
                    "tax": 80.00,
                },
                {
                    "name": "Mouse",
                    "description": "Wireless ergonomic mouse",
                    "price": 49.99,
                    "tax": 4.00,
                },
            ]
        }
    }
```

---

## Key Takeaways

1. **Pydantic models = request bodies** — FastAPI reads JSON and validates automatically
2. **Detection is by type** — simple types = query params, Pydantic models = body
3. **Nesting works naturally** — models within models, lists of models
4. **Multiple body params get keys** — each model becomes a named key in JSON
5. **`Body()` turns simple types into body params** — instead of query params
6. **`embed=True` adds a wrapper key** — useful for single-model bodies

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Using `dict` instead of model | No validation | Define a Pydantic model |
| Missing `Content-Type` header | Body not parsed | Send `Content-Type: application/json` |
| Sending body with GET | Usually ignored | Use POST/PUT/PATCH for bodies |
| Wrong nesting in JSON | Validation error | Match the model structure exactly |

---

> **Next Lesson**: [Headers & Cookies →](../04-headers-cookies/)
