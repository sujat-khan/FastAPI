# Lesson 05 — Lifespan Events

## What Are Lifespan Events?

Lifespan events let you run code when the app **starts up** and **shuts down** — perfect for initializing and cleaning up resources.

---

## The `lifespan` Context Manager (Recommended)

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Simulated resources
ml_model = None
db_pool = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    # Code here runs before the app starts accepting requests
    global ml_model, db_pool
    print("🚀 Starting up...")
    ml_model = load_ml_model()       # Load ML model into memory
    db_pool = create_db_pool()       # Create database connection pool

    yield  # App runs here, handling requests

    # === SHUTDOWN ===
    # Code here runs when the app is stopping
    print("🛑 Shutting down...")
    ml_model = None
    await db_pool.close()            # Close all DB connections

app = FastAPI(lifespan=lifespan)

@app.get("/predict")
async def predict(text: str):
    result = ml_model.predict(text)
    return {"prediction": result}
```

---

## Sharing State via `app.state`

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Store resources on app.state
    app.state.db = create_engine("sqlite:///app.db")
    app.state.redis = await aioredis.from_url("redis://localhost")
    app.state.settings = load_settings()

    yield

    # Cleanup
    app.state.db.dispose()
    await app.state.redis.close()

app = FastAPI(lifespan=lifespan)

@app.get("/info")
async def info(request: Request):
    # Access via request.app.state
    settings = request.app.state.settings
    return {"version": settings.version}
```

---

## Common Use Cases

| Use Case | Startup | Shutdown |
|----------|---------|----------|
| Database | Create connection pool | Close all connections |
| ML Model | Load model into memory | Free memory |
| Redis Cache | Connect to Redis | Close connection |
| Background scheduler | Start scheduler | Stop scheduler |
| External API client | Create HTTP client | Close HTTP client |

---

## Key Takeaways

1. **`lifespan` is the modern way** — replaces deprecated `on_event`
2. **Code before `yield`** runs on startup
3. **Code after `yield`** runs on shutdown
4. **Use `app.state`** to share resources across endpoints
5. **Always clean up** — close connections, free memory

---

> **Next Lesson**: [Static Files & Templates →](../06-static-files-templates/)
