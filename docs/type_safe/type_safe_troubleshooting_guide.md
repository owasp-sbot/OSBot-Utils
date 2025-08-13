# Type_Safe Troubleshooting Guide

## Common Issues and Solutions

### Issue: "variable 'X' is defined as type 'Y' which is not supported by Type_Safe"

**Problem:**
```python
class BadConfig(Type_Safe):
    settings: dict = {}  # ERROR!
```

**Cause:** Type_Safe only allows immutable default values to prevent shared mutable defaults.

**Solution:**
```python
class GoodConfig(Type_Safe):
    settings: Dict[str, Any]  # Let Type_Safe initialize it
    # OR
    settings: Optional[Dict[str, Any]] = None  # Use None as default
```

### Issue: "Invalid type for attribute 'X'. Expected 'Y' but got 'Z'"

**Problem:**
```python
user = User()
user.age = "25"  # ERROR: Expected int, got str
```

**Solutions:**

1. **Convert before assignment:**
```python
user.age = int("25")
```

2. **Use type conversion in setter:**
```python
class User(Type_Safe):
    _age: int
    
    @property
    def age(self) -> int:
        return self._age
    
    @age.setter
    def age(self, value):
        self._age = int(value) if isinstance(value, str) else value
```

3. **Use Safe_Int for automatic conversion:**
```python
from osbot_utils.helpers.Safe_Int import Safe_Int

class User(Type_Safe):
    age: Safe_Int  # Accepts strings and converts them
```

### Issue: "X has no attribute 'Y' and cannot be assigned"

**Problem:**
```python
user = User(username="alice", unknown_field="value")  # ERROR!
```

**Cause:** Type_Safe prevents adding undefined attributes.

**Solution:**
```python
# Option 1: Define all needed attributes
class User(Type_Safe):
    username: str
    extra_field: Optional[str] = None

# Option 2: Use a flexible data field
class User(Type_Safe):
    username: str
    metadata: Dict[str, Any]  # For dynamic data

user = User(username="alice")
user.metadata["unknown_field"] = "value"
```

### Issue: Forward references not working

**Problem:**
```python
class Node(Type_Safe):
    parent: 'TreeNode'  # ERROR: Can't reference other class
```

**Cause:** Type_Safe only supports forward references to the current class.

**Solution:**
```python
# Option 1: Use current class name
class Node(Type_Safe):
    parent: Optional['Node'] = None  # Must be 'Node'

# Option 2: Import the class
from mymodule import TreeNode

class Node(Type_Safe):
    parent: Optional[TreeNode] = None
```

### Issue: Collections not maintaining type safety

**Problem:**
```python
class Store(Type_Safe):
    items: list  # Not type-safe!

store = Store()
store.items.append("text")
store.items.append(123)  # No error!
```

**Solution:**
```python
from typing import List

class Store(Type_Safe):
    items: List[str]  # Now type-safe

store = Store()
store.items.append("text")  # ✓
store.items.append(123)      # ✗ TypeError!
```

### Issue: None assignment rejected

**Problem:**
```python
class Config(Type_Safe):
    value: str

config = Config()
config.value = None  # ERROR: Can't set None
```

**Solution:**
```python
from typing import Optional

class Config(Type_Safe):
    value: Optional[str] = None  # Now accepts None
```

### Issue: Circular imports with forward references

**Problem:**
```python
# file1.py
from file2 import ClassB
class ClassA(Type_Safe):
    b: ClassB

# file2.py  
from file1 import ClassA
class ClassB(Type_Safe):
    a: ClassA
```

**Solution:**
```python
# file1.py
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from file2 import ClassB

class ClassA(Type_Safe):
    b: 'ClassB'  # String reference

# file2.py
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from file1 import ClassA

class ClassB(Type_Safe):
    a: 'ClassA'  # String reference
```

### Issue: Performance degradation

**Symptoms:**
- Slow object creation
- Slow attribute assignments
- High memory usage

**Solutions:**

