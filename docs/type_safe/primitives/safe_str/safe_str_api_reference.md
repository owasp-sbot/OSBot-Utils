# Safe_Str API Reference

## Core Classes

### Safe_Str

Base class for all type-safe string primitives.

```python
class Safe_Str(Type_Safe__Primitive, str)
```

#### Class Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `max_length` | `int` | `512` | Maximum allowed string length |
| `regex` | `re.Pattern` | `r'[^a-zA-Z0-9]'` | Pattern for validation/replacement |
| `regex_mode` | `Enum__Safe_Str__Regex_Mode` | `REPLACE` | How to interpret regex (REPLACE or MATCH) |
| `replacement_char` | `str` | `'_'` | Character to replace invalid chars with |
| `allow_empty` | `bool` | `True` | Whether empty strings are allowed |
| `trim_whitespace` | `bool` | `False` | Whether to trim leading/trailing whitespace |
| `allow_all_replacement_char` | `bool` | `True` | Whether result can be all replacement chars |
| `strict_validation` | `bool` | `False` | If True, reject invalid input instead of sanitizing |
| `exact_length` | `bool` | `False` | If True, require exact length match |

#### Methods

##### `__new__(cls, value: Optional[str] = None) -> 'Safe_Str'`

Creates a new Safe_Str instance with validation and sanitization.

**Parameters:**
- `value`: String to validate/sanitize (or None)

**Returns:**
- New Safe_Str instance

**Raises:**
- `ValueError`: If validation fails or constraints are violated

**Example:**
```python
safe = Safe_Str("Hello@World!")  # Returns: "Hello_World_"
```

##### `validate_and_sanitize(cls, value: str) -> str`

Class method that performs validation and sanitization based on configuration.

**Parameters:**
- `value`: String to process

**Returns:**
- Sanitized string

**Raises:**
- `ValueError`: If strict validation enabled and value is invalid

---

### Enum__Safe_Str__Regex_Mode

Enumeration defining how regex patterns are interpreted.

```python
class Enum__Safe_Str__Regex_Mode(Enum):
    REPLACE = 'replace'  # Regex matches invalid chars to replace
    MATCH = 'match'      # Regex defines valid pattern to match
```

---

## File System Types

### Safe_Str__File__Name

Safe filename preventing directory traversal and invalid characters.

```python
class Safe_Str__File__Name(Safe_Str):
    regex = re.compile(r'[^a-zA-Z0-9_\-. ]')
    allow_empty = False
    trim_whitespace = True
    allow_all_replacement_char = False
```

**Usage:**
```python
filename = Safe_Str__File__Name("my-file.txt")      # ✓ Valid
filename = Safe_Str__File__Name("../etc/passwd")    # Sanitized
filename = Safe_Str__File__Name("")                 # ✗ ValueError
```

### Safe_Str__File__Path

Safe file path allowing directory separators.

```python
class Safe_Str__File__Path(Safe_Str):
    regex = re.compile(r'[^a-zA-Z0-9_\-./\\ ]')
    max_length = 1024
    allow_empty = True
    trim_whitespace = True
    allow_all_replacement_char = False
```

**Usage:**
```python
path = Safe_Str__File__Path("/home/user/file.txt")   # ✓ Valid
path = Safe_Str__File__Path("C:\\Users\\file.txt")   # ✓ Valid
```

---

## Web/Network Types

### Safe_Str__Url

URL validation and sanitization.

```python
class Safe_Str__Url(Safe_Str):
    regex = re.compile(r'^(?!https?://).*|[^a-zA-Z0-9:/\-._~&=?#+%@]')
    max_length = 2048
    trim_whitespace = True
    allow_all_replacement_char = False
```

**Features:**
- Validates URL structure
- Removes invalid URL characters
- Enforces maximum URL length (2048 chars)

**Usage:**
```python
url = Safe_Str__Url("https://example.com/page?q=test")
url = Safe_Str__Url("javascript:alert('xss')")  # Sanitized
```

### Safe_Str__IP_Address

Validates IP addresses using Python's `ipaddress` module.

```python
class Safe_Str__IP_Address(Type_Safe__Primitive, str)
```

**Features:**
- Validates both IPv4 and IPv6 addresses
- Returns canonical representation
- Trims whitespace automatically

