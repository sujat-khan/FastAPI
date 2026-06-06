"""
Module 03: Request Handling — Complete Example
================================================
Run with:
    uvicorn main:app --reload

Demonstrates all 5 types of request data:
- Path parameters
- Query parameters
- Request body
- Headers & Cookies
- Form data & file uploads
"""

from enum import Enum
from fastapi import (
    FastAPI, Path, Query, Header, Cookie,
    Body, Form, File, UploadFile,
    HTTPException, Response,
)
from pydantic import BaseModel, Field

app = FastAPI(title="Request Handling Demo", version="1.0.0")


# ============================================================
# 1. PATH PARAMETERS
# ============================================================

class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"

# Fixed path FIRST
@app.get("/items/featured", tags=["Path Params"])
async def get_featured():
    return {"item": "Featured Item of the Day"}

@app.get("/items/{item_id}", tags=["Path Params"])
async def get_item(
    item_id: int = Path(ge=1, le=10000, description="The item ID"),
):
    return {"item_id": item_id}

@app.get("/categories/{category}", tags=["Path Params"])
async def get_category(category: Category):
    return {"category": category.value}


# ============================================================
# 2. QUERY PARAMETERS
# ============================================================

@app.get("/search", tags=["Query Params"])
async def search(
    q: str = Query(min_length=2, max_length=50, description="Search query"),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=20, ge=1, le=100),
    sort_by: str = Query(default="relevance"),
    tags: list[str] = Query(default=[]),
):
    return {
        "query": q,
        "page": page,
        "per_page": per_page,
        "sort_by": sort_by,
        "tags": tags,
    }


# ============================================================
# 3. REQUEST BODY
# ============================================================

class Address(BaseModel):
    street: str
    city: str
    country: str = "USA"

class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100, examples=["Alice"])
    email: str = Field(examples=["alice@example.com"])
    age: int | None = Field(default=None, ge=0, le=150)
    address: Address | None = None
    tags: list[str] = []

@app.post("/users", tags=["Request Body"], status_code=201)
async def create_user(user: UserCreate):
    return {"id": 1, **user.model_dump()}

class ItemCreate(BaseModel):
    name: str
    price: float = Field(gt=0)

@app.put("/users/{user_id}/items", tags=["Request Body"])
async def add_user_item(
    user_id: int,           # Path parameter
    item: ItemCreate,       # Request body
    priority: int = Body(default=1, ge=1, le=5),  # Body param
    note: str | None = None,  # Query parameter
):
    return {
        "user_id": user_id,
        "item": item.model_dump(),
        "priority": priority,
        "note": note,
    }


# ============================================================
# 4. HEADERS & COOKIES
# ============================================================

@app.get("/headers-demo", tags=["Headers & Cookies"])
async def read_headers(
    user_agent: str | None = Header(default=None),
    x_request_id: str | None = Header(default=None),
    accept_language: str | None = Header(default=None),
):
    return {
        "User-Agent": user_agent,
        "X-Request-Id": x_request_id,
        "Accept-Language": accept_language,
    }

@app.get("/cookies-demo", tags=["Headers & Cookies"])
async def read_cookies(
    session_id: str | None = Cookie(default=None),
    theme: str = Cookie(default="light"),
):
    return {"session_id": session_id, "theme": theme}

@app.post("/set-cookie", tags=["Headers & Cookies"])
async def set_cookie(response: Response):
    response.set_cookie(key="session_id", value="abc123", max_age=3600)
    response.set_cookie(key="theme", value="dark")
    return {"message": "Cookies set!"}


# ============================================================
# 5. FORM DATA & FILE UPLOADS
# ============================================================

@app.post("/login", tags=["Forms & Files"])
async def login(
    username: str = Form(),
    password: str = Form(),
):
    return {"username": username, "logged_in": True}

@app.post("/upload", tags=["Forms & Files"])
async def upload_file(file: UploadFile):
    content = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(content),
    }

@app.post("/upload-multiple", tags=["Forms & Files"])
async def upload_multiple(files: list[UploadFile]):
    results = []
    for f in files:
        content = await f.read()
        results.append({
            "filename": f.filename,
            "size": len(content),
        })
    return {"uploaded": len(results), "files": results}
