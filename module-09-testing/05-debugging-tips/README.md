# Lesson 05 — Debugging Tips

## Logging Configuration

```python
import logging
from fastapi import FastAPI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    logger.info(f"Fetching item {item_id}")
    try:
        item = find_item(item_id)
        logger.info(f"Found item: {item}")
        return item
    except Exception as e:
        logger.error(f"Error fetching item {item_id}: {e}", exc_info=True)
        raise
```

### Log Levels

| Level | When to Use |
|-------|-------------|
| `DEBUG` | Detailed info for debugging |
| `INFO` | General operational messages |
| `WARNING` | Something unexpected but not broken |
| `ERROR` | Something failed |
| `CRITICAL` | System is in a critical state |

---

## VS Code Debugging

### `launch.json` Configuration:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "FastAPI Debug",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": ["main:app", "--reload", "--port", "8000"],
            "jinja": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

Now you can:
- Set breakpoints in your code
- Step through endpoint execution
- Inspect variables
- Use the debug console

---

## Common Pitfalls & Solutions

### 1. Circular Imports
```
ImportError: cannot import name 'X' from partially initialized module
```
**Solution**: Move shared imports to a separate module, use late imports.

### 2. `time.sleep()` in `async def`
```python
# ❌ Blocks the event loop
@app.get("/slow")
async def slow():
    time.sleep(5)  # Blocks ALL requests!

# ✅ Use asyncio.sleep or regular def
@app.get("/slow")
async def slow():
    await asyncio.sleep(5)

# Or use regular def (runs in thread pool)
@app.get("/slow")
def slow():
    time.sleep(5)
```

### 3. Forgetting `await`
```python
# ❌ Returns coroutine object instead of result
result = async_function()

# ✅ Actually executes the function
result = await async_function()
```

### 4. Pydantic Validation Errors
Use the detailed error response to find the exact field:
```json
{
    "detail": [
        {
            "loc": ["body", "email"],
            "msg": "value is not a valid email address",
            "type": "value_error.email"
        }
    ]
}
```

### 5. Database Session Not Closing
Always use the `yield` dependency pattern:
```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Always closes!
```

### 6. SQLAlchemy `check_same_thread`
```
sqlite3.ProgrammingError: SQLite objects created in a thread...
```
**Solution**: Add `connect_args={"check_same_thread": False}` to `create_engine()`.

---

## Useful Debugging Tools

| Tool | Purpose |
|------|---------|
| `uvicorn --log-level debug` | See all HTTP requests |
| `sqlalchemy echo=True` | See all SQL queries |
| `/docs` (Swagger UI) | Test endpoints interactively |
| `httpx` / `curl` | Make requests from terminal |
| Python `breakpoint()` | Drop into debugger |
| `pytest -s` | Show print output in tests |

---

## Key Takeaways

1. **Use proper logging** — not `print()` statements
2. **Configure VS Code** for step-through debugging
3. **Know the common pitfalls** — async, imports, sessions
4. **Use SQLAlchemy echo** to see generated SQL
5. **Swagger UI is your friend** — test endpoints interactively

---

> **Next Module**: [Module 10 — Production & Deployment →](../../module-10-production/)
