# Type_Safe & Python Formatting Guide for LLMs

## Overview

This guide covers two interconnected systems for writing robust Python code: **OSBot-Utils Type_Safe** and a **specialized Python formatting style**. Type_Safe is a runtime type checking framework that enforces type constraints during execution, catching errors at assignment rather than deep in execution. Unlike Python's type hints (which are ignored at runtime), Type_Safe validates every operation, auto-initializes attributes, and provides domain-specific primitive types for common use cases like IDs, money, URLs, and file paths.

The formatting style prioritizes visual pattern recognition and information density over PEP-8 conventions. It uses vertical alignment to create visual lanes that make code structure immediately apparent, groups related information to maintain context, and optimizes for real-world debugging and code review scenarios. This approach recognizes that code is read far more often than written, and that human pattern recognition is most effective when information is structured consistently and predictably.

## Critical Principle: Ban Raw Primitives

**NEVER use raw `str`, `int`, or `float` in Type_Safe classes.** There are very few cases where the full capabilities and range of these primitives are actually needed. Raw primitives enable entire categories of bugs and security vulnerabilities.

### Why Ban Raw Primitives?

```python
# ✗ NEVER DO THIS - Raw primitives are dangerous
class User(Type_Safe):
    name   : str        # Can contain SQL injection, XSS, any length
    age    : int        # Can overflow, be negative, be 999999
    balance: float      # Floating point errors in financial calculations

# ✓ ALWAYS DO THIS - Domain-specific types
class User(Type_Safe):
    name   : Safe_Str__Username        # Sanitized, length-limited
    age    : Safe_UInt__Age            # 0-150 range enforced
    balance: Safe_Float__Money         # Exact decimal arithmetic
```

Raw primitives have caused major bugs and security issues:
- **String**: SQL injection, XSS, buffer overflows, command injection
- **Integer**: Overflow bugs, negative values where positive expected
- **Float**: Financial calculation errors, precision loss

## Type_Safe Core Rules

### 1. Always Inherit from Type_Safe
```python
from osbot_utils.type_safe.Type_Safe import Type_Safe

class MyClass(Type_Safe):    # ✓ CORRECT
    name  : str
    count : int

class MyClass:                # ✗ WRONG - Missing Type_Safe
    name: str
```

### 2. Type Annotate Everything
```python
class Config(Type_Safe):
    host        : str            # ✓ Every attribute has type
    port        : int
    ssl_enabled : bool
    endpoints   : List[str]      # ✓ Specific generic types
    
    # ✗ WRONG:
    # host = "localhost"      # Missing annotation
    # items: list             # Untyped collection
```

### 3. Immutable Defaults Only
```python
class Settings(Type_Safe):
    name  : str       = ""        # ✓ Immutable
    count : int       = 0         # ✓ Immutable
    items : List[str]             # ✓ No default (Type_Safe handles)
    
    # ✗ NEVER:
    # items: List[str] = []   # Mutable default ERROR
```

### 4. Forward References = Current Class Only
```python
class TreeNode(Type_Safe):
    value  : int
    parent : Optional['TreeNode'] = None    # ✓ Same class
    # parent: Optional['Node']              # ✗ Different class
```

### 5. Method Validation
```python
from osbot_utils.type_safe.decorators import type_safe

class Calculator(Type_Safe):
    @type_safe                # Validates params and return
    def add(self, a: int, b: int) -> int:
        return a + b
```

## Python Formatting Guidelines

### Method Signatures
```python
def method_name(self, first_param  : Type1        ,                               # Method purpose comment
                      second_param : Type2        ,                               # Aligned at column 80
                      third_param  : Type3 = None                                 # Default values align
                ) -> ReturnType:                                                  # Return on new line
```
- Parameters stack vertically with opening parenthesis
- Vertical alignment on `:`, `,`, `#`
- Return type format: `) -> ReturnType:`
- Skip formatting for single param or no types/defaults

### Variable Assignment & Assertions
```python
# Aligned equals signs
self.node_id    = Random_Guid()
self.value_type = str

# Aligned comparison operators
assert type(self.node)       is Schema__MGraph__Node
assert self.node.value       == "test_value"
assert len(self.attributes)  == 1
```

### Constructor Calls
```python
node_config = Schema__MGraph__Node__Config(node_id    = Random_Guid(),
                                           value_type = str          )
```

### Imports
```python
from unittest                                                       import TestCase
from mgraph_ai.schemas.Schema__MGraph__Node                        import Schema__MGraph__Node
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id import Safe_Id
```

## Safe Primitives Reference

