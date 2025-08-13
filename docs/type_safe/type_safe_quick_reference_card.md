# Type_Safe Quick Reference Card

## Installation
```bash
pip install osbot-utils
```

## Basic Class Definition
```python
from osbot_utils.type_safe.Type_Safe import Type_Safe
from typing import List, Dict, Optional

class MyClass(Type_Safe):
    name: str                      # Required, auto-init to ''
    count: int = 10               # Optional with default
    items: List[str]              # Auto-init to []
    data: Dict[str, int]          # Auto-init to {}
    note: Optional[str] = None    # Nullable
```

## Type Annotations Cheat Sheet

| Type | Declaration | Auto Default | Example |
|------|------------|--------------|---------|
| String | `name: str` | `''` | `"text"` |
| Integer | `age: int` | `0` | `42` |
| Float | `price: float` | `0.0` | `19.99` |
| Boolean | `active: bool` | `False` | `True` |
| List | `items: List[T]` | `[]` | `[1, 2, 3]` |
| Dict | `data: Dict[K,V]` | `{}` | `{"a": 1}` |
| Set | `ids: Set[T]` | `set()` | `{1, 2, 3}` |
| Tuple | `pos: Tuple[int,int]` | `(0,0)` | `(10, 20)` |
| Optional | `val: Optional[T]` | `None` | `None` or `T` |
| Union | `id: Union[int,str]` | First type | `1` or `"a"` |

## Common Patterns

### Configuration Object
```python
class Config(Type_Safe):
    host: str = "localhost"
    port: int = 8080
    debug: bool = False
    endpoints: List[str]
```

### Nested Objects
```python
class Address(Type_Safe):
    street: str
    city: str

class Person(Type_Safe):
    name: str
    home: Address
    work: Optional[Address] = None
```

### Self-Referential
```python
class Node(Type_Safe):
    value: int
    children: List['Node'] = []
    parent: Optional['Node'] = None
```

## Validators

```python
from osbot_utils.type_safe.validators import Min, Max, Regex, OneOf, Validate

class Validated(Type_Safe):
    age: Validate[int, Min(0), Max(120)]
    email: Validate[str, Regex(r'^[\w\.-]+@[\w\.-]+$')]
    status: Validate[str, OneOf(['active', 'inactive'])]
```

## Method Validation

```python
from osbot_utils.type_safe.decorators import type_safe

class Service(Type_Safe):
    @type_safe
    def process(self, data: List[int], factor: float = 1.0) -> float:
        return sum(data) * factor
```

## Type-Safe Primitives

```python
from osbot_utils.helpers.Safe_Id import Safe_Id

class UserId(Safe_Id): pass
class OrderId(Safe_Id): pass

class Order(Type_Safe):
    id: OrderId
    user: UserId
    amount: float

# Prevents mixing IDs
order = Order()
order.id = OrderId("ORD-123")    # ✓
order.id = UserId("USR-456")     # ✗ TypeError
```

## Serialization

```python
# Object to JSON
obj = MyClass(name="test", count=5)
data = obj.json()                      # Returns dict
json_str = json.dumps(obj.json())      # Returns string

# JSON to Object  
obj = MyClass.from_json(data)          # From dict
obj = MyClass.from_json(json_str)      # From string

# Nested serialization works automatically
person = Person.from_json({
    "name": "Alice",
    "home": {"street": "123 Main", "city": "Boston"}
})
```

## Collection Operations

```python
class Store(Type_Safe):
    items: List[int]
    index: Dict[str, str]

store = Store()

# List - all operations type-checked
store.items.append(1)              # ✓
store.items.extend([2, 3])         # ✓
store.items.append("text")         # ✗ TypeError

# Dict - keys and values checked
store.index["key"] = "value"       # ✓
store.index[123] = "value"         # ✗ TypeError (key)
store.index["key"] = 123           # ✗ TypeError (value)
```

## Error Handling

```python
try:
    obj = MyClass()
    obj.count = "not a number"
except ValueError as e:
    # "Invalid type for attribute 'count'. Expected '<class 'int'>' but got '<class 'str'>'"
    print(e)
```

## Initialization Patterns

```python
# Empty initialization
obj = MyClass()

# Partial initialization
obj = MyClass(name="Alice")

# Full initialization
obj = MyClass(name="Alice", count=10, items=["a", "b"])

# From dictionary
obj = MyClass(**{"name": "Alice", "count": 10})

# Update after creation
obj = MyClass()
obj.name = "Alice"
obj.count = 10
```

## DO's and DON'Ts

### DO ✓
```python
# Use type annotations
name: str

# Use immutable defaults
count: int = 0

# Use specific types
items: List[str]

# Handle errors
try:
    obj.value = wrong_type
except ValueError:
    handle_error()
```

### DON'T ✗
```python
# Skip annotations
name = "default"

# Use mutable defaults
items: list = []

# Use generic types  
data: dict

# Ignore type safety
obj.value = any_value
```

## Common Exceptions

| Exception | Cause | Example |
|-----------|-------|---------|
| `ValueError` | Wrong type assigned | `obj.age = "thirty"` |
| `ValueError` | Invalid constructor arg | `MyClass(unknown_field=1)` |
| `ValueError` | Validation failed | `age = -5` with `Min(0)` |
| `TypeError` | Collection type mismatch | `list_of_ints.append("text")` |

## Performance Tips

1. **Cache Type_Safe objects** - Don't recreate unnecessarily
2. **Use at boundaries** - Validate input/output, not internal ops
3. **Batch operations** - Process collections efficiently
4. **Selective validation** - Use @type_safe only where needed

## Import Reference

```python
# Core
from osbot_utils.type_safe.Type_Safe import Type_Safe

# Decorators
from osbot_utils.type_safe.decorators import type_safe

# Validators
from osbot_utils.type_safe.validators import (
    Min, Max, Regex, OneOf, Validate
)

# Safe Primitives
from osbot_utils.helpers.Safe_Id import Safe_Id
from osbot_utils.helpers.safe_str import Safe_Str
from osbot_utils.type_safe.Type_Safe__List import Type_Safe__List
from osbot_utils.type_safe.Type_Safe__Dict import Type_Safe__Dict
```