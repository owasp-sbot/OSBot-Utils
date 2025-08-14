# LLM Prompt Guidance: Using OSBot-Utils Type_Safe

## For LLMs/AI Assistants

When working with code that uses OSBot-Utils Type_Safe, follow these guidelines to generate correct and safe code.

## Core Understanding

Type_Safe is a runtime type checking system that:
1. **Validates EVERY operation** - Not just at creation/assignment
2. **Auto-initializes attributes** - Based on type annotations
3. **Provides type-safe collections** - Lists, dicts, sets with continuous validation
4. **Supports type-safe primitives** - Safe_Str, Safe_Int, Safe_Float with domain validation

## Code Generation Rules

### Rule 1: Always Inherit from Type_Safe
```python
# ✓ CORRECT
from osbot_utils.type_safe.Type_Safe import Type_Safe

class MyClass(Type_Safe):
    name: str
    count: int

# ✗ WRONG - Missing Type_Safe inheritance
class MyClass:
    name: str
    count: int
```

### Rule 2: Use Type Annotations for All Attributes
```python
# ✓ CORRECT - All attributes have type annotations
class Config(Type_Safe):
    host: str
    port: int
    ssl_enabled: bool
    endpoints: List[str]

# ✗ WRONG - Missing or incomplete annotations
class Config(Type_Safe):
    host = "localhost"  # Missing annotation
    port: int
    ssl_enabled  # Missing annotation and value
```

### Rule 3: Only Immutable Default Values
```python
# ✓ CORRECT - Immutable defaults only
class Settings(Type_Safe):
    name: str = ""                    # Immutable
    count: int = 0                    # Immutable  
    active: bool = True               # Immutable
    value: Optional[float] = None     # Immutable
    items: List[str]                  # No default needed, Type_Safe handles it

# ✗ WRONG - Mutable defaults
class Settings(Type_Safe):
    items: List[str] = []      # ERROR: Mutable default
    config: dict = {}          # ERROR: Mutable default
    cache: set = set()         # ERROR: Mutable default
```

### Rule 4: Use Specific Types for Collections
```python
# ✓ CORRECT - Specific generic types
class DataModel(Type_Safe):
    names: List[str]
    scores: Dict[str, float]
    unique_ids: Set[int]
    coordinates: Tuple[float, float]

# ✗ WRONG - Untyped collections
class DataModel(Type_Safe):
    names: list                # Missing element type
    scores: dict               # Missing key/value types
    unique_ids: set            # Missing element type
```

### Rule 5: Forward References Use Current Class Name
```python
# ✓ CORRECT - Forward ref to same class
class TreeNode(Type_Safe):
    value: int
    parent: Optional['TreeNode'] = None
    children: List['TreeNode'] = []

# ✗ WRONG - Forward ref to different class
class TreeNode(Type_Safe):
    value: int
    parent: Optional['Node']  # ERROR: Must be 'TreeNode'
```

### Rule 6: Use @type_safe for Method Validation
```python
from osbot_utils.type_safe.decorators import type_safe

class Calculator(Type_Safe):
    # ✓ CORRECT - Validates parameters and return
    @type_safe
    def add(self, a: int, b: int) -> int:
        return a + b
    
    # ✗ WRONG - Missing decorator for validation
    def multiply(self, a: int, b: int) -> int:
        return a * b
```

### Rule 7: Use Type-Safe Primitives for Domain Types
```python
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id import Safe_Id

# ✓ CORRECT - Domain-specific type
class UserId(Safe_Id): pass
class Email(Safe_Str): pass

class User(Type_Safe):
    id: UserId
    email: Email
    
# ✗ WRONG - Using raw types for domain concepts  
class User(Type_Safe):
    id: str      # Should be UserId
    email: str   # Should be Email
```

## Common Patterns

### Pattern 1: Configuration Objects
```python
class DatabaseConfig(Type_Safe):
    host: str = "localhost"
    port: int = 5432
    database: str
    username: str
    password: str
    pool_size: int = 10
    ssl: bool = False
    options: Dict[str, str]
```

### Pattern 2: API Request/Response Models
```python
class APIRequest(Type_Safe):
    endpoint: str
    method: str = "GET"
    headers: Dict[str, str]
    params: Dict[str, Any]
    body: Optional[Dict[str, Any]] = None

class APIResponse(Type_Safe):
    status_code: int
    headers: Dict[str, str]
    data: Dict[str, Any]
    errors: List[str]
```

