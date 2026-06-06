# Lesson 01 — Middleware

## What Is Middleware?

Middleware is code that runs **before every request** and **after every response**. It's like a checkpoint that every request must pass through.

```
Client → Middleware A → Middleware B → Endpoint
Client ← Middleware A ← Middleware B ← Endpoint
```

---

## Custom Middleware

```python
import time
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Measure and log how long each request takes."""
    start_time = time.time()

    response = await call_next(request)  # Process the request

    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f"{request.method} {request.url.path} - {process_time:.4f}s")

    return response
```

### Execution Order:
```
1. Code BEFORE call_next() → runs before endpoint
2. call_next(request)      → runs the endpoint
3. Code AFTER call_next()  → runs after endpoint
```

---

## CORS Middleware (Critical!)

**CORS (Cross-Origin Resource Sharing)** is required when your frontend and API are on different domains/ports.

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # React dev server
        "http://localhost:5173",      # Vite dev server
        "https://myapp.com",         # Production frontend
    ],
    allow_credentials=True,           # Allow cookies
    allow_methods=["*"],              # Allow all HTTP methods
    allow_headers=["*"],              # Allow all headers
)
```

> **Without CORS middleware**, browsers will block requests from your frontend to your API if they're on different ports!

---

## Common Middleware Examples

### Logging Middleware
```python
import logging

logger = logging.getLogger("api")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"→ {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"← {request.method} {request.url.path} [{response.status_code}]")
    return response
```

### Authentication Middleware
```python
@app.middleware("http")
async def check_api_key(request: Request, call_next):
    # Skip auth for certain paths
    if request.url.path in ["/docs", "/redoc", "/openapi.json", "/health"]:
        return await call_next(request)

    api_key = request.headers.get("X-API-Key")
    if api_key != "my-secret-key":
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=403,
            content={"detail": "Invalid API key"},
        )

    return await call_next(request)
```

---

## Built-in Middleware

| Middleware | Purpose |
|-----------|---------|
| `CORSMiddleware` | Cross-origin requests |
| `TrustedHostMiddleware` | Restrict allowed hosts |
| `GZipMiddleware` | Compress responses |
| `HTTPSRedirectMiddleware` | Redirect HTTP to HTTPS |

```python
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["example.com", "*.example.com"])
```

---

## Key Takeaways

1. **Middleware runs on every request** — before and after
2. **CORS is essential** for frontend-backend communication
3. **Custom middleware** for logging, timing, auth, etc.
4. **Order matters** — middleware is processed in reverse order of definition

---

> **Next Lesson**: [Background Tasks →](../02-background-tasks/)
