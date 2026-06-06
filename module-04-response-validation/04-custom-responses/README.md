# Lesson 04 — Custom Responses

## Beyond JSON — Different Response Types

FastAPI returns JSON by default, but you can return many other formats.

---

## Available Response Classes

```python
from fastapi.responses import (
    JSONResponse,       # JSON (default)
    HTMLResponse,       # HTML pages
    PlainTextResponse,  # Plain text
    RedirectResponse,   # Redirect to URL
    StreamingResponse,  # Stream data
    FileResponse,       # Send a file
)
```

### JSONResponse (Default)
```python
from fastapi.responses import JSONResponse

@app.get("/custom-json")
async def custom_json():
    return JSONResponse(
        content={"message": "Custom JSON"},
        status_code=200,
        headers={"X-Custom": "value"},
    )
```

### HTMLResponse
```python
from fastapi.responses import HTMLResponse

@app.get("/page", response_class=HTMLResponse)
async def get_page():
    return """
    <html>
        <head><title>My Page</title></head>
        <body>
            <h1>Hello from FastAPI!</h1>
            <p>This is an HTML response.</p>
        </body>
    </html>
    """
```

### PlainTextResponse
```python
from fastapi.responses import PlainTextResponse

@app.get("/text", response_class=PlainTextResponse)
async def get_text():
    return "Just plain text, no JSON wrapping."
```

### RedirectResponse
```python
from fastapi.responses import RedirectResponse

@app.get("/old-page")
async def old_page():
    return RedirectResponse(url="/new-page", status_code=301)

@app.get("/google")
async def go_to_google():
    return RedirectResponse(url="https://google.com")
```

### FileResponse
```python
from fastapi.responses import FileResponse

@app.get("/download")
async def download_file():
    return FileResponse(
        path="files/report.pdf",
        filename="report.pdf",           # Name shown in download dialog
        media_type="application/pdf",
    )
```

### StreamingResponse
```python
from fastapi.responses import StreamingResponse
import io

@app.get("/stream")
async def stream_data():
    def generate():
        for i in range(100):
            yield f"data: line {i}\n"

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )

# Stream a large file without loading into memory
@app.get("/large-file")
async def stream_large_file():
    def iterfile():
        with open("large_file.csv", "rb") as f:
            while chunk := f.read(1024 * 64):  # 64KB chunks
                yield chunk

    return StreamingResponse(iterfile(), media_type="text/csv")
```

---

## Setting Default Response Class

```python
# All endpoints return HTML by default
app = FastAPI(default_response_class=HTMLResponse)

# Override per-endpoint
@app.get("/api/data", response_class=JSONResponse)
async def api_data():
    return {"key": "value"}
```

---

## Key Takeaways

1. **JSONResponse is the default** — returned automatically for dicts/models
2. **HTMLResponse for web pages** — useful with templates (Module 08)
3. **StreamingResponse for large data** — memory-efficient
4. **FileResponse for downloads** — serves files from disk
5. **RedirectResponse for redirects** — 301 (permanent) or 302 (temporary)

---

> **Next Lesson**: [Error Handling →](../05-error-handling/)
