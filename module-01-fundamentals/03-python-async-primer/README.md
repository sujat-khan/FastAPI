# Lesson 03 — Python Async Primer

## Why Async Matters for FastAPI

FastAPI is built on top of **Starlette** (an async web framework) and uses Python's **asyncio** library. Understanding async is crucial because:

1. **Performance**: Async allows your API to handle thousands of concurrent requests
2. **Efficiency**: While waiting for I/O (database, external APIs), other requests can be processed
3. **Modern**: Async is the future of Python web development

---

## Sync vs Async — The Coffee Shop Analogy ☕

### Synchronous (Blocking)
Imagine a coffee shop with **one barista** who handles one customer at a time:

```
Customer 1 orders → Barista makes coffee (3 min) → Serves Customer 1
Customer 2 orders → Barista makes coffee (3 min) → Serves Customer 2
Customer 3 orders → Barista makes coffee (3 min) → Serves Customer 3

Total time: 9 minutes 😰
```

### Asynchronous (Non-Blocking)
Now imagine the barista **starts making coffee, and while waiting for it to brew**, takes the next order:

```
Customer 1 orders → Barista starts brewing (waits...)
Customer 2 orders → Barista starts brewing (waits...)
Customer 3 orders → Barista starts brewing (waits...)
Customer 1's coffee ready → Serves Customer 1
Customer 2's coffee ready → Serves Customer 2
Customer 3's coffee ready → Serves Customer 3

Total time: ~4 minutes 🚀
```

> **Key Insight**: Async doesn't make individual tasks faster — it makes **waiting time productive** by handling other work during I/O waits.

---

## Concurrency vs Parallelism

These terms are often confused:

```
┌─ Concurrency ────────────────────────────────────────────┐
│                                                           │
│  Task A: ████░░░░████░░░░████                            │
│  Task B: ░░░░████░░░░████░░░░████                        │
│                                                           │
│  One worker switching between tasks (async/await)         │
│  Like one person juggling multiple conversations          │
└───────────────────────────────────────────────────────────┘

┌─ Parallelism ────────────────────────────────────────────┐
│                                                           │
│  Worker 1 → Task A: ████████████                         │
│  Worker 2 → Task B: ████████████                         │
│                                                           │
│  Multiple workers doing tasks simultaneously              │
│  Like multiple people each having their own conversation  │
└───────────────────────────────────────────────────────────┘
```

| Concept | What | How | Best For |
|---------|------|-----|----------|
| **Concurrency** | Multiple tasks in progress | Single thread, switching | I/O-bound work (network, disk) |
| **Parallelism** | Multiple tasks executing simultaneously | Multiple threads/processes | CPU-bound work (computation) |

> **FastAPI uses concurrency** (async/await) for handling multiple requests efficiently. For CPU-heavy work, it can also use thread/process pools.

---

## Python's `async`/`await` Syntax

### Regular (Synchronous) Function
```python
import time

def get_data():
    print("Fetching data...")
    time.sleep(2)  # Blocks the entire program for 2 seconds
    print("Data received!")
    return {"data": "value"}

# Calling it
result = get_data()
```

### Async Function (Coroutine)
```python
import asyncio

async def get_data():
    print("Fetching data...")
    await asyncio.sleep(2)  # Yields control, other tasks can run
    print("Data received!")
    return {"data": "value"}

# Calling it
result = await get_data()  # Must use 'await' when calling async functions
```

### Key Differences:

| Feature | Sync | Async |
|---------|------|-------|
| Definition | `def function():` | `async def function():` |
| Sleep | `time.sleep(2)` | `await asyncio.sleep(2)` |
| Calling | `result = function()` | `result = await function()` |
| Blocking | Blocks everything | Yields control during waits |

---

## The Event Loop

The **event loop** is the heart of async Python. It manages and schedules all async tasks:

```
┌─────────────────────────────────────────┐
│              EVENT LOOP                  │
│                                          │
│   ┌─────┐  ┌─────┐  ┌─────┐            │
│   │Task1│  │Task2│  │Task3│   ...       │
│   └──┬──┘  └──┬──┘  └──┬──┘            │
│      │        │        │                 │
│   Running  Waiting  Waiting              │
│      │     (I/O)   (I/O)                │
│      │        │        │                 │
│   When Task1 awaits → switches to Task2  │
│   When Task2 awaits → switches to Task3  │
│   When I/O completes → resumes task      │
└─────────────────────────────────────────┘
```

### Running the Event Loop

```python
import asyncio

async def main():
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Run the event loop (Python 3.10+)
asyncio.run(main())
```

> **FastAPI Note**: You never need to call `asyncio.run()` yourself. FastAPI/Uvicorn manages the event loop for you.

---

## Running Multiple Tasks Concurrently

### Sequential (Slow)
```python
import asyncio

async def fetch_user():
    await asyncio.sleep(2)  # Simulates API call
    return {"name": "Alice"}

async def fetch_posts():
    await asyncio.sleep(2)  # Simulates API call
    return [{"title": "Post 1"}, {"title": "Post 2"}]

async def main():
    # These run one after another — 4 seconds total
    user = await fetch_user()   # Wait 2 seconds
    posts = await fetch_posts()  # Wait 2 more seconds
    print(f"User: {user}, Posts: {posts}")

asyncio.run(main())
# Total: ~4 seconds ❌
```

