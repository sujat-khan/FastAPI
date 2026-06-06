# Lesson 04 — Mocking & Fixtures

## Mocking External Services

When your API calls external services, mock them in tests:

```python
from unittest.mock import patch, AsyncMock

# Your endpoint calls an external API
# @app.get("/weather")
# async def get_weather(city: str):
#     data = await external_weather_api(city)
#     return data

def test_weather_endpoint(client):
    """Mock the external API call."""
    mock_weather = {"temp": 72, "condition": "sunny"}

    with patch("app.services.external_weather_api", return_value=mock_weather):
        response = client.get("/weather?city=NYC")
        assert response.status_code == 200
        assert response.json()["temp"] == 72

# For async mocks
def test_weather_async(client):
    mock_weather = AsyncMock(return_value={"temp": 72, "condition": "sunny"})

    with patch("app.services.external_weather_api", mock_weather):
        response = client.get("/weather?city=NYC")
        assert response.status_code == 200
```

---

## Pytest Fixtures

Reusable test setup/teardown:

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def auth_headers():
    """Get auth headers for a test user."""
    client = TestClient(app)
    response = client.post("/token", data={"username": "testuser", "password": "testpass"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def sample_user():
    return {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpass123",
    }

# Use fixtures in tests
def test_protected_route(client, auth_headers):
    response = client.get("/users/me", headers=auth_headers)
    assert response.status_code == 200

def test_create_user(client, sample_user):
    response = client.post("/users", json=sample_user)
    assert response.status_code == 201
```

---

## Factory Fixtures

Create dynamic test data:

```python
@pytest.fixture
def user_factory(client):
    """Factory to create test users."""
    created_users = []

    def _create_user(name="Test", email=None):
        email = email or f"{name.lower()}@test.com"
        response = client.post("/users", json={
            "name": name,
            "email": email,
            "password": "testpass123",
        })
        user = response.json()
        created_users.append(user)
        return user

    return _create_user

def test_multiple_users(client, user_factory):
    alice = user_factory("Alice")
    bob = user_factory("Bob")

    response = client.get("/users")
    assert len(response.json()) >= 2
```

---

## Key Takeaways

1. **Mock external services** — don't call real APIs in tests
2. **Fixtures provide reusable setup** — DRY test code
3. **Factory fixtures** — dynamic test data creation
4. **`conftest.py`** — shared fixtures auto-discovered by pytest
5. **`dependency_overrides`** — FastAPI's built-in mocking for deps

---

> **Next Lesson**: [Debugging Tips →](../05-debugging-tips/)
