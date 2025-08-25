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
    parent : 'TreeNode' = None    # ✓ Same class
    # parent: 'Node'              # ✗ Different class
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
                 ) -> ReturnType:                                                 # Return on new line
```

- Parameters stack vertically with opening parenthesis
- **First letter of return type aligns with first letter of parameter names** (the `R` in `ReturnType` aligns with `f` in `first_param`, `s` in `second_param`, etc.)
- Vertical alignment on `:`, `,`, `#`
- Return type format: `) -> ReturnType:` where the closing `)` is positioned to achieve the return type alignment
- Skip formatting for single param or no types/defaults
- ONLY do this when there is at least one parameter: for cases like `method_a(self)` just do `method_a(self) -> ReturnType:`

#### Alignment Example - Focus on Return Type
```python
def process_data(self, input_data   : Dict[str, Any] ,                            # Raw input data
                       validator    : Schema__Validator,                          # Validation schema
                       timeout      : int = 30                                    # Timeout in seconds
                  ) -> Schema__Result:                                            # Processed result
    #                  ^-- Note: 'S' in Schema__Result aligns with 'i' in input_data and 'v' in validator
```

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
from unittest                                                      import TestCase
from mgraph_ai.schemas.Schema__MGraph__Node                        import Schema__MGraph__Node
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id import Safe_Id
```


### Documentation Style - NEVER Use Docstrings

**CRITICAL**: In Type_Safe code, NEVER use Python docstrings. All documentation must be inline comments aligned at the end of lines. This maintains the visual pattern recognition that makes Type_Safe code readable.

#### ✗ NEVER DO THIS - Docstrings Break Visual Patterns

```python
# ✗ WRONG - Docstrings clutter the code and break alignment
class Persona__Service(Type_Safe):
    """Core service for persona-based translation and impersonation"""
    
    prompt_builder : Persona__Prompt_Builder
    persona_manager: Persona__Manager
    llm_client     : LLM__Client
    environment    : Enum__Deployment_Environment
    
    def setup(self) -> 'Persona__Service':
        """Initialize the service with configuration"""
        pass
        
    def translate(self, text: Safe_Str, target_persona: Schema__Persona) -> Safe_Str:
        """
        Translate text using the specified persona.
        
        Args:
            text: The text to translate
            target_persona: The persona to use for translation
            
        Returns:
            The translated text
        """
        pass
```

#### ✓ ALWAYS DO THIS - Inline Comments with Alignment

```python
# ✓ CORRECT - Clean visual lanes with aligned comments
class Persona__Service(Type_Safe):                              # Core service for persona-based translation and impersonation
    prompt_builder  : Persona__Prompt_Builder                   # Builds prompts for LLM interactions
    persona_manager : Persona__Manager                          # Manages available personas
    llm_client      : LLM__Client                               # Client for LLM API calls
    environment     : Enum__Deployment_Environment              # Current deployment environment
    
    def setup(self) -> 'Persona__Service':                      # Initialize the service with configuration
        self.prompt_builder  = Persona__Prompt_Builder()
        self.persona_manager = Persona__Manager()
        return self
        
    def translate(self, text          : Safe_Str          ,     # Text to translate
                        target_persona : Schema__Persona        # Persona for translation style
                   ) -> Safe_Str:                               # Returns translated text
        prompt = self.prompt_builder.build(text, target_persona)
        return self.llm_client.complete(prompt)
