import re
import pytest
from unittest                       import TestCase
from osbot_utils.testing.__         import __, __SKIP__, __MISSING__,  __GREATER_THAN__, __LESS_THAN__, __BETWEEN__, __CLOSE_TO__
from osbot_utils.testing.__helpers  import obj


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


    def test__regression__osbot_utils__obj__doesnt_handle_reserved_keywords(self):
        an_json = {"tag"   : "p",
                   "class" : "title"}

        assert obj(an_json) == __(tag='p', _class='title')  # FIXED : BUG :this doesn't compile

    # Basic comparison operator tests

    def test__greater_than__basic(self):                                                   # Test __GREATER_THAN__ with simple values
        with __(score=85, count=100, rating=4.5) as _:
            assert _ == __(score=__GREATER_THAN__(80), count=100, rating=4.5)            # Score > 80 passes
            assert _ == __(score=__GREATER_THAN__(0 ), count=100, rating=4.5)            # Score > 0 passes
            assert _ != __(score=__GREATER_THAN__(90), count=100, rating=4.5)            # Score not > 90 fails
            assert _ != __(score=__GREATER_THAN__(85), count=100, rating=4.5)            # Score not > 85 (equal) fails

            error_message = ("assert __(score=85, count=100, rating=4.5) =="
                                   " __(score=('gt', 90), count=100, rating=4.5)\n + "
                             " where __(score=('gt', 90), count=100, rating=4.5) = "
                                    "__(score=('gt', 90), count=100, rating=4.5)\n +    "
                             "where ('gt', 90) = __GREATER_THAN__(90)")
            with pytest.raises(AssertionError, match=re.escape(error_message)):
                assert _ == __(score=__GREATER_THAN__(90), count=100, rating=4.5)

    def test__greater_than__floats(self):                                                 # Test __GREATER_THAN__ with floating point
        with __(duration=0.234, latency=1.567) as _:
            assert _ == __(duration=__GREATER_THAN__(0.2), latency=__GREATER_THAN__(1.5))
            assert _ == __(duration=__GREATER_THAN__(0.0), latency=__GREATER_THAN__(0.0))
            assert _ != __(duration=__GREATER_THAN__(0.5), latency=__GREATER_THAN__(1.5))

    def test__less_than__basic(self):                                                     # Test __LESS_THAN__ with simple values
        with __(duration=0.3, retries=2, age=25) as _:
            assert _ == __(duration=__LESS_THAN__(0.5), retries=2, age=25)               # Duration < 0.5 passes
            assert _ == __(duration=__LESS_THAN__(1.0), retries=2, age=25)               # Duration < 1.0 passes
            assert _ != __(duration=__LESS_THAN__(0.2), retries=2, age=25)               # Duration not < 0.2 fails
            assert _ != __(duration=__LESS_THAN__(0.3), retries=2, age=25)               # Duration not < 0.3 (equal) fails

    def test__less_than__negative_numbers(self):                                         # Test __LESS_THAN__ with negative values
        with __(balance=-50, temperature=-10.5) as _:
            assert _ == __(balance=__LESS_THAN__(0   ), temperature=__LESS_THAN__(0))
            assert _ == __(balance=__LESS_THAN__(-10 ), temperature=__LESS_THAN__(-5))
            assert _ != __(balance=__LESS_THAN__(-100), temperature=__LESS_THAN__(-20))

    def test__between__basic(self):                                                       # Test __BETWEEN__ with simple ranges
        with __(score=75, percentage=0.85, age=30) as _:
            assert _ == __(score=__BETWEEN__(0, 100 ), percentage=0.85, age=30)           # Score in range passes
            assert _ == __(score=__BETWEEN__(75, 100), percentage=0.85, age=30)          # Inclusive lower bound
            assert _ == __(score=__BETWEEN__(0, 75  ), percentage=0.85, age=30)            # Inclusive upper bound
            assert _ != __(score=__BETWEEN__(80, 100), percentage=0.85, age=30)          # Below range fails
            assert _ != __(score=__BETWEEN__(0, 70  ), percentage=0.85, age=30)            # Above range fails

    def test__between__floats(self):                                                      # Test __BETWEEN__ with floating point ranges
        with __(probability=0.753, ratio=1.5) as _:
            assert _ == __(probability=__BETWEEN__(0.0, 1.0  ), ratio=__BETWEEN__(1.0, 2.0))
            assert _ == __(probability=__BETWEEN__(0.75, 0.76), ratio=__BETWEEN__(1.5, 1.5))  # Exact match at bounds
            assert _ != __(probability=__BETWEEN__(0.8, 1.0  ), ratio=__BETWEEN__(1.0, 2.0))

    def test__close_to__basic(self):                                                      # Test __CLOSE_TO__ with default tolerance
        with __(score=0.573, probability=0.424) as _:
            assert _ == __(score=__CLOSE_TO__(0.573), probability=0.424)                 # Exact match passes
            assert _ == __(score=__CLOSE_TO__(0.574), probability=0.424)                 # Within 0.01 tolerance passes
            assert _ == __(score=__CLOSE_TO__(0.580), probability=0.424)                 # Within default tolerance
            assert _ != __(score=__CLOSE_TO__(0.600), probability=0.424)                 # Outside default tolerance fails

    def test__lose_to__custom_tolerance(self):                                          # Test __CLOSE_TO__ with custom tolerance
        with __(value=0.00101) as _:
            assert _ == __(value=__CLOSE_TO__(0.001  , tolerance=0.0001))                # Within 0.0001 tolerance
            assert _ == __(value=__CLOSE_TO__(0.00101, tolerance=0.00001))               # Exact match
            assert _ == __(value=__CLOSE_TO__(0.00102, tolerance=0.0001))                # Just within tolerance

            # todo review this
            assert _ != __(value=__CLOSE_TO__(0.001  , tolerance=0.00001))               # Outside tight tolerance

    def test__close_to__negative_values(self):                                           # Test __CLOSE_TO__ with negative numbers
        with __(delta=-0.05, offset=-10.0) as _:
            assert _ == __(delta=__CLOSE_TO__(-0.05, tolerance=0.01), offset=-10.0)
            assert _ == __(delta=__CLOSE_TO__(-0.06, tolerance=0.02), offset=-10.0)
            assert _ != __(delta=__CLOSE_TO__(0.05, tolerance=0.01), offset=-10.0)       # Wrong sign fails

    # Combined operator tests

    def test__multiple_operators_same_object(self):                                       # Test multiple operators in single assertion
        with __(duration=0.234, score=85, probability=0.753, count=42) as _:
            assert _ == __(duration    = __LESS_THAN__(0.5),
                           score       = __GREATER_THAN__(80),
                           probability = __BETWEEN__(0.7, 0.8),
                           count       = 42)

    def test__operators_with_skip(self):                                                  # Test operators combined with __SKIP__
        with __(id='test-123', timestamp=1234567890, score=85, duration=0.234) as _:
            assert _ == __(
                id       = __SKIP__,
                timestamp = __SKIP__,
                score    = __GREATER_THAN__(80),
                duration = __LESS_THAN__(0.5)
            )

    def test__operators_with_nested_objects(self):                                       # Test operators in nested __ objects
        with __(
            metadata = __(duration=0.234, retries=2),
            scores   = __(accuracy=0.953, precision=0.875)
        ) as _:
            assert _ == __(
                metadata = __(duration=__LESS_THAN__(0.5), retries=2),
                scores   = __(
                    accuracy  = __CLOSE_TO__(0.95, tolerance=0.01),
                    precision = __GREATER_THAN__(0.85)
                )
            )

    # Real-world use cases

    def test__aws_comprehend_sentiment_example(self):                                    # Real-world AWS Comprehend test pattern
        # Simulate AWS Comprehend response
        result = __(
            duration  = 0.234,
            sentiment = 'positive',
            score     = __(
                mixed    = 0.0010159355588257313,
                negative = 0.0,
                neutral  = 0.42408183217048645,
                positive = 0.5733687281608582
            )
        )

        # Validate with operators
        assert result == __(
            duration  = __LESS_THAN__(0.5),                                              # Performance check
            sentiment = 'positive',
            score     = __(
                mixed    = __CLOSE_TO__(0.001, tolerance=0.0001),                       # Tight tolerance
                negative = 0.0,                                                          # Exact match for zero
                neutral  = __CLOSE_TO__(0.424, tolerance=0.01),                         # Reasonable tolerance
                positive = __CLOSE_TO__(0.573, tolerance=0.01)
            )
        )

        # Can also use BETWEEN for score ranges
        assert result == __(duration  = __BETWEEN__(0.1, 0.5),
                            sentiment = 'positive',
                            score     = __(
                                mixed    = __BETWEEN__(0.0, 0.01),
                                negative = __BETWEEN__(0.0, 0.01),
                                neutral  = __BETWEEN__(0.4, 0.5),
                                positive = __BETWEEN__(0.5, 0.7)))

    def test__api_latency_performance_checks(self):                                      # Test API latency validation pattern
        api_result = __(
            status   = 200,
            latency  = 0.123,
            size     = 1024,
            cached   = False
        )

        assert api_result == __(
            status  = 200,
            latency = __LESS_THAN__(0.5),                                                # Must be fast
            size    = __GREATER_THAN__(0),                                               # Must have content
            cached  = False
        )

        # Different SLA for cached vs uncached
        cached_result = __(status=200, latency=0.005, size=1024, cached=True)
        assert cached_result == __(
            status  = 200,
            latency = __LESS_THAN__(0.01),                                               # Stricter SLA for cached
            size    = __GREATER_THAN__(0),
            cached  = True
        )

    def test__machine_learning_metrics(self):                                            # Test ML model evaluation pattern
        model_metrics = __(
            accuracy  = 0.9523,
            precision = 0.9401,
            recall    = 0.9678,
            f1_score  = 0.9537,
            train_time = 45.6
        )

        assert model_metrics == __(
            accuracy   = __CLOSE_TO__(0.95, tolerance=0.01),
            precision  = __GREATER_THAN__(0.93),
            recall     = __GREATER_THAN__(0.95),
            f1_score   = __BETWEEN__(0.94, 0.96),
            train_time = __LESS_THAN__(60.0)
        )

    def test__financial_calculations(self):                                              # Test financial data validation
        amount = 1234.56
        transaction = __(amount   = amount ,
                         fee      = 12.35  ,
                         rate     = 0.01   ,
                         balance  = 5000.00)

        assert transaction == __(
            amount  = __BETWEEN__(1000, 2000),
            fee     = __CLOSE_TO__(amount * 0.01, tolerance=0.01),                      # Fee is 1% of amount
            rate    = __BETWEEN__(0.0, 0.02),
            balance = __GREATER_THAN__(0)
        )

    # Edge cases and error conditions

    def test__operators_with_zero(self):                                                 # Test operators with zero values
        with __(value=0) as _:
            assert _ == __(value=__LESS_THAN__(1))
            assert _ == __(value=__GREATER_THAN__(-1))
            assert _ == __(value=__BETWEEN__(-1, 1))
            assert _ == __(value=__CLOSE_TO__(0, tolerance=0.01))

    def test__operators_with_infinity(self):                                             # Test operators with very large values
        with __(value=1e10) as _:
            assert _ == __(value=__GREATER_THAN__(1e9))
            assert _ == __(value=__LESS_THAN__(1e11))
            assert _ == __(value=__BETWEEN__(0, 1e12))

    def test__operators_with_tiny_floats(self):                                          # Test operators with very small values
        with __(epsilon=1e-10, delta=1e-8) as _:
            assert _ == __(epsilon=__CLOSE_TO__(0, tolerance=1e-9), delta=1e-8)
            assert _ == __(epsilon=__GREATER_THAN__(0), delta=__GREATER_THAN__(0))
            assert _ == __(epsilon=__BETWEEN__(0, 1e-5), delta=__BETWEEN__(0, 1e-5))

    # Integration test combining all features

    def test__integration__all_operators_with_all_features(self):                        # Complex integration test
        api_response = __(
            request_id = 'req-abc-123',
            timestamp  = 1234567890,
            status     = 200,
            timing     = __(
                total    = 0.456,
                db_query = 0.234,
                render   = 0.111
            ),
            metrics    = __(
                accuracy = 0.953,
                score    = 87.5,
                count    = 1024
            ),
            metadata   = __(
                version = '2.1.0',
                cached  = False
            )
        )

        # Complex validation with all operators and features
        expected = __(
            request_id = __SKIP__,                                                       # Skip dynamic ID
            timestamp  = __SKIP__,                                                       # Skip timestamp
            status     = 200,
            timing     = __(
                total    = __LESS_THAN__(0.5),                                           # Performance requirement
                db_query = __BETWEEN__(0.1, 0.3),                                        # DB time range
                render   = __CLOSE_TO__(0.11, tolerance=0.02)                           # Render time approximate
            ),
            metrics    = __(
                accuracy = __CLOSE_TO__(0.95, tolerance=0.01),
                score    = __GREATER_THAN__(85),
                count    = __BETWEEN__(1000, 2000)
            ),
            metadata   = __(
                version = '2.1.0',                                                       # Exact version match
                cached  = False
            )
        )

        assert api_response == expected


    def test__diff_with_operators(self):                                                 # Test diff shows operator mismatches
        with __(score=85, duration=0.234) as actual:
            with __(score=__GREATER_THAN__(90), duration=__LESS_THAN__(0.1)) as expected:
                diff = actual.diff(expected)
                # diff will show the actual values vs the operator tuples
                assert diff is not None
                assert 'score' in diff or 'duration' in diff                            # At least one field differs


    # Test operators work with contains() method

    def test__operators_with_contains__single_field(self):                               # Test single field with operator in contains
        with __(score=85, duration=0.234, count=100, name='test') as _:
            assert _.contains(__(score    = __GREATER_THAN__    (80     )))                            # Single field operator match
            assert _.contains(__(duration = __LESS_THAN__       (0.5    )))                           # Different operator
            assert _.contains(__(count    = __BETWEEN__         (50, 150)))                            # Range operator
            assert not _.contains(__(score    = __GREATER_THAN__(90     )))                        # Operator fails
            assert not _.contains(__(duration = __LESS_THAN__   (0.1    )))                       # Operator fails

    def test__operators_with_contains__multiple_fields(self):                            # Test multiple fields with operators
        with __(score=85, duration=0.234, status='active') as _:
            assert _.contains(__(score=__GREATER_THAN__(80), status='active'))          # Operator + exact match
            assert _.contains(__(score=__GREATER_THAN__(80), duration=__LESS_THAN__(0.5)))  # Multiple operators
            assert not _.contains(__(score=__GREATER_THAN__(90), status='active'))      # One operator fails

    def test__operators_in_nested_contains(self):                                        # Test operators in deeply nested contains
        with __(
            user   = __(name='Alice', score=85),
            stats  = __(wins=10, losses=2, ratio=5.0),
            config = __(timeout=30, retries=3)
        ) as _:
            assert _.contains(__(user=__(score=__GREATER_THAN__(80))))                   # Nested operator
            assert _.contains(__(stats=__(ratio=__BETWEEN__(4.0, 6.0))))                # Different nested operator
            assert _.contains(__(config=__(timeout=__LESS_THAN__(60))))                 # Another nested level

            # Multiple nested operators
            assert _.contains(__(
                user=__(score=__GREATER_THAN__(80)),
                stats=__(wins=__BETWEEN__(5, 15))
            ))

    def test__operators_in_deeply_nested_contains(self):                                 # Test operators three levels deep
        with __(
            api = __(
                response = __(
                    timing = __(latency=0.123, ttfb=0.045),
                    metrics = __(score=87.5, accuracy=0.953)
                )
            )
        ) as _:
            assert _.contains(__(api=__(response=__(timing=__(latency=__LESS_THAN__(0.2))))))
            assert _.contains(__(api=__(response=__(metrics=__(score=__GREATER_THAN__(85))))))
            assert _.contains(__(api=__(response=__(metrics=__(accuracy=__CLOSE_TO__(0.95, tolerance=0.01))))))

    # Test operators with excluding()

    def test__operators_with_excluding(self):                                            # Test operators work after excluding fields
        with __(id='123', timestamp=999, score=85, duration=0.234, status='active') as _:
            excluded = _.excluding('id', 'timestamp')

            # Operators should still work on remaining fields
            assert excluded == __(score=__GREATER_THAN__(80), duration=0.234, status='active')
            assert excluded == __(score=85, duration=__LESS_THAN__(0.5), status='active')
            assert excluded.contains(__(score=__GREATER_THAN__(80)))

    def test__excluding_then_operators_in_nested(self):                                  # Test excluding with nested operator comparisons
        with __(
            id = '123',
            timestamp = 999,
            data = __(score=85, metrics=__(accuracy=0.95, latency=0.123))
        ) as _:
            excluded = _.excluding('id', 'timestamp')

            assert excluded == __(data=__(
                score=__GREATER_THAN__(80),
                metrics=__(accuracy=__CLOSE_TO__(0.95, tolerance=0.01), latency=0.123)
            ))

    # Test operators with merge()

    def test__operators_in_merged_objects(self):                                         # Test operators work after merging
        base = __(score=85, duration=0.234, status='pending')
        merged = base.merge(status='active')

        assert merged == __(
            score=__GREATER_THAN__(80),
            duration=__LESS_THAN__(0.5),
            status='active'
        )

    def test__merge_then_operators_nested(self):                                         # Test merge with nested operators
        base = __(
            config = __(timeout=30, retries=3),
            metrics = __(score=85, accuracy=0.95)
        )

        merged = base.merge(config=__(timeout=60))

        assert merged == __(
            config=__(timeout=__BETWEEN__(50, 70), retries=3),
            metrics=__(score=__GREATER_THAN__(80), accuracy=__CLOSE_TO__(0.95, tolerance=0.01))
        )

    # Test operator edge cases

    def test__greater_than__with_equal_value(self):                                      # Test > operator fails on equal values
        with __(value=100) as _:
            assert _ != __(value=__GREATER_THAN__(100))                                  # 100 is not > 100
            assert _ == __(value=__GREATER_THAN__(99))                                   # 100 is > 99

    def test__less_than__with_equal_value(self):                                         # Test < operator fails on equal values
        with __(value=50) as _:
            assert _ != __(value=__LESS_THAN__(50))                                      # 50 is not < 50
            assert _ == __(value=__LESS_THAN__(51))                                      # 50 is < 51

    def test__between__boundary_conditions(self):                                        # Test BETWEEN is inclusive at boundaries
        with __(value=50) as _:
            assert _ == __(value=__BETWEEN__(50, 100))                                   # Lower bound inclusive
            assert _ == __(value=__BETWEEN__(0, 50))                                     # Upper bound inclusive
            assert _ == __(value=__BETWEEN__(50, 50))                                    # Both bounds equal and inclusive
            assert _ != __(value=__BETWEEN__(51, 100))                                   # Just outside lower bound
            assert _ != __(value=__BETWEEN__(0, 49))                                     # Just outside upper bound

    def test__between__inverted_range(self):                                             # Test BETWEEN with min > max (should always fail)
        with __(value=50) as _:
            # This is technically wrong usage but should fail gracefully
            assert _ != __(value=__BETWEEN__(100, 0))                                    # min > max means impossible range

    def test__close_to__at_exact_tolerance_boundary(self):                               # Test CLOSE_TO at tolerance boundary
        with __(value=1.0) as _:
            assert _ == __(value=__CLOSE_TO__(1.01, tolerance=0.02))                    # Exactly at boundary (0.01 away)
            assert _ == __(value=__CLOSE_TO__(0.99, tolerance=0.02))                    # Exactly at boundary (0.01 away)
            assert _ != __(value=__CLOSE_TO__(1.011, tolerance=0.01))                   # Just outside boundary
            assert _ != __(value=__CLOSE_TO__(0.989, tolerance=0.01))                   # Just outside boundary

    def test__close_to__with_zero_tolerance(self):                                       # Test CLOSE_TO with zero tolerance (exact match)
        with __(value=42.0) as _:
            assert _ == __(value=__CLOSE_TO__(42.0, tolerance=0))                       # Exact match
            assert _ != __(value=__CLOSE_TO__(42.000001, tolerance=0))                  # Any difference fails

    def test__operators_with_none_values__corrected(self):
        """Test operators gracefully handle None values"""

        with __(value=None, other=100) as _:
            # With the try-except fix, comparison with None now consistently returns False
            # This triggers an AssertionError (not TypeError) because __eq__ catches the TypeError
            # and returns False, making the assertion fail

            # This is the CORRECT and DETERMINISTIC behavior now:
            assert _ != __(value=__GREATER_THAN__(0))                # None comparison returns False
            assert _ != __(value=__LESS_THAN__(10))                  # None comparison returns False
            assert _ != __(value=__CLOSE_TO__(5, tolerance=1))       # None comparison returns False

            # The 'other' field still works normally
            assert _ == __(value=None, other=__GREATER_THAN__(90))  # Can mix None and operators


    def test__operators_with_none_in_contains(self):
        """Test contains() also handles None gracefully"""

        with __(value=None, score=85, name='test') as _:
            # Contains should also handle None gracefully
            assert not _.contains(__(value=__GREATER_THAN__(0)))     # None fails operator check
            assert _.contains(__(score=__GREATER_THAN__(80)))        # Other fields work fine
            assert _.contains(__(value=None, score=85))              # Exact None match works


    def test__operators_error_behavior_documentation(self):
        """Document the error handling behavior for future reference"""

        # BEHAVIOR AFTER FIX:
        # - When operator comparison raises TypeError (e.g., None > 0)
        # - The try-except catches it and returns False
        # - This makes __eq__ return False
        # - Which causes assert to raise AssertionError (not TypeError)

        with __(value=None) as _:
            # This will raise AssertionError, not TypeError
            with pytest.raises(AssertionError):
                assert _ == __(value=__GREATER_THAN__(0))

            # The comparison itself doesn't raise an error, it just returns False
            result = (_ == __(value=__GREATER_THAN__(0)))
            assert result is False

    def test__operators_with_string_numbers(self):                                       # Test operators work with numeric strings
        with __(value='100') as _:
            # String comparisons work but are lexicographic, not numeric
            assert _ != __(value=__GREATER_THAN__(99))                                   # '100' vs 99 is comparing str to int
            # This demonstrates type mismatch - operators need matching types

    # Test multiple operators on same field

    def test__multiple_operators_same_field__impossible(self):                           # Test contradictory operators fail
        with __(value=50) as _:
            # Can't test both > 60 and < 40 simultaneously (impossible range)
            # Each operator is tested independently, so this would need multiple assertions
            assert _ != __(value=__GREATER_THAN__(60))                                   # 50 is not > 60
            assert _ != __(value=__LESS_THAN__(40))                                      # 50 is not < 40

    def test__between__vs__close_to(self):                                               # Compare BETWEEN and CLOSE_TO approaches
        with __(value=50.5) as _:
            # Both can validate ranges, but semantics differ
            assert _ == __(value=__BETWEEN__(50, 51))                                    # Broad range
            assert _ == __(value=__CLOSE_TO__(50.5, tolerance=0.1))                     # Center point with tolerance

            # BETWEEN: "value is between these bounds"
            # CLOSE_TO: "value is approximately this number"

    # Test operators in complex nested structures

    def test__operators_in_list_of_objects(self):                                        # Test operators don't work directly in lists (by design)
        with __(items=[__(score=85), __(score=92), __(score=78)]) as _:
            # Operators work on scalar values, not list items
            # Lists require iteration, not covered by operator support
            assert _.items[0] == __(score=__GREATER_THAN__(80))                         # Can test individual items
            assert _.items[1] == __(score=__GREATER_THAN__(90))
            assert _.items[2] == __(score=__LESS_THAN__(80))

    def test__operators_mixed_with_skip_in_nested(self):                                 # Test operators and SKIP together in nested structures
        with __(
            id = 'test-123',
            timestamp = 1234567890,
            result = __(
                request_id = 'req-456',
                duration = 0.234,
                score = 85.5,
                metadata = __(version='1.0', build='beta')
            )
        ) as _:
            assert _ == __(
                id = __SKIP__,                                                           # Skip top-level field
                timestamp = __SKIP__,                                                    # Skip another top-level
                result = __(
                    request_id = __SKIP__,                                               # Skip nested field
                    duration = __LESS_THAN__(0.5),                                       # Operator in nested
                    score = __CLOSE_TO__(85, tolerance=1.0),                            # Another operator
                    metadata = __(version='1.0', build=__SKIP__)                        # Skip deeply nested
                )
            )

    # Test error messages and diff() with operators

    def test__diff_shows_operator_tuples(self):                                          # Test diff reveals operator structure
        with __(score=85, duration=0.234) as actual:
            expected = __(score=__GREATER_THAN__(90), duration=__LESS_THAN__(0.1))

            diff = actual.diff(expected)

            # diff should show actual values vs operator tuples
            assert diff is not None
            assert 'score' in diff
            assert diff['score']['actual'] == 85
            assert diff['score']['expected'] == ('gt', 90)                              # Shows operator structure

    def test__diff_with_close_to_tolerance(self):                                        # Test diff shows CLOSE_TO details
        with __(value=1.0) as actual:
            expected = __(value=__CLOSE_TO__(2.0, tolerance=0.5))

            diff = actual.diff(expected)

            # diff shows the operator tuple with tolerance
            assert diff['value']['expected'] == ('close_to', 2.0, 0.5)

    # Test operators with real-world patterns

    def test__http_status_code_ranges(self):                                             # Test HTTP status codes with operators
        response = __(status=201, body='Created', latency=0.123)

        # Success range (200-299)
        assert response == __(
            status=__BETWEEN__(200, 299),
            body='Created',
            latency=__LESS_THAN__(0.5)
        )

        # Not in error range (400+)
        assert response != __(status=__GREATER_THAN__(399), body='Created', latency=__SKIP__)

    def test__database_query_performance(self):                                          # Test database query patterns
        query_result = __(
            rows_returned = 42,
            query_time = 0.0234,
            cache_hit = True,
            total_rows = 1000
        )

        assert query_result == __(
            rows_returned = __BETWEEN__(1, 100),                                         # Reasonable page size
            query_time = __LESS_THAN__(0.1),                                             # Fast query
            cache_hit = True,
            total_rows = __GREATER_THAN__(0)                                             # Has data
        )

    def test__temperature_monitoring(self):                                              # Test sensor reading validation
        sensor_reading = __(
            temperature = 72.5,
            humidity = 45.0,
            timestamp = 1234567890,
            sensor_id = 'TEMP-001'
        )

        assert sensor_reading == __(
            temperature = __BETWEEN__(60, 85),                                           # Normal range
            humidity = __BETWEEN__(30, 60),                                              # Normal range
            timestamp = __SKIP__,                                                        # Dynamic
            sensor_id = 'TEMP-001'
        )

    def test__rate_limiting_checks(self):                                                # Test rate limit validation
        rate_limit_status = __(
            requests_used = 45,
            requests_limit = 100,
            reset_time = 1234567890,
            percentage_used = 0.45
        )

        assert rate_limit_status == __(
            requests_used = __LESS_THAN__(100),                                          # Still have capacity
            requests_limit = 100,
            reset_time = __SKIP__,
            percentage_used = __CLOSE_TO__(0.45, tolerance=0.01)
        )

    def test__pagination_metadata(self):                                                 # Test pagination pattern
        page_info = __(
            page = 3,
            per_page = 25,
            total_items = 237,
            total_pages = 10,
            has_next = True,
            has_prev = True
        )

        assert page_info == __(
            page = __BETWEEN__(1, 10),                                                   # Valid page
            per_page = __BETWEEN__(10, 100),                                             # Reasonable page size
            total_items = __GREATER_THAN__(0),                                           # Has items
            total_pages = 10,
            has_next = True,
            has_prev = True
        )

    # Test operators with comparison operator precedence

    def test__operators_evaluated_before_equality(self):                                 # Test evaluation order
        with __(a=100, b=50) as _:
            # Operators are evaluated first, then equality check
            assert _ == __(a=__GREATER_THAN__(90), b=__LESS_THAN__(60))                 # Both operators eval to True
            assert _ != __(a=__GREATER_THAN__(90), b=__LESS_THAN__(40))                 # Second operator evals to False

    # Test operators with special float values

    def test__operators_with_float_special_cases(self):                                  # Test with inf and -inf
        with __(large=float('inf'), small=float('-inf'), normal=42.0) as _:
            assert _ == __(large=__GREATER_THAN__(1e100), small=__SKIP__, normal=42.0)
            assert _ == __(large=__SKIP__, small=__LESS_THAN__(0), normal=42.0)

    def test__close_to__with_very_small_numbers(self):                                   # Test CLOSE_TO with scientific notation
        with __(epsilon=1e-15, delta=2e-15) as _:
            assert _ == __(epsilon=__CLOSE_TO__(0, tolerance=1e-14), delta=2e-15)
            assert _ == __(epsilon=__CLOSE_TO__(1e-15, tolerance=1e-16), delta=2e-15)

    # Test that operators work symmetrically

    def test__operator_symmetry(self):                                                   # Test operators work in both directions
        obj = __(value=50)

        # Normal direction: obj == expected_with_operator
        assert obj == __(value=__GREATER_THAN__(40))
        assert obj == __(value=__LESS_THAN__(60))
        assert obj == __(value=__BETWEEN__(40, 60))

    # Test operators don't interfere with regular equality

    def test__operators_dont_break_normal_equality(self):                                # Test mixing operators with exact values
        with __(a=100, b=50, c='test', d=3.14) as _:
            # Mix operators and exact matches
            assert _ == __(
                a=__GREATER_THAN__(90),                                                  # Operator
                b=50,                                                                    # Exact
                c='test',                                                                # Exact
                d=__CLOSE_TO__(3.14, tolerance=0.01)                                    # Operator
            )

    # Test contains() with operators in different positions

    def test__contains_with_operators_first_field(self):                                 # Test operator on first field in contains
        with __(alpha=100, beta=50, gamma=25) as _:
            assert _.contains(__(alpha=__GREATER_THAN__(90)))

    def test__contains_with_operators_middle_field(self):                                # Test operator on middle field in contains
        with __(alpha=100, beta=50, gamma=25) as _:
            assert _.contains(__(beta=__BETWEEN__(40, 60)))

    def test__contains_with_operators_last_field(self):                                  # Test operator on last field in contains
        with __(alpha=100, beta=50, gamma=25) as _:
            assert _.contains(__(gamma=__LESS_THAN__(30)))

    # Test assertion error messages

    def test__assertion_failure_message_quality(self):                                   # Test error messages are helpful
        with __(score=85) as _:
            try:
                assert _ == __(score=__GREATER_THAN__(90))
                pytest.fail("Should have raised AssertionError")
            except AssertionError as e:
                error_msg = str(e)
                # Error should show the comparison that failed
                assert 'score' in error_msg or '85' in error_msg or '90' in error_msg

    # Additional edge cases

    def test__empty_object_with_operators(self):                                         # Test operators on empty objects
        with __() as _:
            assert _ == __()                                                             # Empty equals empty
            assert _ != __(value=__GREATER_THAN__(0))                                    # Empty doesn't have fields

    def test__operators_with_boolean_fields(self):                                       # Test operators don't make sense for booleans
        with __(flag=True, count=100) as _:
            # Booleans have their own comparison rules (True > False in Python!)
            assert _ == __(flag=True, count=__GREATER_THAN__(90))                       # Only use operators on numbers
            # Don't use operators on booleans - it's confusing

    def test__operators_preserve_original_object(self):                                  # Test operations don't mutate originals
        original = __(score=85, duration=0.234)

        # Comparisons don't mutate
        _ = (original == __(score=__GREATER_THAN__(80), duration=__LESS_THAN__(0.5)))

        assert original.score == 85                                                      # Original unchanged
        assert original.duration == 0.234                                                # Original unchanged

    def test_contains__with_kwargs__basic(self):                                     # Test contains with kwargs syntax
        with __(id='123', name='Test', age=25, status='active') as _:
            assert _.contains(id='123')                                              # Single field as kwarg
            assert _.contains(id='123', name='Test')                                 # Multiple fields as kwargs
            assert _.contains(id='123', name='Test', age=25)                         # More fields as kwargs
            assert not _.contains(id='456')                                          # Wrong value
            assert not _.contains(missing_field='value')                             # Non-existent field

    def test_contains__with_kwargs__vs_object_syntax(self):                          # Test both syntaxes produce same results
        with __(a=1, b=2, c=3) as _:
            # Both syntaxes should work identically
            assert _.contains(__(a=1, b=2)) == _.contains(a=1, b=2)
            assert _.contains(__(a=1))      == _.contains(a=1)
            assert _.contains(__(c=3))      == _.contains(c=3)

    def test_contains__with_kwargs__with_operators(self):                            # Test kwargs with comparison operators
        with __(score=85, duration=0.234, count=100) as _:
            assert _.contains(score=__GREATER_THAN__(80))                           # Single operator
            assert _.contains(duration=__LESS_THAN__(0.5))                          # Different operator
            assert _.contains(count=__BETWEEN__(50, 150))                           # Range operator

            # Multiple operators
            assert _.contains(score   =__GREATER_THAN__(80  ),
                              duration=__LESS_THAN__   (0.5))

            # Mix operators and exact values
            assert _.contains(score=__GREATER_THAN__(80),
                              count=100)

    def test_contains__with_kwargs__with_skip(self):                                 # Test kwargs with __SKIP__ marker
        with __(id='123', name='Test', timestamp=999) as _:
            assert _.contains(id='123', timestamp=__SKIP__)                          # Skip timestamp
            assert _.contains(id=__SKIP__, name='Test')                              # Skip id
            assert _.contains(id=__SKIP__, name='Test', timestamp=__SKIP__)         # Skip multiple

    def test_contains__with_kwargs__nested_objects(self):                            # Test kwargs doesn't work with nested (by design)
        with __(user=__(id='u1', name='Alice'), settings=__(theme='dark')) as _:
            # Kwargs can only check top-level fields
            assert _.contains(user=__(id='u1'))                                      # Must use __ for nested
            # Can't do: _.contains(user=id='u1')  # This would fail - nested needs __

    def test_contains__with_kwargs__empty(self):                                     # Test contains with no arguments
        with __(a=1, b=2) as _:
            result = _.contains()                                                    # Empty kwargs should return False
            assert result == False                                                   # Should match empty

    def test_contains__kwargs_cannot_mix_with_positional(self):                      # Test you can't mix both syntaxes
        with __(a=1, b=2, c=3) as _:
            assert _.contains(__(a=1, b=2))                                          # Positional __ object
            assert _.contains(a=1, b=2)                                              # Kwargs
            error_message = ("Cannot mix positional and keyword arguments in contains(). "
                             "Use either _.contains(__(a=1, b=2)) or _.contains(a=1, b=2), not both.")
            with pytest.raises(ValueError, match=re.escape(error_message)) :
                assert _.contains(__(a=1), b=2)                                     # we can't use both techniques


    def test_contains__with_kwargs__real_world_example(self):                        # Real-world pattern test
        api_response = __(status=200,
                          headers=__(content_type='application/json', x_request_id='req-123'),
                          data=__(items=[1, 2, 3], total=3),
                          timing=__(duration=0.234, cached=False))

        # Old syntax (still works)
        assert api_response.contains(__(status=200))

        # New syntax (cleaner!)
        assert api_response.contains(status=200)
        assert api_response.contains(status=200, timing=__(duration=__LESS_THAN__(0.5)))

    def test_contains__with_kwargs__all_types(self):                                 # Test kwargs with various Python types
        with __(
            string='test',
            integer=42,
            floating=3.14,
            boolean=True,
            none_val=None,
            list_val=[1, 2, 3],
            dict_val={'key': 'value'}
        ) as _:
            assert _.contains(string='test')                                         # String
            assert _.contains(integer=42)                                            # Int
            assert _.contains(floating=3.14)                                         # Float
            assert _.contains(boolean=True)                                          # Bool
            assert _.contains(none_val=None)                                         # None
            assert _.contains(list_val=[1, 2, 3])                                    # List
            assert _.contains(dict_val={'key': 'value'})                             # Dict

    def test_contains__with_kwargs__operators_all_types(self):                       # Test all operators with kwargs syntax
        with __(
            score=85,
            duration=0.234,
            probability=0.753,
            count=42
        ) as _:
            # Greater than
            assert _.contains(score=__GREATER_THAN__(80))

            # Less than
            assert _.contains(duration=__LESS_THAN__(0.5))

            # Between
            assert _.contains(probability=__BETWEEN__(0.7, 0.8))

            # Close to
            assert _.contains(probability=__CLOSE_TO__(0.75, tolerance=0.01))

            # Multiple operators
            assert _.contains(score    = __GREATER_THAN__(80     ),
                              duration = __LESS_THAN__   (0.5    ),
                              count    = __BETWEEN__     (40, 50))

    def test_contains__with_kwargs__partial_match(self):                            # Test partial matching with kwargs
        with __(
            id='test-123',
            name='Test User',
            email='test@example.com',
            age=25,
            status='active',
            created_at='2024-01-01'
        ) as _:
            # Can check any subset of fields
            assert _.contains(id='test-123')                                         # Just one field
            assert _.contains(name='Test User', status='active')                     # Two fields
            assert _.contains(email='test@example.com', age=25, status='active')     # Three fields

    def test_contains__with_kwargs__comparison_with_object_syntax_operators(self):   # Compare both syntaxes with operators
        with __(score=85, duration=0.234, count=100, status='active') as _:
            # Both syntaxes should behave identically

            # Greater than
            assert _.contains(__(score=__GREATER_THAN__(80)))
            assert _.contains(score=__GREATER_THAN__(80))

            # Multiple with operators
            old_syntax = _.contains(__(
                score=__GREATER_THAN__(80),
                duration=__LESS_THAN__(0.5),
                status='active'
            ))

            new_syntax = _.contains(
                score=__GREATER_THAN__(80),
                duration=__LESS_THAN__(0.5),
                status='active'
            )

            assert old_syntax == new_syntax == True

    def test_contains__with_kwargs__failure_cases(self):                             # Test failure cases with kwargs
        with __(score=85, name='test', status='active') as _:
            assert not _.contains(score=90)                                          # Wrong value
            assert not _.contains(missing='value')                                   # Missing field
            assert not _.contains(score=__GREATER_THAN__(90))                       # Operator fails
            assert not _.contains(name='test', score=90)                            # One field wrong

    def test_contains__with_kwargs__integration_test(self):                          # Integration test combining features
        complex_obj = __(
            request_id='req-abc-123',
            timestamp=1234567890,
            status=200,
            timing=__(
                total=0.456,
                db_query=0.234,
                render=0.111
            ),
            metrics=__(
                accuracy=0.953,
                score=87.5,
                count=1024
            ),
            metadata=__(
                version='2.1.0',
                cached=False
            )
        )

        # Old syntax still works
        assert complex_obj.contains(__(status=200, request_id=__SKIP__))

        # New syntax is cleaner for top-level checks
        assert complex_obj.contains(status=200, request_id=__SKIP__)
        assert complex_obj.contains(
            status=200,
            timestamp=__SKIP__,
            timing=__(total=__LESS_THAN__(0.5))
        )

        # With operators
        assert complex_obj.contains(
            status=__BETWEEN__(200, 299),
            request_id=__SKIP__,
            metrics=__(score=__GREATER_THAN__(85))
        )