# Lesson 04 — OAuth2 with Scopes

## What Are Scopes?

Scopes define **what a token is allowed to do** — they're the authorization part of OAuth2.

```
Token with scopes: ["read:users", "write:users"]
→ Can read and write users
→ Cannot access admin endpoints (missing "admin" scope)
```

---

## Implementation

```python
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "read:users": "Read user information",
        "write:users": "Create and modify users",
        "admin": "Full administrative access",
    },
)

async def get_current_user(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
):
    """Verify token AND check required scopes."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": f'Bearer scope="{security_scopes.scope_str}"'},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_scopes = payload.get("scopes", [])
    except JWTError:
        raise credentials_exception

    # Check that token has all required scopes
    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Not enough permissions. Required: {scope}",
            )

    user = get_user(username)
    if user is None:
        raise credentials_exception
    return user

# Use Security() instead of Depends() to specify required scopes
@app.get("/users/me")
async def read_users_me(
    user = Security(get_current_user, scopes=["read:users"]),
):
    return user

@app.post("/users")
async def create_user(
    user = Security(get_current_user, scopes=["write:users"]),
):
    return {"action": "created"}

@app.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    user = Security(get_current_user, scopes=["admin"]),
):
    return {"action": "deleted", "user_id": user_id}
```

---

## Creating Tokens with Scopes

```python
def create_access_token(data: dict, scopes: list[str]):
    to_encode = data.copy()
    to_encode.update({
        "scopes": scopes,
        "exp": datetime.utcnow() + timedelta(minutes=30),
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Admin token
admin_token = create_access_token(
    data={"sub": "alice"},
    scopes=["read:users", "write:users", "admin"],
)

# Regular user token
user_token = create_access_token(
    data={"sub": "bob"},
    scopes=["read:users"],
)
```

---

## Key Takeaways

1. **Scopes = fine-grained permissions** in the token
2. **`Security()` replaces `Depends()`** when scopes are needed
3. **Check scopes in the dependency** — compare required vs token scopes
4. **Swagger UI shows scopes** — users can select which scopes to request

---

> **Next Lesson**: [Protecting Routes →](../05-protecting-routes/)