### Pattern 3: Nested Data Structures
```python
class Address(Type_Safe):
    street: str
    city: str
    state: str
    zip_code: str

class Company(Type_Safe):
    name: str
    headquarters: Address
    branches: List[Address]
    employees: Dict[str, Address]
```

## Serialization Patterns

### JSON Serialization
```python
# Creating from JSON
user = User.from_json('{"name": "Alice", "age": 30}')
user = User.from_json({"name": "Alice", "age": 30})  # Dict also works

# Converting to JSON
json_data = user.json()  # Returns dict
json_str = json.dumps(user.json())  # For string

# Nested objects work automatically
company = Company.from_json({
    "name": "TechCorp",
    "headquarters": {
        "street": "123 Main",
        "city": "Boston",
        "state": "MA",
        "zip_code": "02101"
    }
})
```

## Validation Patterns

### Using Built-in Validators
```python
from osbot_utils.type_safe.validators import Min, Max, Regex, OneOf, Validate

class ValidatedModel(Type_Safe):
    # Numeric ranges
    age: Validate[int, Min(0), Max(150)]
    score: Validate[float, Min(0.0), Max(100.0)]
    
    # String patterns
    username: Validate[str, Regex(r'^[a-z0-9_]{3,20}$')]
    email: Validate[str, Regex(r'^[\w\.-]+@[\w\.-]+\.\w+$')]
    
    # Enumerated values
    status: Validate[str, OneOf(['active', 'inactive', 'pending'])]
    priority: Validate[int, OneOf([1, 2, 3, 4, 5])]
```

## Error Handling

### Expected Exceptions
```python
try:
    user = User()
    user.age = "invalid"  # Not an int
except ValueError as e:
    # "Invalid type for attribute 'age'. Expected '<class 'int'>' but got '<class 'str'>'"
    print(f"Validation error: {e}")

try:
    @type_safe
    def process(data: List[int]) -> int:
        return sum(data)
    
    process(["1", "2"])  # Wrong type in list
except ValueError as e:
    # "Parameter 'data' expected type List[int], but got..."
    print(f"Parameter error: {e}")
```

## Performance Considerations

When generating code with Type_Safe:

1. **Use at boundaries** - Input validation, API endpoints
2. **Cache instances** - Don't recreate Type_Safe objects unnecessarily
3. **Bulk operations** - Process collections in chunks when possible
4. **Selective validation** - Use @type_safe only on public methods

## DO NOT Generate These Anti-Patterns

```python
# ❌ DON'T: Mix Type_Safe with other validation
class Bad(Type_Safe, BaseModel):  # Don't mix with Pydantic
    name: str

# ❌ DON'T: Use mutable defaults
class Bad(Type_Safe):
    items: List[str] = []  # Will raise error

# ❌ DON'T: Forget type annotations
class Bad(Type_Safe):
    name = "default"  # Missing annotation

# ❌ DON'T: Use raw dict/list types
class Bad(Type_Safe):
    data: dict  # Should be Dict[K, V]
    items: list  # Should be List[T]

# ❌ DON'T: Forward reference other classes
class Node(Type_Safe):
    other: 'SomeOtherClass'  # Won't work
```

## Testing Patterns

```python
import pytest
from osbot_utils.type_safe.Type_Safe import Type_Safe

class TestModel(Type_Safe):
    name: str
    value: int

def test_type_validation():
    model = TestModel()
    
    # Test valid assignments
    model.name = "test"
    assert model.name == "test"
    
    # Test invalid assignments
    with pytest.raises(ValueError):
        model.value = "not an int"
    
    # Test serialization
    model.value = 42
    data = model.json()
    assert data == {"name": "test", "value": 42}
    
    # Test deserialization
    new_model = TestModel.from_json(data)
    assert new_model.name == model.name
    assert new_model.value == model.value
```

## Summary Checklist

When generating Type_Safe code:
- [ ] Inherit from Type_Safe
- [ ] Add type annotations for ALL attributes
- [ ] Use only immutable defaults (or none)
- [ ] Use specific generic types (List[T], not list)
- [ ] Forward references only to current class
- [ ] Add @type_safe to validated methods
- [ ] Use Safe_* types for domain concepts
- [ ] Handle ValueError exceptions appropriately
- [ ] Test type validation and serialization