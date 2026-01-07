# ═══════════════════════════════════════════════════════════════════════════════
# test_Dict__Benchmark__Legend - Tests for benchmark legend collection
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title                import Safe_Str__Benchmark__Title
from osbot_utils.helpers.performance.benchmark.testing.QA__Benchmark__Test_Data                           import QA__Benchmark__Test_Data
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark__Legend                import Dict__Benchmark__Legend
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section              import Safe_Str__Benchmark__Section
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                                     import Type_Safe__Dict


class test_Dict__Benchmark__Legend(TestCase):

    @classmethod
    def setUpClass(cls):                                                         # Shared test data
        cls.test_data = QA__Benchmark__Test_Data()

    def test__init__(self):                                                      # Test initialization
        with Dict__Benchmark__Legend() as _:
            assert type(_) is Dict__Benchmark__Legend
            assert isinstance(_, Type_Safe__Dict)
            assert len(_)  == 0

    def test_type_constraints(self):                                             # Test type definitions
        assert Dict__Benchmark__Legend.expected_key_type   is Safe_Str__Benchmark__Section
        assert Dict__Benchmark__Legend.expected_value_type is Safe_Str__Benchmark__Title

    def test_add_item(self):                                                     # Test adding items
        legend = Dict__Benchmark__Legend()
        key    = Safe_Str__Benchmark__Section('A')
        value  = 'Python Baselines'

        legend[key] = value

        assert len(legend) == 1
        assert key in legend

    def test_get_item(self):                                                     # Test retrieving items
        legend = Dict__Benchmark__Legend()
        key    = Safe_Str__Benchmark__Section('A')
        value  = 'Python Baselines'

        legend[key] = value
        retrieved   = legend[key]

        assert retrieved   == value
        assert str(retrieved) == 'Python Baselines'

    def test_factory_method(self):                                               # Test using factory
        legend = self.test_data.create_legend()

        assert type(legend) is Dict__Benchmark__Legend
        assert len(legend)  == 2

    def test_iteration(self):                                                    # Test iterating over keys
        legend = self.test_data.create_legend()

        keys = list(legend.keys())
        assert len(keys) == 2

        for key in keys:
            assert type(key) is Safe_Str__Benchmark__Section

    def test_values(self):                                                       # Test accessing values
        legend = self.test_data.create_legend()

        values = list(legend.values())
        assert len(values) == 2

        for value in values:
            assert type(value) is Safe_Str__Benchmark__Title

    def test_items(self):                                                        # Test key-value pairs
        legend = self.test_data.create_legend()

        items = list(legend.items())
        assert len(items) == 2

        for key, value in items:
            assert type(key)   is Safe_Str__Benchmark__Section
            assert type(value) is Safe_Str__Benchmark__Title

    def test_contains(self):                                                     # Test membership check
        legend = self.test_data.create_legend()
        key    = Safe_Str__Benchmark__Section(self.test_data.section_a)

        assert key in legend

    def test_get_method(self):                                                   # Test .get() with default
        legend  = self.test_data.create_legend()
        key     = Safe_Str__Benchmark__Section(self.test_data.section_a)
        missing = Safe_Str__Benchmark__Section('Z')

        assert legend.get(key)                    is not None
        assert legend.get(missing)                is None
        assert legend.get(missing, 'X') == 'X'

    def test_section_descriptions(self):                                         # Test correct descriptions
        legend = self.test_data.create_legend()
        key_a  = Safe_Str__Benchmark__Section(self.test_data.section_a)
        key_b  = Safe_Str__Benchmark__Section(self.test_data.section_b)

        assert str(legend[key_a]) == 'Python Baselines'
        assert str(legend[key_b]) == 'Type_Safe Creation'