```

#### Key Rules for Comments

1. **Class comments**: Always at the end of the class declaration line
2. **Attribute comments**: Aligned at the same column (typically column 60-80)
3. **Method comments**: At the end of the method signature line
4. **Parameter comments**: Aligned with other parameter comments
5. **Return type comments**: On the same line as the return type annotation

#### Why No Docstrings?

- **Visual consistency**: Docstrings break the vertical alignment patterns
- **Information density**: Inline comments keep related information on the same line
- **Scanability**: Eyes can follow the visual lanes to quickly understand structure
- **Debugging efficiency**: All information visible without scrolling or expanding
- **Pattern recognition**: Misalignments immediately signal potential issues

#### Complex Method Documentation

For methods that need extensive documentation, use a comment block ABOVE the method, not a docstring:

```python
# Transform user input into a structured query by:
# 1. Sanitizing dangerous characters
# 2. Normalizing whitespace and case
# 3. Applying persona-specific transformations
# 4. Validating against schema constraints
def transform_input(self, raw_input    : str                   ,    # Raw user input
                          persona      : Schema__Persona       ,    # Active persona
                          constraints  : Schema__Constraints        # Validation constraints
                     ) -> Safe_Str__Query:                          # Sanitized, validated query
    # Implementation here
    pass
```

#### Remember

The entire Type_Safe philosophy is about making code structure visible through alignment. Docstrings are vertical space wasters that hide the elegant patterns that make Type_Safe code self-documenting. Every piece of documentation should enhance the visual structure, not obscure it.

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

## Default Values and Auto-initialization in Type_Safe

Type_Safe automatically initializes attributes based on their types - you rarely need to use `None` or `Optional`. Understanding this auto-initialization behavior is key to writing clean Type_Safe code.

### Why Type_Safe Prohibits Mutable Default Values

**CRITICAL**: Type_Safe prevents you from assigning mutable default values (lists, dicts, objects) directly in class definitions. This is a security feature that prevents one of Python's most dangerous gotchas - shared mutable state across instances:

```python
# ❌ DANGEROUS Python Pattern (Type_Safe prevents this)
class DangerousClass:
    items = []  # This list is SHARED across ALL instances!
    
obj1 = DangerousClass()
obj2 = DangerousClass()
obj1.items.append("secret_data")
print(obj2.items)  # ['secret_data'] - DATA LEAK! 

# ✅ Type_Safe PREVENTS this vulnerability
class SafeClass(Type_Safe):
    items: List[str]  # Each instance gets its OWN list
    
obj1 = SafeClass()
obj2 = SafeClass()
obj1.items.append("secret_data")
print(obj2.items)  # [] - Safe! Each instance is isolated
```

This shared mutable state has caused:
- **Security breaches**: User A seeing User B's data
- **Memory leaks**: Objects never garbage collected
- **Race conditions**: Concurrent modifications to shared state
- **Data corruption**: Unexpected modifications from other instances

### How Type_Safe Auto-initialization Works

```python
from osbot_utils.type_safe.Type_Safe import Type_Safe
from typing import List, Dict, Set

class Schema__Message(Type_Safe):
    # Safe primitives auto-initialize to their empty/zero values
    content     : Safe_Str                    # Auto-initializes to ''
    count       : Safe_UInt                   # Auto-initializes to 0
    price       : Safe_Float__Money           # Auto-initializes to 0.00
    
    # Collections auto-initialize to empty (NEW instance per object!)
    tags        : List[Safe_Str]              # Auto-initializes to [] (unique instance)
    metadata    : Dict[str, str]              # Auto-initializes to {} (unique instance)
    unique_ids  : Set[Safe_Id]                # Auto-initializes to set() (unique instance)
    
    # Custom Type_Safe classes auto-initialize if possible
    options     : Schema__Options             # Auto-initializes to Schema__Options()
    
    # Use explicit None ONLY when you truly need nullable
    parent_id   : Safe_Id = None              # Explicitly nullable
    expires_at  : Safe_Str__Timestamp = None  # Explicitly nullable

# Usage example
message = Schema__Message()
print(message.content)      # ''  - auto-initialized
print(message.count)        # 0   - auto-initialized  
print(message.tags)         # []  - auto-initialized (unique to this instance)
print(message.options)      # Schema__Options() - auto-initialized
print(message.parent_id)    # None - explicitly set
```

#### Special Auto-initializing Types

Some Type_Safe types have built-in auto-initialization behavior that generates new values on each instantiation. **Never override `__init__` to set these values** - Type_Safe handles this automatically:

```python
from osbot_utils.type_safe.primitives.safe_str.identifiers.Random_Guid import Random_Guid
from osbot_utils.type_safe.primitives.safe_str.identifiers.Timestamp_Now import Timestamp_Now

