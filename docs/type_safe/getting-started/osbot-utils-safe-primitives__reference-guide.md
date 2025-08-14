# OSBot-Utils Safe_* Primitives Complete Reference

## Quick Overview

The Safe_* primitives in OSBot-Utils provide type-safe, validated, and domain-specific wrappers around Python's built-in types (str, int, float). They enforce constraints at creation time and maintain type safety throughout their lifecycle.

## File Organization

```
osbot_utils/type_safe/primitives/
├── safe_float
│   ├── Safe_Float.py
│   ├── Safe_Float__Engineering.py
│   ├── Safe_Float__Money.py
│   └── Safe_Float__Percentage_Exact.py
├── safe_int
│   ├── Safe_Int.py
│   └── Timestamp_Now.py
├── safe_str
│   ├── Enum__Safe_Str__Regex_Mode.py
│   ├── Safe_Str.py
│   ├── cryptography
│   │   ├── hashes
│   │   │   ├── Safe_Str__Hash.py
│   │   │   ├── Safe_Str__SHA1.py
│   │   │   └── Safe_Str__SHA1__Short.py
│   │   └── nacl
│   │       ├── Safe_Str__NaCl__Private_Key.py
│   │       ├── Safe_Str__NaCl__Public_Key.py
│   │       └── Schema__NaCl__Keys.py
│   ├── filesystem
│   │   ├── Safe_Str__File__Name.py
│   │   └── Safe_Str__File__Path.py
│   ├── git
│   │   ├── Safe_Str__Git__Branch.py
│   │   ├── Safe_Str__Git__Ref.py
│   │   ├── Safe_Str__Git__Ref_Base.py
│   │   ├── Safe_Str__Git__Tag.py
│   │   └── Safe_Str__Version.py
│   ├── github
│   │   ├── Safe_Str__GitHub__Repo.py
│   │   ├── Safe_Str__GitHub__Repo_Name.py
│   │   └── Safe_Str__GitHub__Repo_Owner.py
│   ├── http
│   │   ├── Safe_Str__Http__Content_Type.py
│   │   ├── Safe_Str__Http__ETag.py
│   │   ├── Safe_Str__Http__Last_Modified.py
│   │   └── Safe_Str__Http__Text.py
│   ├── identifiers
│   │   ├── Guid.py
│   │   ├── Random_Guid.py
│   │   ├── Random_Guid_Short.py
│   │   └── Safe_Id.py
│   ├── text
│   │   ├── Safe_Str__Text.py
│   │   └── Safe_Str__Text__Dangerous.py
│   └── web
│       ├── Safe_Str__Html.py
│       ├── Safe_Str__IP_Address.py
│       └── Safe_Str__Url.py
└── safe_uint
    ├── Safe_UInt.py
    ├── Safe_UInt__Byte.py
    ├── Safe_UInt__FileSize.py
    ├── Safe_UInt__Percentage.py
    └── Safe_UInt__Port.py
```

## Complete List of Safe_* Primitives

### Categories:
1. **Safe_Str** - String primitives with validation and sanitization
2. **Safe_Int** - Integer primitives with range validation  
3. **Safe_Float** - Floating-point primitives with precision control
4. **Identifiers** - Identity primitives for domain-specific IDs and GUIDs
5. **Timestamps** - Time-based integer primitives

## Summary Table

