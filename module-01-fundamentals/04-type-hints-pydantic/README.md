# Lesson 04 — Type Hints & Pydantic Introduction

## Why Type Hints Matter for FastAPI

FastAPI is **built entirely around Python type hints**. They're not just documentation — FastAPI uses them to:

1. **Validate** incoming request data automatically
2. **Serialize** response data (convert Python objects to JSON)
3. **Generate** interactive API documentation (Swagger/ReDoc)
4. **Provide** editor support (autocomplete, error detection)

> **This is FastAPI's superpower.** You write type hints, and FastAPI gives you validation + docs for free.

---

## Python Type Hints Refresher

Type hints were introduced in Python 3.5 (PEP 484). They don't change how Python runs — they're **annotations** that tools can use.

### Basic Types

```python
# Variable annotations
name: str = "Alice"
age: int = 30
price: float = 19.99
is_active: bool = True

# Function annotations
def greet(name: str, age: int) -> str:
    return f"Hello {name}, you are {age} years old"

# The return type is after ->
def add(a: int, b: int) -> int:
    return a + b
```

### The `typing` Module

For more complex types, use the `typing` module:

```python
from typing import Optional, Union

# Optional — can be the type OR None
def find_user(user_id: int) -> Optional[dict]:
    """Returns a user dict or None if not found."""
    if user_id == 1:
        return {"name": "Alice"}
    return None

# Union — can be one of several types
def process_id(id: Union[int, str]) -> str:
    return str(id)
```

### Collections

```python
from typing import List, Dict, Tuple, Set

# List of strings
names: List[str] = ["Alice", "Bob", "Charlie"]  # or list[str] in Python 3.9+

# Dictionary with string keys and int values
ages: Dict[str, int] = {"Alice": 30, "Bob": 25}  # or dict[str, int]

# Tuple with specific types
coordinate: Tuple[float, float] = (42.0, -73.5)  # or tuple[float, float]

# Set of integers
unique_ids: Set[int] = {1, 2, 3}  # or set[int]

# Function using collections
def get_user_names(users: List[dict]) -> List[str]:
    return [user["name"] for user in users]
```

### Python 3.10+ Syntax (Recommended)

Python 3.10 introduced cleaner syntax:

```python
# Before Python 3.10
from typing import Optional, Union, List

def old_style(
    name: Optional[str] = None,
    value: Union[int, str] = 0,
    items: List[str] = []
) -> Optional[dict]:
    ...

# Python 3.10+ (cleaner!)
def new_style(
    name: str | None = None,        # Optional → Type | None
    value: int | str = 0,           # Union → Type1 | Type2
    items: list[str] = []           # List → list (lowercase)
) -> dict | None:
    ...
```

---

## Type Hints in FastAPI

FastAPI reads your type hints and uses them for **automatic validation**:

```python
from fastapi import FastAPI

app = FastAPI()

# FastAPI reads the type hint 'int' for user_id
# If someone sends /users/abc → automatic 422 error!
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# FastAPI reads the default value 'None' and type 'str'
# Makes 'q' an optional query parameter
@app.get("/search")
async def search(q: str | None = None, limit: int = 10):
    return {"query": q, "limit": limit}
```

---

## Introduction to Pydantic

**Pydantic** is a data validation library that FastAPI uses extensively. It lets you define the shape of your data using Python classes with type hints.

### Why Pydantic?

| Without Pydantic | With Pydantic |
|-----------------|---------------|
| Manual data validation | Automatic validation from type hints |
| Write parsing code for each field | Declarative model definitions |
| Error messages are inconsistent | Structured, detailed error messages |
| No autocomplete in editors | Full IDE support |

### Installing Pydantic

```bash
pip install pydantic
# Note: FastAPI installs Pydantic automatically
```

### Your First Pydantic Model

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int
    is_active: bool = True  # Default value

# ✅ Valid data — works fine
user = User(name="Alice", email="alice@example.com", age=30)
print(user)
# name='Alice' email='alice@example.com' age=30 is_active=True

# ✅ Auto-conversion — "25" is converted to int
user2 = User(name="Bob", email="bob@test.com", age="25")
print(user2.age)
# 25 (int, not str!)

# ❌ Invalid data — raises ValidationError
try:
    user3 = User(name="Charlie", email="charlie@test.com", age="not_a_number")
except Exception as e:
    print(e)
    # 1 validation error for User
    # age
    #   Input should be a valid integer [type=int_parsing, ...]
```

### Accessing Model Data

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    age: int

user = User(name="Alice", email="alice@test.com", age=30)

# Access fields as attributes
print(user.name)    # "Alice"
print(user.email)   # "alice@test.com"

# Convert to dictionary
print(user.model_dump())
# {'name': 'Alice', 'email': 'alice@test.com', 'age': 30}

# Convert to JSON string
print(user.model_dump_json())
# '{"name":"Alice","email":"alice@test.com","age":30}'

# Create from dictionary
data = {"name": "Bob", "email": "bob@test.com", "age": 25}
user2 = User.model_validate(data)
```

