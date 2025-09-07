# Type_Safe Testing Guidance for Fast_API Services 

- **version**: v2.84.1
- **updated**: 25th Aug 2025

## Overview

This guide provides comprehensive instructions for writing tests for Type_Safe-based services using the OSBot framework. When given a service's source code, follow these patterns to create thorough, maintainable test suites that validate both the type safety guarantees and business logic.

## Core Testing Principles

### 1. Test File Naming and Structure

```python
# For service file: mgraph_ai_service_llms/service/llms/LLM__Service.py
# Test file path: tests/unit/service/llms/test_LLM__Service.py

# Always prefix test files with 'test_'
# Mirror the source directory structure under tests/unit/
```

### 2. No Docstrings - Use Inline Comments

**CRITICAL**: Never use docstrings in tests. All documentation must be inline comments at the end of lines, maintaining Type_Safe's visual alignment patterns.

```python
# ✗ NEVER DO THIS - Docstrings break visual patterns
def test__init__(self):
    """Test auto-initialization of Schema__Persona"""    # NO!
    with Schema__Persona() as _:
        assert type(_) is Schema__Persona

# ✓ ALWAYS DO THIS - Inline comments maintain alignment
def test__init__(self):                                   # Test auto-initialization of Schema__Persona
    with Schema__Persona() as _:
        assert type(_)         is Schema__Persona
        assert base_classes(_) == [Type_Safe, object]
        
        assert type(_.id)      is Safe_Id                 # Test all fields are initialized
        assert type(_.name)    is Safe_Str__Text
```

### 3. Context Manager Pattern with '_'

**CRITICAL**: Always use context managers with `_` for better readability and automatic resource management. This is the preferred pattern throughout Type_Safe testing.

```python
# ✓ PREFERRED - Context manager with underscore
def test__init__(self):
    with Schema__Order() as _:
        assert type(_.id)     is Safe_Str__OrderId
        assert _.items        == []
        assert _.status       == "pending"

# ✗ AVOID - Direct variable assignment
def test__init__(self):
    order = Schema__Order()
    assert type(order.id) is Safe_Str__OrderId
```

### 4. Use .obj() for Readable Comparisons

**IMPORTANT**: Use the `.obj()` method with the `__` helper for comprehensive object comparisons. This creates much more readable test assertions than multiple individual checks.

```python
from osbot_utils.utils.Objects import __

def test__init__(self):
    with Schema__Order() as _:
        # ✓ PREFERRED - Single comprehensive comparison
        assert _.obj() == __(id          = _.id                    ,  # Use actual value for auto-generated
                            items       = []                        ,
                            total       = 0.00                      ,
                            status      = "pending"                 ,
                            tracking    = None                      ,
                            created_at  = _.created_at              )  # Use actual for timestamps
        
        # ✗ AVOID - Multiple individual assertions
        # assert _.items == []
        # assert _.total == 0.00  
        # assert _.status == "pending"
        # assert _.tracking is None
```

#### When to Use .obj()

**Use .obj() when:**
- Testing initialization with default values
- Comparing complex nested structures
- Verifying complete object state after operations
- The object structure is relatively stable

**Avoid .obj() when:**
- The object is very large (>40 fields) - becomes brittle
- Field names aren't valid Python identifiers (use .json() instead)
- You only care about a few specific fields
- The structure changes frequently

#### Using .json() as Alternative

When `.obj()` isn't suitable (e.g., keys with special characters), use `.json()`:

```python
def test_api_response(self):
    response = self.client.post('/llms/complete', json={})
    
    # Use .json() for API responses with special characters in keys
    assert response.json() == {'detail': [{'input': None               ,
                                          'loc'  : ['query', 'prompt'] ,
                                          'msg'  : 'Field required'    ,
                                          'type' : 'missing'           }]}
```

#### Complex Nested Structures

```python
def test_nested_initialization(self):
    with File_FS() as _:
        assert _.obj() == __(file__config = __(exists_strategy = 'FIRST'              ,
                                              file_id         = _.file__config.file_id ,
                                              file_paths      = []                     ,
                                              file_type       = __(name           = 'json',
                                                                  content_type   = 'JSON' ,
                                                                  file_extension = 'json' ,
                                                                  encoding       = 'UTF_8',
                                                                  serialization  = 'JSON')),
                            storage_fs   = __(content_data = __()))
```


### 5. Enhanced Testing with .obj() and the __ Class

#### Overview

The `.obj()` method on Type_Safe objects returns an instance of the `__` class (double underscore), which provides powerful testing capabilities beyond simple comparisons. This enhanced object allows you to handle dynamic values, perform partial matching, debug differences, and create test data variations efficiently.

#### The __ Class Capabilities

The `__` class extends `SimpleNamespace` with these key features:
- **`__SKIP__`**: Skip comparison of dynamic fields (IDs, timestamps)
- **`.contains()`**: Partial object matching
- **`.diff()`**: Show differences between objects
- **`.excluding()`**: Remove fields from comparison
- **`.merge()`**: Create object variations

#### Basic Usage with .obj()

```python
def test__init__(self):
    with Schema__User() as _:
        # .obj() returns a __ instance with all Type_Safe fields
        obj = _.obj()
        assert type(obj).__name__ == '__'                           # Returns __ class
        
        # Can use __ for comprehensive comparison
        assert _.obj() == __(user_id     = _.user_id              ,  # Auto-generated
                            name        = ''                       ,  # Empty default
                            email       = ''                       ,
                            age         = 0                        ,
                            is_active   = True                     ,  # Explicit default
                            tags        = []                       ,  # Type_Safe__List as []
                            preferences = __()                     )  # Type_Safe__Dict as __()
```

#### Handling Dynamic Values with __SKIP__

**Problem**: Auto-generated IDs, timestamps, and other dynamic values make tests brittle.

**Solution**: Use `__SKIP__` to ignore specific fields during comparison.

```python
from osbot_utils.testing.__ import __, __SKIP__

def test__with_dynamic_fields(self):
    with Schema__Order() as order:
        # Order has auto-generated ID and timestamp
        order.items = [{'product': 'laptop', 'qty': 1}]
        order.total = 999.99
        
        # Skip dynamic fields in comparison
        assert order.obj() == __(order_id   = __SKIP__           ,  # Skip auto-generated ID
                                items      = [__(product='laptop', qty=1)],
                                total      = 999.99                ,
                                status     = 'pending'             ,
                                created_at = __SKIP__              ,  # Skip timestamp
                                updated_at = __SKIP__              )  # Skip timestamp
```

##### When to Use __SKIP__

Use `__SKIP__` for:
- Auto-generated IDs (`Safe_Id`, UUIDs)
- Timestamps (`created_at`, `updated_at`)
- Random values or tokens
- External API response IDs
- Any value you don't control

Don't use `__SKIP__` for:
- Values you explicitly set
- Business logic results
- Values that should be deterministic

#### Partial Matching with .contains()

**Problem**: You only care about specific fields, not the entire object.

**Solution**: Use `.contains()` for subset matching.

```python
def test__partial_matching(self):
    with Schema__User() as user:
        user.user_id = 'u-123'
        user.name    = 'Alice'
        user.email   = 'alice@test.com'
        user.age     = 30
        user.tags    = ['admin', 'developer']
        
        # Only verify specific fields
        assert user.obj().contains(__(name='Alice', age=30))                    # Subset match
        assert user.obj().contains(__(email='alice@test.com'))                  # Single field
        assert not user.obj().contains(__(name='Bob'))                          # Negative check
        
        # Works with nested structures
        assert user.obj().contains(__(tags=['admin', 'developer']))             # Collection match
```

##### Use Cases for .contains()

- Verify critical fields without full object comparison
- Test API responses where you only care about specific data
- Validate nested structures partially
- Quick assertions in integration tests

#### Debugging with .diff()

**Problem**: Test failures with large objects are hard to debug.

**Solution**: Use `.diff()` to see exactly what's different.

```python
def test__debugging_differences(self):
    with Schema__User() as user1:
        user1.user_id = 'u-100'
        user1.name    = 'Alice'
        user1.email   = 'alice@old.com'
        user1.age     = 25
        
    with Schema__User() as user2:
        user2.user_id = 'u-100'
        user2.name    = 'Alice'
        user2.email   = 'alice@new.com'    # Different
        user2.age     = 26                  # Different
        
    # Get detailed difference report
    diff = user1.obj().diff(user2.obj())
    assert diff == {
        'email': {'actual': 'alice@old.com', 'expected': 'alice@new.com'},
        'age':   {'actual': 25, 'expected': 26}
    }
    
    # Use in test failures for better debugging
    if user1.obj() != user2.obj():
        print(f"Objects differ: {user1.obj().diff(user2.obj())}")
```

#### Excluding Fields with .excluding()

**Problem**: Some fields (timestamps, metadata) shouldn't be part of comparison.

**Solution**: Use `.excluding()` to remove fields before comparison.

```python
def test__excluding_metadata(self):
    with Schema__Event() as event:
        event.event_id   = 'evt-123'
        event.type       = 'user_login'
        event.user_id    = 'u-456'
        event.created_at = '2024-01-01T12:00:00Z'
        event.updated_at = '2024-01-02T15:30:00Z'
        event.request_id = 'req-789-xyz'
        
        # Exclude volatile fields for stable comparison
        assert event.obj().excluding('created_at', 'updated_at', 'request_id') == __(
            event_id = 'evt-123',
            type     = 'user_login',
            user_id  = 'u-456'
        )
```

##### When to Use .excluding()

- Remove timestamps from comparisons
- Ignore metadata fields
- Focus on business data only
- Create reusable test assertions

#### Creating Variations with .merge()

