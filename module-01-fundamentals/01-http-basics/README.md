# Lesson 01 — HTTP Basics

## What is HTTP?

**HTTP (HyperText Transfer Protocol)** is the foundation of data communication on the web. Every time you visit a website, submit a form, or use an API, HTTP is the protocol carrying your data between the client (browser, app, script) and the server.

Think of HTTP like a **conversation** between two people:
- The **client** asks a question (request)
- The **server** gives an answer (response)

---

## The Request-Response Cycle

```
┌──────────┐         HTTP Request          ┌──────────┐
│          │  ──────────────────────────►   │          │
│  Client  │     GET /api/users            │  Server  │
│          │     Host: example.com         │          │
│          │                               │          │
│          │         HTTP Response          │          │
│          │  ◄──────────────────────────   │          │
│          │     200 OK                    │          │
│          │     {"users": [...]}          │          │
└──────────┘                               └──────────┘
```

### Anatomy of an HTTP Request

Every HTTP request has these parts:

```
POST /api/users HTTP/1.1          ← Request Line (Method + Path + HTTP Version)
Host: example.com                 ← Headers (metadata about the request)
Content-Type: application/json
Authorization: Bearer token123

{                                 ← Body (data sent to server, optional)
  "name": "Alice",
  "email": "alice@example.com"
}
```

### Anatomy of an HTTP Response

```
HTTP/1.1 201 Created             ← Status Line (HTTP Version + Status Code + Reason)
Content-Type: application/json   ← Headers (metadata about the response)
X-Request-Id: abc123

{                                ← Body (data returned by server)
  "id": 1,
  "name": "Alice",
  "email": "alice@example.com"
}
```

---

## HTTP Methods (Verbs)

HTTP methods tell the server **what action** to perform. These are the most important ones:

| Method | Purpose | Has Body? | Idempotent? | Safe? |
|--------|---------|-----------|-------------|-------|
| `GET` | Retrieve data | ❌ No | ✅ Yes | ✅ Yes |
| `POST` | Create new data | ✅ Yes | ❌ No | ❌ No |
| `PUT` | Replace/update entire resource | ✅ Yes | ✅ Yes | ❌ No |
| `PATCH` | Partially update a resource | ✅ Yes | ❌ No | ❌ No |
| `DELETE` | Remove a resource | ❌ No | ✅ Yes | ❌ No |
| `HEAD` | Like GET but no body in response | ❌ No | ✅ Yes | ✅ Yes |
| `OPTIONS` | Discover allowed methods | ❌ No | ✅ Yes | ✅ Yes |

### Key Terms:

- **Idempotent**: Making the same request multiple times produces the same result. `PUT /users/1` with the same data always results in the same state.
- **Safe**: The request doesn't modify the server state. `GET` only reads data.

### Real-World Analogy:

| HTTP Method | Real World |
|-------------|------------|
| `GET` | Looking up a contact in your phone |
| `POST` | Adding a new contact |
| `PUT` | Replacing all info for a contact |
| `PATCH` | Updating just the phone number |
| `DELETE` | Deleting a contact |

---

## HTTP Status Codes

Status codes tell the client **what happened** with their request. They're grouped into 5 categories:

### 1xx — Informational
Rarely used directly. The server is still processing.

| Code | Meaning |
|------|---------|
| `100` | Continue |
| `101` | Switching Protocols |

### 2xx — Success ✅
The request was successful!

| Code | Meaning | When Used |
|------|---------|-----------|
| `200` | OK | General success (GET, PUT, PATCH) |
| `201` | Created | A new resource was created (POST) |
| `204` | No Content | Success but nothing to return (DELETE) |

### 3xx — Redirection ↪️
The resource has moved somewhere else.

| Code | Meaning | When Used |
|------|---------|-----------|
| `301` | Moved Permanently | URL has permanently changed |
| `302` | Found (Temporary Redirect) | Temporary redirect |
| `304` | Not Modified | Cached version is still valid |

### 4xx — Client Error ❌
The client made a mistake.

| Code | Meaning | When Used |
|------|---------|-----------|
| `400` | Bad Request | Invalid data sent |
| `401` | Unauthorized | Not authenticated (no/invalid credentials) |
| `403` | Forbidden | Authenticated but not authorized |
| `404` | Not Found | Resource doesn't exist |
| `405` | Method Not Allowed | Wrong HTTP method for this endpoint |
| `409` | Conflict | Conflicts with current state (e.g., duplicate) |
| `422` | Unprocessable Entity | Validation error (FastAPI uses this!) |
| `429` | Too Many Requests | Rate limit exceeded |