### String Types
| Type | Purpose | Example |
|------|---------|---------|
| `Safe_Id` | Most identifiers (letters, numbers, `_`, `-`) | `"user-123"`, `"api_key"` |
| `Safe_Str` | Very restrictive (letters, numbers only) | `"HelloWorld123"` |
| `Safe_Str__File__Name` | Safe filenames | Prevents path traversal |
| `Safe_Str__File__Path` | File paths | Allows `/` and `\` |
| `Safe_Str__Url` | URL validation | Prevents XSS |
| `Safe_Str__IP_Address` | IP validation | IPv4/IPv6 |
| `Safe_Str__Html` | HTML content | Minimal filtering |

### Numeric Types
| Type | Purpose | Range/Features |
|------|---------|----------------|
| `Safe_Int` | Base integer | Range validation |
| `Safe_UInt` | Unsigned int | min_value=0 |
| `Safe_UInt__Port` | Network ports | 0-65535 |
| `Safe_UInt__Byte` | Single byte | 0-255 |
| `Safe_UInt__Percentage` | Percentage | 0-100 |
| `Safe_Float__Money` | Currency | Decimal arithmetic, 2 places |
| `Safe_Float__Percentage_Exact` | Precise % | 0-100, decimal |

### Identity Types
```python
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id import Safe_Id

class UserId(Safe_Id): pass
class ProductId(Safe_Id): pass

user_id    = UserId("USR-123")
product_id = ProductId("PRD-456")
# user_id != product_id  # Different types!
```

## Creating Custom Safe Types

### Domain-Specific Safe_Str Types

Creating custom Safe_Str types is straightforward - usually just requires updating regex and size:

```python
from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str
import re

# Username: alphanumeric, underscores, 3-20 chars
class Safe_Str__Username(Safe_Str):
    max_length      = 20
    regex           = re.compile(r'[^a-zA-Z0-9_]')  # Remove unsafe chars
    regex_mode      = 'REPLACE'
    allow_empty     = False

# Email-like validation
class Safe_Str__Email(Safe_Str):
    max_length         = 255
    regex              = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    regex_mode         = 'MATCH'
    strict_validation  = True

# Database identifier
class Safe_Str__DB_Name(Safe_Str):
    max_length        = 64
    regex             = re.compile(r'[^a-z0-9_]')  # Lowercase, numbers, underscore
    replacement_char  = '_'
    
# API Key format
class Safe_Str__API_Key(Safe_Str):
    max_length         = 32
    regex              = re.compile(r'^[A-Z0-9]{32}$')
    regex_mode         = 'MATCH'
    strict_validation  = True
```

Note: The default Safe_Str is quite restrictive (only letters and numbers), so you'll often need custom versions.

### Domain-Specific Safe_Int Types

```python
from osbot_utils.type_safe.primitives.safe_int.Safe_Int   import Safe_Int
from osbot_utils.type_safe.primitives.safe_uint.Safe_UInt import Safe_UInt

# Age with realistic bounds
class Safe_UInt__Age(Safe_UInt):
    min_value  = 0
    max_value  = 150

# Temperature in Celsius
class Safe_Int__Temperature_C(Safe_Int):
    min_value = -273  # Absolute zero
    max_value = 5778  # Surface of the sun

# HTTP Status Code
class Safe_UInt__HTTP_Status(Safe_UInt):
    min_value = 100
    max_value = 599

# Database ID (positive only)
class Safe_UInt__DB_ID(Safe_UInt):
    min_value   = 1      # No zero IDs
    allow_none  = False
```

## Advanced Topics

### Using Literal for Quick Enums

Type_Safe now supports `Literal` types with runtime enforcement - perfect for quick enums without creating separate Enum classes:

```python
from typing import Literal, Optional

class Schema__Open_Router__Message(Type_Safe):
    # Literal enforces these exact values at runtime!
    role    : Literal["assistant", "system", "user", "tool"]  # Only these 4 values allowed
    content : Safe_Str__Message_Content
    tool_id : Optional[Safe_Str] = None

# Runtime validation works!
message      = Schema__Open_Router__Message()
message.role = "user"       # ✓ Valid
message.role = "admin"      # ✗ ValueError: must be one of ["assistant", "system", "user", "tool"]

class Schema__Provider_Preferences(Type_Safe):
    # Mix Literal with other types
    data_collection : Literal["allow", "deny"]        = "deny"    # Two-state without boolean
    priority        : Literal["low", "medium", "high"] = "medium" # Quick priority levels
    mode            : Literal["dev", "test", "prod"]   = "dev"    # Environment modes
```

Use Literal when:
- You have a small, fixed set of string values
- Creating a full Enum class would be overkill
- Values are unlikely to change or be reused elsewhere

Use a proper Enum when:
- Values are reused across multiple schemas
- You need enum methods or properties
- The set of values might grow significantly

### Schema Files Best Practice

**CRITICAL: Schema files should ONLY contain schema definitions - NO business logic!**

```python
# ✓ CORRECT - Pure schema definition
class Schema__Order(Type_Safe):
    id       : Safe_Str__OrderId
    customer : Safe_Str__CustomerId
    items    : List[Schema__Order__Item]
    total    : Safe_Float__Money
    status   : Safe_Str__Status