class Schema__Response(Type_Safe):          # These types auto-generate values on instantiation:
    request_id : Random_Guid                # Auto-generates new GUID each time
    timestamp  : Timestamp_Now               # Auto-generates current timestamp
    
    # ✗ NEVER DO THIS - redundant __init__ override!
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     if self.timestamp is None:
    #         self.timestamp = Timestamp_Now()  # Already handled!

# Usage
response1 = Schema__Response()
response2 = Schema__Response()

print(response1.request_id)  # e.g., "a4f3c2b1-..."
print(response2.request_id)  # Different: "b7d9e4a2-..."
print(response1.timestamp)   # e.g., "2024-01-15T10:30:45Z"
print(response2.timestamp)   # Different: "2024-01-15T10:30:46Z"
```

**Auto-initializing types include:**
- `Random_Guid` - Generates unique UUID on each instantiation
- `Timestamp_Now` - Captures current timestamp on instantiation
- Any custom Type_Safe class with default generation logic

**Key principle:** If a type generates its own default value, don't override `__init__` to set it. The whole point of these types is to auto-generate their values!

### Complex Object Auto-initialization During __init__

When Type_Safe classes are used as attributes in other classes, they're automatically instantiated during the parent's `__init__` phase:

```python
class Schema__Config(Type_Safe):
    retry_count : Safe_UInt                   # Auto: 0
    timeout     : Safe_UInt = 30              # Explicit default: 30
    max_retries : Safe_UInt = 3               # Explicit default: 3

class Schema__Database__Config(Type_Safe):
    host        : Safe_Str__Host              # Auto: ''
    port        : Safe_UInt__Port             # Auto: 0 (or could set default)
    ssl_enabled : bool = True                 # Explicit default: True

class Schema__Service(Type_Safe):
    name        : Safe_Str                    # Auto: ''
    config      : Schema__Config              # Auto: NEW Schema__Config() during __init__
    db_config   : Schema__Database__Config    # Auto: NEW Schema__Database__Config() during __init__
    fallback    : Schema__Config = None       # Explicitly nullable - no auto-init

# During instantiation, Type_Safe's __init__ creates new instances
service1 = Schema__Service()
service2 = Schema__Service()

# Each service has its OWN config instances (not shared!)
service1.config.retry_count = 5
service2.config.retry_count = 10

print(service1.config.retry_count)      # 5 - instance 1's value
print(service2.config.retry_count)      # 10 - instance 2's value (not affected!)

# The nested objects are fully initialized with their defaults
print(service1.config.timeout)          # 30 - explicit default preserved
print(service1.config.max_retries)      # 3  - explicit default preserved
print(service1.db_config.ssl_enabled)   # True - nested default preserved
print(service1.db_config.port)          # 0 - auto-initialized

# Nullable fields remain None
print(service1.fallback)                # None - explicitly nullable, not auto-initialized
```

### When to Use None vs Relying on Auto-initialization

```python
class Schema__User(Type_Safe):
    # ✓ GOOD: Let Type_Safe handle defaults
    username    : Safe_Str__Username          # Auto: '' (or min length if required)
    age         : Safe_UInt__Age              # Auto: 0
    tags        : List[Safe_Str]              # Auto: [] (unique list)
    settings    : Schema__User_Settings       # Auto: Schema__User_Settings() (unique instance)
    
    # ✓ GOOD: Explicit None for truly optional fields with semantic meaning
    deleted_at  : Safe_Str__Timestamp = None  # None means "never deleted"
    referrer_id : Safe_Id             = None  # None means "no referrer"
    supervisor  : 'Schema__User'      = None  # None means "no supervisor"
    
    # ✗ AVOID: Using Optional when auto-init would work
    # description : Optional[Safe_Str]        # Just use Safe_Str
    # items      : Optional[List[str]]        # Just use List[str]
