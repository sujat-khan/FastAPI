"""
Module 01 - Lesson 04: Type Hints & Pydantic Examples
======================================================
Run this file to see Pydantic validation in action:
    pip install pydantic
    python examples.py
"""

from pydantic import BaseModel, Field, field_validator, model_validator


# ============================================================
# Example 1: Basic Pydantic Model
# ============================================================

print("=" * 50)
print("Example 1: Basic Pydantic Model")
print("=" * 50)

class User(BaseModel):
    name: str
    email: str
    age: int
    is_active: bool = True  # Default value

# Valid data
user = User(name="Alice", email="alice@example.com", age=30)
print(f"User: {user}")
print(f"Name: {user.name}")
print(f"Dict: {user.model_dump()}")
print(f"JSON: {user.model_dump_json()}")
print()

# Auto-conversion (string "25" becomes int 25)
user2 = User(name="Bob", email="bob@test.com", age="25")
print(f"Age type: {type(user2.age)} = {user2.age}")
print()

# Invalid data
try:
    bad_user = User(name="Charlie", email="charlie@test.com", age="not_a_number")
except Exception as e:
    print(f"Validation Error:\n{e}")
print()


# ============================================================
# Example 2: Optional and Default Fields
# ============================================================

print("=" * 50)
print("Example 2: Optional and Default Fields")
print("=" * 50)

class UserProfile(BaseModel):
    name: str                                # Required
    email: str                               # Required
    age: int | None = None                   # Optional (can be None)
    bio: str = "No bio provided"             # Optional with default
    tags: list[str] = []                     # Optional list with default

# Only required fields
profile = UserProfile(name="Alice", email="alice@test.com")
print(f"Profile: {profile.model_dump()}")
print()


# ============================================================
# Example 3: Nested Models
# ============================================================

print("=" * 50)
print("Example 3: Nested Models")
print("=" * 50)

class Address(BaseModel):
    street: str
    city: str
    country: str
    zip_code: str

class Employee(BaseModel):
    name: str
    email: str
    department: str
    address: Address                  # Nested model
    skills: list[str] = []

# Nested data — can pass dict, Pydantic converts it
employee = Employee(
    name="Alice",
    email="alice@company.com",
    department="Engineering",
    address={
        "street": "123 Main St",
        "city": "New York",
        "country": "USA",
        "zip_code": "10001"
    },
    skills=["Python", "FastAPI", "Docker"]
)

print(f"Employee: {employee.name}")
print(f"City: {employee.address.city}")
print(f"Full data: {employee.model_dump()}")
print()


# ============================================================
# Example 4: Field Validation with Constraints
# ============================================================

print("=" * 50)
print("Example 4: Field Validation with Constraints")
print("=" * 50)

class Product(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Product name")
    price: float = Field(gt=0, description="Price must be positive")
    quantity: int = Field(ge=0, le=10000, description="0 to 10000")
    sku: str = Field(pattern=r"^[A-Z]{3}-\d{4}$", description="Format: ABC-1234")

# Valid product
product = Product(name="Laptop", price=999.99, quantity=50, sku="LAP-0001")
print(f"Product: {product}")
print()

# Invalid — negative price
try:
    bad_product = Product(name="Free Item", price=-5, quantity=1, sku="FRE-0001")
except Exception as e:
    print(f"Price Validation Error:\n{e}")
print()

# Invalid — bad SKU format
try:
    bad_sku = Product(name="Widget", price=10, quantity=1, sku="invalid")
except Exception as e:
    print(f"SKU Validation Error:\n{e}")
print()


# ============================================================
# Example 5: Custom Validators
# ============================================================

print("=" * 50)
print("Example 5: Custom Validators")
print("=" * 50)

class UserRegistration(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: str
    password: str = Field(min_length=8)
    confirm_password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("Email must contain @")
        if "." not in v.split("@")[1]:
            raise ValueError("Email domain must contain a dot")
        return v.lower()  # Normalize to lowercase

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("Username must be alphanumeric")
        return v.lower()

    @model_validator(mode="after")
    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

# Valid registration
reg = UserRegistration(
    username="Alice123",
    email="Alice@Example.COM",
    password="securepass123",
    confirm_password="securepass123"
)
print(f"Username: {reg.username}")  # "alice123" (lowercased)
print(f"Email: {reg.email}")       # "alice@example.com" (lowercased)
print()

# Invalid — passwords don't match
try:
    bad_reg = UserRegistration(
        username="bob",
        email="bob@test.com",
        password="password123",
        confirm_password="different456"
    )
except Exception as e:
    print(f"Password Mismatch Error:\n{e}")
print()


# ============================================================
# Example 6: Model Inheritance
# ============================================================

print("=" * 50)
print("Example 6: Model Inheritance")
print("=" * 50)

class UserBase(BaseModel):
    """Shared fields for all user operations."""
    name: str
    email: str

class UserCreate(UserBase):
    """Fields needed to create a user (includes password)."""
    password: str

class UserResponse(UserBase):
    """Fields returned in API responses (no password!)."""
    id: int
    is_active: bool

# Simulating API flow
create_data = UserCreate(name="Alice", email="alice@test.com", password="secret123")
print(f"Create data: {create_data.model_dump()}")

# After saving to DB, return response without password
response_data = UserResponse(
    id=1,
    name=create_data.name,
    email=create_data.email,
    is_active=True
)
print(f"Response data: {response_data.model_dump()}")
# Note: password is NOT in the response!
print()


print("=" * 50)
print("All examples complete!")
print("=" * 50)
