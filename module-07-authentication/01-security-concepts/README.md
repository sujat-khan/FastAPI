# Lesson 01 — Security Concepts

## Authentication vs Authorization

| Concept | Question | Example |
|---------|----------|---------|
| **Authentication (AuthN)** | "Who are you?" | Login with username/password |
| **Authorization (AuthZ)** | "What can you do?" | Admin can delete, user can only read |

```
User sends credentials → Authentication (verify identity)
                              ↓
                        Authorization (check permissions)
                              ↓
                        Access granted/denied
```

---

## Common Authentication Methods

### 1. API Keys
Simple token in the header:
```
GET /api/data
X-API-Key: abc123xyz
```

**Pros**: Simple to implement
**Cons**: No built-in expiration, no user context

### 2. HTTP Basic Auth
Username:password encoded in Base64:
```
GET /api/data
Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=
```

**Pros**: Simple, universally supported
**Cons**: Password sent with every request, needs HTTPS

### 3. JWT (JSON Web Tokens) ⭐
Token-based authentication — the modern standard:
```
GET /api/data
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Pros**: Stateless, contains user info, has expiration
**Cons**: Slightly more complex, token can't be revoked without extra work

### 4. OAuth2
Industry-standard protocol for authorization:
- Used by Google, GitHub, Facebook, etc.
- Supports multiple flows (password, authorization code, etc.)

> **FastAPI has built-in OAuth2 support** — we'll use it in this module!

---

## JWT Token Structure

A JWT has three parts separated by dots:

```
eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMSJ9.signature
├── Header ──────────┤├── Payload ───────────┤├── Signature ┤
```

| Part | Contains | Purpose |
|------|----------|---------|
| **Header** | Algorithm, token type | How to verify the token |
| **Payload** | User data, expiration | Who the user is, when token expires |
| **Signature** | Cryptographic hash | Proves the token hasn't been tampered with |

### Payload Example:
```json
{
    "sub": "user@example.com",
    "exp": 1705312800,
    "role": "admin",
    "iat": 1705309200
}
```

| Claim | Meaning |
|-------|---------|
| `sub` | Subject (user identifier) |
| `exp` | Expiration time (Unix timestamp) |
| `iat` | Issued at (when token was created) |
| `role` | Custom claim (user's role) |

---

## OAuth2 Password Flow

This is the flow we'll implement with FastAPI:

```
1. Client sends username + password to /token endpoint
2. Server verifies credentials
3. Server creates JWT token
4. Server returns token to client
5. Client sends token in Authorization header for subsequent requests
6. Server verifies token on each request

┌──────┐                              ┌──────┐
│Client│                              │Server│
└──┬───┘                              └──┬───┘
   │  POST /token                        │
   │  {username, password}               │
   │ ───────────────────────────────────→ │
   │                                      │ Verify credentials
   │                                      │ Create JWT
   │  {access_token, token_type}         │
   │ ←─────────────────────────────────── │
   │                                      │
   │  GET /users/me                       │
   │  Authorization: Bearer <token>       │
   │ ───────────────────────────────────→ │
   │                                      │ Verify token
   │  {user data}                         │
   │ ←─────────────────────────────────── │
```

---

## Key Takeaways

1. **Authentication = who, Authorization = what**
2. **JWT is the modern standard** for API authentication
3. **OAuth2 Password Flow** works great for first-party apps
4. **Always use HTTPS** in production — tokens are sensitive
5. **FastAPI has built-in security utilities** — makes implementation easy

---

> **Next Lesson**: [Password Hashing →](../02-password-hashing/)