# ✗ WRONG - Schema with business logic
class Schema__Order(Type_Safe):
    id       : Safe_Str__OrderId
    customer : Safe_Str__CustomerId
    items    : List[Schema__Order__Item]
    total    : Safe_Float__Money
    status   : Safe_Str__Status
    
    def calculate_tax(self):  # NO! Business logic doesn't belong here
        return self.total * 0.08
        
    def validate_order(self):  # NO! Validation logic goes elsewhere
        if self.total < 0:
            raise ValueError("Invalid total")
```

Exceptions are rare and usually involve overriding Type_Safe methods for special cases:
```python
# RARE EXCEPTION - Only when absolutely necessary
class Schema__Special(Type_Safe):
    value: Safe_Str
    
    def __setattr__(self, name, value):
        # Only override Type_Safe internals when absolutely required
        if name == 'value' and value == 'special_case':
            value = transform_special(value)
        super().__setattr__(name, value)
```

### Runtime Type Checking & Round-Trip Serialization

Type_Safe provides **continuous runtime type checking** - not just at creation or assignment, but for EVERY operation including collection manipulations. This is unique compared to frameworks like Pydantic which only validate at boundaries.

#### Continuous Runtime Protection

```python
class DataStore(Type_Safe):
    items  : List[Safe_Str__ProductId]
    prices : Dict[Safe_Str__ProductId, Safe_Float__Money]

store = DataStore()

# EVERY operation is type-checked at runtime:
store.items.append(Safe_Str__ProductId("PROD-123"))  # ✓ Valid
store.items.append("raw-string")                     # ✗ TypeError immediately!
store.items[0] = None                                # ✗ TypeError immediately!

store.prices["PROD-123"] = Safe_Float__Money(19.99)  # ✓ Valid  
store.prices["PROD-456"] = 19.99                     # ✓ Auto-converted
store.prices["PROD-789"] = "not-a-number"            # ✗ TypeError immediately!
```

#### Perfect Round-Trip Serialization

```python
# Complex nested structure
class Order(Type_Safe):
    id       : Safe_Str__OrderId
    customer : Safe_Str__CustomerId  
    items    : Dict[Safe_Str__ProductId, Safe_UInt]
    total    : Safe_Float__Money
    status   : Safe_Str__Status

# Create and populate
order = Order(id       = "ORD-2024-001"          ,
              customer = "CUST-123"              , 
              items    = {"PROD-A": 2, "PROD-B": 1},
              total    = 299.99                  ,
              status   = "pending"               )

# Serialize to JSON
json_data = order.json()

# Send over network, save to DB, etc.
send_to_api(json_data)

# Reconstruct with FULL type safety preserved
new_order = Order.from_json(json_data)
assert isinstance(new_order.id, Safe_Str__OrderId)         # Type preserved!
assert isinstance(new_order.total, Safe_Float__Money)      # Exact decimal!
assert new_order.items["PROD-A"] == 2                      # Data intact!
```

### FastAPI Integration - No Pydantic Needed!

With OSBot_Fast_API's built-in Type_Safe support, **you should NOT use Pydantic models**. Type_Safe classes work directly in FastAPI routes with automatic conversion:

```python
from osbot_fast_api.api.routes.Fast_API__Routes import Fast_API__Routes

# Define your Type_Safe models (NOT Pydantic!)
class UserRequest(Type_Safe):
    username : Safe_Str__Username
    email    : Safe_Str__Email
    age      : Safe_UInt__Age

class UserResponse(Type_Safe):
    id         : Safe_Str__UserId
    username   : Safe_Str__Username
    created_at : Safe_Str__Timestamp

# Use directly in routes - automatic conversion happens!
class Routes_Users(Fast_API__Routes):
    tag = 'users'
    
    def create_user(self, request: UserRequest) -> UserResponse:
        # request is Type_Safe with full validation
        # No manual conversion needed!
        user_id = self.user_service.create(request)
        
        return UserResponse(id         = user_id              ,
                           username   = request.username      ,
                           created_at = timestamp_now()       )
    
    def get_user(self, user_id: Safe_Str__UserId) -> UserResponse:
        # Even path parameters can use Safe types!
        return self.user_service.get(user_id)
    
    def setup_routes(self):
        self.add_route_post(self.create_user)
        self.add_route_get(self.get_user)

# FastAPI automatically:
# 1. Converts incoming JSON to Type_Safe objects
# 2. Validates all constraints
# 3. Converts Type_Safe responses back to JSON
# 4. Generates OpenAPI schema from Type_Safe classes
```

#### Why NOT Pydantic with FastAPI?

```python
# ✗ DON'T use Pydantic models anymore
from pydantic import BaseModel

