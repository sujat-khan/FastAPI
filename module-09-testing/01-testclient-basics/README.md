# Lesson 01 — TestClient Basics

## Why Test Your API?

- **Catch bugs early** — before they reach production
- **Confidence in changes** — refactor without fear
- **Documentation** — tests show how the API works
- **Prevent regressions** — ensure fixes don't break other things

---

## Setup

```bash
pip install pytest httpx
```

---

## Your First API Test

```python
# app/main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

items_db = []

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/items")
async def list_items():
    return items_db

@app.post("/items", status_code=201)
async def create_item(item: Item):
    new_item = {"id": len(items_db) + 1, **item.model_dump()}
    items_db.append(new_item)
    return new_item
```

```python
# tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_create_item():
    """Test creating a new item."""
    response = client.post(
        "/items",
        json={"name": "Laptop", "price": 999.99},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99
    assert "id" in data

def test_create_item_invalid():
    """Test validation — missing required field."""
    response = client.post(
        "/items",
        json={"name": "Laptop"},  # Missing 'price'
    )
    assert response.status_code == 422

def test_list_items():
    """Test listing items."""
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run a specific file
pytest tests/test_main.py

# Run a specific test
pytest tests/test_main.py::test_create_item

# Show print output
pytest -s
```

---

## Testing Headers, Auth, and Query Params

```python
def test_with_headers():
    response = client.get(
        "/protected",
        headers={"Authorization": "Bearer my-token"},
    )
    assert response.status_code == 200

def test_with_query_params():
    response = client.get("/items?skip=0&limit=5")
    assert response.status_code == 200

def test_with_path_params():
    response = client.get("/items/42")
    assert response.status_code == 200

def test_with_cookies():
    response = client.get(
        "/dashboard",
        cookies={"session": "abc123"},
    )
    assert response.status_code == 200
```

---

## Key Takeaways

1. **`TestClient` makes HTTP calls** without running the server
2. **Use `pytest`** as the test runner
3. **Test status codes, response body, and headers**
4. **Test both valid and invalid inputs**
5. **Run with `pytest -v`** for detailed output

---

> **Next Lesson**: [Testing with Databases →](../02-testing-with-databases/)
