# Type_Safe - Comprehensive Runtime Type Safety for Python

## 🚀 Quick Start

Type_Safe provides **continuous runtime type checking** that validates every operation, not just at boundaries. It's part of the OSBot-Utils package and offers unique features not found in other Python type safety libraries.

```python
from osbot_utils.type_safe.Type_Safe import Type_Safe
from typing import List, Dict, Optional

class UserProfile(Type_Safe):
    username: str
    age: int
    tags: List[str]
    settings: Dict[str, bool]
    bio: Optional[str] = None

# Type checking happens automatically
user = UserProfile()
user.username = "alice"        # ✓ Valid
user.age = "25"                # ✗ Raises TypeError immediately!
user.tags.append("admin")      # ✓ Valid  
user.tags.append(123)          # ✗ Raises TypeError immediately!
```

## 🎯 Why Type_Safe?

### Continuous Protection vs. Boundary Checking

| Feature | Type_Safe | Pydantic | attrs | dataclasses |
|---------|-----------|----------|--------|-------------|
| Assignment checking | ✓ Every time | ✓ Optional | ✗ | ✗ |
| Collection operations | ✓ Every operation | ✗ | ✗ | ✗ |
| Nested validation | ✓ Automatic | ✓ Manual | ✗ | ✗ |
| Type-safe primitives | ✓ Built-in | ✗ | ✗ | ✗ |
| Auto-initialization | ✓ | ✓ | Partial | ✗ |

## 📚 Core Concepts

### 1. Automatic Initialization
No more boilerplate - Type_Safe automatically initializes based on annotations:

```python
class Config(Type_Safe):
    host: str                    # Auto-initialized to ''
    port: int                    # Auto-initialized to 0
    ssl: bool                    # Auto-initialized to False
    endpoints: List[str]         # Auto-initialized to []
    headers: Dict[str, str]      # Auto-initialized to {}
    
    # Only specify non-default values
    timeout: int = 30
    retries: int = 3
```

### 2. Type-Safe Collections
Every collection operation is validated:

```python
class DataStore(Type_Safe):
    items: List[int]
    index: Dict[str, int]

store = DataStore()

# List operations - all type-checked
store.items.append(42)           # ✓
store.items.extend([1, 2, 3])    # ✓
store.items.append("text")       # ✗ TypeError!

# Dict operations - keys AND values checked  
store.index["key"] = 100         # ✓
store.index[42] = 100            # ✗ TypeError on key!
store.index["key"] = "value"     # ✗ TypeError on value!
```

### 3. Type-Safe Primitives
Domain-specific types with built-in validation:

```python
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id import Safe_Id
from osbot_utils.type_safe.decorators import type_safe

class UserId(Safe_Id): pass
class ProductId(Safe_Id): pass

class Order(Type_Safe):
    user_id: UserId
    product_id: ProductId
    quantity: int

# Type safety prevents ID mix-ups
order = Order()
order.user_id = UserId("user_123")      # ✓
order.user_id = ProductId("prod_456")   # ✗ TypeError!
order.user_id = "user_123"              # Auto-converts to UserId
```

### 4. Method Validation with @type_safe
Validate method parameters and return values:

```python
class Calculator(Type_Safe):
    @type_safe
    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero")
        return a / b
    
    @type_safe
    def process_batch(self, 
                     numbers: List[float],
                     operation: str = "sum") -> float:
        if operation == "sum":
            return sum(numbers)
        return 0.0

calc = Calculator()
calc.divide(10, 2)              # ✓ Returns 5.0
calc.divide("10", 2)            # ✗ TypeError!
calc.process_batch([1.0, 2.0]) # ✓
calc.process_batch([1, "2"])   # ✗ TypeError!
```

## 🔧 Advanced Features

### Nested Type-Safe Objects
```python
class Address(Type_Safe):
    street: str
    city: str
    country: str = "USA"

class Person(Type_Safe):
    name: str
    address: Address              # Nested Type_Safe object
    contacts: List[Address]       # List of Type_Safe objects

# Deep initialization from dict
person = Person.from_json({
    "name": "Alice",
    "address": {
        "street": "123 Main St",
        "city": "Boston"
    },
    "contacts": [
        {"street": "456 Oak Ave", "city": "NYC"}
    ]
})
```

### Custom Validators
```python
from osbot_utils.type_safe.validators import Min, Max, Regex, Validate

class User(Type_Safe):
    username: Validate[str, Regex(r'^[a-z0-9_]+$')]
    age: Validate[int, Min(0), Max(150)]
    score: Validate[float, Min(0.0), Max(100.0)]
```

### Forward References
```python
class Node(Type_Safe):
    value: int
    parent: Optional['Node'] = None
    children: List['Node'] = []

# Create tree structure
root = Node(value=1)
child = Node(value=2)
child.parent = root
root.children.append(child)
```

## 🎯 When to Use Type_Safe

### Perfect For:
- **Security-critical applications** - Input validation, API boundaries
- **Financial systems** - Type-safe money handling with Safe_Float
- **Configuration management** - Validated settings with clear contracts
- **Domain modeling** - Rich types like UserId, EmailAddress, etc.
- **Data pipelines** - Ensure data integrity throughout processing

### Consider Alternatives When:
- Performance is absolutely critical (tight loops, numerical computing)
- You only need validation at boundaries (Pydantic might suffice)
- Working with existing codebases that can't be easily migrated

## 📊 Performance Considerations

Type_Safe adds overhead for safety. Here's what to expect:

| Operation | Overhead | Recommendation |
|-----------|----------|----------------|
| Object creation | ~5-10x | Use at boundaries, cache instances |
| Attribute assignment | ~3-5x | Acceptable for most uses |
| Collection operations | ~2-3x | Consider bulk operations |
| Method calls (@type_safe) | ~2x | Use selectively on public APIs |

### Performance Tips:
1. Use Type_Safe at system boundaries
2. Convert to primitives for heavy computation
3. Cache Type_Safe objects when possible
4. Use `@type_safe` decorator only where needed

## 🔄 Migration Guide

### From Pydantic
```python
# Pydantic
from pydantic import BaseModel, validator

class UserPydantic(BaseModel):
    name: str
    age: int
    
    @validator('age')
    def validate_age(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v

# Type_Safe equivalent
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.type_safe.validators import Min

class UserTypeSafe(Type_Safe):
    name: str
    age: Validate[int, Min(0)]
```

### From dataclasses
```python
# dataclasses
from dataclasses import dataclass, field

@dataclass
class ConfigDataclass:
    host: str = "localhost"
    port: int = 8080
    ssl: bool = False
    endpoints: list = field(default_factory=list)

# Type_Safe equivalent  
class ConfigTypeSafe(Type_Safe):
    host: str = "localhost"
    port: int = 8080
    ssl: bool = False
    endpoints: List[str]  # Auto-initialized, type-safe
```

## 📖 Documentation

- [Complete API Reference](./docs/api/)
- [Type-Safe Primitives Guide](./docs/type_safe_primitives.md)
- [Performance Tuning](./docs/performance.md)
- [Security Best Practices](./docs/security.md)
- [Troubleshooting Guide](./docs/troubleshooting.md)

## 🤝 Contributing

Type_Safe is part of [OSBot-Utils](https://github.com/owasp-sbot/OSBot-Utils). Contributions welcome!

## 📄 License

Apache 2.0 - See LICENSE file for details