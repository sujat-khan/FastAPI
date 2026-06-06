# Lesson 03 — Async Testing

## Why Async Testing?

`TestClient` is sync — but sometimes you need to test async endpoints with async dependencies directly.

---

## Using `httpx.AsyncClient`

```bash
pip install httpx pytest-asyncio
```

```python
# tests/test_async.py
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.anyio
async def test_root():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

@pytest.mark.anyio
async def test_create_item():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/items",
            json={"name": "Widget", "price": 9.99},
        )
    assert response.status_code == 201
```

### pytest configuration (`pyproject.toml`):
```toml
[tool.pytest.ini_options]
anyio_backend = "asyncio"
```

---

## Async Fixture

```python
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.anyio
async def test_with_fixture(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
```

---

## When to Use Async vs Sync Testing

| Use | When |
|-----|------|
| `TestClient` (sync) | Most tests — simpler, covers most cases |
| `AsyncClient` (async) | Testing async dependencies, WebSockets, streaming |

---

> **Next Lesson**: [Mocking & Fixtures →](../04-mocking-fixtures/)
