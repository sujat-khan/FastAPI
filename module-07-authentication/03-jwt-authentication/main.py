"""
Module 07 - Lesson 03: Complete JWT Authentication Example
============================================================
Install dependencies:
    pip install fastapi uvicorn "python-jose[cryptography]" "passlib[bcrypt]"

Run with:
    uvicorn main:app --reload

Test flow:
    1. POST /token with username=alice, password=secret123
    2. Copy the access_token from the response
    3. GET /users/me with header: Authorization: Bearer <token>
    4. Or use the 🔒 Authorize button in Swagger UI (/docs)
"""

from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


# ============================================================
# Configuration
# ============================================================
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ============================================================
# App Setup
# ============================================================
app = FastAPI(
    title="JWT Auth Example",
    description="Complete JWT authentication implementation for FastAPI",
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# ============================================================
# Schemas
# ============================================================
class Token(BaseModel):
    access_token: str
    token_type: str

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
# Utility Functions
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

async def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


# ============================================================
# Endpoints
# ============================================================

@app.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Login and get an access token.

    **Test credentials:**
    - username: `alice`, password: `secret123` (active user)
    - username: `bob`, password: `password456` (disabled user)
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


@app.get("/users/me", response_model=User, tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """Get the current authenticated user's profile."""
    return current_user


@app.get("/users/me/items", tags=["Users"])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    """Get items belonging to the current user."""
    return [
        {"item_id": 1, "name": "Portal Gun", "owner": current_user.username},
        {"item_id": 2, "name": "Plumbus", "owner": current_user.username},
    ]


@app.get("/", tags=["General"])
async def root():
    """Welcome endpoint with instructions."""
    return {
        "message": "JWT Auth Example API",
        "instructions": {
            "1": "POST /token with username=alice, password=secret123",
            "2": "Use the token in Authorization: Bearer <token>",
            "3": "GET /users/me to see your profile",
        },
        "docs": "/docs",
    }
