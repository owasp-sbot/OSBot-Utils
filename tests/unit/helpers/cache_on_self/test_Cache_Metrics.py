from unittest                                           import TestCase
from osbot_utils.helpers.cache_on_self.Cache_Metrics   import Cache_Metrics


class test_Cache_Metrics(TestCase):

    def setUp(self):
        self.metrics = Cache_Metrics()

    def test__init__(self):
        assert type(self.metrics) is Cache_Metrics
        assert self.metrics.hits                    == 0
        assert self.metrics.misses                  == 0
        assert self.metrics.reloads                 == 0
        assert self.metrics.key_generation_time     == 0.0
        assert self.metrics.cache_lookup_time       == 0.0
        assert self.metrics.function_execution_time == 0.0

    def test_hit_rate__no_calls(self):
        # When no hits or misses, hit rate should be 0
        assert self.metrics.hit_rate == 0.0

    def test_hit_rate__with_data(self):
        self.metrics.hits = 10
        self.metrics.misses = 5

        expected_rate = 10 / (10 + 5)
        assert self.metrics.hit_rate == expected_rate
        assert self.metrics.hit_rate == 2/3

        # Test 100% hit rate
        self.metrics.hits = 100
        self.metrics.misses = 0
        assert self.metrics.hit_rate == 1.0

        # Test 0% hit rate
        self.metrics.hits = 0
        self.metrics.misses = 50
        assert self.metrics.hit_rate == 0.0

        # Test 50% hit rate
        self.metrics.hits = 25
        self.metrics.misses = 25
        assert self.metrics.hit_rate == 0.5

    def test_record_hit(self):
        assert self.metrics.hits == 0

        self.metrics.record_hit()
        assert self.metrics.hits == 1

        self.metrics.record_hit()
        self.metrics.record_hit()
        assert self.metrics.hits == 3

    def test_record_miss(self):
        assert self.metrics.misses == 0

        self.metrics.record_miss()
        assert self.metrics.misses == 1

        self.metrics.record_miss()
        self.metrics.record_miss()
        assert self.metrics.misses == 3

    def test_record_reload(self):
        assert self.metrics.reloads == 0

        self.metrics.record_reload()
        assert self.metrics.reloads == 1

        self.metrics.record_reload()
        self.metrics.record_reload()
        assert self.metrics.reloads == 3

    def test_reset(self):
        # Set some values
        self.metrics.hits = 10
        self.metrics.misses = 5
        self.metrics.reloads = 3
        self.metrics.key_generation_time = 1.23
        self.metrics.cache_lookup_time = 0.45
        self.metrics.function_execution_time = 2.34

        # Reset
        self.metrics.reset()

        # Verify all values are reset
        assert self.metrics.hits                    == 0
        assert self.metrics.misses                  == 0
        assert self.metrics.reloads                 == 0
        assert self.metrics.key_generation_time     == 0.0
        assert self.metrics.cache_lookup_time       == 0.0
        assert self.metrics.function_execution_time == 0.0
        assert self.metrics.hit_rate                == 0.0

    def test__timing_attributes(self):
        # Test that timing attributes can be set and retrieved
        self.metrics.key_generation_time = 0.001
        self.metrics.cache_lookup_time = 0.0005
        self.metrics.function_execution_time = 0.1

        assert self.metrics.key_generation_time     == 0.001
        assert self.metrics.cache_lookup_time       == 0.0005
        assert self.metrics.function_execution_time == 0.1

    def test__comprehensive_metrics_scenario(self):
        # Simulate a realistic caching scenario

        # 10 cache misses (initial calls)
        for _ in range(10):
            self.metrics.record_miss()

        # 40 cache hits (repeated calls)
        for _ in range(40):
            self.metrics.record_hit()

        # 5 reloads (forced refreshes)
        for _ in range(5):
            self.metrics.record_reload()

        # Verify metrics
        assert self.metrics.hits    == 40
        assert self.metrics.misses  == 10
        assert self.metrics.reloads == 5
        assert self.metrics.hit_rate == 0.8  # 40 / (40 + 10)

        # Add timing data
        self.metrics.key_generation_time = 0.05      # Total time spent generating keys
        self.metrics.cache_lookup_time = 0.02        # Total time spent on lookups
        self.metrics.function_execution_time = 1.5   # Total time executing functions

        # Calculate some derived metrics
        total_calls = self.metrics.hits + self.metrics.misses
        avg_key_gen_time = self.metrics.key_generation_time / total_calls
        avg_lookup_time = self.metrics.cache_lookup_time / total_calls

        assert total_calls == 50
        assert avg_key_gen_time == 0.001   # 0.05 / 50
        assert avg_lookup_time == 0.0004   # 0.02 / 50