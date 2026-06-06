# Lesson 02 — REST API Concepts

## What is an API?

**API (Application Programming Interface)** is a set of rules that allows different software applications to communicate with each other. Think of it as a **waiter in a restaurant**:

- You (client) look at the menu and tell the waiter what you want
- The waiter (API) takes your order to the kitchen (server)
- The kitchen prepares your food and gives it to the waiter
- The waiter brings it back to you

You don't need to know how the kitchen works — you just need to know **what to order** (the API contract).

---

## What is REST?

**REST (REpresentational State Transfer)** is an **architectural style** for designing APIs. It was introduced by Roy Fielding in his 2000 doctoral dissertation.

REST is NOT a protocol or standard — it's a set of **constraints/principles** that, when followed, create scalable and maintainable APIs.

---

## The 6 REST Constraints

### 1. Client-Server Separation
The client and server are independent. The client doesn't know how the server stores data, and the server doesn't know about the client's UI.

```
✅ Client handles: UI, user experience
✅ Server handles: Data storage, business logic
```

### 2. Statelessness
Each request from the client must contain **all the information** the server needs. The server does NOT store any client context between requests.

```
❌ BAD:  Server remembers "User #5 logged in on request #1"
✅ GOOD: Every request includes authentication token
```

### 3. Cacheability
Responses must define themselves as cacheable or non-cacheable. This improves performance by reducing unnecessary server calls.

```
Cache-Control: max-age=3600    ← "Cache this response for 1 hour"
Cache-Control: no-cache        ← "Don't cache this"
```

### 4. Uniform Interface
The API should have a consistent, predictable structure. This is the most important REST constraint and includes:
- **Resource identification** through URIs
- **Resource manipulation** through representations (JSON)
- **Self-descriptive messages** (headers tell you how to process the data)
- **HATEOAS** — Hypermedia as the Engine of Application State (links in responses)

### 5. Layered System
The client shouldn't know whether it's talking directly to the server or through a load balancer, cache, or proxy.

```
Client → Load Balancer → API Gateway → Server → Database
(Client only sees the first step)
```

### 6. Code on Demand (Optional)
The server can send executable code to the client (e.g., JavaScript). This is optional and rarely used in REST APIs.

---

## Resources — The Core of REST

In REST, everything is a **resource**. A resource is any piece of data that can be named:

| Resource | URI | Description |
|----------|-----|-------------|
| All users | `/api/users` | A collection of user resources |
| Single user | `/api/users/42` | A specific user (ID=42) |
| User's posts | `/api/users/42/posts` | Posts belonging to user 42 |
| Single post | `/api/posts/7` | A specific post (ID=7) |

### Resource Naming Best Practices

| ✅ Do | ❌ Don't | Why |
|-------|---------|-----|
| `/users` | `/getUsers` | Use nouns, not verbs |
| `/users/42` | `/user/42` | Use plural nouns for collections |
| `/users/42/posts` | `/getUserPosts?id=42` | Use path hierarchy for relationships |
| `/blog-posts` | `/blog_posts` or `/blogPosts` | Use hyphens, not underscores or camelCase |
| `/users?status=active` | `/active-users` | Use query params for filtering |

---

## CRUD Operations Mapped to HTTP Methods

**CRUD** stands for Create, Read, Update, Delete — the four basic operations on data:

| CRUD Operation | HTTP Method | URL Example | Description |
|---------------|-------------|-------------|-------------|
| **C**reate | `POST` | `POST /api/users` | Create a new user |
| **R**ead (all) | `GET` | `GET /api/users` | Get all users |
| **R**ead (one) | `GET` | `GET /api/users/42` | Get user by ID |
| **U**pdate (full) | `PUT` | `PUT /api/users/42` | Replace entire user |
| **U**pdate (partial) | `PATCH` | `PATCH /api/users/42` | Update some fields |
| **D**elete | `DELETE` | `DELETE /api/users/42` | Delete user |

### Complete Example — Blog API

```
GET    /api/posts              → List all blog posts
GET    /api/posts/5            → Get post #5
POST   /api/posts              → Create a new post
PUT    /api/posts/5            → Replace post #5 entirely
PATCH  /api/posts/5            → Update post #5 partially
DELETE /api/posts/5            → Delete post #5

GET    /api/posts/5/comments   → List comments on post #5
POST   /api/posts/5/comments   → Add a comment to post #5
```

---

## JSON — The Language of REST APIs

**JSON (JavaScript Object Notation)** is the standard data format for REST APIs. It's human-readable and machine-parseable.

### JSON Data Types