### Optional and Default Fields

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str                          # Required
    email: str                         # Required
    age: int | None = None             # Optional (defaults to None)
    bio: str = "No bio provided"       # Optional with default value
    is_active: bool = True             # Optional with default value

# Only required fields are needed
user = UserCreate(name="Alice", email="alice@test.com")
print(user)
# name='Alice' email='alice@test.com' age=None bio='No bio provided' is_active=True
```

### Nested Models

Pydantic models can contain other Pydantic models:

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class User(BaseModel):
    name: str
    email: str
    address: Address              # Nested model
    tags: list[str] = []          # List of strings

# Using nested models
user = User(
    name="Alice",
    email="alice@test.com",
    address={                      # Can pass a dict — Pydantic converts it!
        "street": "123 Main St",
        "city": "New York",
        "country": "USA",
        "zip_code": "10001"
    },
    tags=["admin", "verified"]
)

print(user.address.city)  # "New York"
print(user.model_dump())
# {
#     'name': 'Alice',
#     'email': 'alice@test.com',
#     'address': {
#         'street': '123 Main St',
#         'city': 'New York',
#         'country': 'USA',
#         'zip_code': '10001'
#     },
#     'tags': ['admin', 'verified']
# }
```

### Field Validation

Pydantic has built-in validators via the `Field()` function:

```python
from pydantic import BaseModel, Field, field_validator

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, description="Price must be positive")
    quantity: int = Field(ge=0, le=10000)
    category: str

    # Custom validator
    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        allowed = ["electronics", "clothing", "food", "books"]
        if v.lower() not in allowed:
            raise ValueError(f"Category must be one of {allowed}")
        return v.lower()

# ✅ Valid
product = Product(name="Laptop", price=999.99, quantity=10, category="Electronics")
print(product.category)  # "electronics" (converted to lowercase by validator)

# ❌ Invalid — price must be > 0
try:
    bad = Product(name="Free Item", price=-5, quantity=1, category="books")
except Exception as e:
    print(e)
    # 1 validation error for Product
    # price
    #   Input should be greater than 0 [type=greater_than, ...]
```

### Field Constraint Reference

| Constraint | Type | Meaning |
|-----------|------|---------|
| `min_length` | str | Minimum string length |
| `max_length` | str | Maximum string length |
| `pattern` | str | Regex pattern match |
| `gt` | number | Greater than |
| `ge` | number | Greater than or equal |
| `lt` | number | Less than |
| `le` | number | Less than or equal |
| `multiple_of` | number | Must be a multiple of |

---

## Pydantic in FastAPI

Here's how Pydantic models work seamlessly with FastAPI:

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# Define the data model
class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str | None = None
    price: float = Field(gt=0)
    tax: float = Field(default=0, ge=0)

class ItemResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    tax: float
    total_price: float

# Use models in endpoints
@app.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    # FastAPI automatically:
    # 1. Reads the JSON body
    # 2. Validates it against ItemCreate
    # 3. Returns 422 if validation fails
    # 4. Gives you a typed 'item' object

    total = item.price + item.tax
    return ItemResponse(
        id=1,
        name=item.name,
        description=item.description,
        price=item.price,
        tax=item.tax,
        total_price=total
    )
```

When a client sends:
```json
POST /items
{
    "name": "Widget",
    "price": 9.99,
    "tax": 0.80
}
```

FastAPI validates the input, creates an `ItemCreate` object, and the response is validated against `ItemResponse`.

---

## Key Takeaways

1. **Type hints are not optional in FastAPI** — they're how FastAPI knows what data to expect
2. **Pydantic models define data shapes** — use them for request bodies and responses
3. **Validation is automatic** — define the rules, and Pydantic enforces them
4. **Type conversion is built-in** — Pydantic tries to convert data (e.g., `"25"` → `25`)
5. **Models can be nested** — complex data structures are naturally represented
6. **Field constraints are declarative** — use `Field()` for rules like min/max, regex, etc.

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Missing type hints on endpoint params | FastAPI can't validate | Always add type hints |
| Using `dict` instead of Pydantic model | No validation | Define a proper model |
| Forgetting `@classmethod` on validators | Validator doesn't work | Always add `@classmethod` decorator |
| Using `Optional[str]` without default | Field is still required | Use `Optional[str] = None` |
| Mutable default values | Shared state bug | Use `Field(default_factory=list)` |

---

## Practice Exercises

1. Create a Pydantic model for a `BlogPost` with: title (required, 5-200 chars), content (required), author (required), tags (optional list of strings), published (bool, default False).
2. Create a nested model structure: `Order` containing a list of `OrderItem` objects, each with a `Product` reference.
3. Add custom validators to ensure an email field contains `@` and a password is at least 8 characters.

---

> **Next Module**: [Module 02 — Getting Started with FastAPI →](../../module-02-getting-started/)