### 5xx — Server Error 💥
Something went wrong on the server.

| Code | Meaning | When Used |
|------|---------|-----------|
| `500` | Internal Server Error | Unhandled exception |
| `502` | Bad Gateway | Upstream server error |
| `503` | Service Unavailable | Server is overloaded or down |

> **FastAPI Tip**: FastAPI returns `422 Unprocessable Entity` when request validation fails (e.g., wrong data type in path parameter). This is different from most frameworks that return `400`.

---

## HTTP Headers

Headers provide **metadata** about the request or response. They're key-value pairs.

### Common Request Headers:

| Header | Purpose | Example |
|--------|---------|---------|
| `Content-Type` | Format of the request body | `application/json` |
| `Accept` | What format the client wants back | `application/json` |
| `Authorization` | Authentication credentials | `Bearer eyJhbG...` |
| `User-Agent` | Client software info | `Mozilla/5.0...` |
| `Host` | Target server domain | `api.example.com` |

### Common Response Headers:

| Header | Purpose | Example |
|--------|---------|---------|
| `Content-Type` | Format of the response body | `application/json` |
| `Content-Length` | Size of response body in bytes | `1234` |
| `Set-Cookie` | Set a cookie on the client | `session=abc123` |
| `X-Request-Id` | Unique request identifier | `uuid-value` |
| `Cache-Control` | Caching instructions | `max-age=3600` |

> **Note**: Headers starting with `X-` are custom headers. This convention is technically deprecated but still widely used.

---

## Content Types (MIME Types)

The `Content-Type` header tells the receiver how to interpret the body:

| Content Type | Description | Used For |
|-------------|-------------|----------|
| `application/json` | JSON data | APIs (most common) |
| `text/html` | HTML document | Web pages |
| `text/plain` | Plain text | Simple text |
| `multipart/form-data` | Form data with files | File uploads |
| `application/x-www-form-urlencoded` | URL-encoded form data | HTML forms |

> **FastAPI**: By default, FastAPI sends and receives `application/json`. This is the standard for modern APIs.

---

## Putting It All Together — A Real Example

Let's trace a complete HTTP conversation for creating a user:

### Step 1: Client Sends Request
```
POST /api/users HTTP/1.1
Host: myapi.example.com
Content-Type: application/json
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiJ9...

{
    "name": "Bob",
    "email": "bob@example.com",
    "age": 30
}
```

### Step 2: Server Processes Request
1. Server receives the request
2. Checks the `Authorization` header → valid token ✅
3. Reads the JSON body
4. Validates the data
5. Creates the user in the database
6. Sends back a response

### Step 3: Server Sends Response
```
HTTP/1.1 201 Created
Content-Type: application/json
Location: /api/users/42

{
    "id": 42,
    "name": "Bob",
    "email": "bob@example.com",
    "age": 30,
    "created_at": "2025-01-15T10:30:00Z"
}
```

---

## Key Takeaways

1. **HTTP is stateless** — each request is independent; the server doesn't remember previous requests
2. **Methods define intent** — use the right method for the right action
3. **Status codes communicate results** — they tell the client what happened
4. **Headers carry metadata** — they provide context about the request/response
5. **JSON is the standard** — modern APIs almost always use JSON for data exchange

---

## Common Mistakes

| Mistake | Why It's Wrong | Correct Approach |
|---------|---------------|-----------------|
| Using GET to create data | GET is for reading only | Use POST for creation |
| Returning 200 for errors | Misleads the client | Use appropriate 4xx/5xx codes |
| Ignoring Content-Type | Server may reject the request | Always set Content-Type header |
| Using POST for everything | Breaks REST conventions | Match method to action |

---

## Practice Exercises

1. Open your browser's Developer Tools (F12) → Network tab, visit any website, and examine the HTTP requests and responses
2. Use a tool like `curl` to make a GET request:
   ```bash
   curl -v https://httpbin.org/get
   ```
3. Try different methods with httpbin.org:
   ```bash
   curl -X POST https://httpbin.org/post -H "Content-Type: application/json" -d '{"name": "test"}'
   ```

---

> **Next Lesson**: [REST API Concepts →](../02-rest-api-concepts/)