1. **Cache Type_Safe objects:**
```python
# Bad
for item in large_list:
    obj = ExpensiveClass(data=item)  # Creates new object each time
    process(obj)

# Good
cache = {}
for item in large_list:
    if item not in cache:
        cache[item] = ExpensiveClass(data=item)
    process(cache[item])
```

2. **Use primitives for computation:**
```python
class DataProcessor(Type_Safe):
    values: List[Safe_Float]
    
    def compute_average(self):
        # Extract primitives for computation
        raw_values = [float(v) for v in self.values]
        result = sum(raw_values) / len(raw_values)
        return Safe_Float(result)  # Convert back
```

3. **Selective validation:**
```python
class Service(Type_Safe):
    # Only validate public API
    @type_safe
    def public_method(self, data: List[int]) -> int:
        return self._internal_method(data)
    
    # Skip validation for internal methods
    def _internal_method(self, data):
        return sum(data)
```

### Issue: JSON serialization/deserialization failing

**Problem:**
```python
data = obj.json()
new_obj = MyClass.from_json(data)  # ERROR!
```

**Common Causes and Solutions:**

1. **Circular references:**
```python
# Problem
class Node(Type_Safe):
    parent: Optional['Node'] = None
    children: List['Node'] = []

# Creates circular reference
parent = Node()
child = Node()
parent.children.append(child)
child.parent = parent
data = parent.json()  # May fail or recurse infinitely

# Solution: Implement custom serialization
class Node(Type_Safe):
    def json(self):
        return {
            'id': self.id,
            'parent_id': self.parent.id if self.parent else None,
            'children_ids': [c.id for c in self.children]
        }
```

2. **Non-serializable types:**
```python
# Problem
class Config(Type_Safe):
    callback: Callable  # Can't serialize functions

# Solution
class Config(Type_Safe):
    callback_name: str  # Store reference instead
```

### Issue: Validation not working as expected

**Problem:**
```python
from osbot_utils.type_safe.validators import Min

class Product(Type_Safe):
    price: Validate[float, Min(0)]

product = Product()
product.price = -10  # Should fail but doesn't?
```

**Check:**
1. Import is correct
2. Validate syntax is correct
3. Type_Safe version supports validators

**Solution:**
```python
from osbot_utils.type_safe.validators import Validate, Min

class Product(Type_Safe):
    price: Validate[float, Min(0.0)]  # Ensure proper syntax
```

## Debugging Tips

### Enable Type Checking Logs
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Will show type checking operations
obj = MyClass()
obj.field = value
```

### Inspect Type_Safe Cache
```python
from osbot_utils.type_safe.shared.Type_Safe__Cache import type_safe_cache

# View cache statistics
type_safe_cache.print_cache_hits()

# Clear cache if needed
type_safe_cache._cls__kwargs_cache.clear()
```

### Check Annotations
```python
class MyClass(Type_Safe):
    name: str
    age: int

# View all annotations
print(MyClass.__annotations__)
# {'name': <class 'str'>, 'age': <class 'int'>}

# View default values
obj = MyClass()
print(obj.__default_kwargs__())
# {'name': '', 'age': 0}
```

### Test Type Validation
```python
def test_type_validation():
    obj = MyClass()
    
    # Test each field
    try:
        obj.field = test_value
        print(f"✓ {field} accepts {type(test_value)}")
    except ValueError as e:
        print(f"✗ {field} rejects {type(test_value)}: {e}")
```

## Performance Profiling

```python
import cProfile
import pstats

def profile_type_safe():
    # Your Type_Safe code here
    for _ in range(1000):
        obj = MyClass()
        obj.field = value

# Profile
cProfile.run('profile_type_safe()', 'stats')

# Analyze
stats = pStats.Stats('stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 time consumers
```

## Getting Help

1. **Check the examples:** Review working examples in tests
2. **Enable debug logging:** See what Type_Safe is doing
3. **Simplify the problem:** Create minimal reproduction
4. **Check version:** Ensure using latest osbot-utils
5. **Review type annotations:** Ensure they're correct
6. **File an issue:** https://github.com/owasp-sbot/OSBot-Utils/issues