```json
{
    "string": "Hello, World!",
    "number_int": 42,
    "number_float": 3.14,
    "boolean": true,
    "null_value": null,
    "array": [1, 2, 3, "four"],
    "object": {
        "nested_key": "nested_value"
    }
}
```

### JSON in Python

Python's dictionaries map directly to JSON:

```python
import json

# Python dict → JSON string
data = {"name": "Alice", "age": 30, "active": True}
json_string = json.dumps(data)
# '{"name": "Alice", "age": 30, "active": true}'

# JSON string → Python dict
parsed = json.loads(json_string)
# {'name': 'Alice', 'age': 30, 'active': True}
```

> **Note**: Python `True`/`False`/`None` become JSON `true`/`false`/`null`.

---

## API Design Example — User Management

Let's design a complete REST API for managing users:

### Endpoints

| Method | Endpoint | Request Body | Response | Status |
|--------|----------|-------------|----------|--------|
| `GET` | `/api/users` | — | List of users | `200` |
| `GET` | `/api/users/{id}` | — | Single user | `200` / `404` |
| `POST` | `/api/users` | User data | Created user | `201` |
| `PUT` | `/api/users/{id}` | Full user data | Updated user | `200` / `404` |
| `PATCH` | `/api/users/{id}` | Partial data | Updated user | `200` / `404` |
| `DELETE` | `/api/users/{id}` | — | — | `204` / `404` |

### Request/Response Examples

**Create a User:**
```
POST /api/users
Content-Type: application/json

{
    "name": "Alice",
    "email": "alice@example.com",
    "role": "admin"
}
```

**Response:**
```
HTTP/1.1 201 Created
Content-Type: application/json

{
    "id": 1,
    "name": "Alice",
    "email": "alice@example.com",
    "role": "admin",
    "created_at": "2025-01-15T10:00:00Z"
}
```

**List Users with Filtering:**
```
GET /api/users?role=admin&page=1&limit=10
```

**Response:**
```json
{
    "data": [
        {"id": 1, "name": "Alice", "role": "admin"},
        {"id": 5, "name": "Bob", "role": "admin"}
    ],
    "total": 2,
    "page": 1,
    "limit": 10
}
```

---

## Query Parameters for Common Operations

| Purpose | Parameter | Example |
|---------|-----------|---------|
| Filtering | `?status=active` | `GET /api/users?status=active` |
| Sorting | `?sort=name&order=asc` | `GET /api/users?sort=name&order=desc` |
| Pagination | `?page=2&limit=20` | `GET /api/users?page=2&limit=20` |
| Searching | `?q=alice` | `GET /api/users?q=alice` |
| Field selection | `?fields=name,email` | `GET /api/users?fields=name,email` |

---

## REST vs Other API Styles

| Feature | REST | GraphQL | gRPC |
|---------|------|---------|------|
| Protocol | HTTP | HTTP | HTTP/2 |
| Data Format | JSON | JSON | Protobuf (binary) |
| Learning Curve | Low | Medium | High |
| Over-fetching | Possible | Solved | Solved |
| Best For | General APIs | Complex queries | Microservices |
| Real-time | Via polling/SSE | Subscriptions | Streams |

> **FastAPI** primarily builds REST APIs, but it also supports WebSockets for real-time communication (covered in Module 08).

---

## Key Takeaways

1. **REST is about resources** — think in terms of nouns (users, posts, orders), not actions
2. **HTTP methods define the action** — the URL identifies WHAT, the method defines HOW
3. **Use proper status codes** — they communicate the outcome clearly
4. **Keep it consistent** — predictable APIs are easier to use
5. **JSON is the standard** — FastAPI handles JSON serialization/deserialization automatically

---

## Common Mistakes

| Mistake | Why It's Wrong | Correct |
|---------|---------------|---------|
| `GET /getUser/42` | Verb in URL | `GET /users/42` |
| `POST /users/42/delete` | Action in URL | `DELETE /users/42` |
| `GET /user` | Singular collection | `GET /users` |
| Returning 200 for everything | Hides errors | Use proper status codes |
| Deeply nested URLs | Too complex | Max 2 levels: `/users/42/posts` |

---

## Practice Exercises

1. Design a REST API for a **library system** with books, authors, and borrowers. Write down the endpoints, methods, and expected responses.
2. Look at a public API like [JSONPlaceholder](https://jsonplaceholder.typicode.com/) and identify the REST patterns.
3. Think about what makes a URL "RESTful" vs "not RESTful" and list 5 examples of each.

---

> **Next Lesson**: [Python Async Primer →](../03-python-async-primer/)