```

### Best Practices

1. **Trust auto-initialization** - Most types have sensible defaults
2. **Never assign mutable defaults in class definition** - Type_Safe prevents this footgun
3. **Use explicit `= None` sparingly** - Only when `None` has semantic meaning (e.g., "not set", "deleted", "unlimited")
4. **Avoid `Optional[]` in most cases** - Type_Safe handles this better with auto-init
5. **Document when None matters** - If `None` has special meaning, comment it
6. **Remember each instance is isolated** - No shared state between instances


### Security Benefits Summary

By preventing mutable defaults and auto-initializing unique instances, Type_Safe eliminates:
- **Data leaks** between user sessions
- **State pollution** across requests
- **Memory leaks** from shared references
- **Race conditions** in concurrent code
- **Debugging nightmares** from unexpected shared state

Each Type_Safe instance is a clean, isolated environment with its own state - exactly what secure, maintainable code needs.

## Advanced Topics

### Using Literal for Quick Enums

Type_Safe now supports `Literal` types with runtime enforcement - perfect for quick enums without creating separate Enum classes:

```python
from typing import Literal

class Schema__Open_Router__Message(Type_Safe):
    # Literal enforces these exact values at runtime!
    role    : Literal["assistant", "system", "user", "tool"]  # Only these 4 values allowed
    content : Safe_Str__Message_Content
    tool_id : Safe_Str = None

# Runtime validation works!
message      = Schema__Open_Router__Message()
message.role = "user"       # ✓ Valid
message.role = "admin"      # ✗ ValueError: must be one of ["assistant", "system", "user", "tool"]

class Schema__Provider_Preferences(Type_Safe):
    # Mix Literal with other types
    data_collection : Literal["allow", "deny"]         = "deny"   # Two-state without boolean
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
        if name == 'value' and value == 'special_case':             # Only override Type_Safe internals when absolutely required
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
    
class Routes_Users(Fast_API__Routes):                                   # Use directly in routes - automatic conversion happens!
    tag = 'users'
    
    def create_user(self, request: UserRequest) -> UserResponse:        # request is Type_Safe with full validation
        # No manual conversion needed!
        user_id = self.user_service.create(request)
        
        return UserResponse(id         = user_id              ,
                            username   = request.username     ,
                            created_at = timestamp_now()      )
    
    def get_user(self, user_id: Safe_Str__UserId) -> UserResponse:      # Even path parameters can use Safe types!
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
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id  import Safe_Id
from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Money  import Safe_Float__Money
from osbot_utils.type_safe.primitives.safe_str.Safe_Str__Url        import Safe_Str__Url
from typing                                                         import List, Dict

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
    status   : str                  = "pending"
    tracking : Safe_Str__Url         = None
    
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
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.decorators                                               import type_safe

# Safe Strings
from osbot_utils.type_safe.primitives.safe_str.Safe_Str                             import Safe_Str
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Name      import Safe_Str__File__Name
from osbot_utils.type_safe.primitives.safe_str.web.Safe_Str__Url                    import Safe_Str__Url
from osbot_utils.type_safe.primitives.safe_str.web.Safe_Str__IP_Address             import Safe_Str__IP_Address

# Safe Numbers  
from osbot_utils.type_safe.primitives.safe_int.Safe_Int                             import Safe_Int
from osbot_utils.type_safe.primitives.safe_uint.Safe_UInt__Port                     import Safe_UInt__Port
from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Money                  import Safe_Float__Money

# Identifiers
from osbot_utils.type_safe.primitives.safe_str.identifiers.Safe_Id                  import Safe_Id
from osbot_utils.type_safe.primitives.safe_str.identifiers.Random_Guid              import Random_Guid
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