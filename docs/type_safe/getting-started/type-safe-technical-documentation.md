# Type_Safe Technical Documentation

## Overview

Type_Safe is a Python class that implements runtime type checking and validation for class attributes. It provides a robust type safety system that enforces type constraints during attribute assignment, serialization, and deserialization. The class is particularly useful for creating data models that require strict type enforcement and validation.

## Problems Type_Safe Solves

### 1. Runtime Type Safety
Unlike Python's type hints which are only used for static analysis, Type_Safe enforces type checking at runtime:
- Prevents type-related bugs during program execution
- Catches type mismatches immediately when they occur
- Provides clear error messages identifying the exact location and nature of type violations
- Supports complex type validation including nested objects and collections

### 2. Automatic Variable Creation and Initialization
Type_Safe automatically handles:
- Creation of class attributes based on type annotations
- Initialization of attributes with appropriate default values
- Proper instantiation of nested Type_Safe objects
- Management of collection types (lists, dictionaries)

For example, instead of writing:
```python
def __init__(self):
    self.items         = []
    self.metadata      = {}
    self.config        = Config()
    self.settings      = Settings()
    self.max_retries   = 3
```

You can simply declare:
```python
class MyClass(Type_Safe):
    items       : List[str]
    metadata    : Dict[str, Any]
    config      : Config
    settings    : Settings
    max_retries : int = 3
```

## Real-World Example: MGraph Schema System

The MGraph schema system demonstrates how Type_Safe can be used to create complex, interconnected data structures with strict type safety:

```python
class Schema__MGraph__Graph(Type_Safe):
    edges        : Dict[Random_Guid, Schema__MGraph__Edge]
    graph_data   : Schema__MGraph__Graph__Data
    graph_id     : Random_Guid
    graph_type   : Type['Schema__MGraph__Graph']
    nodes        : Dict[Random_Guid, Schema__MGraph__Node]
    schema_types : Schema__MGraph__Types

class Schema__MGraph__Node(Type_Safe):
    node_data   : Schema__MGraph__Node__Data
    node_id     : Random_Guid
    node_type   : Type['Schema__MGraph__Node']

class Schema__MGraph__Edge(Type_Safe):
    edge_config  : Schema__MGraph__Edge__Config
    edge_data    : Schema__MGraph__Edge__Data
    edge_type    : Type['Schema__MGraph__Edge']
    from_node_id : Random_Guid
    to_node_id   : Random_Guid
```

This schema system showcases several Type_Safe features:
- Nested type-safe objects
- Type-safe collections with complex key/value types
- Forward references for self-referential types
- Automatic initialization of complex object hierarchies

## Key Features

### 1. Runtime Type Checking

Type_Safe enforces type annotations during program execution:

```python
class Person(Type_Safe):
    name    : str
    age     : int
    active  : bool = True
    
person = Person()
person.name   = "John"     # Valid
person.age    = "25"       # Raises TypeError at runtime - expected int, got str
person.active = None       # Raises TypeError - expected bool, got NoneType
```

Runtime checking includes:
- Type validation during attribute assignment
- Collection element type checking
- Nested object type validation
- Complex type support (Union, Optional, etc.)

### 2. The @type_safe Decorator

The @type_safe decorator provides method-level type checking:

```python
class Calculator(Type_Safe):
    @type_safe
    def add(self, a: int, b: int, multiply: bool = False) -> int:           # Validates params
        result = a + b
        return result * 2 if multiply else result

    @type_safe
    def process_items(self, items     : List[int],
                           threshold  : Optional[float] = None,
                           callbacks  : Dict[str, Callable] = None) -> List[int]:
        return [x for x in items if x > (threshold or 0)]

calc = Calculator()
calc.add(1, 2)                   # Returns 3
calc.add("1", 2)                 # Raises TypeError at runtime
calc.process_items([1,2,3], 1.5) # Valid
```

Key features of @type_safe:
- Validates all method parameters against their type annotations
- Supports default values and optional parameters
- Handles complex type hints including Union and Optional
- Provides clear error messages for type violations

### Automatic Default Value Initialization

Type_Safe automatically initializes attributes based on their type annotations, eliminating the need for explicit default values in most cases:

```python
class AutoInit(Type_Safe):
    # Type_Safe automatically initializes based on type annotations
    name        : str             # Initialized to ''
    count       : int             # Initialized to 0
    active      : bool            # Initialized to False
    items       : List[str]       # Initialized to []
    mapping     : Dict[str, int]  # Initialized to {}
    
    # Only use explicit defaults for non-default values
    status      : str             = "active"
    priority    : int             = 1

auto = AutoInit()
assert auto.name    == ''         # String default
assert auto.count   == 0          # Integer default
assert auto.active  is False      # Boolean default
assert auto.items   == []         # List default
assert auto.mapping == {}         # Dict default
assert auto.status  == "active"   # Explicit default
```

Default values are determined by type:
1. Basic Types:
   - str → ''
   - int → 0
   - float → 0.0
   - bool → False
   - bytes → b''

