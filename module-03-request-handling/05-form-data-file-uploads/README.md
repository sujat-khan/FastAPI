# Lesson 05 — Form Data & File Uploads

## Form Data vs JSON

By default, FastAPI expects **JSON** request bodies. But HTML forms send data in a different format:

| Format | Content-Type | Used For |
|--------|-------------|----------|
| JSON | `application/json` | API clients, JavaScript |
| Form data | `application/x-www-form-urlencoded` | Simple HTML forms |
| Multipart | `multipart/form-data` | Forms with file uploads |

> **Prerequisite**: Install `python-multipart` for form/file support:
> ```bash
> pip install python-multipart
> ```
> (Already included in `fastapi[standard]`)

---

## Basic Form Data

```python
from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login")
async def login(
    username: str = Form(),
    password: str = Form(),
):
    """
    Reads form fields from application/x-www-form-urlencoded body.
    NOT from JSON — this is what HTML <form> elements send.
    """
    return {"username": username}
```

> **Important**: You CANNOT mix `Form()` and Pydantic body models in the same endpoint. Form data and JSON are different content types.

### HTML Form That Sends This:
```html
<form method="POST" action="/login">
    <input type="text" name="username" />
    <input type="password" name="password" />
    <button type="submit">Login</button>
</form>
```

### Form Data with Validation
```python
@app.post("/register")
async def register(
    username: str = Form(min_length=3, max_length=30),
    email: str = Form(),
    password: str = Form(min_length=8),
    age: int = Form(ge=18),
):
    return {"username": username, "email": email, "age": age}
```

---

## File Uploads

### Simple File Upload with `bytes`

```python
from fastapi import File

@app.post("/upload")
async def upload_file(
    file: bytes = File(description="The file to upload"),
):
    """
    Reads the entire file into memory as bytes.
    ⚠️ Only for SMALL files — loads everything into RAM!
    """
    return {"file_size": len(file)}
```

### Better: Using `UploadFile` (Recommended)

```python
from fastapi import UploadFile

@app.post("/upload")
async def upload_file(file: UploadFile):
    """
    UploadFile uses a spooled file — writes to disk for large files.
    Much more memory-efficient than bytes!
    """
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": file.size,
    }
```

### `UploadFile` Attributes and Methods

| Attribute/Method | Description |
|-----------------|-------------|
| `file.filename` | Original filename |
| `file.content_type` | MIME type (e.g., "image/png") |
| `file.size` | File size in bytes |
| `await file.read()` | Read the file content |
| `await file.read(size)` | Read `size` bytes |
| `await file.write(data)` | Write data to file |
| `await file.seek(offset)` | Move to position in file |
| `await file.close()` | Close the file |

### Reading File Content

```python
@app.post("/upload")
async def upload_file(file: UploadFile):
    # Read the entire file
    content = await file.read()

    # Process it...
    line_count = content.decode("utf-8").count("\n")

    # Reset position if you need to read again
    await file.seek(0)

    return {
        "filename": file.filename,
        "size": len(content),
        "lines": line_count,
    }
```

### Saving Uploaded Files

```python
import shutil
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_file(file: UploadFile):
    file_path = UPLOAD_DIR / file.filename

    # Method 1: Read and write
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Method 2: Stream (better for large files)
    # with open(file_path, "wb") as f:
    #     shutil.copyfileobj(file.file, f)

    return {"filename": file.filename, "saved_to": str(file_path)}
```

---

## Multiple File Uploads

```python
from fastapi import UploadFile

@app.post("/upload-multiple")
async def upload_files(files: list[UploadFile]):
    """Accept multiple files at once."""
    results = []
    for file in files:
        content = await file.read()
        results.append({
            "filename": file.filename,
            "size": len(content),
            "type": file.content_type,
        })
    return {"uploaded": len(results), "files": results}
```

---

## Combining Files and Form Data

```python
@app.post("/create-post")
async def create_post(
    title: str = Form(),
    content: str = Form(),
    tags: str = Form(default=""),
    image: UploadFile | None = None,     # Optional file
):
    """Upload a blog post with an optional image."""
    result = {
        "title": title,
        "content": content,
        "tags": tags.split(",") if tags else [],
    }
    if image:
        result["image"] = {
            "filename": image.filename,
            "type": image.content_type,
        }
    return result
```

---

## File Validation

```python
from fastapi import HTTPException

ALLOWED_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
MAX_SIZE = 5 * 1024 * 1024  # 5 MB

@app.post("/upload-image")
async def upload_image(file: UploadFile):
    """Upload an image with type and size validation."""

    # Validate content type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"File type '{file.content_type}' not allowed. "
                   f"Allowed: {ALLOWED_TYPES}",
        )

    # Read and validate size
    content = await file.read()
    if len(content) > MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {MAX_SIZE // 1024 // 1024}MB",
        )

    return {
        "filename": file.filename,
        "type": file.content_type,
        "size_kb": len(content) / 1024,
    }
```

---

## Key Takeaways

1. **`Form()` reads form data** — different from JSON (Pydantic models)
2. **`UploadFile` is preferred** over `bytes` for file uploads — memory efficient
3. **You can't mix Form and JSON** in the same endpoint
4. **Files + Form work together** — use `multipart/form-data`
5. **Always validate uploads** — check file type and size
6. **Use `await` for file operations** — `read()`, `write()`, `seek()`

---

> **Next Module**: [Module 04 — Response Handling & Data Validation →](../../module-04-response-validation/)