### Concurrent (Fast)
```python
import asyncio

async def fetch_user():
    await asyncio.sleep(2)
    return {"name": "Alice"}

async def fetch_posts():
    await asyncio.sleep(2)
    return [{"title": "Post 1"}, {"title": "Post 2"}]

async def main():
    # These run concurrently — 2 seconds total!
    user, posts = await asyncio.gather(
        fetch_user(),
        fetch_posts()
    )
    print(f"User: {user}, Posts: {posts}")

asyncio.run(main())
# Total: ~2 seconds ✅
```

### `asyncio.gather()` vs `asyncio.create_task()`

```python
import asyncio

async def task(name, seconds):
    print(f"{name} started")
    await asyncio.sleep(seconds)
    print(f"{name} finished")
    return f"{name} result"

async def main():
    # Method 1: asyncio.gather() — run and collect all results
    results = await asyncio.gather(
        task("A", 2),
        task("B", 1),
        task("C", 3)
    )
    print(results)  # ['A result', 'B result', 'C result']

    # Method 2: asyncio.create_task() — more control
    task_a = asyncio.create_task(task("A", 2))
    task_b = asyncio.create_task(task("B", 1))

    # Do other work here while tasks run...

    result_a = await task_a
    result_b = await task_b

asyncio.run(main())
```

---

## Async in FastAPI — How It Works

FastAPI supports both sync and async endpoint functions:

### Async Endpoint (Recommended for I/O-bound work)
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Use 'await' for async operations (database, HTTP calls, etc.)
    user = await database.fetch_user(user_id)
    return user
```

### Sync Endpoint (Fine for simple operations)
```python
@app.get("/hello")
def hello():
    # No async/await needed for simple, non-I/O operations
    return {"message": "Hello, World!"}
```

### When to Use Which?

| Scenario | Use | Why |
|----------|-----|-----|
| Database queries (async driver) | `async def` | Non-blocking I/O |
| External API calls (httpx) | `async def` | Non-blocking I/O |
| Simple computation | `def` | No I/O to wait for |
| File operations | `def` | Standard file I/O is blocking* |
| CPU-heavy processing | `def` | Runs in thread pool automatically |

> **FastAPI's Magic**: When you use a regular `def` (sync function), FastAPI automatically runs it in a **thread pool** so it doesn't block the event loop. So sync functions work fine too — they're just slightly less efficient for I/O-heavy operations.

---

## Common Async Pitfalls

### ❌ Pitfall 1: Using Blocking Code in Async Functions
```python
import time

# BAD — time.sleep() blocks the entire event loop!
@app.get("/bad")
async def bad_endpoint():
    time.sleep(5)  # ❌ Blocks everything
    return {"message": "done"}

# GOOD — asyncio.sleep() yields control
@app.get("/good")
async def good_endpoint():
    await asyncio.sleep(5)  # ✅ Other requests can be handled
    return {"message": "done"}
```

### ❌ Pitfall 2: Forgetting `await`
```python
# BAD — Calling async function without await returns a coroutine object
async def get_user(user_id: int):
    return {"id": user_id}

@app.get("/user/{user_id}")
async def endpoint(user_id: int):
    user = get_user(user_id)  # ❌ Returns <coroutine object>, not the actual data!
    return user

# GOOD
@app.get("/user/{user_id}")
async def endpoint(user_id: int):
    user = await get_user(user_id)  # ✅ Actually executes the function
    return user
```

### ❌ Pitfall 3: Making Sync Database Calls in Async Functions
```python
# BAD — Sync database call blocks the event loop
@app.get("/users")
async def get_users():
    users = db.query(User).all()  # ❌ Blocking!
    return users

# GOOD — Either use async def or remove async
@app.get("/users")
def get_users():  # Note: no 'async' — FastAPI runs in thread pool
    users = db.query(User).all()  # ✅ Runs in thread pool
    return users
```

---

## Key Takeaways

1. **Async is about efficiency** — it doesn't make individual tasks faster, but handles more tasks concurrently
2. **Use `async def` for I/O-bound operations** — database queries, HTTP calls, file I/O
3. **Use regular `def` for CPU-bound or simple tasks** — FastAPI handles them in a thread pool
4. **Always `await` async functions** — forgetting it is a common bug
5. **Never use blocking code in async functions** — use async alternatives (`asyncio.sleep`, `httpx`, async DB drivers)
6. **FastAPI handles most complexity for you** — you just need to know when to use `async def` vs `def`

---

## Practice Exercises

1. Write two async functions that each sleep for 2 seconds. First run them sequentially, then concurrently with `asyncio.gather()`. Compare the total execution time.
2. Modify the example below to run tasks concurrently:
   ```python
   import asyncio

   async def download_file(name, seconds):
       print(f"Downloading {name}...")
       await asyncio.sleep(seconds)
       print(f"{name} downloaded!")
       return f"{name}_data"

   async def main():
       # TODO: Run these concurrently instead of sequentially
       a = await download_file("file_a", 3)
       b = await download_file("file_b", 2)
       c = await download_file("file_c", 1)
       print(f"Results: {a}, {b}, {c}")

   asyncio.run(main())
   ```

---

> **Next Lesson**: [Type Hints & Pydantic →](../04-type-hints-pydantic/)