**Problem**: Need multiple test data variations based on a template.

**Solution**: Use `.merge()` to create modified copies.

```python
def test__test_data_variations(self):
    # Create base test data
    with Schema__Request() as base_request:
        base_request.model       = 'gpt-4'
        base_request.prompt      = 'Hello'
        base_request.temperature = 0.7
        base_request.max_tokens  = 100
        
    base_obj = base_request.obj()
    
    # Create variations for different test scenarios
    high_temp_request = base_obj.merge(temperature=0.9, top_p=0.95)
    low_temp_request  = base_obj.merge(temperature=0.1, max_tokens=50)
    streaming_request = base_obj.merge(stream=True, temperature=0.5)
    
    # Verify variations
    assert high_temp_request.temperature == 0.9
    assert high_temp_request.model      == 'gpt-4'              # Base preserved
    assert high_temp_request.top_p      == 0.95                 # New field added
    
    assert low_temp_request.temperature == 0.1
    assert low_temp_request.max_tokens  == 50                   # Override base
    
    assert streaming_request.stream     == True                 # New field
    assert streaming_request.prompt     == 'Hello'              # Base preserved
```

#### Advanced Patterns

##### Nested Type_Safe Objects

```python
def test__nested_structures(self):
    with Schema__Order() as order:
        with Schema__User() as user:
            user.user_id = 'u-001'
            user.name    = 'Alice'
            
        order.order_id = 'ord-001'
        order.user     = user
        order.items    = [{'product': 'laptop', 'qty': 1}]
        
        # Nested Type_Safe becomes nested __ in .obj()
        assert order.obj() == __(
            order_id = 'ord-001',
            user     = __(user_id = 'u-001',             # Nested __ object
                         name    = 'Alice',
                         email   = '',
                         age     = 0),
            items    = [__(product='laptop', qty=1)],    # List items as __
            total    = 0.0,
            status   = 'pending'
        )
```

##### Combining Techniques

```python
def test__api_response_validation(self):
    # Simulate API response
    with Service__API() as service:
        response = service.create_user(name='Test User', email='test@api.com')
        
        # Combine multiple __ techniques for robust testing
        expected = __(
            status_code = 200,
            data = __(
                user_id    = __SKIP__,                   # Skip generated ID
                name       = 'Test User',
                email      = 'test@api.com',
                created_at = __SKIP__,                   # Skip timestamp
                api_token  = __SKIP__                    # Skip generated token
            )
        )
        
        # Full structure validation with dynamic fields skipped
        assert response.obj() == expected
        
        # Partial validation of critical fields
        assert response.obj().data.contains(__(name='Test User', email='test@api.com'))
        
        # Debug if needed
        if response.obj() != expected:
            diff = response.obj().diff(expected)
            self.fail(f"Response differs: {diff}")
```

##### Test Data Factory Pattern

```python
@classmethod
def setUpClass(cls):
    # Define base test objects using __
    cls.base_user = __(
        user_id     = 'test-user',
        name        = 'Test User',
        email       = 'test@example.com',
        age         = 30,
        is_active   = True,
        tags        = [],
        preferences = __()
    )
    
    # Create variations for different scenarios
    cls.admin_user = cls.base_user.merge(
        user_id = 'test-admin',
        name    = 'Admin User',
        tags    = ['admin', 'moderator']
    )
    
    cls.inactive_user = cls.base_user.merge(
        user_id   = 'test-inactive',
        is_active = False
    )
    
def test__with_test_data(self):
    with Schema__User.from_dict(self.admin_user.__dict__) as admin:
        assert admin.tags == ['admin', 'moderator']
        assert admin.email == 'test@example.com'              # Base preserved
```

#### Best Practices

1. **Use `__SKIP__` liberally**: Don't test what you don't control
2. **Prefer `.contains()` for API responses**: Focus on what matters
3. **Add `.diff()` to failure messages**: Makes debugging easier
4. **Use `.excluding()` for cleaner assertions**: Remove noise from tests
5. **Build test data with `.merge()`**: DRY principle for test data
6. **Combine techniques**: Use multiple __ methods together for powerful assertions

#### Common Patterns Reference

```python
# Full comparison with skips
assert obj == __(field1=value1, field2=__SKIP__, field3=value3)

# Partial matching
assert obj.contains(__(critical_field=expected_value))

# Exclude volatile fields
assert obj.excluding('timestamp', 'request_id') == expected_obj

# Create variation
variation = base_obj.merge(field=new_value, new_field=added_value)

# Debug differences
if obj != expected:
    print(f"Diff: {obj.diff(expected)}")
    
# Nested structures
assert obj == __(outer=__(inner=__(value=123)))

# Multiple techniques
assert (obj.excluding('id', 'timestamp')
           .contains(__(status='success', data=__SKIP__)))
```

#### Type_Safe Collections in .obj()

```python
def test__collections_in_obj(self):
    with Schema__Data() as data:
        # Type_Safe__List becomes regular list in .obj()
        data.items.append('item1')
        data.items.append('item2')
        
        # Type_Safe__Dict becomes __ in .obj()
        data.config['key1'] = 'value1'
        data.config['key2'] = 'value2'
        
        # Type_Safe__Set becomes list in .obj()
        data.tags.add('tag1')
        data.tags.add('tag2')
        
        assert data.obj() == __(
            items  = ['item1', 'item2'],              # List
            config = __(key1='value1', key2='value2'), # Dict as __
            tags   = ['tag1', 'tag2']                 # Set as sorted list
        )
```

#### Migration from Simple Comparisons

```python
# OLD: Brittle, hard to maintain
def test__old_way(self):
    with Schema__User() as user:
        assert user.user_id == user.user_id    # Tautology for dynamic values
        assert user.name == ''
        assert user.email == ''
        assert user.age == 0
        # Must update every time schema changes

# NEW: Flexible, maintainable
def test__new_way(self):
    with Schema__User() as user:
        assert user.obj() == __(
            user_id     = __SKIP__,             # Handle dynamic ID
            name        = '',
            email       = '',
            age         = 0,
            is_active   = True,
            tags        = [],
            preferences = __()
        )
        # Or focus on what matters
        assert user.obj().contains(__(is_active=True, age=0))
```

This enhanced testing approach with `.obj()` and the `__` class provides the flexibility and power needed for comprehensive Type_Safe testing while maintaining readability and maintainability.


### 6. Optimize Performance with setUpClass

**CRITICAL**: Use `setUpClass` for expensive operations to dramatically improve test performance. Creating services, database connections, or S3 clients in `setUp` instead of `setUpClass` can make tests 10-100x slower.

```python
class test_Heavy_Service(TestCase):
    
    @classmethod
    def setUpClass(cls):                                              # ONE-TIME expensive setup
        # Create expensive resources ONCE
        setup__service_fast_api_test_objs()                          # LocalStack setup
        cls.s3_client = S3()                                         # Reuse S3 connection
        cls.test_bucket = create_test_bucket()                       # Create bucket once
        cls.service = Heavy_Service()                                # Initialize service once
        cls.service.connect_to_database()                            # Connect to DB once
        
        # Define reusable test data
        cls.test_request = {'model': 'gpt-4', 'prompt': 'test'}
        cls.test_response = {'status': 'success', 'data': {}}
        
    @classmethod  
    def tearDownClass(cls):                                          # ONE-TIME cleanup
        # Clean up in reverse order of creation
        cls.service.disconnect()                                     # Disconnect DB
        cls.s3_client.bucket_delete_all_files(cls.test_bucket)      # Clear bucket
        cls.s3_client.bucket_delete(cls.test_bucket)                # Delete bucket
        
    def setUp(self):                                                 # PER-TEST lightweight setup
        # Only create test-specific, lightweight items here
        self.test_id = Random_Guid()                                # Unique ID per test
        self.temp_file = f"test_{self.test_id}.json"               # Unique filename
        
    def tearDown(self):                                             # PER-TEST cleanup
        # Reset state between tests
        self.service.clear_cache()                                  # Clear any cached data
        if self.s3_client.file_exists(self.test_bucket, self.temp_file):
            self.s3_client.file_delete(self.test_bucket, self.temp_file)
```

#### When to Use setUpClass vs setUp

**Use setUpClass for:**
- Service initialization
- Database/S3/API connections
- Loading configuration
- Creating test buckets/tables
- Any operation taking >100ms
- Resources that can be safely shared

**Use setUp for:**
- Test-specific IDs/timestamps
- Temporary files/data
- Mutable state that must be fresh
- Quick variable assignments (<10ms)

#### Test Atomicity Validation

If you find yourself needing fresh instances for every test, this indicates potential design issues:

```python
# ❌ BAD SIGN - Service can't be reused
class test_Problematic_Service(TestCase):
    def setUp(self):
        self.service = Problematic_Service()  # Required fresh for each test
        
    def test_1(self):
        self.service.process("data")
        
    def test_2(self):
        # This fails if using shared instance - indicates hidden state!
        self.service.process("data")

# ✓ GOOD - Service is properly atomic
class test_Atomic_Service(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = Atomic_Service()  # Can be safely shared
        
    def tearDown(self):
        self.service.reset()  # Explicit state reset if needed
```

#### Execution Order

Understanding the execution order helps optimize setup/teardown:

1. `setUpClass` (once at start)
2. For each test method:
   - `setUp`
   - `test_method`
   - `tearDown`
3. `tearDownClass` (once at end)

### 7. Testing Type_Safe Auto-Conversion Behavior

#### Understanding Auto-Conversion vs Type Enforcement

Type_Safe automatically converts compatible values to their Safe type equivalents when possible. This is a **feature**, not a bug. Understanding when auto-conversion happens vs when TypeError is raised is critical for writing correct tests.

