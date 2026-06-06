# Lesson 04 — Headers & Cookies

## Reading Request Headers

HTTP headers carry metadata about the request. FastAPI makes it easy to access them.

### Using the `Header()` Function

```python
from fastapi import FastAPI, Header

app = FastAPI()

@app.get("/items")
async def read_items(
    user_agent: str | None = Header(default=None),
    accept_language: str | None = Header(default=None),
    x_request_id: str | None = Header(default=None),
):
    """
    FastAPI automatically converts header names:
    - 'user_agent' parameter → reads 'user-agent' header
    - 'accept_language' → reads 'accept-language' header
    - 'x_request_id' → reads 'x-request-id' header

    Python underscores (_) are converted to hyphens (-)
    """
    return {
        "User-Agent": user_agent,
        "Accept-Language": accept_language,
        "X-Request-Id": x_request_id,
    }
```

### Why the Conversion?

HTTP headers use hyphens (`Content-Type`), but Python variables can't have hyphens. FastAPI automatically converts:
- Python `user_agent` ↔ HTTP `user-agent`
- Python `content_type` ↔ HTTP `content-type`

To disable this conversion:
```python
@app.get("/items")
async def read_items(
    strange_header: str | None = Header(default=None, convert_underscores=False),
):
    """This reads the header literally as 'strange_header' (with underscores)."""
    return {"strange_header": strange_header}
```

---

## Common Header Patterns

### Authorization Header
```python
@app.get("/protected")
async def protected_route(
    authorization: str | None = Header(default=None),
):
    if not authorization:
        return {"error": "No authorization header"}

    # Typically: "Bearer <token>"
    scheme, _, token = authorization.partition(" ")
    return {"scheme": scheme, "token": token[:20] + "..."}
```

### Custom Headers
```python
@app.get("/custom")
async def custom_headers(
    x_api_key: str = Header(description="Your API key"),
    x_client_version: str | None = Header(default=None),
):
    return {
        "api_key": x_api_key,
        "client_version": x_client_version,
    }
```

### Duplicate Headers (List of Values)
```python
@app.get("/items")
async def read_items(
    x_forwarded_for: list[str] | None = Header(default=None),
):
    """When proxies add multiple X-Forwarded-For headers."""
    return {"X-Forwarded-For": x_forwarded_for}
```

---

## Setting Response Headers

### Using `Response` Parameter
```python
from fastapi import Response

@app.get("/items")
async def get_items(response: Response):
    response.headers["X-Custom-Header"] = "my-value"
    response.headers["X-Process-Time"] = "0.05"
    return {"items": ["item1", "item2"]}
```

### Using Custom Response
```python
from fastapi.responses import JSONResponse

@app.get("/items")
async def get_items():
    content = {"items": ["item1", "item2"]}
    headers = {
        "X-Custom-Header": "my-value",
        "X-Total-Count": "2",
    }
    return JSONResponse(content=content, headers=headers)
```

---

## Cookies

### Reading Cookies
```python
from fastapi import Cookie

@app.get("/items")
async def read_items(
    session_id: str | None = Cookie(default=None),
    tracking_id: str | None = Cookie(default=None),
):
    return {
        "session_id": session_id,
        "tracking_id": tracking_id,
    }
```

### Setting Cookies
```python
from fastapi import Response

@app.post("/login")
async def login(response: Response):
    response.set_cookie(
        key="session_id",
        value="abc123xyz",
        max_age=3600,            # Expires in 1 hour (seconds)
        httponly=True,            # Not accessible via JavaScript
        secure=True,             # Only sent over HTTPS
        samesite="lax",          # CSRF protection
    )
    return {"message": "Logged in!"}

@app.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="session_id")
    return {"message": "Logged out!"}
```

### Cookie Parameters

| Parameter | Purpose | Default |
|-----------|---------|---------|
| `key` | Cookie name | Required |
| `value` | Cookie value | Required |
| `max_age` | Lifetime in seconds | Session (until browser closes) |
| `expires` | Absolute expiry datetime | None |
| `path` | URL path scope | `/` |
| `domain` | Domain scope | Current domain |
| `secure` | HTTPS only | `False` |
| `httponly` | Block JavaScript access | `False` |
| `samesite` | CSRF protection | `"lax"` |

---

## Real-World Example: Request Tracking

```python
import uuid
from fastapi import FastAPI, Header, Response

app = FastAPI()

@app.middleware("http")
async def add_request_id(request, call_next):
    """Add a unique request ID to every response."""
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-Id"] = request_id
    return response

@app.get("/data")
async def get_data(
    x_api_key: str = Header(description="Your API key"),
    x_client_id: str | None = Header(default=None),
    response: Response = None,
):
    """Endpoint that reads custom headers and sets response headers."""
    response.headers["X-Rate-Limit-Remaining"] = "99"
    return {
        "data": "sensitive information",
        "client": x_client_id,
    }
```

---

## Key Takeaways

1. **`Header()` reads request headers** — underscores auto-convert to hyphens
2. **`Cookie()` reads cookies** — works like `Header()` but for cookies
3. **`Response` object sets headers/cookies** — inject it as a parameter
4. **Security matters** — use `httponly`, `secure`, `samesite` for cookies
5. **Custom headers use `X-` prefix** — convention (though technically deprecated)

---

> **Next Lesson**: [Form Data & File Uploads →](../05-form-data-file-uploads/)