| Category | Class Name | Purpose | Key Features |
|----------|------------|---------|--------------|
| **String Types** | | | |
| Core | `Safe_Str` | Base string validation | Regex validation, length limits, sanitization |
| File System | `Safe_Str__File__Name` | Safe filenames | Prevents path traversal, removes dangerous chars |
| | `Safe_Str__File__Path` | Safe file paths | Allows directory separators, validates paths |
| Web/Network | `Safe_Str__Url` | URL validation | Sanitizes URLs, prevents XSS |
| | `Safe_Str__IP_Address` | IP address validation | IPv4/IPv6 validation |
| HTTP | `Safe_Str__Http__Content_Type` | HTTP Content-Type headers | Prevents header injection |
| | `Safe_Str__Http__ETag` | HTTP ETag headers | Validates ETag format |
| | `Safe_Str__Http__Last_Modified` | HTTP Last-Modified headers | Date format validation |
| | `Safe_Str__Http__Text` | HTTP text content | Removes control characters |
| | `Safe_Str__Html` | HTML content | Minimal filtering for HTML |
| Text | `Safe_Str__Text` | General text | Moderate restrictions |
| | `Safe_Str__Text__Dangerous` | Text with special chars | More permissive (use with caution) |
| Crypto | `Safe_Str__Hash` | Hash values | Fixed-length hex validation |
| Version | `Safe_Str__Version` | Semantic versions | Pattern: vX.Y.Z |
| **Integer Types** | | | |
| Core | `Safe_Int` | Base integer validation | Range validation, type conversion |
| Unsigned | `Safe_UInt` | Unsigned integers | min_value=0, no bool |
| | `Safe_UInt__Byte` | Single byte | 0-255 range |
| | `Safe_UInt__Port` | Network ports | 0-65535 range |
| | `Safe_UInt__FileSize` | File sizes | With KB/MB/GB conversions |
| | `Safe_UInt__Percentage` | Percentage values | 0-100 range |
| **Float Types** | | | |
| Core | `Safe_Float` | Base float validation | Precision control, range validation |
| Financial | `Safe_Float__Money` | Currency calculations | Decimal arithmetic, 2 decimal places |
| | `Safe_Float__Percentage_Exact` | Precise percentages | 0-100, decimal arithmetic |
| Engineering | `Safe_Float__Engineering` | Engineering calculations | Epsilon tolerance, rounding |
| **Identity Types** | | | |
| Core | `Safe_Id` | Base identity type | Type-safe IDs, prevents mixing |
| | `Guid` | Deterministic GUID generation | UUID5 from string values |
| | `Random_Guid` | UUID/GUID generation | Auto-generates unique IDs |
| | `Random_Guid_Short` | Short GUID variant | Shorter unique identifiers |
| **Integer Timestamps** | | | |
| | `Timestamp_Now` | Unix timestamp | Auto-generates current timestamp |

---

## Detailed Reference

## Safe_Str Types

### Core String Type

#### `Safe_Str`
**Import:** `from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str`

**Purpose:** Base class for all type-safe string primitives with validation and sanitization.

**Configuration:**
```python
class Safe_Str(Type_Safe__Primitive, str):
    max_length = 512                    # Maximum string length
    regex = re.compile(r'[^a-zA-Z0-9]') # Pattern for validation/replacement
    regex_mode = REPLACE                 # REPLACE or MATCH mode
    replacement_char = '_'               # Character for replacements
    allow_empty = True                   # Whether empty strings allowed
    trim_whitespace = False              # Auto-trim whitespace
    strict_validation = False            # Reject vs sanitize
    exact_length = False                 # Require exact length
```

**Usage:**
```python
safe_text = Safe_Str("Hello@World!")  # Returns: "Hello_World_"
```

---

### File System Types

#### `Safe_Str__File__Name`
**Import:** `from osbot_utils.type_safe.primitives.safe_str.Safe_Str__File__Name import Safe_Str__File__Name`

**Purpose:** Prevents directory traversal and invalid filename characters.

**Key Features:**
- Removes `.` and `/` characters
- Prevents empty filenames
- Auto-trims whitespace
- Sanitizes dangerous characters

**Usage:**
```python
filename = Safe_Str__File__Name("../../etc/passwd")  # Returns: "___etc_passwd"
filename = Safe_Str__File__Name("my-file.txt")       # Returns: "my-file.txt"
```