#### Auto-Conversion Rules

Type_Safe attempts conversion in this order:
1. **Direct assignment** if already correct type
2. **Auto-conversion** if source type can be converted (str→Safe_Str, int→str→Safe_Str, etc.)
3. **Validation** after conversion (may raise ValueError)
4. **TypeError** only if conversion is impossible

#### Testing Pattern for Auto-Conversion

```python
def test_type_auto_conversion(self):                                    # Test Type_Safe's automatic type conversion
    with Schema__Persona() as _:
        # Type_Safe auto-converts compatible values to Safe types
        # This is EXPECTED BEHAVIOR, not a bug
        
        # String to Safe_Id - sanitizes special characters
        _.id = "raw-string!@£"
        assert type(_.id) is Safe_Id                                   # Auto-converted to Safe_Id
        assert _.id == 'raw-string___'                                 # Special chars replaced with _
        
        # Integer to Safe_Str - converts via str()
        _.name = 123
        assert type(_.name) is Safe_Str__Text                         # Auto-converted
        assert _.name == '123'                                        # Integer stringified
        
        # Float to Safe_Str - converts via str()
        _.description = 45.67
        assert type(_.description) is Safe_Str__Text                  # Auto-converted
        assert _.description == '45.67'                               # Float stringified
        
        # String to Safe_Str__Language_Code - validates format
        _.language = "en-US"
        assert type(_.language) is Safe_Str__Language_Code            # Auto-converted
        assert _.language == 'en-US'                                  # Valid format preserved
        
        # Auto-conversion can still fail validation
        with pytest.raises(ValueError, match=re.escape("Invalid language code format: 'invalid-format'")):
            _.language = "invalid-format"                             # Conversion succeeds, validation fails

def test_type_enforcement_incompatible_types(self):                     # Test what CANNOT be auto-converted
    with Schema__User() as _:
        # Some conversions are impossible and will raise TypeError
        
        # Dict cannot become Safe_Str
        with pytest.raises(TypeError):
            _.name = {'dict': 'value'}                                # Cannot convert dict to string
            
        # List cannot become Safe_Id  
        with pytest.raises(TypeError):
            _.user_id = ['list', 'of', 'items']                      # Cannot convert list to Safe_Id
            
        # Complex objects cannot be auto-converted
        from datetime import datetime
        with pytest.raises(TypeError):
            _.age = datetime.now()                                    # Cannot convert datetime to int
            
        # None to non-nullable field
        with pytest.raises(TypeError):
            _.required_field = None                                   # Non-nullable field rejects None
```

#### Common Auto-Conversion Scenarios

```python
def test_safe_type_conversions_matrix(self):                          # Document all conversion behaviors
    with Schema__Test() as _:
        # Safe_Id conversions
        _.user_id = "valid-id-123"                                    # str → Safe_Id ✓
        assert _.user_id == "valid-id-123"
        
        _.user_id = "invalid!@#$%"                                    # str → Safe_Id (sanitized) ✓
        assert _.user_id == "invalid_____"                            # Special chars become _
        
        # Safe_UInt conversions  
        _.age = 25                                                    # int → Safe_UInt ✓
        assert _.age == 25
        
        _.age = "30"                                                  # str → int → Safe_UInt ✓
        assert _.age == 30
        
        with pytest.raises(ValueError):
            _.age = -5                                                # Negative fails validation
            
        with pytest.raises(ValueError):
            _.age = "not-a-number"                                   # Non-numeric string fails
            
        # Safe_Float__Money conversions
        _.price = 19.99                                              # float → Safe_Float__Money ✓
        assert _.price == 19.99
        
        _.price = "29.99"                                            # str → float → Safe_Float__Money ✓
        assert _.price == 29.99
        
        _.price = 30                                                 # int → float → Safe_Float__Money ✓
        assert _.price == 30.00
```

#### Testing Strategy for Auto-Conversion

1. **Test the conversion path**: Verify type after assignment
   ```python
   _.field = "raw_value"
   assert type(_.field) is Expected_Safe_Type
   ```

2. **Test the sanitization result**: Verify how value was transformed
   ```python
   _.field = "test!@#"
   assert _.field == "test___"  # Sanitized result
   ```

3. **Test validation failures**: Conversion works but validation fails
   ```python
   with pytest.raises(ValueError):  # Not TypeError!
       _.field = "invalid_but_convertible"
   ```

4. **Test true type incompatibilities**: Cannot convert at all
   ```python
   with pytest.raises(TypeError):  # Cannot convert dict to str
       _.field = {"dict": "value"}
   ```

#### Key Testing Principles

- **ValueError = Validation failed** (after successful conversion)
- **TypeError = Conversion impossible** (incompatible types)
- **Always check type()** after assignment to verify conversion
- **Test sanitization rules** for Safe_Str types (special chars → _)
- **Test numeric bounds** for Safe_Int/UInt types
- **Document expected transformations** in test comments

#### Anti-Pattern to Avoid

```python
# ✗ WRONG - Assumes no auto-conversion
def test_type_enforcement_wrong(self):
    with Schema__User() as _:
        with pytest.raises(TypeError):  # WRONG! Will auto-convert
            _.name = 123                 # Gets converted to "123"
            
        with pytest.raises(TypeError):  # WRONG! Will auto-convert  
            _.id = "raw-string"         # Gets converted to Safe_Id

# ✓ CORRECT - Tests actual conversion behavior
def test_type_enforcement_correct(self):
    with Schema__User() as _:
        _.name = 123
        assert _.name == "123"                                        # Verify conversion
        assert type(_.name) is Safe_Str__Username                    # Verify type
        
        _.id = "raw-string!@#"  
        assert _.id == "raw-string___"                               # Verify sanitization
        assert type(_.id) is Safe_Id                                 # Verify type
```

#### Summary

Type_Safe's auto-conversion is a powerful feature that reduces boilerplate while maintaining type safety. Tests should:
- Verify conversions happen correctly
- Check sanitization/transformation rules
- Test validation boundaries
- Only expect TypeError for truly incompatible types

This behavior makes Type_Safe practical for real-world use where data often comes from JSON, forms, or APIs as raw primitives that need to be safely converted to domain types.

--- 

## Testing Patterns by Component Type

### 1. Type_Safe Schema Classes

```python
from osbot_utils.utils.Objects import __

class test_Schema__Order(TestCase):
    
    def test__init__(self):                                            # Test auto-initialization
        with Schema__Order() as _:
            assert type(_)         is Schema__Order
            assert base_classes(_) == [Type_Safe, object]
            
            # Verify type initialization - collections become Type_Safe variants
            assert type(_.id)       is Safe_Str__OrderId
            assert type(_.items)    is Type_Safe__Dict              # Dict[K,V] -> Type_Safe__Dict
            assert type(_.tags)     is Type_Safe__List              # List[T] -> Type_Safe__List
            assert type(_.categories) is Type_Safe__Set             # Set[T] -> Type_Safe__Set
            assert type(_.total)    is Safe_Float__Money
            assert type(_.metadata) is Type_Safe__Dict              # All dicts become Type_Safe__Dict
            
            # Use .obj() for comprehensive state verification
            assert _.obj() == __(id          = _.id               ,    # Auto-generated values
                                items       = {}                   ,    # Empty dict (not regular dict)
                                tags        = []                   ,    # Empty list (Type_Safe__List)
                                categories  = []                   ,    # Empty set shows as list in obj()
                                total       = 0.00                 ,    # Zero values
                                status      = "pending"            ,    # Explicit defaults
                                metadata    = {}                   ,    # Type_Safe__Dict shows as {}
                                tracking_url = None                ,    # Nullable fields
                                created_at  = _.created_at         )    # Timestamps
        
    def test_type_enforcement(self):                                   # Test runtime type checking
        with Schema__Order() as _:
            # Test valid assignments
            _.id = Safe_Str__OrderId("ORD-123")                       # ✓ Correct type
            
            # Test type violations
            with pytest.raises(TypeError):
                _.id = "raw-string"                                    # ✗ Wrong type
                
            with pytest.raises(ValueError):
                _.id = Safe_Str__ProductId("PRD-123")                 # ✗ Different Safe_Id subtype
            
    def test_serialization_round_trip(self):                          # Test JSON conversion
        with Schema__Order(id    = "ORD-123",
                          items = {"PRD-1": 2},
                          total = 99.99) as _:
            # Serialize
            json_data = _.json()
            
            # Deserialize and verify with .obj()
            with Schema__Order.from_json(json_data) as restored:
                assert restored.obj() == _.obj()                      # Perfect round-trip
```

### 2. Service Classes with Dependencies

```python
class test_Service__OpenRouter(TestCase):
    
    @classmethod
    def setUpClass(cls):
        setup__service_fast_api_test_objs()                           # Setup LocalStack/mocks
        cls.service = Service__OpenRouter()
        
        # Mock or skip tests if API key missing
        if not get_env(ENV_NAME_OPEN_ROUTER__API_KEY):
            pytest.skip("OpenRouter API key required")
                
    def test_setup(self):                                             # Test initialization chain
        with self.service as _:
            assert _.api_base_url      == "https://openrouter.ai/api"
            assert type(_.models_service) is Service__OpenRouter__Models
            assert _.s3_storage        is not None
            
    def test_api_call_with_mock(self):                               # Test with mocked response
        with self.service as _:
            # Store original method
            original_execute = _.execute
            
            # Mock the API call
            def mock_execute(payload):
                return {"choices": [{"message": {"content": "mocked"}}]}
                
            _.execute = mock_execute
            
            try:
                result = _.chat_completion("test prompt")
                assert result["choices"][0]["message"]["content"] == "mocked"
            finally:
                _.execute = original_execute                          # Restore original
            
    @pytest.mark.skip(reason="Costs money")                          # Skip expensive tests
    def test_paid_model(self):
        with self.service as _:
            result = _.chat_completion(
                prompt = "test",
                model  = "openai/gpt-4"
            )
            assert 'choices' in result
```

