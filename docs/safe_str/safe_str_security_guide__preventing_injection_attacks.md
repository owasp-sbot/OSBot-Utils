# Safe_Str Security Guide: Preventing Injection Attacks and Data Validation

## Introduction

Safe_Str is designed with security as its primary goal. This guide demonstrates how Safe_Str types prevent common security vulnerabilities and provides best practices for using them in security-critical applications.

## Threat Model and Protection

### What Safe_Str Protects Against

| Threat | Protection Mechanism | Safe_Str Types |
|--------|---------------------|----------------|
| **SQL Injection** | Character filtering, pattern validation | Safe_Str (custom) |
| **Command Injection** | Shell metacharacter removal | Safe_Str (custom) |
| **Path Traversal** | Directory separator filtering | Safe_Str__File__Name |
| **XSS Attacks** | HTML/JS character sanitization | Safe_Str__Text, Safe_Str__Html |
| **Header Injection** | CRLF removal | Safe_Str__Http__* types |
| **URL Manipulation** | URL validation and sanitization | Safe_Str__Url |
| **IP Spoofing** | IP address validation | Safe_Str__IP_Address |
| **Format String Attacks** | Character restrictions | Safe_Str (custom) |

## SQL Injection Prevention

### The Vulnerability

```python
# DANGEROUS - SQL Injection vulnerable
def get_user_unsafe(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# Attack vector
get_user_unsafe("admin' OR '1'='1")  # Returns all users!
```

### Safe_Str Protection

```python
import re
from osbot_utils.helpers.safe_str.Safe_Str import Safe_Str

class Safe_Str__SQL_Identifier(Safe_Str):
    """Safe SQL identifier - table/column names only"""
    regex = re.compile(r'[^a-zA-Z0-9_]')
    max_length = 64  # MySQL identifier limit
    allow_empty = False
    trim_whitespace = True

class Safe_Str__SQL_Value(Safe_Str):
    """Safe SQL value - alphanumeric and basic punctuation"""
    regex = re.compile(r"[^a-zA-Z0-9\s\-_.,]")
    max_length = 255
    strict_validation = False  # Sanitize instead of reject

# Safe usage
def get_user_safe(username):
    safe_username = Safe_Str__SQL_Value(username)
    # Even with string formatting, injection is prevented
    query = f"SELECT * FROM users WHERE username = '{safe_username}'"
    return db.execute(query)

# Attack attempt is neutralized
get_user_safe("admin' OR '1'='1")
# Sanitized to: "admin__OR__1___1"
# Query becomes: SELECT * FROM users WHERE username = 'admin__OR__1___1'
```

### Best Practice: Defense in Depth

```python
class UserRepository(Type_Safe):
    table_name: Safe_Str__SQL_Identifier
    
    def get_user(self, username: Safe_Str__SQL_Value):
        # Layer 1: Safe_Str sanitization
        # Layer 2: Parameterized queries
        query = "SELECT * FROM users WHERE username = ?"
        return db.execute(query, [str(username)])
    
    def get_from_table(self, table: Safe_Str__SQL_Identifier):
        # Safe for dynamic table names (where parameterization doesn't work)
        query = f"SELECT * FROM {table}"
        return db.execute(query)
```

## Command Injection Prevention

### The Vulnerability

```python
# DANGEROUS - Command injection vulnerable
import os

def process_file_unsafe(filename):
    os.system(f"cat {filename}")
    
# Attack vector
process_file_unsafe("file.txt; rm -rf /")  # Executes deletion!
```

### Safe_Str Protection

```python
class Safe_Str__Shell_Arg(Safe_Str):
    """Safe shell argument - no shell metacharacters"""
    regex = re.compile(r'[^a-zA-Z0-9\-_./]')
    max_length = 255
    allow_empty = False
    
    def __new__(cls, value):
        # Additional validation for suspicious patterns
        if value and ('..' in value or value.startswith('/')):
            raise ValueError("Absolute paths and parent directory access not allowed")
        return super().__new__(cls, value)

def process_file_safe(filename):
    safe_filename = Safe_Str__Shell_Arg(filename)
    # Even with os.system, injection is prevented
    os.system(f"cat {safe_filename}")
    
# Attack neutralized
try:
    process_file_safe("file.txt; rm -rf /")
except ValueError:
    # Sanitized to: "file.txt_rm_-rf_"
    pass
```

### Safer Alternative with subprocess

```python
import subprocess

def process_file_best(filename):
    safe_filename = Safe_Str__Shell_Arg(filename)
    # Best practice: use subprocess with list arguments
    result = subprocess.run(
        ["cat", str(safe_filename)],
        capture_output=True,
        text=True
    )
    return result.stdout
```

## Path Traversal Prevention

### The Vulnerability

