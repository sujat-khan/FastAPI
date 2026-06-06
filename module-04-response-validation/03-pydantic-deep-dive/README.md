# Lesson 03 — Pydantic Deep Dive

## Advanced Pydantic for FastAPI

This lesson covers the advanced Pydantic features you'll use frequently in real FastAPI applications.

---

## Field Validators

### `@field_validator` — Validate Individual Fields

```python
from pydantic import BaseModel, field_validator

class User(BaseModel):
    name: str
    email: str
    age: int

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name cannot be blank")
        return v.strip().title()  # "john doe" → "John Doe"

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v.lower()

    @field_validator("age")
    @classmethod
    def age_must_be_reasonable(cls, v: int) -> int:
        if v < 0 or v > 150:
            raise ValueError("Age must be between 0 and 150")
        return v
```

### `@model_validator` — Validate Across Fields

```python
from pydantic import BaseModel, model_validator

class DateRange(BaseModel):
    start_date: str
    end_date: str

    @model_validator(mode="after")
    def check_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError("end_date must be after start_date")
        return self

class PasswordForm(BaseModel):
    password: str
    confirm_password: str

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
```

---

## Computed Fields

Fields that are calculated from other fields:

```python
from pydantic import BaseModel, computed_field

class Order(BaseModel):
    items: list[dict]
    tax_rate: float = 0.08

    @computed_field
    @property
    def subtotal(self) -> float:
        return sum(item["price"] * item["quantity"] for item in self.items)

    @computed_field
    @property
    def tax(self) -> float:
        return round(self.subtotal * self.tax_rate, 2)

    @computed_field
    @property
    def total(self) -> float:
        return round(self.subtotal + self.tax, 2)

order = Order(items=[
    {"name": "Widget", "price": 10.00, "quantity": 3},
    {"name": "Gadget", "price": 25.00, "quantity": 1},
])
print(order.total)  # 59.40
```

---

## Model Inheritance Patterns

### The Base/Create/Response Pattern

```python
class ProductBase(BaseModel):
    """Fields shared across all operations."""
    name: str
    description: str | None = None
    price: float
    category: str

class ProductCreate(ProductBase):
    """Fields needed to create a product."""
    sku: str  # Only needed at creation

class ProductUpdate(BaseModel):
    """All fields optional for partial updates."""
    name: str | None = None
    description: str | None = None
    price: float | None = None
    category: str | None = None

class ProductResponse(ProductBase):
    """Fields returned in API responses."""
    id: int
    sku: str
    created_at: str
    in_stock: bool

    model_config = {"from_attributes": True}
```

### `from_attributes = True` (Important for Databases!)

This allows Pydantic to read data from ORM model attributes (not just dicts):

```python
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    model_config = {"from_attributes": True}

# Now you can create from an ORM object:
# user_orm = db.query(User).first()
# response = UserResponse.model_validate(user_orm)  # Works!
```

---

## Serialization Control

### `model_dump()` Options

```python
class User(BaseModel):
    name: str
    email: str
    password: str
    age: int | None = None
    bio: str = "No bio"

user = User(name="Alice", email="alice@test.com", password="secret")

# Exclude fields
user.model_dump(exclude={"password"})
# {'name': 'Alice', 'email': 'alice@test.com', 'age': None, 'bio': 'No bio'}

# Include only specific fields
user.model_dump(include={"name", "email"})
# {'name': 'Alice', 'email': 'alice@test.com'}

# Exclude fields with None values
user.model_dump(exclude_none=True)
# {'name': 'Alice', 'email': 'alice@test.com', 'password': 'secret', 'bio': 'No bio'}

# Exclude fields that weren't explicitly set
user.model_dump(exclude_unset=True)
# {'name': 'Alice', 'email': 'alice@test.com', 'password': 'secret'}

# Exclude fields with default values
user.model_dump(exclude_defaults=True)
# {'name': 'Alice', 'email': 'alice@test.com', 'password': 'secret'}
```

---

## Custom Types and Validators

### Email Validation
```python
from pydantic import BaseModel, EmailStr

# pip install email-validator (included in fastapi[standard])
class User(BaseModel):
    name: str
    email: EmailStr  # Built-in email validation!

User(name="Alice", email="alice@example.com")  # ✅
User(name="Alice", email="not-an-email")       # ❌ ValidationError
```

### Constrained Types
```python
from pydantic import BaseModel, Field
from typing import Annotated

# Using Annotated for reusable constraints
PositiveFloat = Annotated[float, Field(gt=0)]
ShortString = Annotated[str, Field(min_length=1, max_length=100)]
Percentage = Annotated[float, Field(ge=0, le=100)]

class Product(BaseModel):
    name: ShortString
    price: PositiveFloat
    discount: Percentage = 0
```

---

## Key Takeaways

1. **`@field_validator`** validates individual fields with custom logic
2. **`@model_validator`** validates relationships between fields
3. **`computed_field`** creates derived values automatically
4. **Model inheritance** reduces duplication (Base/Create/Update/Response)
5. **`from_attributes=True`** enables ORM model conversion
6. **`model_dump()` options** control serialization output

---

> **Next Lesson**: [Custom Responses →](../04-custom-responses/)