#### `Safe_Str__File__Path`
**Import:** `from osbot_utils.type_safe.primitives.safe_str.Safe_Str__File__Path import Safe_Str__File__Path`

**Purpose:** Safe file paths with directory separators allowed.

**Key Features:**
- Allows `/` and `\` for paths
- Max length: 1024 characters
- Preserves directory structure

**Usage:**
```python
path = Safe_Str__File__Path("/home/user/docs/file.txt")  # Valid
path = Safe_Str__File__Path("C:\\Users\\Docs\\file.txt")  # Valid
```

---

### Web/Network Types

#### `Safe_Str__Url`
**Import:** `from osbot_utils.type_safe.primitives.safe_str.Safe_Str__Url import Safe_Str__Url`

**Purpose:** URL validation and sanitization, prevents XSS and injection.

**Key Features:**
- Max length: 2048 characters
- Removes invalid URL characters
- Sanitizes dangerous patterns
- Validates URL structure

**Usage:**
```python
url = Safe_Str__Url("https://example.com/page?q=test")  # Valid
url = Safe_Str__Url("javascript:alert('xss')")          # Sanitized
```

#### `Safe_Str__IP_Address`
**Import:** `from osbot_utils.type_safe.primitives.safe_str.Safe_Str__IP_Address import Safe_Str__IP_Address`

**Purpose:** Validates IPv4 and IPv6 addresses using Python's ipaddress module.

**Key Features:**
- Validates both IPv4 and IPv6
- Returns canonical representation
- Auto-trims whitespace
- Rejects invalid IPs

**Usage:**
```python
ip = Safe_Str__IP_Address("192.168.1.1")       # Valid IPv4
ip = Safe_Str__IP_Address("::1")               # Valid IPv6
ip = Safe_Str__IP_Address("999.999.999.999")   # Raises ValueError
```

---

### HTTP Header Types

#### `Safe_Str__Http__Content_Type`
**Import:** `from osbot_utils.helpers.safe_str.http.Safe_Str__Http__Content_Type import Safe_Str__Http__Content_Type`

**Purpose:** HTTP Content-Type header validation, prevents header injection.

**Key Features:**
- Max length: 256 characters
- Removes CRLF characters
- Validates MIME type format

**Usage:**
```python
ct = Safe_Str__Http__Content_Type("application/json")
ct = Safe_Str__Http__Content_Type("text/html; charset=utf-8")
```

#### `Safe_Str__Http__ETag`
**Import:** `from osbot_utils.helpers.safe_str.http.Safe_Str__Http__ETag import Safe_Str__Http__ETag`

**Purpose:** HTTP ETag header validation.

**Usage:**
```python
etag = Safe_Str__Http__ETag('"33a64df551"')      # Strong ETag
etag = Safe_Str__Http__ETag('W/"weak-etag-123"')  # Weak ETag
```

#### `Safe_Str__Html`
**Import:** `from osbot_utils.helpers.safe_str.http.Safe_Str__Html import Safe_Str__Html`

**Purpose:** HTML content with minimal filtering (allows HTML tags).

**Key Features:**
- Max length: 1MB
- Removes null bytes and control characters
- Allows HTML structure

---

### Cryptographic Types

#### `Safe_Str__Hash`
**Import:** `from osbot_utils.type_safe.primitives.safe_str.Safe_Str__Hash import Safe_Str__Hash`

**Purpose:** Fixed-length hexadecimal hash values.

**Key Features:**
- Exactly 10 characters (by default)
- Hexadecimal only (0-9, a-f, A-F)
- Strict validation

**Helper Function:**
```python
from osbot_utils.type_safe.primitives.safe_str.Safe_Str__Hash import safe_str_hash

