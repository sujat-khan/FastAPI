# Lesson 02 — Password Hashing

## Never Store Plain Text Passwords!

```
❌ BAD:  password = "mysecret123"          → Stored as-is
✅ GOOD: password = "$2b$12$LJ3m5..."     → Stored as hash
```

**Hashing** is a one-way function — you can verify a password against a hash, but you can't reverse the hash back to the password.

---

## Using Passlib with Bcrypt

```bash
pip install "passlib[bcrypt]"
```

```python
from passlib.context import CryptContext

# Configure password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash a password
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Verify a password against a hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Example usage
hashed = hash_password("mysecret123")
print(hashed)
# $2b$12$LJ3m5eYoLBkXsEqr8V.bhuOd7yOXhJKdGzs1k...

print(verify_password("mysecret123", hashed))  # True
print(verify_password("wrongpass", hashed))     # False
```

---

## Integrating with FastAPI

```python
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Fake user database
fake_users_db = {}

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str
    message: str

@app.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    if user.username in fake_users_db:
        raise HTTPException(status_code=409, detail="Username taken")

    fake_users_db[user.username] = {
        "username": user.username,
        "hashed_password": pwd_context.hash(user.password),
    }
    return {"username": user.username, "message": "User created!"}

@app.post("/verify")
async def verify(user: UserCreate):
    stored_user = fake_users_db.get(user.username)
    if not stored_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not pwd_context.verify(user.password, stored_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    return {"message": "Password verified!"}
```

---

## Key Takeaways

1. **Never store plain passwords** — always hash
2. **Bcrypt is the standard** — slow by design (makes brute-force hard)
3. **Passlib handles complexity** — salting, rounds, verification
4. **Verification is one-way** — compare hash of input with stored hash
5. **Each hash is unique** — same password produces different hashes (due to salt)

---

> **Next Lesson**: [JWT Authentication →](../03-jwt-authentication/)
