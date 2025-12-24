"""Tests for @timestamp_args dynamic name interpolation"""

from unittest                                                                         import TestCase
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                        import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector__Analysis              import Timestamp_Collector__Analysis
from osbot_utils.helpers.timestamp_capture.decorators.timestamp_args                  import timestamp_args


class test_timestamp_args(TestCase):

    def test_timestamp_args__single_arg(self):                                        # Test interpolation of single argument
        @timestamp_args(name="process.{item_type}")
        def process(item_type: str):
            return f"processed {item_type}"

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            process("json")
            process("xml")
            process("csv")

        names = [e.name for e in _timestamp_collector_.entries if e.event == 'enter']
        assert names == ['process.json', 'process.xml', 'process.csv']

    def test_timestamp_args__multiple_args(self):                                     # Test interpolation of multiple arguments
        @timestamp_args(name="handler.{method}.{path}")
        def handle_request(method: str, path: str):
            return f"{method} {path}"

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            handle_request("GET", "/api/users")
            handle_request("POST", "/api/items")

        names = [e.name for e in _timestamp_collector_.entries if e.event == 'enter']
        assert names == ['handler.GET./api/users', 'handler.POST./api/items']

    def test_timestamp_args__with_self(self):                                         # Test on instance methods (self is ignored)
        class MyService:
            @timestamp_args(name="service.{operation}")
            def execute(self, operation: str):
                return operation

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            service = MyService()
            service.execute("create")
            service.execute("update")
            service.execute("delete")

        names = [e.name for e in _timestamp_collector_.entries if e.event == 'enter']
        assert names == ['service.create', 'service.update', 'service.delete']

    def test_timestamp_args__kwargs(self):                                            # Test with keyword arguments
        @timestamp_args(name="query.{table}")
        def query(table: str, limit: int = 100):
            return f"SELECT * FROM {table} LIMIT {limit}"

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            query(table="users")
            query("orders", limit=50)

        names = [e.name for e in _timestamp_collector_.entries if e.event == 'enter']
        assert names == ['query.users', 'query.orders']

    def test_timestamp_args__aggregation(self):                                       # Test that dynamic names aggregate correctly
        @timestamp_args(name="op.{name}")
        def operation(name: str):
            pass

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            operation("alpha")
            operation("beta")
            operation("alpha")                                                        # Called twice
            operation("alpha")                                                        # Called three times

        analysis = Timestamp_Collector__Analysis(collector=_timestamp_collector_)
        timings  = analysis.get_method_timings()

        assert 'op.alpha' in timings
        assert 'op.beta'  in timings
        assert timings['op.alpha'].call_count == 3
        assert timings['op.beta'].call_count  == 1

    def test_timestamp_args__with_parens_style(self):                                 # Test function-call style naming
        @timestamp_args(name="link_component({name})")
        def link_component(name: str, root_id: int):
            return f"linked {name}"

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            link_component("head", 1)
            link_component("body", 2)
            link_component("attrs", 3)

        names = [e.name for e in _timestamp_collector_.entries if e.event == 'enter']
        assert names == ['link_component(head)', 'link_component(body)', 'link_component(attrs)']

    def test_timestamp_args__fallback_on_missing_key(self):                           # Test graceful fallback if key missing
        @timestamp_args(name="process.{missing_arg}")
        def process(actual_arg: str):
            return actual_arg

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            process("test")

        # Should fall back to the raw template string
        names = [e.name for e in _timestamp_collector_.entries if e.event == 'enter']
        assert names == ['process.{missing_arg}']

    def test_timestamp_args__numeric_arg(self):                                       # Test with numeric arguments
        @timestamp_args(name="batch.{batch_id}.process")
        def process_batch(batch_id: int, items: list):
            return len(items)

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            process_batch(1, [1, 2, 3])
            process_batch(2, [4, 5])
            process_batch(100, [6])

        names = [e.name for e in _timestamp_collector_.entries if e.event == 'enter']
        assert names == ['batch.1.process', 'batch.2.process', 'batch.100.process']

    def test_timestamp_args__no_collector(self):                                      # Test dynamic names work without collector
        @timestamp_args(name="process.{item}")
        def process(item: str):
            return item.upper()

        # No collector - should just execute normally
        result = process("test")
        assert result == "TEST"

    def test_timestamp_args__requires_name(self):                                     # Test that name parameter is required
        with self.assertRaises(TypeError):
            @timestamp_args                                                           # Missing name parameter
            def my_func():
                pass

    def test_timestamp_args__requires_placeholder(self):                              # Test that name must have placeholders
        with self.assertRaises(ValueError) as context:
            @timestamp_args(name="static.name")                                       # No {placeholder}
            def my_func():
                pass

        assert "placeholders" in str(context.exception).lower()

    def test_timestamp_args__empty_name_raises(self):                                 # Test that empty name raises
        with self.assertRaises(ValueError):
            @timestamp_args(name="")
            def my_func():
                pass

    def test_timestamp_args__preserves_function_metadata(self):                       # Test functools.wraps preserves metadata
        @timestamp_args(name="test.{x}")
        def documented_function(x: int) -> str:
            """This is the docstring."""
            return str(x)

        assert documented_function.__name__ == 'documented_function'
        assert documented_function.__doc__  == "This is the docstring."

    def test_timestamp_args__preserves_return_value(self):                            # Test return value is passed through
        @timestamp_args(name="calc.{op}")
        def calculate(op: str, a: int, b: int):
            if op == "add":
                return a + b
            return a - b

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            result1 = calculate("add", 10, 5)
            result2 = calculate("sub", 10, 5)

        assert result1 == 15
        assert result2 == 5

    def test_timestamp_args__exception_handling(self):                                # Test exceptions propagate correctly
        @timestamp_args(name="fail.{mode}")
        def may_fail(mode: str):
            if mode == "error":
                raise ValueError("Expected error")
            return "ok"

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            result = may_fail("safe")
            assert result == "ok"

            with self.assertRaises(ValueError):
                may_fail("error")

        # Both enter and exit should be recorded even for failed call
        names = [e.name for e in _timestamp_collector_.entries]
        assert 'fail.safe'  in names
        assert 'fail.error' in names
        assert len(_timestamp_collector_.entries) == 4                                # 2 calls × (enter + exit)

    def test_timestamp_args__keyword_only_args(self):                                 # Test keyword-only arguments (after *)
        @timestamp_args(name="config.{env}.{region}")
        def configure(*, env: str, region: str = "us-east-1"):
            return f"{env}-{region}"

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            configure(env="prod")
            configure(env="staging", region="eu-west-1")

        names = [e.name for e in _timestamp_collector_.entries if e.event == 'enter']
        assert names == ['config.prod.us-east-1', 'config.staging.eu-west-1']

    def test_timestamp_args__all_defaults(self):                                      # Test function with all default values
        @timestamp_args(name="settings.{mode}.{level}")
        def apply_settings(mode: str = "auto", level: int = 5):
            return f"{mode}:{level}"

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            apply_settings()                                                          # All defaults
            apply_settings(mode="manual")                                             # Partial override
            apply_settings(level=10)                                                  # Different partial
            apply_settings(mode="custom", level=99)                                   # All overridden

        names = [e.name for e in _timestamp_collector_.entries if e.event == 'enter']
        assert names == [
            'settings.auto.5',
            'settings.manual.5',
            'settings.auto.10',
            'settings.custom.99'
        ]

    def test_timestamp_args__mixed_positional_and_kwargs(self):                       # Test mix of positional and keyword-only
        @timestamp_args(name="request.{method}.{endpoint}")
        def make_request(method: str, endpoint: str, *, timeout: int = 30):
            return f"{method} {endpoint} ({timeout}s)"

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            make_request("GET", "/users")
            make_request("POST", "/items", timeout=60)

        names = [e.name for e in _timestamp_collector_.entries if e.event == 'enter']
        assert names == ['request.GET./users', 'request.POST./items']

    def test_timestamp_args__kwargs_in_name(self):                                    # Test using keyword-only arg in name template
        @timestamp_args(name="cache.{strategy}")
        def cache_data(data: dict, *, strategy: str = "lru"):
            return data

        _timestamp_collector_ = Timestamp_Collector()

        with _timestamp_collector_:
            cache_data({"a": 1})                                                      # Default strategy
            cache_data({"b": 2}, strategy="fifo")

        names = [e.name for e in _timestamp_collector_.entries if e.event == 'enter']
        assert names == ['cache.lru', 'cache.fifo']