**Usage:**
```python
ip = Safe_Str__IP_Address("192.168.1.1")       # ✓ IPv4
ip = Safe_Str__IP_Address("::1")               # ✓ IPv6
ip = Safe_Str__IP_Address("999.999.999.999")   # ✗ ValueError
```

---

## HTTP Types

### Safe_Str__Http__Content_Type

HTTP Content-Type header validation.

```python
class Safe_Str__Http__Content_Type(Safe_Str):
    regex = re.compile(r'[^a-zA-Z0-9/\-+.;= ]')
    max_length = 256
    allow_empty = False
    trim_whitespace = True
    allow_all_replacement_char = False
```

**Usage:**
```python
ct = Safe_Str__Http__Content_Type("application/json")
ct = Safe_Str__Http__Content_Type("text/html; charset=utf-8")
```

### Safe_Str__Http__ETag

HTTP ETag header validation.

```python
class Safe_Str__Http__ETag(Safe_Str):
    regex = re.compile(r'[^a-zA-Z0-9"\/\-_.:]')
    max_length = 128
    trim_whitespace = True
```

**Usage:**
```python
etag = Safe_Str__Http__ETag('"33a64df551"')
etag = Safe_Str__Http__ETag('W/"weak-etag"')
```

### Safe_Str__Http__Last_Modified

HTTP Last-Modified header validation.

```python
class Safe_Str__Http__Last_Modified(Safe_Str):
    regex = re.compile(r'[^a-zA-Z0-9:, -]')
    max_length = 64
    trim_whitespace = True
```

### Safe_Str__Http__Text

General HTTP text content with minimal filtering.

```python
class Safe_Str__Http__Text(Safe_Str):
    max_length = 1048576  # 1MB
    regex = re.compile(r'[\x00\x01-\x08\x0B\x0C\x0E-\x1F\x7F]')
    trim_whitespace = True
    normalize_newlines = True
```

**Features:**
- Removes control characters
- Normalizes newlines (CRLF → LF)
- Allows most printable characters

### Safe_Str__Html

HTML content with minimal filtering.

```python
class Safe_Str__Html(Safe_Str):
    max_length = 1048576  # 1MB
    regex = re.compile(r'[\x00\x01-\x08\x0B\x0C\x0E-\x1F]')
```

**Features:**
- Allows HTML tags and structure
- Removes null bytes and control characters
- Suitable for sanitized HTML content

---

## Text Types

### Safe_Str__Text

General text with moderate restrictions.

```python
class Safe_Str__Text(Safe_Str):
    regex = re.compile(r'[^a-zA-Z0-9_ ()\[\]\-+=:;,.?]')
    max_length = 4096
```

**Usage:**
```python
text = Safe_Str__Text("Hello, World! (2024)")  # ✓ Valid
text = Safe_Str__Text("<script>alert()</script>")  # Sanitized
```

### Safe_Str__Text__Dangerous

Text allowing more special characters (use with caution).

```python
class Safe_Str__Text__Dangerous(Safe_Str):
    regex = re.compile(r'[^a-zA-Z0-9_\s!@#$%^&*()\[\]{}\-+=:;,.?"/\\<>\']')
    max_length = 65536
```

---

## Cryptographic Types

### Safe_Str__Hash

Fixed-length hexadecimal hash values.

```python
class Safe_Str__Hash(Safe_Str):
    regex = re.compile(r'[^a-fA-F0-9]')
    max_length = 10
    allow_empty = False
    trim_whitespace = True
    strict_validation = True
    exact_length = True
```

**Helper Function:**

```python
def safe_str_hash(value: Any) -> Safe_Str__Hash:
    """Create a 10-character MD5 hash"""
```

**Usage:**
```python
# Direct creation
hash_val = Safe_Str__Hash("a1b2c3d4e5")  # ✓ Valid

# Using helper
from osbot_utils.type_safe.primitives.safe_str.Safe_Str__Hash import safe_str_hash
hash_val = safe_str_hash("my data")  # Creates hash
```

---

## Version Types

### Safe_Str__Version

Semantic version string validation.

```python
class Safe_Str__Version(Safe_Str):
    regex = re.compile(r'^v(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    regex_mode = Enum__Safe_Str__Regex_Mode.MATCH
    max_length = 12
    allow_empty = False
    trim_whitespace = True
    strict_validation = True
```

**Pattern:** `vX.Y.Z` where X, Y, Z are 1-3 digit numbers