hash_value = safe_str_hash("my data")  # Creates 10-char MD5 hash
```

---

## Safe_Int Types

### Core Integer Type

#### `Safe_Int`
**Import:** `from osbot_utils.type_safe.primitives.safe_int.Safe_Int import Safe_Int`

**Purpose:** Base integer type with range validation and type conversion.

**Configuration:**
```python
class Safe_Int(Type_Safe__Primitive, int):
    min_value = None        # Minimum allowed value
    max_value = None        # Maximum allowed value
    allow_none = True       # Convert None to 0
    allow_bool = False      # Accept boolean values
    allow_str = True        # Convert strings to int
    strict_type = False     # Only accept int type
```

**Usage:**
```python
value = Safe_Int("42")        # Converts string to 42
value = Safe_Int(None)        # Returns 0 (if allow_none=True)
value = Safe_Int(True)        # Raises TypeError (if allow_bool=False)
```

---

### Unsigned Integer Types

#### `Safe_UInt`
**Import:** `from osbot_utils.helpers.safe_int.Safe_UInt import Safe_UInt`

**Purpose:** Base unsigned integer (non-negative).

**Configuration:**
- `min_value = 0`
- `allow_bool = False`

#### `Safe_UInt__Byte`
**Import:** `from osbot_utils.helpers.safe_int.Safe_UInt__Byte import Safe_UInt__Byte`

**Purpose:** Single byte value (0-255).

**Usage:**
```python
byte = Safe_UInt__Byte(128)   # Valid
byte = Safe_UInt__Byte(256)   # ValueError: must be <= 255
```

#### `Safe_UInt__Port`
**Import:** `from osbot_utils.helpers.safe_int.Safe_UInt__Port import Safe_UInt__Port`

**Purpose:** Network port numbers (0-65535).

**Usage:**
```python
port = Safe_UInt__Port(8080)   # Valid HTTP port
port = Safe_UInt__Port(443)    # Valid HTTPS port
port = Safe_UInt__Port(70000)  # ValueError: must be <= 65535
```

#### `Safe_UInt__FileSize`
**Import:** `from osbot_utils.helpers.safe_int.Safe_UInt__FileSize import Safe_UInt__FileSize`

**Purpose:** File sizes with conversion methods.

**Features:**
- Max value: 2^63-1
- Conversion methods: `to_kb()`, `to_mb()`, `to_gb()`

**Usage:**
```python
size = Safe_UInt__FileSize(1048576)  # 1 MB in bytes
print(f"{size.to_mb():.2f} MB")      # 1.00 MB
print(f"{size.to_gb():.4f} GB")      # 0.0010 GB
```

#### `Safe_UInt__Percentage`
**Import:** `from osbot_utils.helpers.safe_int.Safe_UInt__Percentage import Safe_UInt__Percentage`

**Purpose:** Percentage values (0-100).

**Usage:**
```python
progress = Safe_UInt__Percentage(75)   # 75%
progress = Safe_UInt__Percentage(101)  # ValueError: must be <= 100
```

---

## Safe_Float Types

### Core Float Type

#### `Safe_Float`
**Import:** `from osbot_utils.type_safe.primitives.safe_float.Safe_Float import Safe_Float`

**Purpose:** Base float type with precision control and range validation.

**Configuration:**
```python
class Safe_Float(Type_Safe__Primitive, float):
    min_value = None          # Minimum value
    max_value = None          # Maximum value
    decimal_places = None     # Decimal precision
    use_decimal = False       # Use Python's Decimal
    epsilon = 1e-9           # Equality tolerance
    round_output = True      # Round to decimal_places
    clamp_to_range = False   # Clamp vs error
    allow_none = True        # Convert None to 0.0
    allow_str = True         # Convert strings
    allow_int = True         # Convert integers
```

---

### Financial Types

#### `Safe_Float__Money`
**Import:** `from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Money import Safe_Float__Money`

**Purpose:** Financial calculations with exact decimal arithmetic.

**Configuration:**
- `decimal_places = 2` (cents precision)
- `use_decimal = True` (exact arithmetic)
- `min_value = 0.0` (no negative amounts)

**Usage:**
```python
price = Safe_Float__Money(19.99)
tax = Safe_Float__Money(1.65)
total = price + tax  # Exactly 21.64 (no float errors)

