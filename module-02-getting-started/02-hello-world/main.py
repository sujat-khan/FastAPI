"""
Module 02 - Lesson 02: Hello World FastAPI App
================================================
Run with:
    uvicorn main:app --reload

Then visit:
    http://127.0.0.1:8000
    http://127.0.0.1:8000/docs
"""

from datetime import datetime
from fastapi import FastAPI

# ============================================================
# Create the FastAPI application instance
# ============================================================
app = FastAPI(
    title="Hello World API",
    description="My first FastAPI application",
    version="1.0.0",
)


# ============================================================
# Endpoints
# ============================================================

@app.get("/")
async def root():
    """The root endpoint — returns a welcome message."""
    return {"message": "Hello, World! Welcome to FastAPI! 🚀"}


@app.get("/about")
async def about():
    """Returns information about this API."""
    return {
        "app": "Hello World API",
        "version": "1.0.0",
        "framework": "FastAPI",
        "python_version": "3.10+",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint — useful for monitoring."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/time")
async def current_time():
    """Returns the current date and time."""
    now = datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "iso": now.isoformat(),
    }


@app.get("/greet/{name}")
async def greet(name: str):
    """Greet a user by name (preview of path parameters!)."""
    return {"message": f"Hello, {name}! Welcome to my API!"}