**Usage:**
```python
version = Safe_Str__Version("v1.2.3")     # ✓ Valid
version = Safe_Str__Version("v999.0.1")   # ✓ Valid
version = Safe_Str__Version("1.2.3")      # ✗ Missing 'v'
version = Safe_Str__Version("v1.2")       # ✗ Missing patch
```

---

## Creating Custom Safe_Str Types

### Basic Custom Type

```python
import re
from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str

class Safe_Str__Username(Safe_Str):
    regex = re.compile(r'[^a-z0-9_]')
    max_length = 20
    allow_empty = False
    trim_whitespace = True
```

### Advanced Custom Type

```python
class Safe_Str__Email(Safe_Str):
    regex = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
    regex_mode = Enum__Safe_Str__Regex_Mode.MATCH
    max_length = 254
    strict_validation = True
    
    def __new__(cls, value):
        # Additional validation
        if value and '@' in value:
            local, domain = value.rsplit('@', 1)
            if len(local) > 64:
                raise ValueError("Local part too long")
        
        return super().__new__(cls, value)
```

---

## Integration with Type_Safe

### Using in Type_Safe Classes

```python
from osbot_utils.type_safe.Type_Safe import Type_Safe

class UserData(Type_Safe):
    username: Safe_Str__Username
    email: Safe_Str__Email
    homepage: Safe_Str__Url
    ip_address: Safe_Str__IP_Address

# Automatic type conversion
user = UserData()
user.username = "john_doe"  # Converted to Safe_Str__Username
```

### Serialization

```python
# Serialize to JSON
data = user.json()
# Safe_Str values become regular strings

# Deserialize from JSON
user = UserData.from_json(data)
# Strings are converted back to Safe_Str types
```

---

## Error Handling

### Common Exceptions

| Exception | Cause | Example |
|-----------|-------|---------|
| `ValueError` | Value exceeds max_length | `Safe_Str("x" * 1000)` |
| `ValueError` | Empty when not allowed | `Safe_Str__File__Name("")` |
| `ValueError` | Pattern doesn't match (strict mode) | `Safe_Str__Version("invalid")` |
| `ValueError` | Invalid IP address | `Safe_Str__IP_Address("999.999.999.999")` |
| `ValueError` | All replacement chars when not allowed | Result is all underscores |

### Error Handling Pattern

```python
try:
    safe_value = Safe_Str__Email(user_input)
except ValueError as e:
    # Log the validation failure
    logger.warning(f"Invalid email: {e}")
    # Use default or reject
    safe_value = Safe_Str__Email("noreply@example.com")
```

---

## Performance Considerations

### Validation Timing

- Validation occurs once at object creation
- Subsequent string operations have no overhead
- Cache Safe_Str instances when possible

### Regex Performance

- Simple character class patterns are fastest
- Complex patterns with lookahead/lookbehind are slower
- Consider pattern complexity for high-frequency operations

### Memory Usage

- Safe_Str instances have minimal overhead over regular strings
- Class attributes are shared across instances
- No additional instance attributes beyond the string value

---

## Best Practices

1. **Choose Appropriate Types**
   - Use specific Safe_Str types for their intended purpose
   - Don't use Safe_Str__Html for SQL values

2. **Strict vs Sanitization**
   - Use `strict_validation=True` for critical validation
   - Use sanitization for user-facing inputs

3. **Length Limits**
   - Set appropriate `max_length` to prevent DoS
   - Consider storage and processing limits

4. **Custom Types**
   - Create domain-specific types for your application
   - Document validation rules clearly

5. **Error Handling**
   - Always handle `ValueError` exceptions
   - Log validation failures for security monitoring

6. **Testing**
   - Test with known attack vectors
   - Verify edge cases (empty, max length, special chars)

---

## Migration Guide

### From Regular Strings

```python
# Before
username = str(user_input)[:20]  # Basic truncation

# After
username = Safe_Str__Username(user_input)  # Full validation
```

### From Manual Validation

```python
# Before
if re.match(r'^[a-z0-9_]+$', username):
    safe_username = username
else:
    raise ValueError("Invalid username")

# After
safe_username = Safe_Str__Username(username)  # Automatic
```

### From Other Libraries

```python
# From bleach (HTML sanitization)
import bleach
clean_html = bleach.clean(user_html)

# With Safe_Str
clean_html = Safe_Str__Html(user_html)

# From validators library
import validators
if validators.email(email):
    valid_email = email

# With Safe_Str
valid_email = Safe_Str__Email(email)
```