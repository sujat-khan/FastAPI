# Lesson 05 — Error Handling

## HTTPException — The Basic Way

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

items = {"foo": "The Foo item", "bar": "The Bar item"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail=f"Item '{item_id}' not found",
            headers={"X-Error": "Item not found"},  # Optional custom headers
        )
    return {"item": items[item_id]}
```

Response when item not found:
```json
{
    "detail": "Item 'baz' not found"
}
```

### `detail` Can Be Any JSON-Serializable Value

```python
raise HTTPException(
    status_code=400,
    detail={
        "error": "validation_failed",
        "message": "Multiple errors found",
        "errors": [
            {"field": "name", "error": "Name is required"},
            {"field": "email", "error": "Invalid email format"},
        ],
    },
)
```

---

## Custom Exception Classes

Define your own exceptions for cleaner code:

```python
class ItemNotFoundException(HTTPException):
    def __init__(self, item_id: str):
        super().__init__(
            status_code=404,
            detail=f"Item '{item_id}' not found",
        )

class InsufficientPermissionsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="You don't have permission to perform this action",
        )

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    if item_id not in items:
        raise ItemNotFoundException(item_id)
    return {"item": items[item_id]}
```

---

## Custom Exception Handlers

Override how exceptions are formatted in responses:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Define a custom exception
class AppException(Exception):
    def __init__(self, status_code: int, error_code: str, message: str):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message

# Register the handler
@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "path": str(request.url),
            }
        },
    )

@app.get("/items/{item_id}")
async def get_item(item_id: str):
    if item_id not in items:
        raise AppException(
            status_code=404,
            error_code="ITEM_NOT_FOUND",
            message=f"No item with ID '{item_id}' exists",
        )
    return {"item": items[item_id]}
```

Response:
```json
{
    "error": {
        "code": "ITEM_NOT_FOUND",
        "message": "No item with ID 'baz' exists",
        "path": "http://localhost:8000/items/baz"
    }
}
```

---

## Override Default Validation Errors

FastAPI's default validation error format can be customized:

```python
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    """Custom format for validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " → ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Failed",
            "detail": errors,
            "body": jsonable_encoder(exc.body),
        },
    )
```

---

## Global Error Handler (Catch-All)

```python
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch any unhandled exception."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            # Don't expose details in production!
        },
    )
```

---

## Error Handling Best Practices

| Practice | Why |
|----------|-----|
| Use specific status codes | Helps clients handle errors properly |
| Include error codes | Enables programmatic error handling |
| Don't expose internal details | Security risk in production |
| Log errors server-side | Debug without exposing to clients |
| Use custom exception classes | Cleaner, reusable error handling |
| Handle validation errors | Better UX with clear error messages |

---

## Key Takeaways

1. **`HTTPException`** is the standard way to return errors
2. **Custom exceptions** make code cleaner and more consistent
3. **Exception handlers** control how errors are formatted
4. **Override validation errors** for better error messages
5. **Never expose internal details** in production error responses

---

> **Next Module**: [Module 05 — Dependency Injection →](../../module-05-dependency-injection/)
