"""
Module 02 - Lesson 03: Interactive Documentation Example
==========================================================
Run with:
    uvicorn main:app --reload

Then visit:
    http://127.0.0.1:8000/docs     (Swagger UI)
    http://127.0.0.1:8000/redoc    (ReDoc)
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

# ============================================================
# App with rich metadata — shows up in docs
# ============================================================
app = FastAPI(
    title="User Management API",
    description="""
## User Management API 🚀

A demo API showcasing FastAPI's automatic documentation features.

### Features
* **Create** users with validation
* **List** all users
* **Get** a single user by ID
* **Health check** endpoint

### Notes
This is a learning example — data is stored in memory only.
    """,
    version="1.0.0",
    contact={
        "name": "FastAPI Course",
        "email": "learn@fastapi.example.com",
    },
    license_info={
        "name": "MIT License",
    },
)


# ============================================================
# Pydantic Models — these appear as "Schemas" in docs
# ============================================================

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    name: str = Field(
        min_length=1,
        max_length=50,
        examples=["Alice Johnson"],
        description="The user's full name"
    )
    email: str = Field(
        examples=["alice@example.com"],
        description="The user's email address"
    )
    age: int | None = Field(
        default=None,
        ge=0,
        le=150,
        examples=[30],
        description="The user's age (optional)"
    )


class UserResponse(BaseModel):
    """Schema for user response (includes generated ID)."""
    id: int = Field(description="Unique user identifier")
    name: str = Field(description="The user's full name")
    email: str = Field(description="The user's email address")
    age: int | None = Field(default=None, description="The user's age")


# ============================================================
# In-memory storage
# ============================================================
users_db: list[dict] = []
next_id = 1


# ============================================================
# Endpoints with tags and descriptions
# ============================================================

@app.get("/", tags=["General"])
async def root():
    """
    Welcome endpoint.

    Returns a welcome message and links to documentation.
    """
    return {
        "message": "Welcome to the User Management API!",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health", tags=["General"])
async def health_check():
    """
    Health check endpoint.

    Returns the current health status of the API.
    Useful for monitoring and load balancers.
    """
    return {
        "status": "healthy",
        "users_count": len(users_db),
    }


@app.get("/users", tags=["Users"], response_model=list[UserResponse])
async def get_users():
    """
    List all users.

    Returns a list of all registered users in the system.
    """
    return users_db


@app.post(
    "/users",
    tags=["Users"],
    response_model=UserResponse,
    status_code=201,
    summary="Register a new user",
)
async def create_user(user: UserCreate):
    """
    Create a new user.

    Provide user details in the request body:
    - **name**: Required. The user's full name (1-50 characters)
    - **email**: Required. The user's email address
    - **age**: Optional. Must be between 0 and 150

    Returns the created user with a generated ID.
    """
    global next_id
    new_user = {"id": next_id, **user.model_dump()}
    users_db.append(new_user)
    next_id += 1
    return new_user


@app.get("/users/{user_id}", tags=["Users"], response_model=UserResponse)
async def get_user(user_id: int):
    """
    Get a specific user by ID.

    - **user_id**: The unique identifier of the user to retrieve.
    """
    for user in users_db:
        if user["id"] == user_id:
            return user
    return {"error": "User not found"}


# ============================================================
# Deprecated endpoint example
# ============================================================

@app.get(
    "/api/v1/users",
    tags=["Deprecated"],
    deprecated=True,
    response_model=list[UserResponse],
)
async def get_users_v1():
    """
    ⚠️ **DEPRECATED** — Use `GET /users` instead.

    This endpoint will be removed in version 2.0.0.
    """
    return users_db