### 3. FastAPI Route Classes with Shared Test Objects

**CRITICAL PATTERN**: Use a shared test objects file at `tests/unit/Service__Fast_API__Test_Objs.py` to create FastAPI, TestClient, and LocalStack instances ONCE for the entire test suite. This dramatically improves test performance.

```python
# tests/unit/Service__Fast_API__Test_Objs.py
from fastapi                                    import FastAPI
from osbot_fast_api.api.Fast_API                import Fast_API
from osbot_utils.type_safe.Type_Safe            import Type_Safe
from starlette.testclient                       import TestClient
from mgraph_ai_service_llms.fast_api.Service__Fast_API import Service__Fast_API
from mgraph_ai_service_llms.utils.LocalStack__Setup    import LocalStack__Setup

class Service__Fast_API__Test_Objs(Type_Safe):
    fast_api         : Service__Fast_API     = None
    fast_api__app    : FastAPI               = None
    fast_api__client : TestClient            = None
    localstack_setup : LocalStack__Setup     = None
    setup_completed  : bool                  = False

service_fast_api_test_objs = Service__Fast_API__Test_Objs()  # Singleton instance

def setup__service_fast_api_test_objs():
    with service_fast_api_test_objs as _:
        if _.setup_completed is False:                       # Only setup once
            _.localstack_setup = LocalStack__Setup().setup() # Setup LocalStack
            _.fast_api         = Service__Fast_API().setup() # Setup Fast_API service
            _.fast_api__app    = _.fast_api.app()           # Get FastAPI app
            _.fast_api__client = _.fast_api.client()        # Create TestClient
            _.setup_completed  = True                        # Mark as complete
    return service_fast_api_test_objs
```

#### Using Shared Test Objects in Tests

```python
class test_Routes__LLMs__client(TestCase):
    
    @classmethod
    def setUpClass(cls):
        with setup__service_fast_api_test_objs() as _:       # Get shared objects
            cls.client = _.fast_api__client                  # Reuse TestClient
            cls.app    = _.fast_api__app                     # Reuse FastAPI app
            cls.client.headers[TEST_API_KEY__NAME] = TEST_API_KEY__VALUE
            
    def test__llms__models(self):                            # Test endpoint responses
        response = self.client.get('/llms/models')           # Uses shared client
        
        assert response.status_code == 200
        result = response.json()
        assert 'models' in result
```

#### Key Benefits

1. **Performance**: FastAPI app and LocalStack setup happen ONCE, not per test class
2. **Consistency**: All tests use the same configured environment
3. **No state pollution**: Tests shouldn't modify FastAPI state anyway
4. **Fast startup**: Modern setup() is very quick with proper configuration

#### OSBot-Fast-API Integration

This pattern leverages two key packages:
- **`osbot-fast-api`**: Provides Type_Safe-aware FastAPI integration
- **`osbot-fast-api-serverless`**: Adds AWS Lambda/serverless support

These packages provide:
- Automatic Type_Safe ↔ Pydantic conversion
- Built-in authentication middleware
- Request/response validation
- Lambda handler integration
- TestClient with proper Type_Safe support

```python
from osbot_fast_api.api.Fast_API import Fast_API              # Base Fast_API class
from osbot_fast_api_serverless.fast_api.Serverless__Fast_API import Serverless__Fast_API

class Service__Fast_API(Serverless__Fast_API):                # Inherit serverless support
    def setup_routes(self):
        self.add_routes(Routes__LLMs())                        # Type_Safe routes work directly
        self.add_routes(Routes__Info())
```

### 4. Cache and Storage Classes

```python
class test_Open_Router__Cache(TestCase):
    
    @classmethod
    def setUpClass(cls):
        setup__service_fast_api_test_objs()
        
        # Use test bucket to avoid polluting production
        cls.test_bucket = str_to_valid_s3_bucket_name(random_string_short("test-cache-"))
        cls.cache = Open_Router__Cache(s3__bucket=cls.test_bucket).setup()
        
    @classmethod
    def tearDownClass(cls):                                           # Clean up test resources
        with cls.cache.s3__storage.s3 as _:
            if _.bucket_exists(cls.test_bucket):
                _.bucket_delete_all_files(cls.test_bucket)
                _.bucket_delete(cls.test_bucket)
                
    def tearDown(self):                                               # Clean between tests
        self.cache.clear_all()
        
    def test_save_and_load(self):                                     # Test basic operations
        test_data = {"key": "value"}
        
        with self.cache as _:
            # Save
            assert _.save_to_latest("test-id", test_data) is True
            
            # Load
            loaded = _.load_from_latest("test-id")
            assert loaded == test_data
            
            # Delete
            assert _.delete_latest("test-id") is True
            assert _.load_from_latest("test-id") is None
```

---


## Critical Testing Requirements

### 1. Always Test Type Safety

```python
from osbot_utils.utils.Objects import __

def test_type_safety_enforcement(self):
    with Schema__User() as _:
        # Verify collections become Type_Safe variants
        assert type(_.preferences) is Type_Safe__Dict            # Dict -> Type_Safe__Dict
        assert type(_.tags)        is Type_Safe__List            # List -> Type_Safe__List  
        assert type(_.permissions) is Type_Safe__Set             # Set -> Type_Safe__Set
        
        # NEVER accept raw primitives where Safe types expected
        with pytest.raises(TypeError):
            _.user_id = "raw-string"                             # Must be Safe_Id
            
        with pytest.raises(ValueError):  
            _.age = -5                                           # Safe_UInt rejects negative
            
        with pytest.raises(ValueError):
            _.email = "not-an-email"                            # Safe_Str__Email validates format
```

### 2. Test Collection Type Conversion

**CRITICAL**: All `list`, `dict`, and `set` annotations in Type_Safe classes are automatically converted to their Type_Safe equivalents:

```python
def test_collection_type_conversion(self):                      # Verify Type_Safe collection conversion
    class Schema__Test(Type_Safe):
        regular_dict : dict                                     # Becomes Type_Safe__Dict
        typed_dict   : Dict[str, int]                          # Becomes Type_Safe__Dict
        regular_list : list                                     # Becomes Type_Safe__List
        typed_list   : List[str]                               # Becomes Type_Safe__List
        regular_set  : set                                      # Becomes Type_Safe__Set
        typed_set    : Set[int]                                # Becomes Type_Safe__Set
        
    with Schema__Test() as _:
        # All collections are Type_Safe variants, never raw Python types
        assert type(_.regular_dict) is Type_Safe__Dict
        assert type(_.typed_dict)   is Type_Safe__Dict
        assert type(_.regular_list) is Type_Safe__List
        assert type(_.typed_list)   is Type_Safe__List
        assert type(_.regular_set)  is Type_Safe__Set
        assert type(_.typed_set)    is Type_Safe__Set
        
        # Never raw Python collections
        assert type(_.regular_dict) is not dict
        assert type(_.regular_list) is not list
        assert type(_.regular_set)  is not set
```

### 3. Test Serialization Fidelity

```python
def test_json_preserves_types(self):
    with Schema__Complex(id     = Safe_Id("TEST-123"),
                        amount = Safe_Float__Money(99.99),
                        items  = [Safe_Str("item1"), Safe_Str("item2")]) as original:
        
        json_data = original.json()
        
        with Schema__Complex.from_json(json_data) as restored:
            # Use .obj() to verify complete round-trip
            assert restored.obj() == original.obj()
            
            # Also verify specific type preservation
            assert type(restored.id)        is Safe_Id
            assert type(restored.amount)    is Safe_Float__Money
            assert type(restored.items[0])  is Safe_Str
```

### 4. Test Complex Nested Structures

```python
def test_complex_initialization(self):
    with File_FS() as _:
        # Use .obj() with __ for nested structure verification
        assert _.obj() == __(file__config = __(exists_strategy = 'FIRST'              ,
                                              file_id         = _.file__config.file_id ,
                                              file_paths      = []                     ,
                                              file_type       = __(name           = 'json',
                                                                  content_type   = 'JSON' ,
                                                                  file_extension = 'json' ,
                                                                  encoding       = 'UTF_8',
                                                                  serialization  = 'JSON')),
                            storage_fs   = __(content_data = __()))
```

### 5. Test LocalStack Integration

```python
def test_s3_operations(self):
    with self.storage as _:
        # Verify LocalStack is being used
        assert aws_config.account_id()  == OSBOT_AWS__LOCAL_STACK__AWS_ACCOUNT_ID
        assert aws_config.region_name() == OSBOT_AWS__LOCAL_STACK__AWS_DEFAULT_REGION
        
        # Test S3 operations work
        assert _.s3.bucket_exists(self.test_bucket) is True
```

### 6. Testing Safe Type Auto-Conversion and Validation

#### The Auto-Conversion Edge Case

Type_Safe automatically converts raw strings to Safe types during initialization, but this conversion can mask validation bugs in custom Safe types. Always test with both pre-converted Safe types AND raw values to ensure proper validation.

#### Testing Pattern for Safe Type Validation

