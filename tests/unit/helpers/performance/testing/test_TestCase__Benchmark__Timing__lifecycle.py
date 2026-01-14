from unittest                                                                                        import TestCase
from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                                import Perf_Benchmark__Timing
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.helpers.performance.benchmark.testing.TestCase__Benchmark__Timing                   import TestCase__Benchmark__Timing
from osbot_utils.testing.Stdout import Stdout


class test_TestCase__Benchmark__Timing__lifecycle(TestCase):
    """Test lifecycle methods independently"""

    def test_setUpClass_creates_default_config(self):                            # Test default config
        # Create a test class without config
        class TestWithoutConfig(TestCase__Benchmark__Timing):
            pass
        TestWithoutConfig.setUpClass()

        assert TestWithoutConfig.config is not None
        assert TestWithoutConfig.timing is not None
        assert type(TestWithoutConfig.timing) is Perf_Benchmark__Timing
        with Stdout() as stdout:
            TestWithoutConfig.tearDownClass()
        assert stdout.value() == ('\n'
                                  '┌──────────────────────────────┐\n'
                                  '│ ID │ Benchmark │ Score │ Raw │\n'
                                  '├──────────────────────────────┤\n'
                                  '├──────────────────────────────┤\n'
                                  '│ Total: 0 benchmarks          │\n'
                                  '└──────────────────────────────┘\n')

    def test_setUpClass_uses_provided_config(self):                              # Test provided config
        class TestWithConfig(TestCase__Benchmark__Timing):
            config = Schema__Perf_Benchmark__Timing__Config(title            = 'Custom',
                                                            print_to_console = False)

        TestWithConfig.setUpClass()

        assert str(TestWithConfig.config.title) == 'Custom'
        assert TestWithConfig.timing is not None

        TestWithConfig.tearDownClass()

    def test_tearDownClass_calls_stop(self):                                     # Test tearDown calls stop
        class TestTearDown(TestCase__Benchmark__Timing):
            config = Schema__Perf_Benchmark__Timing__Config(print_to_console = False)

        TestTearDown.setUpClass()
        TestTearDown.tearDownClass()

        # After tearDown, timing should still exist but stop() was called
        assert TestTearDown.timing is not None
