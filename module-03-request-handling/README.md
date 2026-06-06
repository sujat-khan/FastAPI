# Module 03 — Request Handling In-Depth

Master all the ways data flows into your FastAPI endpoints — from URL segments to file uploads.

---

## Lessons

| # | Lesson | Topics |
|---|--------|--------|
| 01 | [Path Parameters](./01-path-parameters/) | Dynamic URL segments, type validation, `Path()` |
| 02 | [Query Parameters](./02-query-parameters/) | Optional/required params, defaults, `Query()` |
| 03 | [Request Body](./03-request-body/) | Pydantic models, nested bodies, multiple bodies |
| 04 | [Headers & Cookies](./04-headers-cookies/) | Reading/setting headers and cookies |
| 05 | [Form Data & File Uploads](./05-form-data-file-uploads/) | `Form()`, `File()`, `UploadFile` |

---

## The Big Picture

FastAPI receives data from clients in 5 main ways:

```
URL: https://api.example.com/users/42?active=true
     ├── Path Params ──┘          └── Query Params
     │
Headers: Authorization: Bearer token123
         Content-Type: application/json
     │
Cookies: session=abc123
     │
Body: {"name": "Alice", "email": "alice@test.com"}
     │
Files: <binary file data>
```

Each lesson covers one of these data sources in detail.
