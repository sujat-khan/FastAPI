# Lesson 04 — Relationships

## Database Relationships in SQLAlchemy

### One-to-Many

A user has many posts:

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(255), unique=True)

    # Relationship — access user.posts to get all posts
    posts = relationship("Post", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200))
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))  # Foreign key

    # Relationship — access post.author to get the user
    author = relationship("User", back_populates="posts")
```

### Pydantic Schemas for Relationships
```python
from pydantic import BaseModel

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    model_config = {"from_attributes": True}

class UserWithPosts(BaseModel):
    id: int
    name: str
    email: str
    posts: list[PostResponse] = []
    model_config = {"from_attributes": True}
```

### Querying with Relationships
```python
@app.get("/users/{user_id}", response_model=UserWithPosts)
def get_user_with_posts(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404)
    return user  # user.posts is automatically loaded
```

---

### Many-to-Many

Posts can have multiple tags, tags can belong to multiple posts:

```python
from sqlalchemy import Table

# Association table
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    posts = relationship("Post", secondary=post_tags, back_populates="tags")
```

---

### Eager vs Lazy Loading

```python
from sqlalchemy.orm import joinedload, selectinload

# Lazy loading (default) — N+1 query problem
users = db.query(User).all()
for user in users:
    print(user.posts)  # Each access = new SQL query!

# Eager loading — single query
users = db.query(User).options(joinedload(User.posts)).all()
# or
users = db.query(User).options(selectinload(User.posts)).all()
```

---

## Key Takeaways

1. **`ForeignKey`** creates the database relationship
2. **`relationship()`** adds Python-level access (user.posts)
3. **`back_populates`** links both sides of the relationship
4. **Many-to-many uses an association table** with `secondary=`
5. **Use eager loading** to avoid N+1 query problems

---

> **Next Lesson**: [Alembic Migrations →](../05-alembic-migrations/)
