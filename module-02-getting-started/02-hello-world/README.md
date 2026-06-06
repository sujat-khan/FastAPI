# Lesson 02 — Hello World API

## Your First FastAPI Application

Let's build the simplest possible API and understand every line:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}
```

That's it! Just **4 lines of meaningful code** to create a working API. Let's break it down.

---

## Line-by-Line Explanation

### Line 1: Import FastAPI
```python
from fastapi import FastAPI
```
Import the `FastAPI` class — this is the main class that provides all API functionality.

### Line 2: Create the App Instance
```python
app = FastAPI()
```
Create an instance of `FastAPI`. This `app` object is your entire API. It:
- Collects all your routes (endpoints)
- Handles incoming requests
- Generates API documentation
- Manages middleware, events, etc.

> **Convention**: The variable is always named `app` because Uvicorn expects it by default.

### Line 3: Define a Route Decorator
```python
@app.get("/")
```
This is a **path operation decorator**. It tells FastAPI:
- **HTTP Method**: `GET` (use `@app.get()`)
- **Path**: `/` (the root URL)
- **Associate the function below** with this method + path combination

### Line 4: The Endpoint Function
```python
async def root():
    return {"message": "Hello, World!"}
```
This is the **path operation function** (also called endpoint function or route handler). It:
- Is called when someone makes a `GET` request to `/`
- Returns a Python dictionary
- FastAPI automatically converts the dict to **JSON**

> **Note**: `async def` makes this an async function. You can also use regular `def` — both work fine!

---

## Running Your App

### Start the Server
```bash
uvicorn main:app --reload
```

Let's break down this command:

| Part | Meaning |
|------|---------|
| `uvicorn` | The ASGI server command |
| `main` | The Python file name (`main.py`, without `.py`) |
| `:` | Separator |
| `app` | The FastAPI instance variable name |
| `--reload` | Auto-restart on code changes (dev only!) |

### What You'll See
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345]
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Test It!

Open your browser and visit: **http://127.0.0.1:8000**

You'll see:
```json
{"message": "Hello, World!"}
```

🎉 **Congratulations!** You just built your first API!

---

## Useful Uvicorn Options

```bash
# Basic run
uvicorn main:app

# With auto-reload (development)
uvicorn main:app --reload

# Custom host and port
uvicorn main:app --host 0.0.0.0 --port 3000

# With more workers (production — NOT with --reload)
uvicorn main:app --workers 4

# Verbose logging
uvicorn main:app --log-level debug
```

| Option | Purpose | Default |
|--------|---------|---------|
| `--reload` | Auto-restart on file changes | Off |
| `--host` | Bind address | `127.0.0.1` |
| `--port` | Port number | `8000` |
| `--workers` | Number of worker processes | `1` |
| `--log-level` | Logging verbosity | `info` |

---

## Multiple Endpoints

You can define as many endpoints as you want:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to my API!"}

@app.get("/about")
async def about():
    return {
        "app": "My FastAPI App",
        "version": "1.0.0",
        "author": "Your Name"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

Now you have three endpoints:
- `GET /` → Welcome message
- `GET /about` → App info
- `GET /health` → Health check

---

## Return Types

FastAPI can return various Python types, and it converts them to JSON:

```python
# Dictionary → JSON object
@app.get("/dict")
async def return_dict():
    return {"key": "value"}
# Response: {"key": "value"}

# List → JSON array
@app.get("/list")
async def return_list():
    return [1, 2, 3, "four"]
# Response: [1, 2, 3, "four"]

# String → JSON string
@app.get("/string")
async def return_string():
    return "Hello!"
# Response: "Hello!"

# Number → JSON number
@app.get("/number")
async def return_number():
    return 42
# Response: 42

# Boolean → JSON boolean
@app.get("/bool")
async def return_bool():
    return True
# Response: true

# None → JSON null
@app.get("/null")
async def return_none():
    return None
# Response: null
```

---

## `async def` vs `def` — When to Use Which?

Both work in FastAPI, but they behave differently:

```python
# Async function — runs directly in the event loop
@app.get("/async")
async def async_endpoint():
    # Use 'await' for async operations
    data = await some_async_function()
    return data

# Sync function — FastAPI runs it in a thread pool
@app.get("/sync")
def sync_endpoint():
    # Regular blocking operations are fine here
    data = some_sync_function()
    return data
```

### Decision Guide:

| Your Code Uses | Use | Why |
|---------------|-----|-----|
| `await` (async DB, httpx, etc.) | `async def` | Direct event loop, most efficient |
| Blocking I/O (sync DB, file ops) | `def` | FastAPI uses thread pool |
| Pure computation, simple returns | Either | Both work fine |
| Not sure | `def` | Safer default, always works |

---

## Key Takeaways

1. **FastAPI apps start with `FastAPI()`** — the app instance is the center of everything
2. **Decorators define routes** — `@app.get("/path")` maps a URL to a function
3. **Return Python types** — FastAPI converts them to JSON automatically
4. **Use Uvicorn to run** — `uvicorn main:app --reload` for development
5. **Both `async def` and `def` work** — use async for I/O, sync for everything else

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Forgetting `--reload` flag | Have to restart manually after changes | Add `--reload` in development |
| Naming file `fastapi.py` | Import conflict with the library | Use `main.py` or any other name |
| Not activating virtual env | Wrong Python/packages used | Always activate before running |
| Using `time.sleep()` in `async def` | Blocks the event loop | Use `asyncio.sleep()` or `def` |

---

## Practice Exercises

1. Create an API with endpoints for `/`, `/about`, and `/health` that return appropriate JSON responses.
2. Add an endpoint `/time` that returns the current date and time (hint: use `datetime.datetime.now()`).
3. Try changing the port to 3000 and accessing the API.
4. Experiment with returning different data types (lists, nested dicts, etc.).

---

> **Next Lesson**: [Interactive Docs →](../03-interactive-docs/)
