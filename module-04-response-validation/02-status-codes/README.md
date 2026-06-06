# Lesson 02 — Status Codes

## Setting Status Codes

### In the Decorator

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items", status_code=201)  # 201 Created
async def create_item(item: Item):
    return {"id": 1, **item.model_dump()}

@app.delete("/items/{item_id}", status_code=204)  # 204 No Content
async def delete_item(item_id: int):
    return None  # No body for 204
```

### Using `status` Module (Readable Constants)

```python
from fastapi import FastAPI, status

app = FastAPI()

@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return {"id": 1, **item.model_dump()}

@app.get("/items/{item_id}", status_code=status.HTTP_200_OK)
async def get_item(item_id: int):
    return {"id": item_id}

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    return None
```

### Common Status Constants:

| Constant | Code | Use |
|----------|------|-----|
| `HTTP_200_OK` | 200 | Success (default) |
| `HTTP_201_CREATED` | 201 | Resource created (POST) |
| `HTTP_204_NO_CONTENT` | 204 | Success, no body (DELETE) |
| `HTTP_400_BAD_REQUEST` | 400 | Bad input |
| `HTTP_401_UNAUTHORIZED` | 401 | Not authenticated |
| `HTTP_403_FORBIDDEN` | 403 | Not authorized |
| `HTTP_404_NOT_FOUND` | 404 | Resource doesn't exist |
| `HTTP_409_CONFLICT` | 409 | Conflict (duplicate) |
| `HTTP_422_UNPROCESSABLE_ENTITY` | 422 | Validation error |
| `HTTP_500_INTERNAL_SERVER_ERROR` | 500 | Server error |

---

## Dynamic Status Codes with `Response`

Sometimes you need different status codes based on logic:

```python
from fastapi import Response, status

items_db = {}

@app.put("/items/{item_id}")
async def upsert_item(item_id: int, item: Item, response: Response):
    """Create or update — status depends on whether item existed."""
    if item_id in items_db:
        items_db[item_id] = item.model_dump()
        response.status_code = status.HTTP_200_OK
        return {"action": "updated", **items_db[item_id]}
    else:
        items_db[item_id] = item.model_dump()
        response.status_code = status.HTTP_201_CREATED
        return {"action": "created", **items_db[item_id]}
```

---

## Status Codes Best Practices

| Operation | Success Code | Error Codes |
|-----------|-------------|-------------|
| GET (read) | 200 OK | 404 Not Found |
| POST (create) | 201 Created | 400 Bad Request, 409 Conflict |
| PUT (replace) | 200 OK | 404 Not Found |
| PATCH (update) | 200 OK | 404 Not Found, 400 Bad Request |
| DELETE (remove) | 204 No Content | 404 Not Found |

---

> **Next Lesson**: [Pydantic Deep Dive →](../03-pydantic-deep-dive/)