# Division with rounding
split = Safe_Float__Money(100.00)
three_way = split / 3  # 33.33 (not 33.333333...)
```

#### `Safe_Float__Percentage_Exact`
**Import:** `from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Percentage_Exact import Safe_Float__Percentage_Exact`

**Purpose:** Precise percentage calculations (0-100).

**Configuration:**
- `min_value = 0.0`, `max_value = 100.0`
- `decimal_places = 2`
- `use_decimal = True`

**Usage:**
```python
completion = Safe_Float__Percentage_Exact(75.5)
remaining = Safe_Float__Percentage_Exact(100.0) - completion  # Exactly 24.50
```

---

### Engineering Types

#### `Safe_Float__Engineering`
**Import:** `from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Engineering import Safe_Float__Engineering`

**Purpose:** Engineering calculations with tolerance-based comparisons.

**Configuration:**
- `epsilon = 1e-6` (engineering tolerance)
- `round_output = True`
- `use_decimal = False` (performance over exactness)

**Usage:**
```python
voltage = Safe_Float__Engineering(3.3)
current = Safe_Float__Engineering(0.025)
power = voltage * current  # Clean result without excessive decimals
```

---

## Identity Types (identifiers/)

### Core Identity Type

#### `Safe_Id`
**Import:** `from osbot_utils.type_safe.primitives.identifiers.Safe_Id import Safe_Id`

**Purpose:** Base class for creating domain-specific type-safe identifiers.

**Key Features:**
- Type identity preservation (UserId ≠ ProductId)
- Prevents mixing different ID types
- String-based with type checking
- Auto-generates safe ID if none provided
- Applies safe_id sanitization (regex: `[^a-zA-Z0-9_-]`)
- Max length: 512 characters (configurable)

**Creating Domain IDs:**
```python
class UserId(Safe_Id): pass
class ProductId(Safe_Id): pass
class OrderId(Safe_Id): pass

# Usage
user_id = UserId("USR-123")
product_id = ProductId("PRD-456")

# Type safety
assert user_id != product_id  # Different types, even with same value!

# But convenient string comparison
assert user_id == "USR-123"  # Works for convenience
```

#### `Guid`
**Import:** `from osbot_utils.type_safe.primitives.identifiers.Guid import Guid`

**Purpose:** Deterministic GUID generation from string values using UUID5.

**Key Features:**
- Generates deterministic UUIDs (same input = same output)
- Uses UUID5 with a fixed namespace (`2cfec064-537a-4ff7-8fdc-2fc9e2606f3d`)
- If input is already a valid GUID, returns it unchanged
- If input is any other string, generates UUID5 from it
- Type-safe GUID handling
- Raises ValueError if input is not a string

**Usage:**
```python
# Generate deterministic GUID from string
guid1 = Guid("user@example.com")  # Always same GUID for this email
guid2 = Guid("user@example.com")  # Same as guid1
assert guid1 == guid2

# Pass through existing valid GUIDs
existing = Guid("550e8400-e29b-41d4-a716-446655440000")  # Returns unchanged

# Different inputs = different GUIDs
user_guid = Guid("user123")
prod_guid = Guid("product456")
assert user_guid != prod_guid

# Non-string input raises error
guid = Guid(123)  # Raises ValueError: value provided was not a string
```

#### `Random_Guid`
**Import:** `from osbot_utils.type_safe.primitives.identifiers.Random_Guid import Random_Guid`

**Purpose:** UUID/GUID generation and validation.

**Features:**
- Auto-generates UUID if none provided
- Validates UUID format using `is_guid()`
- Type-safe GUID handling
- Raises ValueError if invalid GUID provided

**Usage:**
```python
# Auto-generate
guid = Random_Guid()  # Creates new UUID

