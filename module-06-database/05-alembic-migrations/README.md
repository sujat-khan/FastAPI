# Lesson 05 — Alembic Migrations

## Why Migrations?

`Base.metadata.create_all()` creates tables **once**, but can't:
- Add new columns to existing tables
- Rename columns
- Change column types
- Track schema changes over time

**Alembic** is SQLAlchemy's migration tool — it tracks and applies database schema changes.

---

## Setup

```bash
pip install alembic

# Initialize Alembic in your project
alembic init alembic
```

This creates:
```
project/
├── alembic/
│   ├── versions/        ← Migration files go here
│   ├── env.py           ← Alembic configuration
│   └── script.py.mako   ← Template for new migrations
├── alembic.ini          ← Main config file
└── ...
```

---

## Configure Alembic

### 1. Set the database URL in `alembic.ini`:
```ini
sqlalchemy.url = sqlite:///./app.db
```

### 2. Update `alembic/env.py` to know about your models:
```python
# In alembic/env.py, add:
from database import Base
from models import User, Post  # Import all models!

target_metadata = Base.metadata
```

---

## Common Commands

```bash
# Create a new migration (auto-detect changes)
alembic revision --autogenerate -m "Add users table"

# Apply all pending migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# See current version
alembic current

# See migration history
alembic history

# Apply to specific version
alembic upgrade <revision_id>
```

---

## Migration File Example

Auto-generated migration:
```python
"""Add users table

Revision ID: a1b2c3d4e5f6
Create Date: 2025-01-15 10:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = None

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )

def downgrade():
    op.drop_table('users')
```

---

## Workflow

```
1. Modify your SQLAlchemy models
2. Run: alembic revision --autogenerate -m "description"
3. Review the generated migration file
4. Run: alembic upgrade head
5. Commit migration file to version control
```

---

## Key Takeaways

1. **Use Alembic for schema changes** — not `create_all()` in production
2. **Autogenerate detects changes** — but always review before applying
3. **Migrations are version controlled** — commit them with your code
4. **`upgrade`/`downgrade`** — apply or rollback changes
5. **Import all models in `env.py`** — so Alembic can detect them

---

> **Next Lesson**: [Async Database (SQLModel) →](../06-async-database-sqlmodel/)