```python
# DANGEROUS - Path traversal vulnerable
def read_user_file_unsafe(user_id, filename):
    path = f"/data/users/{user_id}/{filename}"
    with open(path, 'r') as f:
        return f.read()

# Attack vector
read_user_file_unsafe("123", "../../etc/passwd")  # Reads system file!
```

### Safe_Str Protection

```python
from osbot_utils.helpers.safe_str.Safe_Str__File__Name import Safe_Str__File__Name
from osbot_utils.helpers.safe_str.Safe_Str__File__Path import Safe_Str__File__Path
from pathlib import Path

class SecureFileAccess(Type_Safe):
    base_directory: Safe_Str__File__Path
    
    def read_user_file(self, user_id: str, filename: str):
        # Sanitize filename - removes directory separators
        safe_filename = Safe_Str__File__Name(filename)
        # "../../etc/passwd" becomes "___etc_passwd"
        
        # Construct safe path
        user_dir = Safe_Str__File__Path(f"{self.base_directory}/{user_id}")
        full_path = Path(str(user_dir)) / str(safe_filename)
        
        # Additional check: ensure path is within base directory
        try:
            full_path = full_path.resolve()
            base = Path(str(self.base_directory)).resolve()
            if not str(full_path).startswith(str(base)):
                raise ValueError("Path traversal attempt detected")
        except (ValueError, OSError) as e:
            raise ValueError(f"Invalid file path: {e}")
        
        with open(full_path, 'r') as f:
            return f.read()

# Safe usage
file_access = SecureFileAccess(base_directory="/data/users")
content = file_access.read_user_file("123", "profile.json")  # ✓ Safe

# Attack prevented
try:
    content = file_access.read_user_file("123", "../../etc/passwd")
    # Filename becomes "___etc_passwd", path traversal prevented
except FileNotFoundError:
    pass  # File doesn't exist in safe directory
```

## Cross-Site Scripting (XSS) Prevention

### The Vulnerability

```python
# DANGEROUS - XSS vulnerable
def render_comment_unsafe(comment):
    return f"<div class='comment'>{comment}</div>"

# Attack vector
html = render_comment_unsafe("<script>alert('XSS')</script>")
# Browser executes the script!
```

### Safe_Str Protection

```python
from osbot_utils.helpers.safe_str.Safe_Str__Text import Safe_Str__Text
from osbot_utils.helpers.safe_str.http.Safe_Str__Html import Safe_Str__Html
import html

class Safe_Str__Comment(Safe_Str):
    """User comments - no HTML allowed"""
    regex = re.compile(r'[<>\"\'&]')  # Remove HTML special chars
    max_length = 1000
    replacement_char = ''  # Remove instead of replace

class ContentRenderer(Type_Safe):
    
    def render_comment_safe(self, comment: str) -> str:
        # Option 1: Strip HTML characters
        safe_comment = Safe_Str__Comment(comment)
        return f"<div class='comment'>{safe_comment}</div>"
    
    def render_comment_escaped(self, comment: str) -> str:
        # Option 2: HTML escape (preserves but neutralizes)
        safe_text = Safe_Str__Text(comment)
        escaped = html.escape(str(safe_text))
        return f"<div class='comment'>{escaped}</div>"
    
    def render_rich_content(self, content: str) -> str:
        # Option 3: Allow some HTML but sanitize
        safe_html = Safe_Str__Html(content)
        # Additional sanitization with a library like bleach
        return f"<div class='content'>{safe_html}</div>"

renderer = ContentRenderer()

# XSS attempts are neutralized
comment = "<script>alert('XSS')</script>"

# Method 1: Strips tags completely
result1 = renderer.render_comment_safe(comment)
# Returns: <div class='comment'>scriptalert('XSS')/script</div>

# Method 2: Escapes HTML
result2 = renderer.render_comment_escaped(comment)
# Returns: <div class='comment'>&lt;script&gt;alert('XSS')&lt;/script&gt;</div>
```

## HTTP Header Injection Prevention

### The Vulnerability

```python
# DANGEROUS - Header injection vulnerable
def set_cookie_unsafe(name, value):
    response.headers['Set-Cookie'] = f"{name}={value}"
    
# Attack vector
set_cookie_unsafe("user", "admin\r\nX-Injected-Header: malicious")
# Injects additional header!
```

### Safe_Str Protection