2. Collections:
   - List[T] → []
   - Dict[K,V] → {}
   - Set[T] → set()
   - Tuple[...] → (0,...,0)

3. Optional/Custom:
   - Optional[T] → None
   - Custom Classes → None (if no default constructor)
   - Union[T1,T2] → Default of first type

Note: Type_Safe only performs automatic initialization if the type has a default constructor available. This prevents issues with classes that require specific initialization parameters.

### Let Type_Safe handle defaults through type annotations

```
class ComplexTypes(Type_Safe):
    # Basic types (Type_Safe will initialize to: '', 0, False)
    name        : str                                         # → ''
    age         : int                                         # → 0
    active      : bool                                        # → False
    
    # Collections (Type_Safe will initialize to: [], {}, (0,0))
    tags        : List[str]                                   # → []
    scores      : Dict[str, float]                            # → {}
    coordinates : Tuple[int, int]                             # → (0,0)
    
    # Optional and Union types
    nickname    : Optional[str]                               # → None
    id_value    : Union[int, str]                             # → 0 (default of first type)
    
    # Custom types and forward refs
    config      : 'Config'                                    # → None
    parent      : Optional['ComplexTypes']                    # → None
    
    # Nested collections
    matrix      : List[List[int]]                             # → []
    tree        : Dict[str, Dict[str, Any]]                   # → {}

    # Only immutable defaults are allowed and needed
    version     : int              = 1                        # Explicit immutable default
    status      : str              = "draft"                  # Explicit immutable default
    created_at  : Optional[str]    = None                     # Explicit None is immutable
```

### 4. Serialization Support

Type_Safe provides built-in JSON serialization:

```python
class UserProfile(Type_Safe):
    user_id   : int
    username  : str
    settings  : Dict[str, Any]
    tags      : List[str]        = []
    active    : bool             = True

# Create and populate object
profile = UserProfile(user_id   = 1,
                     username  = "john_doe",
                     settings  = {"theme": "dark"},
                     tags      = ["admin", "staff"])

# Serialize to JSON
json_data = profile.json()

# Deserialize from JSON
new_profile = UserProfile.from_json(json_data)

# Verify equality
assert new_profile.json() == profile.json()
```

## Implementation Details

### Type-Safe Collections

Type_Safe provides automatic type safety for collection types:

```python
class UserSystem(Type_Safe):
    # Type-safe list - ensures all elements are strings
    usernames     : List[str]                         
    
    # Type-safe dict - ensures keys are strings and values are integers
    user_scores   : Dict[str, int]                    
    
    # Nested collections maintain type safety at all levels
    user_metadata : Dict[str, List[str]]              

system = UserSystem()

# List type safety
system.usernames.append("alice")                      # Valid
system.usernames.append(123    )                      # ERROR: Expected str, got int

# Dict type safety - both keys and values are checked
system.user_scores["alice"] = 100                     # Valid
system.user_scores["bob"  ] = "high"                  # ERROR: Expected int, got str
system.user_scores[42     ] = 100                     # ERROR: Expected str key, got int

# Nested collection type safety
system.user_metadata["alice"] = ["admin", "user"]     # Valid
system.user_metadata["bob"  ] = [1, 2, 3]             # ERROR: Expected List[str]
```

Key features of Type_Safe collections:
- Automatic type checking of all elements
- Runtime validation of collection operations
- Support for nested collections
- Clear error messages for type violations

All collection operations maintain type safety:

```python
# Lists
users : List[str] = []                               # Type_Safe initializes empty list
users.append("alice"           )                     # Type checked
users.extend(["bob", "charlie"])                     # Each element type checked
users.insert(0, 123            )                     # ERROR: Wrong type

# Dictionaries
scores : Dict[str, float] = {}                       # Type_Safe initializes empty dict
scores["alice"]           = 95.5                     # Types checked
scores.update({"bob": 87.5})                         # Each element checked
scores.update({42: 90.0}   )                          # ERROR: Wrong key type
```

### Type Resolution and Validation

Type_Safe handles various typing scenarios:

```python
class TypeValidation(Type_Safe):
    # Forward references - only works with current class name
    self_ref     : 'TypeValidation'            # Correct: Matches class name
    children     : List['TypeValidation']      # Correct: Matches class name
    
    # These would raise exceptions
    # other_type   : 'OtherClass'              # ERROR: Can't reference other classes
    # items        : List['Item']              # ERROR: Can't reference other classes
    # wrong_name   : 'TypeVal'                 # ERROR: Must match class name exactly
    
    # Union types are validated against all possible types
    id_field     : Union[int, str, UUID]
    
    # Optional is treated as Union[T, None]
    maybe_int    : Optional[int]
    
    # Collections are checked both at container and element level
    matrix       : List[List[int]]
    tree         : Dict[str, Dict[str, Any]]
```

### Error Handling

Type_Safe provides detailed error messages:

```python
try:
    profile = UserProfile(user_id="invalid")  # Should be int
except ValueError as e:
    # Error: Invalid type for attribute 'user_id'. 
    # Expected '<class 'int'>' but got '<class 'str'>'
    print(f"Error: {e}")
```

## Best Practices

