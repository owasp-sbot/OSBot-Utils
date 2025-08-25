# Type_Safe Testing Guidance for Fast_API Services 

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

### 3. Use .obj() for Readable Comparisons

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
- The object is very large (>20 fields) - becomes brittle
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

### 4. Optimize Performance with setUpClass

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

### 5. Standard Test Class Structure

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

## Testing Checklist

When writing tests for a Type_Safe service:

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
- [ ] Test auto-initialization creates isolated instances
- [ ] Test error conditions and edge cases
- [ ] Use `setup__service_fast_api_test_objs()` for LocalStack
- [ ] Skip tests requiring API keys when not available
- [ ] Test FastAPI routes with TestClient
- [ ] Verify S3 operations use LocalStack
- [ ] Group related tests logically
- [ ] Use descriptive test method names
- [ ] Define reusable test data in `setUpClass`
- [ ] Verify service atomicity (can be reused across tests)

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

This guide ensures consistent, thorough testing of Type_Safe services while maintaining the visual formatting patterns and type safety guarantees that make the framework valuable.
