# Lesson 03 — Interactive Documentation

## FastAPI's Killer Feature: Auto-Generated Docs

One of FastAPI's most impressive features is **automatic interactive API documentation**. You get it for free — no extra code needed!

When you run your FastAPI app, three documentation endpoints are automatically available:

| URL | What | Description |
|-----|------|-------------|
| `/docs` | **Swagger UI** | Interactive API playground |
| `/redoc` | **ReDoc** | Beautiful read-only documentation |
| `/openapi.json` | **OpenAPI Schema** | Raw JSON specification |

---

## Swagger UI (`/docs`)

Visit: **http://127.0.0.1:8000/docs**

Swagger UI is an **interactive** documentation page where you can:
- See all your endpoints
- Read descriptions and expected parameters
- **Try out endpoints** directly from the browser (click "Try it out")
- See request/response examples
- View validation rules

```
┌─────────────────────────────────────────────────────────┐
│  My API - Swagger UI                                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  GET  /              root           [Try it out]         │
│  GET  /users         get_users      [Try it out]         │
│  POST /users         create_user    [Try it out]         │
│  GET  /users/{id}    get_user       [Try it out]         │
│  PUT  /users/{id}    update_user    [Try it out]         │
│  DELETE /users/{id}  delete_user    [Try it out]         │
│                                                          │
│  Schemas:                                                │
│  ├── UserCreate                                          │
│  ├── UserResponse                                        │
│  └── HTTPValidationError                                 │
└─────────────────────────────────────────────────────────┘
```

---

## ReDoc (`/redoc`)

Visit: **http://127.0.0.1:8000/redoc**

ReDoc provides a **clean, read-only** documentation page. It's great for sharing with API consumers who don't need to test endpoints interactively.

---

## OpenAPI Schema (`/openapi.json`)

Visit: **http://127.0.0.1:8000/openapi.json**

This is the raw **OpenAPI specification** in JSON format. It's the machine-readable description of your entire API. Tools like Swagger UI and ReDoc read this to generate the visual docs.

FastAPI follows the **OpenAPI 3.1** standard (previously known as Swagger).

---

## Customizing Your Documentation

### App-Level Metadata

```python
from fastapi import FastAPI

app = FastAPI(
    title="My Awesome API",
    description="""
    ## User Management API 🚀

    This API allows you to:
    * **Create** users
    * **Read** user information
    * **Update** user profiles
    * **Delete** users

    ### Authentication
    All endpoints require a Bearer token.
    """,
    version="2.0.0",
    contact={
        "name": "API Support",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
    },
)
```

### Endpoint Descriptions

FastAPI uses the function's **docstring** as the endpoint description in docs:

```python
@app.get("/users")
async def get_users():
    """
    Retrieve all users.

    Returns a list of all registered users in the system.
    Supports pagination via query parameters.
    """
    return [{"id": 1, "name": "Alice"}]
```

### Tagging Endpoints

Tags group related endpoints together in the documentation:

```python
@app.get("/users", tags=["Users"])
async def get_users():
    """Get all users."""
    return []

@app.post("/users", tags=["Users"])
async def create_user():
    """Create a new user."""
    return {"id": 1}

@app.get("/posts", tags=["Posts"])
async def get_posts():
    """Get all posts."""
    return []
```

In Swagger UI, this creates collapsible sections:
```
▼ Users
    GET  /users     Get all users
    POST /users     Create a new user
▼ Posts
    GET  /posts     Get all posts
```

### Deprecating Endpoints

Mark old endpoints as deprecated:

```python
@app.get("/old-endpoint", deprecated=True, tags=["Deprecated"])
async def old_endpoint():
    """This endpoint is deprecated. Use /new-endpoint instead."""
    return {"message": "Use /new-endpoint"}
```

This shows a ~~strikethrough~~ in the docs, warning users it's deprecated.

---

## Adding Response Examples

You can add examples to make your docs more helpful:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class User(BaseModel):
    name: str = Field(examples=["Alice"])
    email: str = Field(examples=["alice@example.com"])
    age: int = Field(examples=[30])

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Alice",
                    "email": "alice@example.com",
                    "age": 30,
                }
            ]
        }
    }

@app.post("/users")
async def create_user(user: User):
    """Create a new user with the provided information."""
    return {"id": 1, **user.model_dump()}
```

---

## Disabling Documentation

In production, you might want to disable the docs:

```python
# Disable Swagger UI
app = FastAPI(docs_url=None)

# Disable ReDoc
app = FastAPI(redoc_url=None)

# Disable both
app = FastAPI(docs_url=None, redoc_url=None)

# Change the URL
app = FastAPI(docs_url="/api/docs", redoc_url="/api/redoc")
```

---

## How It Works Under the Hood

```
┌─────────────────────────────────────────────────────┐
│                    YOUR CODE                         │
│                                                      │
│  @app.get("/users/{id}")                            │
│  async def get_user(id: int) -> UserResponse:       │
│      ...                                             │
└──────────────────────┬──────────────────────────────┘
                       │ FastAPI reads type hints,
                       │ decorators, docstrings
                       ▼
┌─────────────────────────────────────────────────────┐
│              OpenAPI Schema (JSON)                   │
│                                                      │
│  {                                                   │
│    "paths": {                                        │
│      "/users/{id}": {                               │
│        "get": {                                      │
│          "parameters": [{"name": "id", ...}],       │
│          "responses": {"200": {...}}                 │
│        }                                             │
│      }                                               │
│    }                                                 │
│  }                                                   │
└──────────────────────┬──────────────────────────────┘
                       │ Consumed by
                       ▼
┌──────────────┐  ┌──────────────┐  ┌─────────────────┐
│  Swagger UI  │  │    ReDoc     │  │ API Clients     │
│  /docs       │  │  /redoc      │  │ (Postman, etc.) │
└──────────────┘  └──────────────┘  └─────────────────┘
```

---

## Key Takeaways

1. **Documentation is automatic** — just write your code with type hints
2. **Swagger UI (`/docs`) is interactive** — you can test endpoints directly
3. **ReDoc (`/redoc`) is for reading** — share with API consumers
4. **OpenAPI schema is the source** — it's the machine-readable spec
5. **Customize with metadata** — title, description, tags, examples
6. **Docstrings become descriptions** — write good docstrings!

---

## Practice Exercises

1. Run the example `main.py` and explore both `/docs` and `/redoc`
2. Add tags to group your endpoints in the docs
3. Add a detailed docstring to an endpoint and see it appear in Swagger UI
4. Try the "Try it out" button in Swagger UI to make API calls

---

> **Next Lesson**: [Path Operations →](../04-path-operations/)
