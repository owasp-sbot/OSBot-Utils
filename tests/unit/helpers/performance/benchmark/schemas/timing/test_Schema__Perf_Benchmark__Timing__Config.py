# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Benchmark__Timing__Config - Tests for benchmark configuration
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description          import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title                import Safe_Str__Benchmark__Title
from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config      import Schema__Perf_Benchmark__Timing__Config
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark__Legend                import Dict__Benchmark__Legend
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Time_Unit                              import Enum__Time_Unit
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Name                         import Safe_Str__File__Name
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                         import Safe_Str__File__Path


class test_Schema__Perf_Benchmark__Timing__Config(TestCase):

    def test__init__(self):                                                      # Test initialization
        with Schema__Perf_Benchmark__Timing__Config() as _:
            assert type(_) is Schema__Perf_Benchmark__Timing__Config
            assert isinstance(_, Type_Safe)
            assert type(_.title)                 is Safe_Str__Benchmark__Title
            assert type(_.description)           is Safe_Str__Benchmark__Description
            assert type(_.output_path)           is Safe_Str__File__Path
            assert type(_.output_prefix)         is Safe_Str__File__Name
            assert type(_.legend)                is Dict__Benchmark__Legend
            assert _.time_unit                   == Enum__Time_Unit.NANOSECONDS
            assert _.print_to_console            is True
            assert _.auto_save_on_completion     is False

    def test__init____with_values(self):                                         # Test with explicit values
        with Schema__Perf_Benchmark__Timing__Config(title                   = 'Test Title'                ,
                                                    description             = 'Test Description'          ,
                                                    output_path             = '/tmp/benchmarks'           ,
                                                    output_prefix           = 'test_benchmark'            ,
                                                    time_unit               = Enum__Time_Unit.MICROSECONDS,
                                                    print_to_console        = False                       ,
                                                    auto_save_on_completion = True) as _:
            assert str(_.title)                  == 'Test Title'
            assert str(_.description)            == 'Test Description'
            assert str(_.output_path)            == '/tmp/benchmarks'
            assert str(_.output_prefix)          == 'test_benchmark'
            assert _.time_unit                   == Enum__Time_Unit.MICROSECONDS
            assert _.print_to_console            is False
            assert _.auto_save_on_completion     is True

    def test_default_time_unit(self):                                            # Test default time unit
        with Schema__Perf_Benchmark__Timing__Config() as _:
            assert _.time_unit       == Enum__Time_Unit.NANOSECONDS
            assert _.time_unit.value == 'ns'

    def test_all_time_units(self):                                               # Test all time units work
        for unit in Enum__Time_Unit:
            with Schema__Perf_Benchmark__Timing__Config(time_unit=unit) as _:
                assert _.time_unit == unit

    def test_legend_initialization(self):                                        # Test legend is empty dict
        with Schema__Perf_Benchmark__Timing__Config() as _:
            assert type(_.legend) is Dict__Benchmark__Legend
            assert len(_.legend)  == 0

    def test_legend_with_values(self):                                           # Test legend with values
        from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section import Safe_Str__Benchmark__Section

        legend = Dict__Benchmark__Legend()
        legend[Safe_Str__Benchmark__Section('A')] = 'Python'

        with Schema__Perf_Benchmark__Timing__Config(legend=legend) as _:
            assert len(_.legend) == 1

    def test_boolean_defaults(self):                                             # Test boolean defaults
        with Schema__Perf_Benchmark__Timing__Config() as _:
            assert _.print_to_console        is True                             # Default True
            assert _.auto_save_on_completion is False                            # Default False

    def test_json_serialization(self):                                           # Test JSON round-trip
        with Schema__Perf_Benchmark__Timing__Config(title       = 'Test',
                                                    output_path = '/tmp') as _:
            json_data = _.json()

            assert type(json_data)       is dict
            assert 'title'               in json_data
            assert 'output_path'         in json_data
            assert 'time_unit'           in json_data
            assert 'print_to_console'    in json_data
