# Lesson 03 — Performance & Optimization

## Async Best Practices

### Use `async def` for I/O-Bound Operations
```python
# ✅ Async database queries
@app.get("/users")
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    return result.scalars().all()

# ✅ Async HTTP calls
import httpx

@app.get("/external")
async def get_external():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
    return response.json()
```

### Use `def` for CPU-Bound or Sync Operations
```python
# ✅ FastAPI runs this in a thread pool
@app.get("/compute")
def heavy_computation():
    result = sum(i ** 2 for i in range(1000000))
    return {"result": result}
```

---

## Caching with Redis

```python
import redis.asyncio as redis
from fastapi import FastAPI

app = FastAPI()
redis_client = redis.from_url("redis://localhost")

@app.get("/data/{item_id}")
async def get_data(item_id: int):
    # Check cache first
    cached = await redis_client.get(f"item:{item_id}")
    if cached:
        import json
        return json.loads(cached)

    # Cache miss — fetch from database
    data = await fetch_from_db(item_id)

    # Store in cache (expire after 5 minutes)
    import json
    await redis_client.setex(f"item:{item_id}", 300, json.dumps(data))

    return data
```

---

## Rate Limiting

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from starlette.requests import Request

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

@app.get("/api/data")
@limiter.limit("10/minute")
async def get_data(request: Request):
    return {"data": "rate limited to 10 requests per minute"}
```

---

## Connection Pooling

```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=20,          # Max persistent connections
    max_overflow=10,       # Extra connections when pool is full
    pool_timeout=30,       # Wait time for connection
    pool_recycle=1800,     # Recycle connections after 30 min
)
```

---

## Performance Checklist

| Area | Optimization |
|------|-------------|
| **Database** | Use connection pooling, indexes, eager loading |
| **Caching** | Redis/Memcached for frequently accessed data |
| **Async** | Use async libraries for all I/O |
| **Pagination** | Always paginate list endpoints |
| **Compression** | Enable GZip middleware |
| **Response model** | Only return needed fields |
| **Monitoring** | Track response times, error rates |

---

> **Next Lesson**: [API Versioning →](../04-api-versioning/)
