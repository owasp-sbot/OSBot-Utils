import time
from unittest                                                                      import TestCase

from osbot_fast_api_serverless.utils.testing.skip_tests import skip__if_not__in_github_actions

from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                     import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.decorators.timestamp                    import timestamp
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe


class test_timestamp(TestCase):

    def test_timestamp__no_collector(self):                                        # Test decorator works without collector
        @timestamp
        def simple_function():
            return 42

        result = simple_function()
        assert result == 42                                                        # Function executes normally

    def test_timestamp__with_collector(self):                                      # Test decorator records with collector
        @timestamp
        def tracked_function():
            return 'result'

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            result = tracked_function()

        assert result                            == 'result'
        assert _timestamp_collector_.entry_count() == 2                            # enter + exit
        assert _timestamp_collector_.entries[0].name  == 'test_timestamp.test_timestamp__with_collector.<locals>.tracked_function'
        assert _timestamp_collector_.entries[0].event == 'enter'
        assert _timestamp_collector_.entries[1].event == 'exit'

    def test_timestamp__custom_name(self):                                         # Test decorator with custom name
        @timestamp(name='custom.method.name')
        def named_function():
            return True

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            named_function()

        assert _timestamp_collector_.entries[0].name == 'custom.method.name'

    def test_timestamp__preserves_function_metadata(self):                         # Test decorator preserves __name__ etc
        @timestamp
        def documented_function():
            """This is the docstring."""
            pass

        assert documented_function.__name__ == 'documented_function'
        assert documented_function.__doc__  == 'This is the docstring.'

    def test_timestamp__with_arguments(self):                                      # Test decorator with function arguments
        @timestamp
        def func_with_args(a, b, c=None):
            return a + b + (c or 0)

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            result = func_with_args(1, 2, c=3)

        assert result == 6
        assert _timestamp_collector_.entry_count() == 2

    def test_timestamp__with_return_value(self):                                   # Test decorator preserves return value
        @timestamp
        def returns_dict():
            return {'key': 'value', 'count': 42}

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            result = returns_dict()

        assert result == {'key': 'value', 'count': 42}

    def test_timestamp__with_exception(self):                                      # Test decorator handles exceptions correctly
        @timestamp
        def raises_error():
            raise ValueError('test error')

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            try:
                raises_error()
            except ValueError:
                pass

        assert _timestamp_collector_.entry_count() == 2                            # Still records enter and exit
        assert _timestamp_collector_.entries[0].event == 'enter'
        assert _timestamp_collector_.entries[1].event == 'exit'

    def test_timestamp__nested_decorated_functions(self):                          # Test nested decorated functions
        @timestamp
        def outer():
            return inner()

        @timestamp
        def inner():
            return 'inner result'

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            result = outer()

        assert result                            == 'inner result'
        assert _timestamp_collector_.entry_count() == 4                            # 2 enters + 2 exits
        assert _timestamp_collector_.entries[0].event == 'enter'                   # outer enter
        assert _timestamp_collector_.entries[1].event == 'enter'                   # inner enter
        assert _timestamp_collector_.entries[2].event == 'exit'                    # inner exit
        assert _timestamp_collector_.entries[3].event == 'exit'                    # outer exit

    def test_timestamp__on_method(self):                                           # Test decorator on class method
        class MyClass(Type_Safe):
            @timestamp
            def my_method(self, value):
                return value * 2

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            obj = MyClass()
            result = obj.my_method(21)

        assert result == 42
        assert _timestamp_collector_.entry_count() == 2
        assert 'MyClass.my_method' in _timestamp_collector_.entries[0].name

    def test_timestamp__multiple_calls(self):                                      # Test multiple calls are all recorded
        @timestamp
        def repeated():
            pass

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            for _ in range(5):
                repeated()

        assert _timestamp_collector_.entry_count()  == 10                          # 5 * (enter + exit)
        assert _timestamp_collector_.method_count() == 1                           # Still just one unique method

    def test_timestamp__timing_accuracy(self):                                     # Test timing is reasonably accurate
        skip__if_not__in_github_actions()
        @timestamp
        def sleep_function():
            time.sleep(0.01)                                                       # 10ms

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            sleep_function()

        enter_entry = _timestamp_collector_.entries[0]
        exit_entry  = _timestamp_collector_.entries[1]
        duration_ns = exit_entry.timestamp_ns - enter_entry.timestamp_ns

        assert duration_ns >= 10_000_000                                           # At least 10ms
        assert duration_ns <  50_000_000                                           # Less than 50ms (reasonable overhead)