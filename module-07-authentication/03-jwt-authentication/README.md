# Lesson 03 — JWT Authentication

## Complete JWT Auth Implementation

This is the most important lesson in the auth module. We'll build a complete login system.

---

## Installation

```bash
pip install "python-jose[cryptography]" "passlib[bcrypt]"
```

---

## Complete Implementation

```python
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# ============================================================
# Configuration
# ============================================================
SECRET_KEY = "your-secret-key-keep-this-safe"  # Use env variable in production!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme — tells FastAPI to look for Bearer token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ============================================================
# Models
# ============================================================
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None
    disabled: bool = False

class UserInDB(User):
    hashed_password: str


# ============================================================
# Fake Database
# ============================================================
fake_users_db = {
    "alice": {
        "username": "alice",
        "email": "alice@example.com",
        "full_name": "Alice Wonderland",
        "disabled": False,
        "hashed_password": pwd_context.hash("secret123"),
    },
    "bob": {
        "username": "bob",
        "email": "bob@example.com",
        "full_name": "Bob Builder",
        "disabled": True,
        "hashed_password": pwd_context.hash("password456"),
    },
}


# ============================================================
# Helper Functions
# ============================================================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db: dict, username: str) -> UserInDB | None:
    if username in db:
        return UserInDB(**db[username])
    return None

def authenticate_user(db: dict, username: str, password: str) -> UserInDB | None:
    user = get_user(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ============================================================
# Dependencies
# ============================================================
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """Extract and validate user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Ensure the user is not disabled."""
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# ============================================================
# Endpoints
# ============================================================
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login endpoint — exchange username/password for JWT token.

    Uses OAuth2PasswordRequestForm which expects:
    - username (form field)
    - password (form field)
    """
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get the current logged-in user's profile."""
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """Get items belonging to the current user."""
    return [{"item_id": "Foo", "owner": current_user.username}]
```

---

## How to Use

### 1. Get a Token
```bash
curl -X POST "http://localhost:8000/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice&password=secret123"
```

Response:
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "bearer"
}
```

### 2. Use the Token
```bash
curl -X GET "http://localhost:8000/users/me" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."
```

### 3. In Swagger UI
Click the 🔒 "Authorize" button → enter username and password → all endpoints auto-include the token!

---

## The Auth Flow Diagram

```
Client                          Server
  │                                │
  │ POST /token                    │
  │ username=alice                 │
  │ password=secret123             │
  │──────────────────────────────→ │
  │                                │ 1. Find user "alice"
  │                                │ 2. Verify password hash
  │                                │ 3. Create JWT with sub="alice"
  │ {access_token: "eyJ...",       │
  │  token_type: "bearer"}        │
  │ ←────────────────────────────── │
  │                                │
  │ GET /users/me                  │
  │ Authorization: Bearer eyJ...   │
  │──────────────────────────────→ │
  │                                │ 1. Extract token
  │                                │ 2. Decode JWT
  │                                │ 3. Get user from "sub"
  │                                │ 4. Check user is active
  │ {username: "alice", ...}       │
  │ ←────────────────────────────── │
```

---

## Key Takeaways

1. **`OAuth2PasswordBearer`** — tells FastAPI where to find the token
2. **`OAuth2PasswordRequestForm`** — standard form for login
3. **Create JWT with `jose`** — encode user info + expiration
4. **Dependency chain** — `get_current_user` → `get_current_active_user`
5. **Token in header** — `Authorization: Bearer <token>`
6. **Swagger UI integrates** — lock icon for auth testing

---

> **Next Lesson**: [OAuth2 with Scopes →](../04-oauth2-with-scopes/)