```python
def test__init__with_safe_types(self):                                  # Test with pre-converted Safe types
    test_id   = Safe_Id("test-persona-1")
    test_name = Safe_Str__Text("Test Persona")
    test_lang = Safe_Str__Language_Code("pt-PT")
    
    with Schema__Persona(id       = test_id,
                        name     = test_name,
                        language = test_lang) as _:
        assert _.id       == test_id
        assert _.name     == test_name
        assert _.language == test_lang                                  # May pass even with bugs

def test__init__with_raw_values(self):                                  # Test with raw string values
    test_id   = "test-persona-1"
    test_name = "Test Persona"
    test_lang = "pt-PT"
    
    with Schema__Persona(id       = test_id,
                        name     = test_name,
                        language = test_lang) as _:
        # These reveal validation bugs
        assert _.id       == test_id                                    # Safe_Id conversion works
        assert _.name     == test_name                                  # Safe_Str__Text works
        assert _.language != test_lang                                  # BUG: reveals issue
        assert _.language == '_'                                        # BUG: incorrect conversion
```

#### Testing LLM-Specific Safe Types

The LLM Safe types require specific testing patterns due to their specialized validation rules:

```python
def test_llm_message_types(self):                                      # Test LLM message type constraints
    class Schema__Conversation(Type_Safe):
        system_prompt: Safe_Str__LLM__Message__System
        user_message: Safe_Str__LLM__Message__User
        assistant_reply: Safe_Str__LLM__Message__Assistant
        tool_response: Safe_Str__LLM__Message__Tool
        
    with Schema__Conversation() as _:
        # Test size limits
        _.system_prompt = "Configure the assistant behavior"
        assert len(_.system_prompt) <= 4096  # System messages are shorter
        
        # Test large user message
        large_message = "Hello " * 5000  # ~30KB
        _.user_message = large_message
        assert len(_.user_message) <= 32768  # Full context window
        
        # Test control character filtering
        _.assistant_reply = "Response\x00with\x01control\x02chars"
        assert '\x00' not in _.assistant_reply  # Control chars removed
        assert '\x01' not in _.assistant_reply
        
def test_llm_model_identifiers(self):                                 # Test model ID formats
    class Schema__Model_Config(Type_Safe):
        model_id: Safe_Str__LLM__Model_ID
        model_name: Safe_Str__LLM__Model_Name
        model_slug: Safe_Str__LLM__Model_Slug
        
    with Schema__Model_Config() as _:
        # Test various model ID formats
        _.model_id = "openai/gpt-4"
        assert _.model_id == "openai/gpt-4"  # Slash preserved
        
        _.model_id = "anthropic/claude-3-opus@20240229"
        assert "@" in _.model_id  # @ symbol preserved
        
        # Test display name with special chars
        _.model_name = "GPT-4 Turbo (Latest)"
        assert "(" in _.model_name  # Parentheses allowed
        
        # Test URL-safe slug
        _.model_slug = "gpt-4-turbo"
        assert _.model_slug == "gpt-4-turbo"
        
        # Invalid characters in slug
        _.model_slug = "gpt 4 turbo!"
        assert _.model_slug == "gpt_4_turbo_"  # Spaces and ! replaced
```

#### Testing Git/GitHub Safe Types

```python
def test_github_types(self):                                          # Test GitHub-specific validation
    class Schema__Repository(Type_Safe):
        repo: Safe_Str__GitHub__Repo
        branch: Safe_Str__Git__Branch
        tag: Safe_Str__Git__Tag
        ref: Safe_Str__Git__Ref  # Can be branch, tag, or SHA
        
    with Schema__Repository() as _:
        # Test full repo format
        _.repo = "octocat/Hello-World"
        assert _.repo == "octocat/Hello-World"
        assert _.repo.repo_owner == "octocat"  # Parsed owner
        assert _.repo.repo_name == "Hello-World"  # Parsed name
        
        # Test invalid repo format
        with pytest.raises(ValueError, match="must be in 'owner/repo' format"):
            _.repo = "just-a-name"
            
        # Test branch validation
        _.branch = "feature/new-feature"
        assert _.branch == "feature/new-feature"
        
        with pytest.raises(ValueError, match="cannot start with dash"):
            _.branch = "-invalid-branch"
            
        # Test Git ref accepts multiple types
        _.ref = "main"  # Branch
        assert _.ref == "main"
        
        _.ref = "v1.0.0"  # Tag
        assert _.ref == "v1.0.0"
        
        _.ref = "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d"  # SHA
        assert _.ref == "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d"
        
        _.ref = "7fd1a60"  # Short SHA
        assert _.ref == "7fd1a60"

def test_version_string(self):                                        # Test version format validation
    class Schema__Release(Type_Safe):
        version: Safe_Str__Version
        
    with Schema__Release() as _:
        # Valid version formats
        _.version = "v1.0.0"
        assert _.version == "v1.0.0"
        
        _.version = "v999.999.999"  # Max values
        assert _.version == "v999.999.999"
        
        # Invalid formats
        with pytest.raises(ValueError):
            _.version = "1.0.0"  # Missing 'v' prefix
            
        with pytest.raises(ValueError):
            _.version = "v1.0"  # Missing patch version
```

#### Testing Cryptographic Safe Types

```python
def test_crypto_types(self):                                          # Test cryptographic type validation
    class Schema__Crypto_Keys(Type_Safe):
        sha1_full: Safe_Str__SHA1
        sha1_short: Safe_Str__SHA1__Short
        nacl_public: Safe_Str__NaCl__Public_Key
        nacl_private: Safe_Str__NaCl__Private_Key
        content_hash: Safe_Str__Hash
        
    with Schema__Crypto_Keys() as _:
        # Test SHA1 validation (40 hex chars)
        _.sha1_full = "7fd1a60b01f91b314f59955a4e4d4e80d8edf11d"
        assert len(_.sha1_full) == 40
        
        with pytest.raises(ValueError):
            _.sha1_full = "not-40-chars"  # Wrong length
            
        # Test short SHA1 (7 hex chars)
        _.sha1_short = "7fd1a60"
        assert len(_.sha1_short) == 7
        
        # Test NaCl keys (64 hex chars)
        valid_key = "a" * 64
        _.nacl_public = valid_key
        _.nacl_private = valid_key
        assert len(_.nacl_public) == 64
        assert len(_.nacl_private) == 64
        
        # Test hash generation
        from osbot_utils.type_safe.primitives.safe_str.cryptography.hashes.Safe_Str__Hash import safe_str_hash
        
        _.content_hash = safe_str_hash("test content")
        assert len(_.content_hash) == 10  # Truncated MD5
```

#### Testing HTTP Safe Types

```python
def test_http_types(self):                                            # Test HTTP-specific types
    class Schema__HTTP_Response(Type_Safe):
        content_type: Safe_Str__Http__Content_Type
        etag: Safe_Str__Http__ETag
        last_modified: Safe_Str__Http__Last_Modified
        body: Safe_Str__Http__Text
        
    with Schema__HTTP_Response() as _:
        # Test content type
        _.content_type = "application/json; charset=utf-8"
        assert ";" in _.content_type  # Semicolon preserved
        
        # Test ETag format
        _.etag = '"33a64df551425fcc55e4d42a148795d9f25f89d4"'
        assert '"' in _.etag  # Quotes preserved
        
        # Test HTTP date format
        _.last_modified = "Wed, 21 Oct 2024 07:28:00 GMT"
        assert "," in _.last_modified  # Comma preserved
        
        # Test large text body (1MB limit)
        large_text = "a" * 1_000_000
        _.body = large_text
        assert len(_.body) <= 1_048_576  # 1MB limit
```

#### Why This Pattern Matters

##### The Hidden Bug Pattern

```python
class Safe_Str__Language_Code(Safe_Str):
    max_length = 5
    regex      = re.compile(r'[^a-zA-Z-]')                             # BUG: removes the dash!
    regex_mode = 'REPLACE'
    
# When using pre-converted type:
lang = Safe_Str__Language_Code("pt-PT")                                # Creates with "pt-PT"
assert lang == "pt-PT"                                                 # Passes - no validation yet

# When Type_Safe auto-converts:
schema = Schema__Persona(language="pt-PT")                             # Auto-converts
assert schema.language == "pt-PT"                                      # FAILS: actually "pt_PT" or "_"
```

#### Comprehensive Testing Strategy

```python
def test_safe_type_validation_both_ways(self):                         # Test both conversion paths
    # Test 1: Pre-converted Safe types (may hide bugs)
    with Schema__Config() as _:
        _.api_key = Safe_Str__API_Key("KEY-123-ABC")
        assert _.api_key == "KEY-123-ABC"                              # Might pass
        
    # Test 2: Raw values (reveals conversion bugs)
    with Schema__Config(api_key="KEY-123-ABC") as _:
        assert _.api_key == "KEY-123-ABC"                              # Might fail if validation wrong
        
    # Test 3: Use .obj() to see actual stored value
    with Schema__Config(api_key="KEY-123-ABC") as _:
        actual_obj = _.obj()
        assert actual_obj.api_key == "KEY-123-ABC"                     # Shows real value
```

### 7. Testing Safe Float Types

Type_Safe includes advanced Safe_Float types with specific behaviors that need careful testing:

