# Lesson 02 — Background Tasks

## What Are Background Tasks?

Background tasks run **after the response is sent** to the client. The client doesn't wait for them.

```
Client sends request
    ↓
Server processes request
    ↓
Server sends response to client     ← Client gets response here
    ↓
Background task runs                 ← Client doesn't wait for this
```

---

## Basic Usage

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def write_log(message: str):
    """This runs after the response is sent."""
    with open("log.txt", "a") as f:
        f.write(f"{message}\n")

@app.post("/items")
async def create_item(name: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Item created: {name}")
    return {"message": f"Item '{name}' created"}
    # Response sent immediately, logging happens in background
```

---

## Real-World Examples

### Sending Emails
```python
def send_email(email: str, subject: str, body: str):
    """Send email after user registration."""
    import smtplib
    # Email sending logic here...
    print(f"Email sent to {email}: {subject}")

@app.post("/register")
async def register(
    email: str,
    background_tasks: BackgroundTasks,
):
    # Create user immediately
    user = create_user(email)

    # Send welcome email in background
    background_tasks.add_task(
        send_email,
        email,
        "Welcome!",
        "Thanks for registering!",
    )

    return {"message": "User registered!"}
    # User gets response fast, email sends in background
```

### Multiple Background Tasks
```python
@app.post("/orders")
async def create_order(background_tasks: BackgroundTasks):
    order = process_order()

    # Queue multiple background tasks
    background_tasks.add_task(send_confirmation_email, order)
    background_tasks.add_task(update_inventory, order)
    background_tasks.add_task(notify_warehouse, order)

    return {"order_id": order.id}
```

---

## Background Tasks in Dependencies

```python
def write_audit_log(
    background_tasks: BackgroundTasks,
    user = Depends(get_current_user),
):
    """Dependency that adds audit logging as a background task."""
    def _log():
        print(f"Audit: {user.username} accessed the system")

    background_tasks.add_task(_log)
    return user

@app.get("/data")
async def get_data(user = Depends(write_audit_log)):
    return {"data": "sensitive"}
```

---

## When to Use Background Tasks vs Celery

| Feature | BackgroundTasks | Celery/Redis |
|---------|----------------|--------------|
| Setup | Zero config | Requires broker (Redis/RabbitMQ) |
| Runs in | Same process | Separate worker process |
| Good for | Quick tasks (< 10s) | Long-running jobs (minutes/hours) |
| Retry | No built-in | Built-in retry with backoff |
| Monitoring | None | Flower, logging |
| Examples | Emails, logging | Video processing, ML training |

---

## Key Takeaways

1. **Background tasks run after response** — client doesn't wait
2. **Use `BackgroundTasks` parameter** — FastAPI injects it
3. **`add_task(function, *args)`** — queue tasks easily
4. **Good for quick tasks** — emails, logging, notifications
5. **For heavy jobs** → use Celery, Redis Queue, or similar

---

> **Next Lesson**: [WebSockets →](../03-websockets/)