### 1. Immutable Default Values

Type_Safe enforces immutability for default values to prevent the classic Python mutable default argument problem. The system only allows immutable types as default values:

```python
# These are safe - using immutable types
class SafeDefaults(Type_Safe):
    count       : int               = 0
    name        : str               = ""
    enabled     : bool             = False
    precision   : float            = 0.0
    bytes_data  : bytes            = b""
    fixed_tuple : tuple            = ()
    frozen      : frozenset        = frozenset()

# These will raise exceptions - mutable defaults not allowed
class UnsafeDefaults(Type_Safe):
    settings    : dict             = {}    # ERROR: Mutable default
    items       : list             = []    # ERROR: Mutable default
    cache       : set              = set() # ERROR: Mutable default
```

The allowed immutable types are:
- int
- float
- str
- bool
- bytes
- tuple
- frozenset
- None

For collections, instead of using mutable defaults, you should either:
1. Leave without a default (Type_Safe will initialize appropriately)
2. Use None as the default value
3. Initialize in __init__ if you need a specific starting state

### 2. Define Clear Type Annotations
```python
# Good
class Config(Type_Safe):
    port        : int              = 0     # Immutable default
    host        : str              = ""    # Immutable default
    retries     : Optional[int]    = None  # None is immutable
    credentials : Dict[str, str]           # Type_Safe handles initialization

# These will raise exceptions
class InvalidConfig(Type_Safe):
    port      : Any                        # Too permissive
    host                                   # Missing type annotation
    settings  : Dict = {'a':'b'}           # ERROR: Type_Safe prevents Dict with values
    users     : List = ['a']               # ERROR: Type_Safe prevents List with values
    items     : dict = {}                  # ERROR: Use Dict[K,V] instead of dict
    data      : list = []                  # ERROR: Use List[T] instead of list

InvalidConfig()  # Will raise this exception:  
                 #  ValueError: variable 'settings' is defined as type 'typing.Dict' which is not 
                 #  supported by Type_Safe, with only the following immutable types being supported: 
                 #  '(<class 'bool'>, <class 'int'>, <class 'float'>, <class 'complex'>, 
                 #  <class 'str'>, <class 'tuple'>, <class 'frozenset'>, <class 'bytes'>, 
                 #  <class 'NoneType'>, <class 'enum.EnumType'>, <class 'type'>)'
```

2. Use Specific Types
```python
# Good
class Order(Type_Safe):
    items      : List[OrderItem]
    total      : Decimal
    status     : OrderStatus

# Avoid
class Order(Type_Safe):
    items      : list        # Not type-safe
    total      : float       # Less precise
    status     : str         # Not type-safe
```

3. Leverage Forward References

Important: Forward references in Type_Safe only work when referencing the current class name as a string. 
This means you can only use the exact class name as the forward reference:

```python
# Good - using current class name
class Node(Type_Safe):
    value    : int
    children : List['Node']         # Correct: References current class
    parent   : Optional['Node']     # Correct: References current class

# ERROR - trying to reference other classes
class Tree(Type_Safe):
    root     : 'Node'              # ERROR: Can't forward reference other classes
    nodes    : List['OtherNode']   # ERROR: Can't forward reference other classes

# ERROR - using wrong class name
class DataNode(Type_Safe):
    next     : 'Node'              # ERROR: Must use 'DataNode' not 'Node'
    items    : List['DataNodes']   # ERROR: Must match class name exactly
```

The correct way to reference other classes is to import them:
```python
from my_module import Node, OtherNode

class Tree(Type_Safe):
    root     : Node                # Correct: Direct reference
    nodes    : List[OtherNode]     # Correct: Direct reference
```

## Common Patterns

### 1. Configuration Objects
```python
class DatabaseConfig(Type_Safe):
    host            : str
    port            : int               = 5432            # Immutable default
    username        : str
    password        : str
    max_connections : Optional[int]     = None           # None is immutable
    ssl_enabled     : bool             = False          # Immutable default
    retry_config    : Dict[str, Union[int, float]]      # Complex defaults need __init__

    def __init__(self, **kwargs):
        super().__init__(**kwargs)                      # Always call super().__init__ first
        
        # Complex initialization after super().__init__
        if not self.retry_config:                       # Check if not set via kwargs
            self.retry_config = {                       # Set complex defaults
                "max_retries": 3,
                "timeout": 30.0
            }
```

### 2. API Models
```python
class UserResponse(Type_Safe):
    id          : int
    username    : str
    email       : str
    roles       : List[str]         = []
    settings    : Dict[str, Any]    = {}
    created_at  : datetime
    updated_at  : Optional[datetime] = None
```

### 3. Data Transfer Objects
```python
class OrderDTO(Type_Safe):
    order_id    : str
    items       : List[Dict[str, Union[str, int]]]
    total       : Decimal
    status      : str
    customer_id : Optional[int] = None
```

## Conclusion

Type_Safe provides a robust, feature-rich system for implementing runtime type safety in Python applications. It combines the flexibility of Python with the safety of static typing, making it particularly valuable for large-scale applications where type safety is crucial.