```python
def test_safe_float_precision(self):                                    # Test precision handling in Safe_Float types
    # Test Safe_Float__Money with exact decimal arithmetic
    with Schema__Invoice() as _:
        _.subtotal = 19.99
        _.tax = 1.60
        _.total = _.subtotal + _.tax
        
        assert type(_.subtotal) is Safe_Float__Money
        assert type(_.total) is Safe_Float__Money
        assert _.total == 21.59                                        # Exact decimal, no float errors
        
    # Test Safe_Float__Engineering with epsilon tolerance
    with Schema__Measurement() as _:
        _.temperature = 273.15
        _.pressure = 101.325
        
        assert type(_.temperature) is Safe_Float__Engineering
        # Engineering floats use epsilon for comparison
        assert abs(_.temperature - 273.15) < 1e-6

def test_safe_float_bounds_and_clamping(self):                        # Test range enforcement and clamping
    # Test percentage bounds
    with Schema__Discount() as _:
        _.percentage = Safe_Float__Percentage_Exact(50.0)
        assert _.percentage == 50.0
        
        # Test max bound enforcement
        with pytest.raises(ValueError, match="must be <= 100.0"):
            _.percentage = Safe_Float__Percentage_Exact(150.0)
            
    # Test clamping behavior (if enabled)
    class Safe_Float__Clamped(Safe_Float):
        min_value = 0.0
        max_value = 100.0
        clamp_to_range = True  # Auto-clamp instead of error
        
    value = Safe_Float__Clamped(150.0)
    assert value == 100.0  # Clamped to max
```

### 8. Testing Enum Support

```python
def test_enum_handling(self):                                          # Test Enum serialization and validation
    from enum import Enum
    
    class Enum__Status(str, Enum):
        PENDING = "pending"
        ACTIVE = "active"
        COMPLETED = "completed"
        
    class Schema__Task(Type_Safe):
        status: Enum__Status = Enum__Status.PENDING
        
    with Schema__Task() as _:
        # Test enum default
        assert _.status == Enum__Status.PENDING
        assert _.status.value == "pending"
        
        # Test string auto-conversion to enum
        _.status = "active"
        assert _.status == Enum__Status.ACTIVE
        assert isinstance(_.status, Enum__Status)
        
        # Test invalid enum value
        with pytest.raises(ValueError, match="Invalid value 'invalid'"):
            _.status = "invalid"
            
        # Test JSON serialization preserves enums
        json_data = _.json()
        assert json_data['status'] == 'active'  # Serializes to value
        
        restored = Schema__Task.from_json(json_data)
        assert restored.status == Enum__Status.ACTIVE  # Restores as enum

def test_enum_llm_role(self):                                         # Test LLM-specific enum
    from osbot_utils.type_safe.primitives.safe_str.llm.Enum__LLM__Role import Enum__LLM__Role
    
    class Schema__Message(Type_Safe):
        role: Enum__LLM__Role
        content: Safe_Str__LLM__Message__User
        
    with Schema__Message() as _:
        _.role = "user"  # String converts to enum
        assert _.role == Enum__LLM__Role.USER
        assert str(_.role) == "user"  # __str__ returns value
```

### 9. Testing Literal Types

```python
def test_literal_validation(self):                                     # Test Literal type enforcement
    from typing import Literal
    
    class Schema__Config(Type_Safe):
        environment: Literal["dev", "test", "prod"] = "dev"
        log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
        
    with Schema__Config() as _:
        # Test default literal value
        assert _.environment == "dev"
        
        # Test valid literal assignment
        _.environment = "prod"
        assert _.environment == "prod"
        
        # Test invalid literal value
        error_msg = "must be one of ['dev', 'test', 'prod'], got 'staging'"
        with pytest.raises(ValueError, match=re.escape(error_msg)):
            _.environment = "staging"
            
        # Test with Optional[Literal]
        from typing import Optional
        
        class Schema__Settings(Type_Safe):
            mode: Optional[Literal["auto", "manual"]] = None
            
        with Schema__Settings() as settings:
            assert settings.mode is None
            settings.mode = "auto"
            assert settings.mode == "auto"
            
            with pytest.raises(ValueError):
                settings.mode = "invalid"
```

### 10. Testing Safe_Str Regex Modes

The Safe_Str types now support two regex modes that fundamentally change validation behavior:

```python
def test_regex_mode_replace(self):                                    # Test REPLACE mode (default)
    from osbot_utils.type_safe.primitives.safe_str.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode
    
    class Safe_Str__Sanitizing(Safe_Str):
        regex = re.compile(r'[^a-zA-Z0-9]')  # Remove non-alphanumeric
        regex_mode = Enum__Safe_Str__Regex_Mode.REPLACE
        replacement_char = '_'
        
    # REPLACE mode sanitizes input
    value = Safe_Str__Sanitizing("hello@world.com")
    assert value == "hello_world_com"  # Special chars replaced
    
    value = Safe_Str__Sanitizing("test-123!")
    assert value == "test_123_"  # Dash and ! replaced

def test_regex_mode_match(self):                                      # Test MATCH mode for validation
    from osbot_utils.type_safe.primitives.safe_str.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode
    
    class Safe_Str__Validating(Safe_Str):
        regex = re.compile(r'^[A-Z]{3}-[0-9]{4}$')  # Pattern to match
        regex_mode = Enum__Safe_Str__Regex_Mode.MATCH
        strict_validation = True  # Required with MATCH mode
        
    # MATCH mode validates pattern
    value = Safe_Str__Validating("ABC-1234")
    assert value == "ABC-1234"  # Valid pattern preserved
    
    # Invalid pattern raises error
    with pytest.raises(ValueError, match="does not match required pattern"):
        Safe_Str__Validating("abc-1234")  # Lowercase not allowed
        
    with pytest.raises(ValueError, match="does not match required pattern"):
        Safe_Str__Validating("ABC-12")  # Wrong number count

def test_regex_mode_interactions(self):                               # Test mode-specific behaviors
    # strict_validation + REPLACE = reject invalid chars
    class Safe_Str__Strict_Replace(Safe_Str):
        regex = re.compile(r'[^a-zA-Z]')
        regex_mode = Enum__Safe_Str__Regex_Mode.REPLACE
        strict_validation = True
        
    with pytest.raises(ValueError, match="contains invalid characters"):
        Safe_Str__Strict_Replace("hello123")  # Numbers not allowed
        
    # strict_validation + MATCH = pattern matching
    class Safe_Str__Pattern(Safe_Str):
        regex = re.compile(r'^v\d+\.\d+\.\d+$')  # Version pattern
        regex_mode = Enum__Safe_Str__Regex_Mode.MATCH
        strict_validation = True
        
    value = Safe_Str__Pattern("v1.2.3")
    assert value == "v1.2.3"
    
    # Non-strict MATCH mode not allowed
    with pytest.raises(ValueError, match="cannot use regex_mode='match' without strict_validation"):
        class Safe_Str__Invalid(Safe_Str):
            regex = re.compile(r'^test$')
            regex_mode = Enum__Safe_Str__Regex_Mode.MATCH
            strict_validation = False
        
        Safe_Str__Invalid("test")
```

### 11. Testing Safe_Str Attributes

```python
def test_safe_str_new_attributes(self):                              # Test Safe_Str configuration options
    # Test exact_length enforcement
    class Safe_Str__Fixed_Length(Safe_Str):
        max_length = 10
        exact_length = True  # NEW: Require exactly max_length chars
        
    value = Safe_Str__Fixed_Length("1234567890")
    assert len(value) == 10
    
    with pytest.raises(ValueError, match="must be exactly 10 characters"):
        Safe_Str__Fixed_Length("123")  # Too short
        
    with pytest.raises(ValueError, match="must be exactly 10 characters"):
        Safe_Str__Fixed_Length("12345678901")  # Too long
        
    # Test to_lower_case transformation
    class Safe_Str__Lowercase(Safe_Str):
        to_lower_case = True  # NEW: Force lowercase
        
    value = Safe_Str__Lowercase("Hello WORLD")
    assert value == "hello world"  # Converted to lowercase
    
    # Test allow_all_replacement_char
    class Safe_Str__No_All_Underscores(Safe_Str):
        regex = re.compile(r'[^a-zA-Z]')
        allow_all_replacement_char = False  # Reject if all chars replaced
        
    with pytest.raises(ValueError, match="consists entirely of '_' characters"):
        Safe_Str__No_All_Underscores("123456")  # All become underscores
```


---

## Common Safe Type Validation Bugs

### 1. Regex Removing Valid Characters

```python
def test_regex_validation_bug(self):
    # Bug: Language code regex removes dashes
    with Schema__Persona(language="en-US") as _:
        assert _.language != "en-US"                                   # BUG: dash removed
        assert _.language == "enUS" or _.language == "_"               # Actual buggy result
```

### 2. Overly Restrictive Length Limits

```python
def test_length_validation_bug(self):
    # Bug: UUID max_length too short
    test_uuid = "550e8400-e29b-41d4-a716-446655440000"
    with Schema__Resource(resource_id=test_uuid) as _:
        assert _.resource_id != test_uuid                              # BUG: truncated
        assert len(_.resource_id) == 32                                # Max length hit
```

### 3. Case Sensitivity Issues

```python
def test_case_sensitivity_bug(self):
    # Bug: Email validation changes case
    with Schema__User(email="John.Doe@Example.COM") as _:
        assert _.email != "John.Doe@Example.COM"                       # BUG: case changed
        assert _.email == "john.doe@example.com"                       # Forced lowercase
```

---

## Example: Complete Safe Type Validation Test

```python
def test_complete_safe_type_validation(self):                          # Comprehensive validation test
    # Test all input formats
    test_cases = [
        ("raw string"        , "test-id-123"),
        ("safe type"         , Safe_Id("test-id-123")),
        ("with special chars", "test_id!@#"),
        ("empty"             , ""),
        ("max length"        , "x" * 100)
    ]
    
    for description, input_value in test_cases:
        with self.subTest(description):
            if description in ["with special chars", "empty"]:
                # Should reject invalid values
                with pytest.raises(ValueError):
                    Schema__Test(id=input_value)
            else:
                # Should accept and preserve valid values
                with Schema__Test(id=input_value) as _:
                    expected = input_value[:50] if len(str(input_value)) > 50 else input_value
                    assert _.id == expected
```


---

## Test Organization Best Practices

