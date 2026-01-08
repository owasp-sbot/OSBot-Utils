# ═══════════════════════════════════════════════════════════════════════════════
# test_Dict__Benchmark_Results - Tests for benchmark results collection
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                    import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results       import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result import Schema__Perf__Benchmark__Result
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id           import Safe_Str__Benchmark_Id
from osbot_utils.helpers.performance.benchmark.testing.QA__Benchmark__Test_Data                  import QA__Benchmark__Test_Data
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                            import Type_Safe__Dict


class test_Dict__Benchmark_Results(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.test_data = QA__Benchmark__Test_Data()

    def test__init__(self):                                                      # Test initialization
        with Dict__Benchmark_Results() as _:
            assert type(_) is Dict__Benchmark_Results
            assert isinstance(_, Type_Safe__Dict)
            assert len(_)  == 0

    def test_type_constraints(self):                                             # Test type definitions
        assert Dict__Benchmark_Results.expected_key_type   is Safe_Str__Benchmark_Id
        assert Dict__Benchmark_Results.expected_value_type is Schema__Perf__Benchmark__Result

    def test_add_item(self):                                                     # Test adding items
        results = Dict__Benchmark_Results()
        key     = Safe_Str__Benchmark_Id('A_01__test')
        value   = self.test_data.create_benchmark_result()

        results[key] = value

        assert len(results) == 1
        assert key in results

    def test_get_item(self):                                                     # Test retrieving items
        results = Dict__Benchmark_Results()
        key     = Safe_Str__Benchmark_Id('A_01__test')
        value   = self.test_data.create_benchmark_result()

        results[key] = value
        retrieved    = results[key]

        assert retrieved is value
        assert type(retrieved) is Schema__Perf__Benchmark__Result

    def test_factory_method(self):                                               # Test using factory
        results = self.test_data.create_results_dict(count=3)

        assert type(results)  is Dict__Benchmark_Results
        assert len(results)   == 3

    def test_iteration(self):                                                    # Test iterating over keys
        results = self.test_data.create_results_dict(count=2)

        keys = list(results.keys())
        assert len(keys) == 2

        for key in keys:
            assert type(key) is Safe_Str__Benchmark_Id

    def test_values(self):                                                       # Test accessing values
        results = self.test_data.create_results_dict(count=2)

        values = list(results.values())
        assert len(values) == 2

        for value in values:
            assert type(value) is Schema__Perf__Benchmark__Result

    def test_items(self):                                                        # Test key-value pairs
        results = self.test_data.create_results_dict(count=2)

        items = list(results.items())
        assert len(items) == 2

        for key, value in items:
            assert type(key)   is Safe_Str__Benchmark_Id
            assert type(value) is Schema__Perf__Benchmark__Result

    def test_contains(self):                                                     # Test membership check
        results = self.test_data.create_results_dict(count=1)
        key     = Safe_Str__Benchmark_Id(self.test_data.benchmark_id_1)

        assert key in results

    def test_get_method(self):                                                   # Test .get() with default
        results = self.test_data.create_results_dict(count=1)
        key     = Safe_Str__Benchmark_Id(self.test_data.benchmark_id_1)
        missing = Safe_Str__Benchmark_Id('missing')

        assert results.get(key)            is not None
        assert results.get(missing)        is None
        assert results.get(missing, 'def') == 'def'

    def test_delete_item(self):                                                  # Test removing items
        results = self.test_data.create_results_dict(count=2)
        key     = Safe_Str__Benchmark_Id(self.test_data.benchmark_id_1)

        assert len(results) == 2
        del results[key]
        assert len(results) == 1
        assert key not in results

    def test_sorted_keys(self):                                                  # Test sorting by key
        results     = self.test_data.create_results_dict(count=3)
        sorted_keys = sorted(results.keys())

        assert len(sorted_keys) == 3
        assert str(sorted_keys[0]) == self.test_data.benchmark_id_1              # A_01 first
        assert str(sorted_keys[1]) == self.test_data.benchmark_id_2              # A_02 second
        assert str(sorted_keys[2]) == self.test_data.benchmark_id_3              # B_01 third
