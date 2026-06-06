"""
Module 02 - Lesson 04: Path Operations — Complete CRUD Example
===============================================================
Run with:
    uvicorn main:app --reload

Try these endpoints:
    GET    http://127.0.0.1:8000/books           → List all books
    POST   http://127.0.0.1:8000/books           → Create a book
    GET    http://127.0.0.1:8000/books/1          → Get book by ID
    PUT    http://127.0.0.1:8000/books/1          → Replace a book
    PATCH  http://127.0.0.1:8000/books/1          → Partially update a book
    DELETE http://127.0.0.1:8000/books/1          → Delete a book
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# ============================================================
# App setup
# ============================================================
app = FastAPI(
    title="Bookstore API",
    description="A complete CRUD API demonstrating all path operations",
    version="1.0.0",
)

# ============================================================
# Pydantic Models
# ============================================================

class BookCreate(BaseModel):
    """Schema for creating a new book."""
    title: str = Field(min_length=1, max_length=200, examples=["The Great Gatsby"])
    author: str = Field(min_length=1, max_length=100, examples=["F. Scott Fitzgerald"])
    price: float = Field(gt=0, examples=[12.99])
    genre: str = Field(examples=["Fiction"])
    in_stock: bool = Field(default=True)

class BookUpdate(BaseModel):
    """Schema for full update (PUT) — all fields required."""
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0)
    genre: str
    in_stock: bool

class BookPatch(BaseModel):
    """Schema for partial update (PATCH) — all fields optional."""
    title: str | None = None
    author: str | None = None
    price: float | None = Field(default=None, gt=0)
    genre: str | None = None
    in_stock: bool | None = None

class BookResponse(BaseModel):
    """Schema for book responses."""
    id: int
    title: str
    author: str
    price: float
    genre: str
    in_stock: bool


# ============================================================
# In-memory database
# ============================================================
books_db: dict[int, dict] = {
    1: {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "price": 12.99,
        "genre": "Fiction",
        "in_stock": True,
    },
    2: {
        "id": 2,
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "price": 29.99,
        "genre": "Programming",
        "in_stock": True,
    },
    3: {
        "id": 3,
        "title": "Dune",
        "author": "Frank Herbert",
        "price": 15.99,
        "genre": "Science Fiction",
        "in_stock": False,
    },
}
next_id = 4


# ============================================================
# Fixed path — MUST come before /books/{book_id}
# ============================================================

@app.get("/books/bestsellers", tags=["Books"], response_model=list[BookResponse])
async def get_bestsellers():
    """
    Get bestseller books.

    Returns books priced above $15 (simulated bestsellers list).
    This fixed path MUST be defined before `/books/{book_id}`
    to avoid being captured as a path parameter.
    """
    bestsellers = [b for b in books_db.values() if b["price"] > 15]
    return bestsellers


# ============================================================
# GET — Read operations
# ============================================================

@app.get("/books", tags=["Books"], response_model=list[BookResponse])
async def list_books():
    """
    List all books.

    Returns all books in the bookstore inventory.
    """
    return list(books_db.values())


@app.get("/books/{book_id}", tags=["Books"], response_model=BookResponse)
async def get_book(book_id: int):
    """
    Get a specific book by ID.

    - **book_id**: The unique identifier of the book.
    """
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")
    return books_db[book_id]


# ============================================================
# POST — Create
# ============================================================

@app.post("/books", tags=["Books"], response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate):
    """
    Create a new book.

    Provide book details in the request body.
    Returns the created book with a generated ID.
    """
    global next_id
    new_book = {"id": next_id, **book.model_dump()}
    books_db[next_id] = new_book
    next_id += 1
    return new_book


# ============================================================
# PUT — Full update (replace)
# ============================================================

@app.put("/books/{book_id}", tags=["Books"], response_model=BookResponse)
async def replace_book(book_id: int, book: BookUpdate):
    """
    Replace a book entirely (PUT).

    ALL fields must be provided. The existing book is completely replaced.
    """
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    updated_book = {"id": book_id, **book.model_dump()}
    books_db[book_id] = updated_book
    return updated_book


# ============================================================
# PATCH — Partial update
# ============================================================

@app.patch("/books/{book_id}", tags=["Books"], response_model=BookResponse)
async def patch_book(book_id: int, book: BookPatch):
    """
    Partially update a book (PATCH).

    Only the provided fields are updated. Missing fields remain unchanged.
    """
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    existing_book = books_db[book_id]
    update_data = book.model_dump(exclude_unset=True)  # Only fields that were sent

    for field, value in update_data.items():
        existing_book[field] = value

    return existing_book


# ============================================================
# DELETE — Remove
# ============================================================

@app.delete("/books/{book_id}", tags=["Books"], status_code=204)
async def delete_book(book_id: int):
    """
    Delete a book.

    Removes the book from the inventory. Returns 204 No Content on success.
    """
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail=f"Book with ID {book_id} not found")

    del books_db[book_id]
    return None