### 1. One-to-One Method Mapping

**CRITICAL**: Maintain a one-to-one mapping between class methods and test methods. Every public method should have a corresponding test method, with variations using double underscore suffixes.

```python
class An_Class(Type_Safe):
    an_str : Safe_Str = 'abc'

    def method_1(self):
        return self.an_str

    def method_2(self, var_1):
        return self.an_str + var_1

class test_An_Class(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.an_class = An_Class()

    def test__init__(self):                                           # Always test initialization
        with An_Class() as _:
            assert type(_) is An_Class
            assert _.an_str == 'abc'

    def test_method_1(self):                                          # Direct mapping to method_1
        with self.an_class as _:
            assert _.method_1() == 'abc'

    def test_method_2(self):                                          # Direct mapping to method_2
        var_1 = '_var_1'
        with self.an_class as _:
            assert _.method_2(var_1) == 'abc_var_1'                   # Static for readability
            assert _.method_2(var_1) == f'abc{var_1}'                # Dynamic for maintainability

    def test_method_2__handle_bad_data(self):                         # Variation with __ suffix
        with self.an_class as _:
            assert _.method_2(None) == 'abcNone'
            assert _.method_2('')   == 'abc'
            
    def test_method_2__with_special_chars(self):                      # Another variation
        with self.an_class as _:
            assert _.method_2('!@#') == 'abc!@#'

    # Tests starting with __ are for scenarios/integrations
    def test__with_custom_values(self):                               # Scenario test
        with An_Class(an_str='xyz') as _:
            assert _.method_1() == 'xyz'
            assert _.method_2('123') == 'xyz123'
    
    def test__integration_scenario(self):                             # Integration test
        # Tests that cross method boundaries or test workflows
        pass
```

#### Method Naming Convention

- `test_method_name()` - Primary test for the method
- `test_method_name__variation()` - Specific variations (edge cases, error handling)
- `test__scenario_name()` - Cross-method scenarios or integration tests

This ensures:
- **Complete coverage** - Easy to see if any method lacks a test
- **Organized variations** - Related tests grouped by method name
- **Clear scenarios** - Double underscore prefix for non-method-specific tests

### 2. Context Manager Pattern Throughout

```python
class test_Service__LLM(TestCase):
    
    # Always use context managers with '_'
    def test__init__(self):
        with self.service as _:
            assert type(_)         is Service__LLM
            assert base_classes(_) == [Type_Safe, object]
    
    def test_execute_request(self):
        with self.service as _:
            result = _.execute_request(prompt="test")
            assert 'response' in result
    
    def test__nested_operations(self):
        with self.service as _:
            with _.get_provider() as provider:
                with provider.create_session() as session:
                    result = session.execute(payload)
                    assert result['status'] == 'success'
```

### 2. Group Related Tests

```python
class test_Service__LLM(TestCase):
    
    # Initialization tests
    def test__init__(self): 
        with self.service as _:
            assert type(_) is Service__LLM
            
    def test_setup(self): 
        with self.service as _:
            _.setup()
            assert _.is_configured is True
    
    # Core functionality tests  
    def test_execute_request(self): 
        with self.service as _:
            result = _.execute_request("test")
            assert result is not None
            
    def test_execute_request__with_system_prompt(self): 
        with self.service as _:
            result = _.execute_request("test", system="prompt")
            assert 'system' in result
            
    def test_execute_request__error_handling(self): 
        with self.service as _:
            with pytest.raises(ValueError):
                _.execute_request("")
    
    # Edge cases
    def test__empty_prompt(self): 
        with self.service as _:
            with pytest.raises(ValueError):
                _.execute_request("")
                
    def test__max_tokens_exceeded(self): 
        with self.service as _:
            with pytest.raises(ValueError):
                _.execute_request("test", max_tokens=999999)
    
    # Integration tests
    @pytest.mark.skip(reason="requires API key")
    def test__with_actual_api(self): 
        with self.service as _:
            result = _.execute_request("test")
            assert len(result['response']) > 0
```

### 2. Use Descriptive Test Names

```python
# Good test names - describe what's being tested
def test__cache_models__response(self): pass
def test__get_cached_models__when__expired(self): pass
def test__calculate_cost__with__cache_hits(self): pass

# Bad test names - too vague
def test_cache(self): pass
def test_models(self): pass
def test_cost(self): pass
```

### 3. Test Data Patterns with Context Managers

```python
@classmethod
def setUpClass(cls):
    # Define reusable test data
    cls.test_request_simple = {
        'model'   : 'openai/gpt-4o-mini',
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'temperature': 0.7
    }
    
    cls.test_response_simple = {
        'choices': [{'message': {'content': 'Hi there!'}}],
        'usage'  : {'total_tokens': 25}
    }
    
def test__with_test_data(self):
    with self.service as _:
        result = _.process(self.test_request_simple)
        # Use class-level test data for consistency
        assert result['status'] == 'success'
        
def test__multiple_contexts(self):
    # Nested context managers for complex scenarios
    with self.service as service:
        with service.create_request(self.test_request_simple) as request:
            with service.execute(request) as response:
                assert response.data == self.test_response_simple
```

### 4. Skip Patterns for External Dependencies

```python
# Skip when API key missing
if not get_env(ENV_NAME_OPEN_ROUTER__API_KEY):
    pytest.skip("OpenRouter API key required")
    
# Skip expensive operations
@pytest.mark.skip(reason="Costs money - run manually")
def test_paid_api_call(self): pass

# Skip in CI/CD
if in_github_action():
    pytest.skip("Flaky in GitHub Actions")
```

---

## Bug Testing and Regression Pattern

### Writing Passing Tests for Bugs

**CRITICAL PATTERN**: When encountering bugs, write tests that PASS with the current buggy behavior, clearly documenting what SHOULD happen. These automatically become regression tests when the bug is fixed.

```python
class test_Type_Safe__bugs(TestCase):
    
    def test__bug__type_safety_assignments__on_obj__bool_assigned_to_int(self):     # Document bug where bool values are incorrectly allowed in int fields
        
        class An_Class(Type_Safe):
            an_int: int
            
        an_class = An_Class()
        
        # Document the correct behavior that should happen
        # asserts_exception('an_int', True, 'int', 'bool')  # Should raise but doesn't
        
        # Document the current buggy behavior
        an_class.an_int = True                              # BUG: should have raised exception
        assert an_class.an_int       is True                # BUG: confirming int field contains bool
        assert type(an_class.an_int) is bool                # BUG: type is bool not int
        
    def test__bug__roundtrip_tuple_support(self):           # Document bug in tuple type safety and serialization
        
        class An_Class(Type_Safe):
            tuple_1: tuple[str, str]
            
        an_class = An_Class()
        
        # Document what should happen
        # with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
        #     an_class.tuple_1 = (123, '123')                # BUG: should have raised
        
        # Document current buggy behavior
        an_class.tuple_1 = (123, '123')                     # BUG: accepts invalid types
        assert type(an_class.tuple_1)     is tuple          # BUG: should be Type_Safe__Tuple
        assert an_class.json()['tuple_1'] == [123, '123']   # BUG: wrong values in JSON
```

### Regression Test Pattern

When bugs are fixed, uncomment the correct assertions and comment out the buggy behavior:

```python
def test__regression__list__forward_ref__fails_roundtrip(self):             # Regression test for forward reference handling in lists
    
    class An_Class(Type_Safe):
        an_list: List['An_Class']
        
    an_class = An_Class(an_list=[An_Class()])
    json_data = an_class.json()
    
    # Original bug (now commented out after fix)
    # with pytest.raises(TypeError, match="'ForwardRef' object is not callable"):
    #     An_Class.from_json(json_data)                  # BUG: ForwardRef not handled
    
    # Fixed behavior (was commented during bug phase)
    assert An_Class.from_json(json_data).json() == json_data  # FIXED: Works correctly
```

### Bug Test Organization

```python
# Separate files for different bug categories
tests/unit/type_safe/
    test_Type_Safe__bugs.py              # Active bugs in main Type_Safe
    test_Type_Safe__Dict__bugs.py        # Active bugs in Dict implementation
    test_Type_Safe__List__bugs.py        # Active bugs in List implementation
    test_Type_Safe__regression.py        # Fixed bugs (regression suite)
    test_Type_Safe__Dict__regression.py  # Fixed Dict bugs
    test_Type_Safe__List__regression.py  # Fixed List bugs
```

### Bug Documentation Standards

1. **Clear bug markers**: Use `# BUG:` comments to mark buggy behavior
2. **Expected behavior**: Comment out what SHOULD happen with explanation
3. **Current behavior**: Assert what ACTUALLY happens (passing test)
4. **Context**: Include enough setup to reproduce the issue
5. **Migration path**: Structure so uncommenting fixes the test when bug is fixed

```python
def test__bug__nested_types__not_supported(self):
    """Bug: Type_Safe__Dict doesn't validate nested custom types"""
    
    class Inner(Type_Safe):
        value: str
        
    class Outer(Type_Safe):
        items: Dict[str, Inner]
        
    outer = Outer()
    
    # What SHOULD happen (currently commented)
    # with pytest.raises(TypeError, match="Expected 'Inner', but got 'str'"):
    #     outer.items['key'] = "not_an_inner"           # Should reject string
    
    # What ACTUALLY happens (bug - test passes)
    outer.items['key'] = "not_an_inner"                   # BUG: accepts invalid type
    assert type(outer.items['key']) is str                # BUG: stored as string
    assert outer.items['key'] == "not_an_inner"           # BUG: no type conversion
```

### Benefits of This Pattern

