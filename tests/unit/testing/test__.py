from unittest                import TestCase
import pytest
from osbot_utils.testing.__  import __, __SKIP__, __MISSING__


class test__(TestCase):

    def test__init__(self):                                                                 # Test basic initialization
        with __() as _:
            assert type(_).__name__        == '__'
            assert type(_).__module__      == 'osbot_utils.testing.__'
            assert _.__dict__              == {}                                           # Empty on init

        with __(a=1, b='test', c=True) as _:                                              # With initial values
            assert _.a == 1
            assert _.b == 'test'
            assert _.c == True

    def test__context_manager(self):                                                       # Test context manager protocol
        with __() as _:
            assert _ is not None
            _.test_value = 'inside'
            assert _.test_value == 'inside'

        # Test __exit__ returns False (doesn't suppress exceptions)
        try:
            with __() as _:
                raise ValueError("test error")
        except ValueError as e:
            assert str(e) == "test error"                                                  # Exception propagated

    def test__contains__(self):                                                            # Test 'in' operator overload
        with __(a=1, b=2, c=3) as superset:
            with __(a=1, b=2) as subset:
                assert subset in superset                                                  # Subset check works
                assert __(a=1) in superset                                                # Single field
                assert not __(d=4) in superset                                            # Missing field
                assert not __(a=2) in superset                                            # Wrong value

    def test__eq__(self):                                                                  # Test equality with __SKIP__ support
        with __(a=1, b='test', c=3.14) as obj1:
            with __(a=1, b='test', c=3.14) as obj2:
                assert obj1 == obj2                                                        # Exact match

            with __(a=1, b='test', c=2.71) as obj3:
                assert obj1 != obj3                                                        # Different value

    def test__eq__with_skip(self):                                                        # Test __SKIP__ marker in equality
        with __(id='test-123', name='Test', timestamp=1234567890) as _:
            # Can skip dynamic fields
            assert _ == __(id=__SKIP__, name='Test', timestamp=__SKIP__)                  # Skip ID and timestamp
            assert _ == __(id='test-123', name='Test', timestamp=__SKIP__)               # Skip only timestamp
            assert _ != __(id='wrong', name='Test', timestamp=__SKIP__)                   # Wrong ID not skipped

    def test__eq__with_nested(self):                                                      # Test equality with nested __ objects
        with __(a=1, nested=__(x=10, y=20)) as obj1:
            with __(a=1, nested=__(x=10, y=20)) as obj2:
                assert obj1 == obj2                                                        # Nested objects equal

            with __(a=1, nested=__(x=10, y=30)) as obj3:
                assert obj1 != obj3                                                        # Nested difference detected

    def test_contains(self):                                                              # Test contains method for partial matching
        with __(id='123', name='Test', age=25, status='active') as _:
            assert _.contains(__(id='123'))                                               # Single field match
            assert _.contains(__(id='123', name='Test'))                                 # Multiple fields match
            assert _.contains(__(id='123', name='Test', age=25))                        # More fields match
            assert not _.contains(__(id='456'))                                          # Wrong value
            assert not _.contains(__(missing_field='value'))                             # Non-existent field

    def test_contains__with_dict(self):                                                   # Test contains with dict input
        with __(a=1, b=2, c=3) as _:
            assert _.contains({'a': 1})                                                   # Dict with single field
            assert _.contains({'a': 1, 'b': 2})                                          # Dict with multiple fields
            assert not _.contains({'d': 4})                                              # Dict with missing field

    def test_contains__with_nested(self):                                                 # Test contains with nested structures
        with __(user=__(id='u1', name='Alice'), settings=__(theme='dark')) as _:
            assert _.contains(__(user=__(id='u1')))                                      # Partial nested match
            assert _.contains(__(user=__(name='Alice')))                                 # Different nested field
            assert not _.contains(__(user=__(id='u2')))                                  # Wrong nested value

    def test_contains__with_skip(self):                                                   # Test contains with __SKIP__ marker
        with __(id='123', name='Test', timestamp=999) as _:
            assert _.contains(__(id='123', timestamp=__SKIP__))                          # Skip timestamp in contains
            assert _.contains(__(id=__SKIP__, name='Test'))                              # Skip id in contains

    def test_contains__with_invalid_input(self):                                          # Test contains with invalid inputs
        with __(a=1) as _:
            assert not _.contains("string")                                               # String input returns False
            assert not _.contains(123)                                                    # Number input returns False
            assert not _.contains(None)                                                   # None input returns False

    def test_diff(self):                                                                  # Test diff method for debugging
        with __(a=1, b='test', c=3.14) as obj1:
            with __(a=1, b='test', c=3.14) as obj2:
                assert obj1.diff(obj2) is None                                            # No differences

            with __(a=2, b='test', c=3.14) as obj3:
                diff = obj1.diff(obj3)
                assert diff == {'a': {'actual': 1, 'expected': 2}}                       # Single difference

            with __(a=2, b='changed', d=4) as obj4:
                diff = obj1.diff(obj4)
                assert 'a' in diff                                                        # Changed field
                assert 'b' in diff                                                        # Another changed field
                assert 'c' in diff                                                        # Missing in obj4
                assert 'd' in diff                                                        # Extra in obj4

    def test_diff__with_dict(self):                                                       # Test diff with dict comparison
        with __(a=1, b=2) as _:
            diff = _.diff({'a': 1, 'b': 3})
            assert diff == {'b': {'actual': 2, 'expected': 3}}                          # Dict comparison works

    def test_diff__with_missing_fields(self):                                            # Test diff with missing fields
        with __(a=1, b=2) as obj1:
            with __(a=1) as obj2:
                diff = obj1.diff(obj2)
                assert diff == {'b': {'actual': 2, 'expected': __MISSING__}}            # Missing marked correctly

            with __(a=1, b=2, c=3) as obj3:
                diff = obj1.diff(obj3)
                assert diff == {'c': {'actual': __MISSING__, 'expected': 3}}            # Extra field detected

    def test_excluding(self):                                                             # Test excluding fields from comparison
        with __(id='123', name='Test', created_at='2024-01-01', updated_at='2024-01-02') as _:
            excluded = _.excluding('created_at', 'updated_at')
            assert excluded.id   == '123'
            assert excluded.name == 'Test'
            assert not hasattr(excluded, 'created_at')                                   # Field removed
            assert not hasattr(excluded, 'updated_at')                                   # Field removed

    def test_excluding__returns_new_instance(self):                                      # Test excluding returns new instance
        with __(a=1, b=2, c=3) as original:
            excluded = original.excluding('b')
            assert hasattr(original, 'b')                                                # Original unchanged
            assert not hasattr(excluded, 'b')                                            # New instance modified
            assert original is not excluded                                              # Different instances

    def test_excluding__with_non_existent_field(self):                                   # Test excluding non-existent fields
        with __(a=1, b=2) as _:
            excluded = _.excluding('c', 'd')                                             # Non-existent fields
            assert excluded.a == 1                                                       # Existing fields preserved
            assert excluded.b == 2

    def test_merge(self):                                                                 # Test merge for creating variations
        with __(model='gpt-4', temperature=0.7, max_tokens=100) as base:
            merged = base.merge(temperature=0.9)
            assert merged.model       == 'gpt-4'                                         # Unchanged field
            assert merged.temperature == 0.9                                             # Updated field
            assert merged.max_tokens  == 100                                             # Unchanged field

    def test_merge__adds_new_fields(self):                                               # Test merge adds new fields
        with __(a=1, b=2) as base:
            merged = base.merge(c=3, d=4)
            assert merged.a == 1
            assert merged.b == 2
            assert merged.c == 3                                                         # New field added
            assert merged.d == 4                                                         # New field added

    def test_merge__with_nested(self):                                                   # Test merge with nested __ objects
        with __(config=__(host='localhost', port=8080), timeout=30) as base:
            merged = base.merge(config=__(port=9090))
            assert merged.config.host == 'localhost'                                     # Nested unchanged field
            assert merged.config.port == 9090                                            # Nested updated field
            assert merged.timeout     == 30                                              # Top-level unchanged

    def test_merge__returns_new_instance(self):                                          # Test merge returns new instance
        with __(a=1, b=2) as original:
            merged = original.merge(b=3)
            assert original.b == 2                                                       # Original unchanged
            assert merged.b   == 3                                                       # New instance updated
            assert original is not merged                                                # Different instances

    def test_merge__replaces_non_nested(self):                                          # Test merge replaces non-__ nested values
        with __(config=__(a=1), value='test') as base:
            merged = base.merge(config={'completely': 'new'}, value='changed')
            assert merged.config == {'completely': 'new'}                                # Dict replaced entirely
            assert merged.value  == 'changed'                                            # Value replaced

    # Integration tests combining multiple features

    def test__integration__excluding_and_equality(self):                                 # Test excluding with equality check
        with __(id='123', name='Test', timestamp=999, version=1) as obj1:
            with __(id='123', name='Test', timestamp=888, version=1) as obj2:
                # Objects differ in timestamp
                assert obj1 != obj2
                # But are equal when timestamp excluded
                assert obj1.excluding('timestamp') == obj2.excluding('timestamp')

    def test__integration__merge_and_contains(self):                                     # Test merge with contains check
        with __(base='value', extra='data') as template:
            variation = template.merge(extra='modified', new_field='added')
            assert variation.contains(__(base='value'))                                  # Still contains base
            assert variation.contains(__(extra='modified'))                              # Contains modification
            assert variation.contains(__(new_field='added'))                             # Contains addition

    def test__integration__nested_operations(self):                                      # Test all operations with nested structures
        with __(
            user    = __(id='u1', name='Alice', role='admin'),
            settings = __(theme='dark', notifications=__(email=True, sms=False)),
            metadata = __(created_at='2024-01-01', updated_at='2024-01-02')
        ) as complex_obj:

            # Test contains with nested
            assert complex_obj.contains(__(user=__(role='admin')))
            assert complex_obj.contains(__(settings=__(notifications=__(email=True))))

            # Test merge with nested
            updated = complex_obj.merge(
                user=__(role='user'),
                settings=__(theme='light')
            )
            assert updated.user.role        == 'user'                                    # Nested field updated
            assert updated.user.name        == 'Alice'                                   # Nested field preserved
            assert updated.settings.theme   == 'light'                                   # Nested field updated
            assert updated.settings.notifications.email == True                          # Deep nested preserved

            # Test excluding works on top level only
            excluded = complex_obj.excluding('metadata')
            assert not hasattr(excluded, 'metadata')
            assert hasattr(excluded, 'user')
            assert hasattr(excluded, 'settings')

    def test__integration__skip_in_complex_comparison(self):                             # Test __SKIP__ in complex scenarios
        with __(request_id = 'req-123'                                       ,
                timestamp  = 1234567890                                      ,
                payload    = __(action='create', resource='user', id='u-456'),
                response   = __(status=200, duration_ms=45                   )) as api_log:

            # Can skip multiple dynamic fields at different levels
            expected = __(request_id = __SKIP__,                                                   # Skip request ID
                          timestamp  = __SKIP__,                                                   # Skip timestamp
                          payload    = __(action='create', resource='user', id='u-456'),
                          response   = __(status=200, duration_ms=__SKIP__            ))           # Skip duration

            assert api_log == expected                                                            # Comparison works with skips

            # Contains also respects __SKIP__
            assert api_log.contains(__(
                payload=__(action='create', id=__SKIP__),                               # Skip nested ID
                response=__(status=200)
            ))

    def test__real_world_example__test_data_builder(self):                              # Real-world pattern from docs
        # Build test data incrementally
        base_request = __(
            model       = 'openai/gpt-4o-mini',
            messages    = [{'role': 'user', 'content': 'Hello'}],
            temperature = 0.7
        )

        # Create variations for different test cases
        high_temp_request = base_request.merge(temperature=0.9, top_p=0.95)
        system_request = base_request.merge(
            messages=[
                {'role': 'system', 'content': 'You are helpful'},
                {'role': 'user', 'content': 'Hello'}
            ]
        )

        # Verify variations
        assert high_temp_request.temperature == 0.9
        assert high_temp_request.model      == 'openai/gpt-4o-mini'                     # Base preserved
        assert 'top_p' in high_temp_request.__dict__                                    # New field added

        assert len(system_request.messages) == 2
        assert system_request.temperature   == 0.7                                      # Base preserved

    def test__real_world_example__api_response_validation(self):                        # Real-world API response testing
        # Simulate API response
        api_response = __(
            status_code = 200,
            headers     = __(content_type='application/json', x_request_id='req-789'),
            json        = __(
                data   = [__(id='1', value='first'), __(id='2', value='second')],
                meta   = __(total=2, page=1),
                timestamp = '2024-01-01T12:00:00Z'
            )
        )

        # Validate structure without caring about dynamic values
        expected_structure = __(
            status_code = 200,
            headers     = __(content_type='application/json', x_request_id=__SKIP__),
            json        = __(
                data      = __SKIP__,                                                   # Don't care about specific data
                meta      = __(total=2, page=1),
                timestamp = __SKIP__                                                    # Skip timestamp
            )
        )

        assert api_response == expected_structure                                       # Structure valid
        assert api_response.json.contains(__(meta=__(total=2)))                        # Specific check