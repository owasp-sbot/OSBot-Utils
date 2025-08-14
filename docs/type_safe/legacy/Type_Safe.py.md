# Type Safe Class - Usage Guide

The Type_Safe class provides robust runtime type checking and serialization for Python objects. It acts as a base class that enforces type safety through Python's type hints and annotations while offering convenient serialization methods and utilities. This enables developers to create strongly-typed classes with validation, safe serialization, and clear interfaces - all with minimal boilerplate code.

## Key Features

Type_Safe combines runtime type validation with modern Python type annotations to provide a comprehensive solution for type-safe programming. The class validates all attribute assignments against their declared types, supports the full range of Python's typing hints (Optional, Union, List, Dict, etc.), and provides type-safe versions of Python's built-in collections. Built-in serialization capabilities enable safe conversion to and from JSON, while automatic default value handling and context manager support streamline common programming patterns.

- Runtime type checking with annotations
- Support for Python typing hints including Optional, Union, List, Dict
- JSON serialization/deserialization 
- Type-safe collections (lists, dicts, sets)
- Automatic default value handling
- Context manager support

## Basic Usage

The Type_Safe class is designed to be used as a base class for your own classes. By inheriting from Type_Safe and using Python's type annotations, you get automatic type checking and validation with minimal setup. The class validates all attribute assignments against their declared types and raises informative errors when type mismatches occur.

### Simple Type Safety

```python
class User(Type_Safe):
    name: str
    age: int 
    active: bool = True

# Type checking enforced
user = User(name="Alice", age=30)
user.name = "Bob"      # OK
user.age = "30"        # Raises ValueError - wrong type
user.active = None     # Raises ValueError - None not allowed
```

### Optional Types

Type_Safe fully supports Python's Optional type hint, allowing attributes to accept None values when explicitly declared as Optional. This provides flexibility while maintaining type safety, making it easy to work with nullable fields and optional configurations.

```python
from typing import Optional

class Config(Type_Safe):
    debug: Optional[bool] = None
    port: Optional[int] = None

config = Config()
config.debug = True    # OK
config.debug = None    # OK - Optional allows None
```

### Collections

Type_Safe provides specialized collection classes (Type_Safe_List, Type_Safe_Dict, Type_Safe_Set) that maintain type safety for their contents. These collections enforce type checking on all operations, ensuring that only values of the correct type can be added or assigned. This type safety extends to nested collections and complex data structures.

```python
from typing import List, Dict

class DataStore(Type_Safe):
    items: List[str] = []           # Type-safe list
    mappings: Dict[str, int] = {}   # Type-safe dict

store = DataStore()
store.items.append("item1")         # OK
store.items.append(123)             # Raises TypeError
store.mappings["key1"] = 42         # OK 
store.mappings[123] = "value"       # Raises TypeError
```

### Serialization

Built-in serialization capabilities allow Type_Safe objects to be easily converted to and from JSON-compatible formats. The serialization system handles complex types, nested objects, and maintains type safety during deserialization. This makes it simple to persist objects, transfer them over networks, or integrate with APIs while maintaining type safety.

```python
class Record(Type_Safe):
    id: int
    data: str

record = Record(id=1, data="test")

# To JSON-compatible dict
json_data = record.json()           # {"id": 1, "data": "test"}

# From JSON 
new_record = Record.from_json(json_data)
```

### Context Manager

Type_Safe implements the context manager protocol, allowing instances to be used in 'with' statements. This enables resource management patterns and ensures proper setup/cleanup of objects. The context manager implementation is lightweight and can be extended by subclasses to add custom setup and cleanup behavior.

```python
class Resource(Type_Safe):
    name: str
    state: str = "new"

with Resource(name="test") as resource:
    resource.state = "active"
```

## Advanced Features

Type_Safe provides several advanced features for handling complex type requirements and data validation scenarios. These features enable fine-grained control over type checking, custom validation rules, and support for complex type hierarchies.

### Union Types

Union types allow attributes to accept multiple types while maintaining type safety. Type_Safe fully supports Python's Union type hint, enabling flexible type definitions while ensuring that only allowed types can be assigned. This is particularly useful when attributes need to handle multiple valid types.

```python
from typing import Union

class Value(Type_Safe):
    data: Union[str, int]

value = Value()
value.data = "test"    # OK
value.data = 42        # OK
value.data = True      # Raises ValueError
```

### Complex Types

Type_Safe handles nested object hierarchies and complex type relationships. Objects can contain other Type_Safe objects as attributes, creating type-safe object graphs. The system maintains type safety throughout the object hierarchy, including during serialization and deserialization.

```python
class Component(Type_Safe):
    type: str

class System(Type_Safe):
    name: str
    main: Component
    parts: List[Component]

# Nested type-safe objects
system = System(
    name="test",
    main=Component(type="primary"),
    parts=[Component(type="secondary")]
)
```

### Custom Type Validation

Beyond basic type checking, Type_Safe supports custom validation rules through validator classes. These validators can enforce additional constraints like minimum/maximum values, regular expression patterns, or custom validation logic. Validators are applied during attribute assignment and maintain the same error handling patterns as basic type checking.

```python
from osbot_utils.type_safe.validators import Min, Max, Regex

class ValidatedData(Type_Safe):
    count: Min[int, 0]              # Must be >= 0
    size: Max[int, 100]            # Must be <= 100
    code: Regex[str, r"^[A-Z]+$"]  # Must be uppercase letters

data = ValidatedData()
data.count = -1       # Raises ValueError
data.size = 200      # Raises ValueError
data.code = "abc"    # Raises ValueError
```

## Utility Methods

Type_Safe provides a comprehensive set of utility methods for working with type-safe objects. These methods facilitate common operations like serialization, object inspection, and state management. Each utility method is designed to maintain type safety while providing convenient access to object functionality.

- `json()` - Convert to JSON-compatible dict
- `obj()` - Convert to simple object
- `print()` - Pretty print object state
- `reset()` - Reset to default values
- `__locals__()` - Get current attributes
- `__kwargs__()` - Get all attributes including inherited

## Best Practices

Following these best practices ensures effective use of Type_Safe's features while maintaining code quality and type safety. These guidelines have been developed based on common usage patterns and help avoid potential pitfalls while maximizing the benefits of runtime type checking.

1. Define types using annotations for all attributes
2. Use Optional[] for attributes that can be None
3. Use type-safe collections when managing lists/dicts
4. Handle type validation errors appropriately
5. Use context manager when managing resources

## Common Gotchas

While Type_Safe aims to make type safety intuitive, there are some behaviors that might be unexpected. Understanding these common pitfalls helps prevent errors and ensures proper usage of the type system. Most of these gotchas relate to Python's type system limitations or design decisions made to balance type safety with usability.

- Attributes without type annotations aren't type checked
- Type validation occurs on every attribute assignment
- Mutable defaults (lists, dicts) are not shared between instances
- Direct dict/list assignments bypass type checking - use provided collections