1. **Living documentation**: Bugs are documented with executable tests
2. **Automatic regression suite**: Fixed bugs stay fixed
3. **Clear communication**: Team knows about issues without breaking CI
4. **Progress tracking**: See bugs get fixed over time
5. **No lost knowledge**: Bug context preserved in tests

## Common Assertions Reference

```python
# Type checking
assert type(obj)           is ExpectedClass
assert base_classes(obj)   == [Type_Safe, object]
assert isinstance(obj, Type_Safe)

# Value checking  
assert obj.value           == expected_value
assert obj.json()          == expected_dict
assert len(collection)     == expected_count

# Collection membership
assert item in collection
assert key in dictionary
assert all(condition for item in collection)
assert any(term in text for term in ["expected", "terms"])

# Exception testing
with pytest.raises(TypeError):
    invalid_operation()

error_message = "specific error"    
with pytest.raises(ValueError, match=re.escape(error_message)):
    invalid_value()

# API response testing
assert response.status_code == 200
assert 'field' in response.json()
assert response.json()['field'] == expected_value
```

---


## Error Message Testing Pattern

### Full Error Message Validation

When testing exceptions, always validate the complete error message rather than partial matches. This ensures error messages remain consistent and catches unintended changes to error text.

```python
import re
from unittest import TestCase
import pytest

class test_Service__Validation(TestCase):
    
    def test_validation_errors(self):
        # ✗ AVOID - Partial match can hide message changes
        with pytest.raises(ValueError, match="specific error"):
            self.service.validate("bad_input")
            
        # ✓ PREFERRED - Full message with re.escape for special characters
        error_message = "Invalid type for attribute 'user_id'. Expected '<class 'Safe_Id'>' but got '<class 'str'>'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            self.service.validate("bad_input")
```

### Multiple Error Scenarios

When testing multiple error conditions, use descriptive variable names for each error message:

```python
def test_multiple_validation_errors(self):                              # Test various error conditions
    # Test missing required field
    error_message_missing_field = "Required field 'user_id' is missing from request"
    with pytest.raises(ValueError, match=re.escape(error_message_missing_field)):
        self.service.process({})
        
    # Test invalid type
    error_message_invalid_type = "Invalid type for attribute 'age'. Expected '<class 'int'>' but got '<class 'str'>'"
    with pytest.raises(TypeError, match=re.escape(error_message_invalid_type)):
        self.service.process({'user_id': '123', 'age': 'not_a_number'})
        
    # Test out of range
    error_message_out_of_range = "Value 999 exceeds maximum allowed value of 150 for field 'age'"
    with pytest.raises(ValueError, match=re.escape(error_message_out_of_range)):
        self.service.process({'user_id': '123', 'age': 999})
```

### Benefits of Full Message Testing

1. **Regression detection**: Catches any changes to error messages
2. **Documentation**: Error messages serve as documentation
3. **User experience**: Ensures consistent error messages for API users
4. **Debugging**: Full messages make test failures more informative
5. **Special character safety**: `re.escape()` handles regex special characters

### Pattern for Type_Safe Errors

Type_Safe generates consistent error messages that should be tested in full:

```python
def test_type_safe_enforcement_errors(self):
    with Schema__User() as _:
        # Test each type violation with full message
        error_bool_to_str = "Invalid type for attribute 'name'. Expected '<class 'str'>' but got '<class 'bool'>'"
        with pytest.raises(ValueError, match=re.escape(error_bool_to_str)):
            _.name = True
            
        error_int_to_safe_id = "Invalid type for attribute 'user_id'. Expected 'Safe_Id' but got '<class 'int'>'"
        with pytest.raises(TypeError, match=re.escape(error_int_to_safe_id)):
            _.user_id = 12345
            
        error_negative_age = "Value -5 is below minimum value 0 for Safe_UInt__Age"
        with pytest.raises(ValueError, match=re.escape(error_negative_age)):
            _.age = -5
```

### Complex Error Messages with Special Characters

Some error messages contain regex special characters that must be escaped:

```python
def test_error_with_special_characters(self):
    # Error message with parentheses, brackets, dots
    error_complex = "Invalid format for field 'config'. Expected Dict[str, Any] but got <class 'list'>"
    with pytest.raises(TypeError, match=re.escape(error_complex)):
        self.service.set_config([1, 2, 3])
        
    # Error with file paths
    error_file_path = "File not found: /path/to/file.json (expected .yaml extension)"
    with pytest.raises(FileNotFoundError, match=re.escape(error_file_path)):
        self.service.load_config("/path/to/file.json")
```

### Best Practices

1. **Store messages in variables**: Makes tests more readable and maintainable
2. **Use descriptive variable names**: `error_message_invalid_type` not `err1`
3. **Always use `re.escape()`**: Prevents regex interpretation of special characters
4. **Test the exact message**: Not just keywords or partial matches
5. **Group related errors**: Keep error tests for similar functionality together


## Example: Complete Test File with Context Managers and .obj()

```python
from unittest                                      import TestCase
import pytest
from osbot_utils.utils.Env                         import get_env, load_dotenv
from osbot_utils.utils.Objects                     import base_classes, __
from mgraph_ai_service_llms.service.llms.LLM_Service import LLM_Service
from tests.unit.Service__Fast_API__Test_Objs       import setup__service_fast_api_test_objs

class test_LLM_Service(TestCase):
    
    @classmethod
    def setUpClass(cls):
        load_dotenv()
        setup__service_fast_api_test_objs()
        cls.service = LLM_Service()
        
        if not get_env("OPEN_ROUTER__API_KEY"):
            pytest.skip("API key required")
            
    def test__init__(self):
        with self.service as _:
            # Use .obj() for comprehensive verification
            assert _.obj() == __(provider       = _.provider         ,  # Auto-initialized
                                cache_enabled  = True                ,
                                max_retries    = 3                   ,
                                timeout        = 30                  ,
                                api_key        = _.api_key           )  # Loaded from env
            
    def test_execute_request(self):
        with self.service as _:
            result = _.execute_request(
                prompt = "Say 'test'",
                model  = "mistral-small-free"
            )
            
            # Use dict comparison for API responses
            assert result == {'model'    : 'mistral-small-free'      ,
                            'prompt'   : "Say 'test'"                ,
                            'response' : result['response']          ,  # Dynamic value
                            'usage'    : result['usage']             ,  # Dynamic value
                            'status'   : 'success'                   }
        
    def test_execute_request__error_handling(self):
        with self.service as _:
            with pytest.raises(ValueError, match="Input must have"):
                _.execute_request(prompt="", model="test")
                
    def test_complex_nested_state(self):
        with self.service as service:
            service.configure(cache=True, retries=5)
            
            # Verify complete configuration state
            assert service.config.obj() == __(cache_settings = __(enabled     = True ,
                                                                  ttl_seconds = 3600 ,
                                                                  max_size    = 1000 ),
                                             retry_settings = __(max_attempts = 5    ,
                                                                backoff      = 2.0  ,
                                                                timeout      = 30   ),
                                             models         = service.config.models )
```

---

## Testing Checklist

### For Safe Types

When testing schemas with custom Safe types:

- [ ] Test with pre-converted Safe type instances
- [ ] Test with raw string/int/float values
- [ ] Compare both results - they should match
- [ ] Use `.obj()` to see actual stored values
- [ ] Test edge cases: special characters, max length, empty values
- [ ] Test invalid inputs to ensure proper rejection
- [ ] Document any conversion behavior as intentional or bug
- [ ] **NEW: Test Safe_Float precision and rounding behaviors**
- [ ] **NEW: Test Safe_Float bounds enforcement and clamping**
- [ ] **NEW: Test Enum auto-conversion from strings**
- [ ] **NEW: Test Literal value constraints**
- [ ] **NEW: Test regex_mode behavior (REPLACE vs MATCH)**
- [ ] **NEW: Test exact_length, to_lower_case attributes**
- [ ] **NEW: Test LLM message size limits**
- [ ] **NEW: Test Git/GitHub format validation**
- [ ] **NEW: Test cryptographic key length validation**

---

### For a Type_Safe service:

- [ ] Test file mirrors source structure under `tests/unit/`
- [ ] Test class named `test_ClassName` 
- [ ] Use `setUpClass` for all expensive operations (services, connections)
- [ ] Use `setUp` only for lightweight, test-specific data
- [ ] Implement proper `tearDownClass` and `tearDown` cleanup
- [ ] Use context managers with `_` throughout
- [ ] Use `.obj()` with `__` for comprehensive comparisons
- [ ] Use `.json()` for API responses with special characters
- [ ] `test__init__` verifies Type_Safe inheritance and attributes
- [ ] Test type enforcement for all Safe types
- [ ] Test serialization round-trips preserve types
- [ ] **NEW: Test Enum serialization/deserialization in JSON**
- [ ] **NEW: Test Literal types in JSON round-trips**
- [ ] Test auto-initialization creates isolated instances
- [ ] Test error conditions and edge cases
- [ ] **NEW: Test full error messages with re.escape()**
- [ ] Use `setup__service_fast_api_test_objs()` for LocalStack
- [ ] Skip tests requiring API keys when not available
- [ ] Test FastAPI routes with TestClient
- [ ] Verify S3 operations use LocalStack
- [ ] Group related tests logically
- [ ] Use descriptive test method names
- [ ] Define reusable test data in `setUpClass`
- [ ] Verify service atomicity (can be reused across tests)
- [ ] **NEW: Test LLM-specific Safe types for model IDs**
- [ ] **NEW: Test HTTP Safe types for headers and content**
- [ ] **NEW: Test version string validation patterns**

## Wrapping up

This guide ensures consistent, thorough testing of Type_Safe services while maintaining the visual formatting patterns and type safety guarantees that make the framework valuable.