```python
from osbot_utils.helpers.safe_str.http.Safe_Str__Http__Content_Type import Safe_Str__Http__Content_Type

class Safe_Str__Cookie_Value(Safe_Str):
    """Safe cookie value - no control characters"""
    regex = re.compile(r'[\r\n\x00-\x1f\x7f;,\\"]')
    max_length = 4096  # Common cookie size limit
    trim_whitespace = True

class Safe_Str__Header_Value(Safe_Str):
    """Generic safe HTTP header value"""
    regex = re.compile(r'[\r\n\x00-\x1f\x7f]')
    max_length = 8192
    trim_whitespace = True

class HTTPResponse(Type_Safe):
    headers: Dict[str, Safe_Str__Header_Value]
    
    def set_cookie(self, name: str, value: str):
        safe_name = Safe_Str__Cookie_Value(name)
        safe_value = Safe_Str__Cookie_Value(value)
        
        cookie_header = f"{safe_name}={safe_value}; HttpOnly; Secure; SameSite=Strict"
        self.headers['Set-Cookie'] = Safe_Str__Header_Value(cookie_header)
    
    def set_content_type(self, content_type: str):
        safe_ct = Safe_Str__Http__Content_Type(content_type)
        self.headers['Content-Type'] = safe_ct

# Safe usage
response = HTTPResponse()
response.set_cookie("user", "admin\r\nX-Injected: bad")
# CRLF characters are removed, injection prevented
```

## URL Manipulation Prevention

### The Vulnerability

```python
# DANGEROUS - Open redirect vulnerable
def redirect_unsafe(url):
    return flask.redirect(url)

# Attack vector
redirect_unsafe("javascript:alert('XSS')")
redirect_unsafe("//evil.com")
```

### Safe_Str Protection

```python
from osbot_utils.helpers.safe_str.Safe_Str__Url import Safe_Str__Url
from urllib.parse import urlparse

class Safe_Str__Redirect_Url(Safe_Str__Url):
    """Safe redirect URL - only HTTPS to known domains"""
    
    def __new__(cls, value):
        # First apply parent sanitization
        safe_url = super().__new__(cls, value)
        
        # Parse and validate
        parsed = urlparse(str(safe_url))
        
        # Only allow HTTPS
        if parsed.scheme not in ['https']:
            raise ValueError("Only HTTPS URLs allowed for redirects")
        
        # Whitelist of allowed domains
        allowed_domains = ['example.com', 'app.example.com']
        if parsed.netloc not in allowed_domains:
            raise ValueError(f"Domain {parsed.netloc} not in whitelist")
        
        return safe_url

class SecureRedirect(Type_Safe):
    
    def redirect(self, url: str):
        try:
            safe_url = Safe_Str__Redirect_Url(url)
            return flask.redirect(str(safe_url))
        except ValueError as e:
            # Log potential attack
            logger.warning(f"Blocked redirect attempt: {e}")
            # Redirect to safe default
            return flask.redirect("https://example.com/")

# Attack prevented
redirector = SecureRedirect()
redirector.redirect("javascript:alert('XSS')")  # Blocked
redirector.redirect("//evil.com")                # Blocked
redirector.redirect("https://example.com/page")  # ✓ Allowed
```

## Input Validation Best Practices

### 1. Layer Your Defenses

```python
class SecureUserInput(Type_Safe):
    """Multi-layer input validation"""
    
    # Layer 1: Type-safe attributes
    username: Safe_Str__Username
    email: Safe_Str__Email
    bio: Safe_Str__Text
    
    # Layer 2: Business logic validation
    def validate(self):
        if len(self.username) < 3:
            raise ValueError("Username too short")
        
        if self.email.count('@') != 1:
            raise ValueError("Invalid email format")
        
        # Check for prohibited words in bio
        prohibited = ['spam', 'viagra', 'casino']
        bio_lower = str(self.bio).lower()
        for word in prohibited:
            if word in bio_lower:
                raise ValueError(f"Prohibited content detected")
    
    # Layer 3: Rate limiting (external)
    # Layer 4: CAPTCHA verification (external)
```

### 2. Fail Securely

```python
class SafeInputHandler:
    
    def process_input(self, user_input: str, input_type: str):
        """Fail securely with safe defaults"""
        
        try:
            if input_type == "username":
                return Safe_Str__Username(user_input)
            elif input_type == "email":
                return Safe_Str__Email(user_input)
            elif input_type == "url":
                return Safe_Str__Url(user_input)
            else:
                # Unknown type - use most restrictive
                return Safe_Str(user_input)
                
        except ValueError as e:
            # Log the attempt
            logger.warning(f"Invalid input rejected: {e}")
            
            # Return safe default or raise
            if input_type == "username":
                return Safe_Str__Username("anonymous")
            else:
                raise  # Reject the request
```

### 3. Context-Aware Validation

```python
class ContextAwareSanitizer(Type_Safe):
    
    def sanitize_for_context(self, data: str, context: str) -> str:
        """Apply different sanitization based on usage context"""
        
        if context == "html_display":
            # Most restrictive for HTML
            return Safe_Str__Text(data)
            
        elif context == "sql_query":
            # SQL-safe characters only
            return Safe_Str__SQL_Value(data)
            
        elif context == "file_system":
            # File system safe
            return Safe_Str__File__Name(data)
            
        elif context == "shell_command":
            # Shell-safe characters
            return Safe_Str__Shell_Arg(data)
            
        elif context == "json_value":
            # JSON-safe (escape quotes, newlines)
            class Safe_Str__JSON(Safe_Str):
                regex = re.compile(r'["\\\n\r\t]')
            return Safe_Str__JSON(data)
            
        else:
            # Default to strictest
            return Safe_Str(data)
```