# From existing
guid = Random_Guid("550e8400-e29b-41d4-a716-446655440000")

# Invalid GUID
guid = Random_Guid("not-a-guid")  # Raises ValueError
```

#### `Random_Guid_Short`
**Import:** `from osbot_utils.type_safe.primitives.identifiers.Random_Guid_Short import Random_Guid_Short`

**Purpose:** Shorter unique identifier generation.

**Features:**
- Auto-generates short GUID if none provided
- More compact than full UUID
- Useful for readable identifiers

**Usage:**
```python
# Auto-generate
short_id = Random_Guid_Short()  # Creates short GUID

# From existing
short_id = Random_Guid_Short("abc123")
```

---

## Integer Timestamp Types

### Timestamp Type

#### `Timestamp_Now`
**Import:** `from osbot_utils.type_safe.primitives.safe_int.Timestamp_Now import Timestamp_Now`

**Purpose:** Unix timestamp generation and handling.

**Features:**
- Auto-generates current timestamp if none provided
- Integer-based (Unix timestamp)
- Inherits from Type_Safe__Primitive and int

**Usage:**
```python
# Auto-generate current timestamp
timestamp = Timestamp_Now()  # Current Unix timestamp

# From existing timestamp
timestamp = Timestamp_Now(1234567890)

# Convert to string
print(str(timestamp))  # "1234567890"
```

---

## Usage in Type_Safe Classes

### Example: Complete Domain Model

```python
from osbot_utils.type_safe.Type_Safe import Type_Safe
from typing import List, Dict

# Define domain-specific IDs
class UserId(Safe_Id): pass
class OrderId(Safe_Id): pass
class ProductId(Safe_Id): pass

class Order(Type_Safe):
    # Identity
    id: OrderId
    user_id: UserId
    
    # Financial
    subtotal: Safe_Float__Money
    tax: Safe_Float__Money
    shipping: Safe_Float__Money
    discount_percentage: Safe_Float__Percentage_Exact
    
    # Items
    product_ids: List[ProductId]
    quantities: List[Safe_UInt]
    
    # Metadata
    status: Safe_Str
    tracking_url: Safe_Str__Url
    customer_ip: Safe_Str__IP_Address
    
    def total(self) -> Safe_Float__Money:
        discount = self.subtotal * (self.discount_percentage / 100)
        return self.subtotal - discount + self.tax + self.shipping

# Usage
order = Order(
    id=OrderId("ORD-12345"),
    user_id=UserId("USR-67890"),
    subtotal=99.99,
    tax=8.25,
    shipping=5.00,
    discount_percentage=10.0,
    product_ids=[ProductId("PRD-001"), ProductId("PRD-002")],
    quantities=[1, 2],
    status="pending",
    tracking_url="https://tracking.example.com/12345",
    customer_ip="192.168.1.100"
)

# All operations are type-safe!
print(f"Order Total: ${order.total()}")  # Exact calculation
```

---

## Key Benefits

1. **Type Safety**: Prevents mixing incompatible types (UserId ≠ ProductId)
2. **Validation**: Enforces domain constraints at creation
3. **Security**: Automatic sanitization prevents injection attacks
4. **Precision**: Exact arithmetic for financial calculations
5. **Self-Documenting**: Type names express intent and constraints
6. **Error Prevention**: Catches issues at assignment, not deep in execution

## Best Practices

1. **Create Domain-Specific Types**: Don't use generic Safe_Str, create `Safe_Str__Email`, `Safe_Str__Username`, etc.
2. **Use at Boundaries**: Apply Safe_* types at system entry points
3. **Cache Instances**: Safe_* objects have validation overhead - cache when possible
4. **Choose Appropriate Types**: Use Safe_Float__Money for currency, Safe_UInt__Port for ports, etc.
5. **Layer Security**: Safe_* types are one layer - combine with other security measures