class UserModel(BaseModel):  # Unnecessary!
    username: str             # No sanitization
    age: int                  # No bounds checking

# ✓ DO use Type_Safe directly
class User(Type_Safe):
    username : Safe_Str__Username  # Sanitized
    age      : Safe_UInt__Age      # Bounded
```

Benefits of Type_Safe over Pydantic in FastAPI:
- **Continuous validation** throughout request lifecycle
- **Automatic sanitization** of inputs
- **Domain type safety** (UserID ≠ ProductID)
- **No duplicate model definitions** (one model for all layers)
- **Built-in security** via Safe primitives

## Complete Example

```python
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id import Safe_Id
from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Money import Safe_Float__Money
from osbot_utils.type_safe.primitives.safe_str.Safe_Str__Url       import Safe_Str__Url
from typing                                                         import List, Dict, Optional

# Domain IDs
class UserId(Safe_Id): pass
class OrderId(Safe_Id): pass
class ProductId(Safe_Id): pass

class Order(Type_Safe):
    id       : OrderId
    user_id  : UserId
    items    : Dict[ProductId, int]
    subtotal : Safe_Float__Money
    tax      : Safe_Float__Money
    status   : str                        = "pending"
    tracking : Optional[Safe_Str__Url]    = None
    
    def total(self) -> Safe_Float__Money:                                 # Calculate total
        return self.subtotal + self.tax

# Usage
order = Order(id       = OrderId("ORD-001")        ,
              user_id  = UserId("USR-123")         ,
              items    = {ProductId("P1"): 2}      ,
              subtotal = Safe_Float__Money(99.99)  ,
              tax      = Safe_Float__Money(9.99)   )

# Type safety
order.user_id = OrderId("ORD-999")  # ValueError! Wrong type

# Serialization
json_data = order.json()
new_order = Order.from_json(json_data)  # Types preserved
```

## Critical Anti-Patterns to Avoid

```python
# ✗ DON'T: Mutable defaults
class Bad(Type_Safe):
    items: List[str] = []      # ERROR

# ✗ DON'T: Missing annotations  
class Bad(Type_Safe):
    name = "default"           # Missing type

# ✗ DON'T: Untyped collections
class Bad(Type_Safe):
    data: dict                 # Should be Dict[K, V]

# ✗ DON'T: Forward ref other classes
class Node(Type_Safe):
    other: 'SomeOtherClass'    # Won't work
```

## Serialization

```python
# From/to JSON
user      = User.from_json('{"name": "Alice", "age": 30}')
json_data = user.json()  # Returns dict

# Nested objects work automatically
company = Company.from_json({
    "name"         : "TechCorp",
    "headquarters" : {
        "street" : "123 Main",
        "city"   : "Boston"
    }
})
```

## Import Reference

```python
# Core
from osbot_utils.type_safe.Type_Safe                                       import Type_Safe
from osbot_utils.type_safe.decorators                                      import type_safe

# Safe Strings
from osbot_utils.type_safe.primitives.safe_str.Safe_Str                    import Safe_Str
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Name     import Safe_Str__File__Name
from osbot_utils.type_safe.primitives.safe_str.web.Safe_Str__Url          import Safe_Str__Url
from osbot_utils.type_safe.primitives.safe_str.web.Safe_Str__IP_Address   import Safe_Str__IP_Address

# Safe Numbers  
from osbot_utils.type_safe.primitives.safe_int.Safe_Int                   import Safe_Int
from osbot_utils.type_safe.primitives.safe_uint.Safe_UInt__Port           import Safe_UInt__Port
from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Money        import Safe_Float__Money

# Identifiers
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id        import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.identifiers.Random_Guid    import Random_Guid
```

## Key Benefits

1. **Runtime Type Safety**: Catches type errors at assignment, not deep in execution
2. **Auto-initialization**: Lists, dicts, sets initialize automatically
3. **Domain Modeling**: Safe_Id prevents mixing incompatible ID types
4. **Perfect Serialization**: JSON round-trips preserve all type information
5. **Visual Code Structure**: Alignment patterns make bugs obvious

## Summary Checklist

When generating Type_Safe code:
- [ ] Inherit from Type_Safe
- [ ] Add type annotations for ALL attributes  
- [ ] Use only immutable defaults (or none)
- [ ] Use specific generic types (List[T], not list)
- [ ] Forward references only to current class
- [ ] Add @type_safe to validated methods
- [ ] Use Safe_* types for domain concepts
- [ ] Follow vertical alignment formatting rules
- [ ] Ban raw primitives - use domain-specific Safe types
- [ ] Keep schemas pure - no business logic