### 4. Audit and Logging

```python
import logging
from datetime import datetime

class AuditedSafeInput(Type_Safe):
    """Input validation with audit trail"""
    
    def validate_with_audit(self, 
                           input_value: str, 
                           input_type: type,
                           user_id: str) -> Safe_Str:
        """Validate input and log all attempts"""
        
        start_time = datetime.now()
        success = False
        sanitized_value = None
        
        try:
            # Attempt validation
            if input_type == Safe_Str__Email:
                sanitized_value = Safe_Str__Email(input_value)
            elif input_type == Safe_Str__Username:
                sanitized_value = Safe_Str__Username(input_value)
            else:
                sanitized_value = Safe_Str(input_value)
            
            success = True
            return sanitized_value
            
        except ValueError as e:
            # Log validation failure
            logging.warning(
                "INPUT_VALIDATION_FAILED",
                extra={
                    'user_id': user_id,
                    'input_type': input_type.__name__,
                    'input_length': len(input_value),
                    'error': str(e),
                    'timestamp': start_time.isoformat()
                }
            )
            raise
            
        finally:
            # Always log attempt
            logging.info(
                "INPUT_VALIDATION_ATTEMPT",
                extra={
                    'user_id': user_id,
                    'input_type': input_type.__name__,
                    'success': success,
                    'original_length': len(input_value),
                    'sanitized_length': len(str(sanitized_value)) if sanitized_value else 0,
                    'duration_ms': (datetime.now() - start_time).total_seconds() * 1000
                }
            )
```

## Security Checklist

When implementing Safe_Str for security:

- [ ] **Choose the right Safe_Str type** for your use case
- [ ] **Use strict_validation=True** for critical inputs
- [ ] **Set appropriate max_length** to prevent DoS
- [ ] **Layer your defenses** - don't rely on Safe_Str alone
- [ ] **Test with malicious input** - use OWASP testing guides
- [ ] **Log validation failures** for security monitoring
- [ ] **Handle errors securely** - don't expose internal details
- [ ] **Review regex patterns** - ensure they're not too permissive
- [ ] **Keep Safe_Str types updated** as threats evolve
- [ ] **Document security assumptions** in your code

## Common Mistakes to Avoid

### 1. Don't Trust Safe_Str Alone

```python
# BAD - Safe_Str is not a complete security solution
def execute_query_bad(table_name):
    safe_table = Safe_Str__SQL_Identifier(table_name)
    # Still vulnerable if database user has too many permissions
    return db.execute(f"SELECT * FROM {safe_table}")

# GOOD - Defense in depth
def execute_query_good(table_name):
    safe_table = Safe_Str__SQL_Identifier(table_name)
    
    # Additional validation
    allowed_tables = ['users', 'posts', 'comments']
    if str(safe_table) not in allowed_tables:
        raise ValueError("Table not in whitelist")
    
    # Use least-privilege database user
    # Use prepared statements where possible
    return db.execute(f"SELECT * FROM {safe_table}")
```

### 2. Don't Bypass Safe_Str

```python
# BAD - Bypassing Safe_Str protection
user_input = Safe_Str__Username(raw_input)
# Later in code...
query = f"SELECT * FROM users WHERE name = '{raw_input}'"  # Used original!

# GOOD - Always use the sanitized value
user_input = Safe_Str__Username(raw_input)
query = f"SELECT * FROM users WHERE name = '{user_input}'"
```

### 3. Don't Mix Contexts

```python
# BAD - Using wrong Safe_Str type for context
html_content = Safe_Str__SQL_Value(user_input)  # Wrong type!
return f"<div>{html_content}</div>"

# GOOD - Use context-appropriate type
html_content = Safe_Str__Text(user_input)
return f"<div>{html_content}</div>"
```

## Summary

Safe_Str provides powerful primitives for input validation and sanitization, serving as a critical first line of defense against injection attacks. However, remember:

1. **Safe_Str is one layer** in a defense-in-depth strategy
2. **Choose the right type** for your specific context
3. **Combine with other controls** like parameterized queries, CSP headers, etc.
4. **Test thoroughly** with known attack vectors
5. **Monitor and log** validation failures for security insights
6. **Stay updated** on new attack techniques and update patterns accordingly

When properly implemented, Safe_Str significantly reduces the attack surface of your application by ensuring that string data conforms to expected patterns before it's used in security-sensitive contexts.