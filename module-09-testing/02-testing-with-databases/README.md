# Lesson 02 — Testing with Databases

## The Problem

You don't want tests to use your real database — they should use an **isolated test database**.

---

## Solution: Override the Database Dependency

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.main import app
from app.dependencies import get_db

# Use a separate test database (in-memory SQLite)
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Provide test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(autouse=True)
def setup_database():
    """Create tables before each test, drop after."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """Provide a test client with overridden database."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
```

```python
# tests/test_users.py
def test_create_user(client):
    response = client.post(
        "/users",
        json={"name": "Alice", "email": "alice@test.com", "password": "secret123"},
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Alice"

def test_create_duplicate_user(client):
    # Create first user
    client.post("/users", json={"name": "Alice", "email": "alice@test.com", "password": "secret"})

    # Try duplicate
    response = client.post("/users", json={"name": "Alice2", "email": "alice@test.com", "password": "secret"})
    assert response.status_code == 409

def test_list_users_empty(client):
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == []
```

---

## Key Points

1. **`dependency_overrides`** — swap real DB for test DB
2. **`autouse=True` fixture** — runs before every test automatically
3. **Create/drop tables per test** — ensures isolation
4. **In-memory SQLite** — fast, no cleanup needed
5. **Always clear overrides** — prevent leaks between tests

---

> **Next Lesson**: [Async Testing →](../03-async-testing/)
