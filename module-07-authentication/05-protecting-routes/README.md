# Lesson 05 — Protecting Routes

## Patterns for Route Protection

### Pattern 1: Individual Endpoint Protection
```python
@app.get("/profile")
async def get_profile(user: User = Depends(get_current_active_user)):
    return user
```

### Pattern 2: Router-Level Protection
```python
from fastapi import APIRouter

# All routes in this router require authentication
protected_router = APIRouter(
    prefix="/api",
    dependencies=[Depends(get_current_active_user)],
)

@protected_router.get("/data")
async def get_data():
    return {"data": "protected"}
```

### Pattern 3: Role-Based Access Control (RBAC)
```python
from enum import Enum

class Role(str, Enum):
    USER = "user"
    EDITOR = "editor"
    ADMIN = "admin"

class RoleChecker:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)):
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Role '{user.role}' not authorized"
            )
        return user

# Create reusable role checkers
require_admin = RoleChecker([Role.ADMIN])
require_editor = RoleChecker([Role.EDITOR, Role.ADMIN])
require_user = RoleChecker([Role.USER, Role.EDITOR, Role.ADMIN])

@app.get("/admin/users")
async def admin_users(user: User = Depends(require_admin)):
    return {"admin": True}

@app.post("/posts")
async def create_post(user: User = Depends(require_editor)):
    return {"editor": True}

@app.get("/feed")
async def get_feed(user: User = Depends(require_user)):
    return {"user": True}
```

### Pattern 4: Resource Ownership
```python
@app.put("/posts/{post_id}")
async def update_post(
    post_id: int,
    user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404)

    # Only the author or admin can update
    if post.author_id != user.id and user.role != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Not your post")

    return {"updated": True}
```

---

## Security Best Practices

| Practice | Why |
|----------|-----|
| Use HTTPS | Tokens are visible in plain HTTP |
| Short token expiry | Limits damage from stolen tokens |
| Store SECRET_KEY in env vars | Never hardcode secrets |
| Validate token on every request | Don't trust cached auth |
| Hash passwords with bcrypt | Slow by design = secure |
| Use refresh tokens for long sessions | Better UX + security |
| Rate limit login attempts | Prevent brute force |
| Log authentication events | Audit trail |

---

## Key Takeaways

1. **Individual, router, or app-level** — choose the right protection scope
2. **RBAC with dependency classes** — clean, reusable role checking
3. **Check resource ownership** — not just authentication
4. **Follow security best practices** — HTTPS, short expiry, env vars

---

> **Next Module**: [Module 08 — Advanced Features →](../../module-08-advanced-features/)
