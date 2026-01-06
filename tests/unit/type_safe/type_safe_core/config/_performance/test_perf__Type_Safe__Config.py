# ═══════════════════════════════════════════════════════════════════════════════
# Performance Baselines for Type_Safe__Config
# Captures baseline measurements for config creation and stack discovery
# ═══════════════════════════════════════════════════════════════════════════════
#
# LEGEND:
#   A = Python Baselines (raw Python operations for reference)
#   B = Type_Safe__Config Creation & Operations
#   C = find_type_safe_config Stack Discovery
#   D = Type_Safe Object Creation (various complexity levels)
#   E = Python @dataclass Object Creation (for comparison)
#   F = Pydantic BaseModel Object Creation (for comparison)
#
# ═══════════════════════════════════════════════════════════════════════════════

import json
from dataclasses                                                                              import dataclass, field
from typing                                                                                   import List, Dict
from unittest                                                                                 import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Str                                           import Safe_Str
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                             import Safe_Id
from osbot_utils.utils.Files                                                                  import path_combine
from osbot_utils.testing.performance.Performance_Measure__Session                             import Perf
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import Type_Safe__Config
from osbot_utils.type_safe.type_safe_core.config.static_methods.find_type_safe_config         import find_type_safe_config


# ═══════════════════════════════════════════════════════════════════════════════
# Reference Classes for Python Baselines (Section A)
# ═══════════════════════════════════════════════════════════════════════════════

class Empty_Class:                                                                            # Plain Python class with no attributes
    pass

class Class_With_Init:                                                                        # Plain Python class with __init__
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3

class Class_With_Slots:                                                                       # Python class with __slots__
    __slots__ = ('a', 'b', 'c')
    def __init__(self):
        self.a = 1
        self.b = 2
        self.c = 3


def empty_function():                                                                         # Empty function for invocation baseline
    pass


# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe Test Classes (Section D)
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Empty(Type_Safe):                                                                   # Empty Type_Safe class
    pass

class TS__With_Primitives(Type_Safe):                                                         # Type_Safe with Python primitives
    name   : str  = ''
    count  : int  = 0
    active : bool = False

class TS__With_Safe_Types(Type_Safe):                                                         # Type_Safe with type-safe primitives
    id     : Safe_Id
    name   : Safe_Str
    label  : Safe_Str

class TS__Inner(Type_Safe):                                                                   # Inner class for nesting tests
    value : str = ''

class TS__With_Nested(Type_Safe):                                                             # Type_Safe with nested Type_Safe
    inner  : TS__Inner
    name   : str = ''

class TS__With_Python_Collections(Type_Safe):                                                 # Type_Safe with Python collections
    items : list
    data  : dict

class TS__With_TypeSafe_Collections(Type_Safe):                                               # Type_Safe with Type_Safe collections
    items : List[str]
    data  : Dict[str, str]


# ═══════════════════════════════════════════════════════════════════════════════
# @dataclass Test Classes (Section E)
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class DC__Empty:                                                                              # Empty dataclass
    pass

@dataclass
class DC__With_Primitives:                                                                    # Dataclass with Python primitives
    name   : str  = ''
    count  : int  = 0
    active : bool = False

@dataclass
class DC__Inner:                                                                              # Inner dataclass for nesting tests
    value : str = ''

@dataclass
class DC__With_Nested:                                                                        # Dataclass with nested dataclass
    inner  : DC__Inner = field(default_factory=DC__Inner)
    name   : str       = ''

@dataclass
class DC__With_Collections:                                                                   # Dataclass with Python collections
    items : List[str]       = field(default_factory=list)
    data  : Dict[str, int]  = field(default_factory=dict)




# check if we have pydantic available
try:
    # ═══════════════════════════════════════════════════════════════════════════════
    # Pydantic BaseModel Test Classes (Section F)
    # ═══════════════════════════════════════════════════════════════════════════════
    from pydantic import BaseModel
    HAS_PYDANTIC = True
except:
    BaseModel = None
    HAS_PYDANTIC = False


if HAS_PYDANTIC:
    class PD__Empty(BaseModel):                                                                   # Empty Pydantic model
        pass

    class PD__With_Primitives(BaseModel):                                                         # Pydantic with Python primitives
        name   : str  = ''
        count  : int  = 0
        active : bool = False

    class PD__Inner(BaseModel):                                                                   # Inner Pydantic model for nesting tests
        value : str = ''

    class PD__With_Nested(BaseModel):                                                             # Pydantic with nested model
        inner  : PD__Inner = PD__Inner()
        name   : str       = ''

    class PD__With_Collections(BaseModel):                                                        # Pydantic with Python collections
        items : List[str]       = []
        data  : Dict[str, int]  = {}


class test_perf__Type_Safe__Config(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.session = Perf(assert_enabled=True)
        cls.results = {}                                                                      # Collect all results

        # Time thresholds (in nanoseconds)
        cls.time_100_ns  =     100                                                            # Sub-microsecond
        cls.time_500_ns  =     500                                                            # Half microsecond
        cls.time_1_kns   =   1_000                                                            # 1 microsecond
        cls.time_2_kns   =   2_000                                                            # 2 microseconds
        cls.time_5_kns   =   5_000                                                            # 5 microseconds
        cls.time_10_kns  =  10_000                                                            # 10 microseconds
        cls.time_20_kns  =  20_000                                                            # 20 microseconds
        cls.time_50_kns  =  50_000                                                            # 50 microseconds

    @classmethod
    def tearDownClass(cls):
        output_text = cls.build_results_text()
        print(output_text)

        target_json = path_combine(__file__, '../type-safe__config-stats/test_perf__Type_Safe__Config.json')
        target_txt  = path_combine(__file__, '../type-safe__config-stats/test_perf__Type_Safe__Config.txt')

        cls.save_results_json(target_json)
        cls.save_results_txt(target_txt, output_text)

    def setUp(self):
        if self._testMethodName.startswith("test_perf__F_") and not HAS_PYDANTIC:           # add this check here so that need to add a check to all tests
            self.skipTest("pydantic not installed")

    @classmethod
    def build_results_text(cls) -> str:                                                       # Build results as string, sorted by ID
        lines = []
        lines.append("")
        lines.append("═" * 100)
        lines.append(" Type_Safe__Config Performance Baselines - values in nanoseconds (ns)")
        lines.append("─" * 100)
        lines.append(" LEGEND: A=Python | B=Config | C=Stack Discovery | D=Type_Safe | E=@dataclass | F=Pydantic")
        lines.append("═" * 100)

        if cls.results:
            sorted_results = sorted(cls.results.items(), key=lambda x: x[0])                  # Sort by ID alphabetically
            max_name_len   = max(len(name) for name, _ in sorted_results)

            current_section = None
            for name, data in sorted_results:
                section = name[0] if name else '?'                                            # Get section letter
                if section != current_section:
                    current_section = section
                    lines.append("─" * 100)

                score = data['final_score']
                raw   = data['raw_score']
                lines.append(f"  {name:<{max_name_len}} | score: {score:>10,} ns | raw: {raw:>10,} ns")

        lines.append("═" * 100)
        lines.append(f" Total tests: {len(cls.results)}")
        lines.append("═" * 100)
        lines.append("")

        return "\n".join(lines)

    @classmethod
    def save_results_json(cls, filepath: str):                                                # Save results to JSON
        sorted_results = dict(sorted(cls.results.items(), key=lambda x: x[0]))                # Sort by ID
        output = {'test_class' : 'test_perf__Type_Safe__Config'    ,
                  'results'    : sorted_results                    ,
                  'thresholds' : {'time_100_ns' : cls.time_100_ns  ,
                                  'time_500_ns' : cls.time_500_ns  ,
                                  'time_1_kns'  : cls.time_1_kns   ,
                                  'time_2_kns'  : cls.time_2_kns   ,
                                  'time_5_kns'  : cls.time_5_kns   ,
                                  'time_10_kns' : cls.time_10_kns  ,
                                  'time_20_kns' : cls.time_20_kns  ,
                                  'time_50_kns' : cls.time_50_kns  }}

        with open(filepath, 'w') as f:
            json.dump(output, f, indent=2)

        print(f"Results saved to: {filepath}")

    @classmethod
    def save_results_txt(cls, filepath: str, output_text: str):                               # Save results to TXT
        with open(filepath, 'w') as f:
            f.write(output_text)

        print(f"Results saved to: {filepath}")

    def capture_result(self, name: str, result):                                              # Capture measurement result
        self.results[name] = {'final_score' : int(result.final_score)                    ,
                              'raw_score'   : int(result.raw_score  )                    ,
                              'name'        : result.name                                }
        return result

    # ═══════════════════════════════════════════════════════════════════════════
    # Section A: Python Baselines
    # ═══════════════════════════════════════════════════════════════════════════

    def test_perf__A_01__python__nop(self):                                                   # Baseline: no operation
        def nop():
            pass

        with self.session as _:
            _.measure__quick(nop)
            self.capture_result('A_01__python__nop', _.result)

    def test_perf__A_02__python__var_assignment(self):                                        # Baseline: variable assignment
        def var_assignment():
            x = 42
            return x

        with self.session as _:
            _.measure__quick(var_assignment)
            self.capture_result('A_02__python__var_assignment', _.result)

    def test_perf__A_03__python__function_invocation(self):                                   # Baseline: calling empty function
        def invoke_empty():
            empty_function()

        with self.session as _:
            _.measure__quick(invoke_empty)
            self.capture_result('A_03__python__function_invocation', _.result)

    def test_perf__A_04__python__function_invocation_x10(self):                               # Baseline: calling empty function 10x
        def invoke_empty_x10():
            for _ in range(10):
                empty_function()

        with self.session as _:
            _.measure__quick(invoke_empty_x10)
            self.capture_result('A_04__python__function_invocation_x10', _.result)

    def test_perf__A_05__python__class_empty(self):                                           # Baseline: empty class creation
        def create_empty_class():
            return Empty_Class()

        with self.session as _:
            _.measure__quick(create_empty_class)
            self.capture_result('A_05__python__class_empty', _.result)

    def test_perf__A_06__python__class_with_init(self):                                       # Baseline: class with __init__
        def create_class_with_init():
            return Class_With_Init()

        with self.session as _:
            _.measure__quick(create_class_with_init)
            self.capture_result('A_06__python__class_with_init', _.result)

    def test_perf__A_07__python__class_with_slots(self):                                      # Baseline: class with __slots__
        def create_class_with_slots():
            return Class_With_Slots()

        with self.session as _:
            _.measure__quick(create_class_with_slots)
            self.capture_result('A_07__python__class_with_slots', _.result)

    def test_perf__A_08__python__class_with_init_x10(self):                                   # Baseline: class creation 10x
        def create_class_x10():
            for _ in range(10):
                Class_With_Init()

        with self.session as _:
            _.measure__quick(create_class_x10)
            self.capture_result('A_08__python__class_with_init_x10', _.result)

    def test_perf__A_09__python__class_with_init_x100(self):                                  # Baseline: class creation 100x
        def create_class_x100():
            for _ in range(100):
                Class_With_Init()

        with self.session as _:
            _.measure__quick(create_class_x100)
            self.capture_result('A_09__python__class_with_init_x100', _.result)

    # ═══════════════════════════════════════════════════════════════════════════
    # Section B: Type_Safe__Config Creation & Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test_perf__B_01__config_creation__default(self):                                      # Config: default creation
        def create_default_config():
            return Type_Safe__Config()

        with self.session as _:
            _.measure__quick(create_default_config)
            self.capture_result('B_01__config_creation__default', _.result)
            _.assert_time__less_than(self.time_2_kns)

    def test_perf__B_02__config_creation__single_flag(self):                                  # Config: with one flag
        def create_single_flag_config():
            return Type_Safe__Config(skip_validation=True)

        with self.session as _:
            _.measure__quick(create_single_flag_config)
            self.capture_result('B_02__config_creation__single_flag', _.result)
            _.assert_time__less_than(self.time_2_kns)

    def test_perf__B_03__config_creation__all_flags(self):                                    # Config: with all flags
        def create_all_flags_config():
            return Type_Safe__Config(skip_setattr     = True,
                                     skip_validation  = True,
                                     skip_conversion  = True,
                                     skip_mro_walk    = True,
                                     on_demand_nested = True,
                                     fast_collections = True)

        with self.session as _:
            _.measure__quick(create_all_flags_config)
            self.capture_result('B_03__config_creation__all_flags', _.result)
            _.assert_time__less_than(self.time_2_kns)

    def test_perf__B_04__factory__fast_mode(self):                                            # Config: fast_mode factory
        with self.session as _:
            _.measure__quick(Type_Safe__Config.fast_mode)
            self.capture_result('B_04__factory__fast_mode', _.result)
            _.assert_time__less_than(self.time_2_kns)

    def test_perf__B_05__factory__on_demand_mode(self):                                       # Config: on_demand_mode factory
        with self.session as _:
            _.measure__quick(Type_Safe__Config.on_demand_mode)
            self.capture_result('B_05__factory__on_demand_mode', _.result)
            _.assert_time__less_than(self.time_2_kns)

    def test_perf__B_06__factory__bulk_load_mode(self):                                       # Config: bulk_load_mode factory
        with self.session as _:
            _.measure__quick(Type_Safe__Config.bulk_load_mode)
            self.capture_result('B_06__factory__bulk_load_mode', _.result)
            _.assert_time__less_than(self.time_2_kns)

    def test_perf__B_07__config__repr(self):                                                  # Config: __repr__ with flags
        config = Type_Safe__Config.fast_mode()
        def get_repr():
            return repr(config)

        with self.session as _:
            _.measure__quick(get_repr)
            self.capture_result('B_07__config__repr', _.result)
            _.assert_time__less_than(self.time_2_kns)

    def test_perf__B_08__config__equality(self):                                              # Config: __eq__ comparison
        config1 = Type_Safe__Config.fast_mode()
        config2 = Type_Safe__Config.fast_mode()
        def compare_configs():
            return config1 == config2

        with self.session as _:
            _.measure__quick(compare_configs)
            self.capture_result('B_08__config__equality', _.result)
            _.assert_time__less_than(self.time_1_kns)

    def test_perf__B_09__context_manager__overhead(self):                                     # Config: context manager enter/exit
        def context_manager_cycle():
            config = Type_Safe__Config()
            config.__enter__()
            config.__exit__(None, None, None)

        with self.session as _:
            _.measure__quick(context_manager_cycle)
            self.capture_result('B_09__context_manager__overhead', _.result)
            _.assert_time__less_than(self.time_2_kns)

    # ═══════════════════════════════════════════════════════════════════════════
    # Section C: find_type_safe_config Stack Discovery
    # ═══════════════════════════════════════════════════════════════════════════

    def test_perf__C_01__find_config__no_config(self):                                        # Stack: negative lookup
        with self.session as _:
            _.measure__quick(find_type_safe_config)
            self.capture_result('C_01__find_config__no_config', _.result)
            _.assert_time__less_than(self.time_2_kns)

    def test_perf__C_02__find_config__depth_1(self):                                          # Stack: config at depth 1
        def measure_depth_1():
            return find_type_safe_config()

        _type_safe_config_ = Type_Safe__Config()
        with _type_safe_config_:
            with self.session as _:
                _.measure__quick(measure_depth_1)
                self.capture_result('C_02__find_config__depth_1', _.result)
                _.assert_time__less_than(self.time_2_kns)

    def test_perf__C_03__find_config__depth_3(self):                                          # Stack: config at depth 3
        def depth_3():
            return find_type_safe_config()
        def depth_2():
            return depth_3()
        def depth_1():
            return depth_2()

        _type_safe_config_ = Type_Safe__Config()
        with _type_safe_config_:
            with self.session as _:
                _.measure__quick(depth_1)
                self.capture_result('C_03__find_config__depth_3', _.result)
                _.assert_time__less_than(self.time_5_kns)

    def test_perf__C_04__find_config__depth_5(self):                                          # Stack: config at depth 5
        def depth_5():
            return find_type_safe_config()
        def depth_4():
            return depth_5()
        def depth_3():
            return depth_4()
        def depth_2():
            return depth_3()
        def depth_1():
            return depth_2()

        _type_safe_config_ = Type_Safe__Config()
        with _type_safe_config_:
            with self.session as _:
                _.measure__quick(depth_1)
                self.capture_result('C_04__find_config__depth_5', _.result)
                _.assert_time__less_than(self.time_5_kns)

    def test_perf__C_05__find_config__depth_10(self):                                         # Stack: config at depth 10
        def depth_10():
            return find_type_safe_config()
        def depth_9():
            return depth_10()
        def depth_8():
            return depth_9()
        def depth_7():
            return depth_8()
        def depth_6():
            return depth_7()
        def depth_5():
            return depth_6()
        def depth_4():
            return depth_5()
        def depth_3():
            return depth_4()
        def depth_2():
            return depth_3()
        def depth_1():
            return depth_2()

        _type_safe_config_ = Type_Safe__Config()
        with _type_safe_config_:
            with self.session as _:
                _.measure__quick(depth_1)
                self.capture_result('C_05__find_config__depth_10', _.result)
                _.assert_time__less_than(self.time_10_kns)

    def test_perf__C_06__find_config__repeated_x3(self):                                      # Stack: 3 repeated lookups
        def three_lookups():
            find_type_safe_config()
            find_type_safe_config()
            find_type_safe_config()

        _type_safe_config_ = Type_Safe__Config()
        with _type_safe_config_:
            with self.session as _:
                _.measure__quick(three_lookups)
                self.capture_result('C_06__find_config__repeated_x3', _.result)
                _.assert_time__less_than(self.time_5_kns)

    def test_perf__C_07__find_config__no_config_x3(self):                                     # Stack: repeated negative lookups
        def three_negative_lookups():
            find_type_safe_config()
            find_type_safe_config()
            find_type_safe_config()

        with self.session as _:
            _.measure__quick(three_negative_lookups)
            self.capture_result('C_07__find_config__no_config_x3', _.result)
            _.assert_time__less_than(self.time_5_kns)

    def test_perf__C_08__full_pattern__create_and_lookup(self):                               # Stack: full usage pattern
        def full_pattern():
            _type_safe_config_ = Type_Safe__Config(skip_validation=True)
            with _type_safe_config_:
                return find_type_safe_config()

        with self.session as _:
            _.measure__quick(full_pattern)
            self.capture_result('C_08__full_pattern__create_and_lookup', _.result)
            _.assert_time__less_than(self.time_5_kns)

    # ═══════════════════════════════════════════════════════════════════════════
    # Section D: Type_Safe Object Creation
    # ═══════════════════════════════════════════════════════════════════════════

    def test_perf__D_01__type_safe__empty(self):                                              # Type_Safe: empty class
        def create_ts_empty():
            return TS__Empty()

        with self.session as _:
            _.measure__quick(create_ts_empty)
            self.capture_result('D_01__type_safe__empty', _.result)
            _.assert_time__less_than(self.time_10_kns)

    def test_perf__D_02__type_safe__with_primitives(self):                                    # Type_Safe: with Python primitives
        def create_ts_primitives():
            return TS__With_Primitives()

        with self.session as _:
            _.measure__quick(create_ts_primitives)
            self.capture_result('D_02__type_safe__with_primitives', _.result)
            _.assert_time__less_than(self.time_20_kns)

    def test_perf__D_03__type_safe__with_safe_types(self):                                    # Type_Safe: with type-safe primitives
        def create_ts_safe_types():
            return TS__With_Safe_Types()

        with self.session as _:
            _.measure__quick(create_ts_safe_types)
            self.capture_result('D_03__type_safe__with_safe_types', _.result)
            _.assert_time__less_than(self.time_50_kns)

    def test_perf__D_04__type_safe__with_nested(self):                                        # Type_Safe: with nested Type_Safe
        def create_ts_nested():
            return TS__With_Nested()

        with self.session as _:
            _.measure__quick(create_ts_nested)
            self.capture_result('D_04__type_safe__with_nested', _.result)
            _.assert_time__less_than(self.time_50_kns)

    def test_perf__D_05__type_safe__with_python_collections(self):                            # Type_Safe: with Python collections
        def create_ts_py_collections():
            return TS__With_Python_Collections()

        with self.session as _:
            _.measure__quick(create_ts_py_collections)
            self.capture_result('D_05__type_safe__with_python_collections', _.result)
            _.assert_time__less_than(self.time_50_kns)

    def test_perf__D_06__type_safe__with_typesafe_collections(self):                          # Type_Safe: with Type_Safe collections
        def create_ts_ts_collections():
            return TS__With_TypeSafe_Collections()

        with self.session as _:
            _.measure__quick(create_ts_ts_collections)
            self.capture_result('D_06__type_safe__with_typesafe_collections', _.result)
            _.assert_time__less_than(self.time_50_kns)

    def test_perf__D_07__type_safe__empty_x10(self):                                          # Type_Safe: empty class 10x
        def create_ts_empty_x10():
            for _ in range(10):
                TS__Empty()

        with self.session as _:
            _.measure__quick(create_ts_empty_x10)
            self.capture_result('D_07__type_safe__empty_x10', _.result)

    def test_perf__D_08__type_safe__empty_x100(self):                                         # Type_Safe: empty class 100x
        def create_ts_empty_x100():
            for _ in range(100):
                TS__Empty()

        with self.session as _:
            _.measure__quick(create_ts_empty_x100)
            self.capture_result('D_08__type_safe__empty_x100', _.result)

    def test_perf__D_09__type_safe__with_primitives_x10(self):                                # Type_Safe: with primitives 10x
        def create_ts_primitives_x10():
            for _ in range(10):
                TS__With_Primitives()

        with self.session as _:
            _.measure__quick(create_ts_primitives_x10)
            self.capture_result('D_09__type_safe__with_primitives_x10', _.result)

    def test_perf__D_10__type_safe__with_nested_x10(self):                                    # Type_Safe: with nested 10x
        def create_ts_nested_x10():
            for _ in range(10):
                TS__With_Nested()

        with self.session as _:
            _.measure__quick(create_ts_nested_x10)
            self.capture_result('D_10__type_safe__with_nested_x10', _.result)

    # ═══════════════════════════════════════════════════════════════════════════
    # Section E: @dataclass Object Creation
    # ═══════════════════════════════════════════════════════════════════════════

    def test_perf__E_01__dataclass__empty(self):                                              # Dataclass: empty
        def create_dc_empty():
            return DC__Empty()

        with self.session as _:
            _.measure__quick(create_dc_empty)
            self.capture_result('E_01__dataclass__empty', _.result)

    def test_perf__E_02__dataclass__with_primitives(self):                                    # Dataclass: with Python primitives
        def create_dc_primitives():
            return DC__With_Primitives()

        with self.session as _:
            _.measure__quick(create_dc_primitives)
            self.capture_result('E_02__dataclass__with_primitives', _.result)

    def test_perf__E_03__dataclass__with_nested(self):                                        # Dataclass: with nested dataclass
        def create_dc_nested():
            return DC__With_Nested()

        with self.session as _:
            _.measure__quick(create_dc_nested)
            self.capture_result('E_03__dataclass__with_nested', _.result)

    def test_perf__E_04__dataclass__with_collections(self):                                   # Dataclass: with Python collections
        def create_dc_collections():
            return DC__With_Collections()

        with self.session as _:
            _.measure__quick(create_dc_collections)
            self.capture_result('E_04__dataclass__with_collections', _.result)

    def test_perf__E_05__dataclass__empty_x10(self):                                          # Dataclass: empty 10x
        def create_dc_empty_x10():
            for _ in range(10):
                DC__Empty()

        with self.session as _:
            _.measure__quick(create_dc_empty_x10)
            self.capture_result('E_05__dataclass__empty_x10', _.result)

    def test_perf__E_06__dataclass__empty_x100(self):                                         # Dataclass: empty 100x
        def create_dc_empty_x100():
            for _ in range(100):
                DC__Empty()

        with self.session as _:
            _.measure__quick(create_dc_empty_x100)
            self.capture_result('E_06__dataclass__empty_x100', _.result)

    def test_perf__E_07__dataclass__with_primitives_x10(self):                                # Dataclass: with primitives 10x
        def create_dc_primitives_x10():
            for _ in range(10):
                DC__With_Primitives()

        with self.session as _:
            _.measure__quick(create_dc_primitives_x10)
            self.capture_result('E_07__dataclass__with_primitives_x10', _.result)

    def test_perf__E_08__dataclass__with_nested_x10(self):                                    # Dataclass: with nested 10x
        def create_dc_nested_x10():
            for _ in range(10):
                DC__With_Nested()

        with self.session as _:
            _.measure__quick(create_dc_nested_x10)
            self.capture_result('E_08__dataclass__with_nested_x10', _.result)

    # ═══════════════════════════════════════════════════════════════════════════
    # Section F: Pydantic BaseModel Object Creation
    # ═══════════════════════════════════════════════════════════════════════════

    def test_perf__F_01__pydantic__empty(self):                                               # Pydantic: empty
        def create_pd_empty():
            return PD__Empty()

        with self.session as _:
            _.measure__quick(create_pd_empty)
            self.capture_result('F_01__pydantic__empty', _.result)

    def test_perf__F_02__pydantic__with_primitives(self):                                     # Pydantic: with Python primitives
        def create_pd_primitives():
            return PD__With_Primitives()

        with self.session as _:
            _.measure__quick(create_pd_primitives)
            self.capture_result('F_02__pydantic__with_primitives', _.result)

    def test_perf__F_03__pydantic__with_nested(self):                                         # Pydantic: with nested model
        def create_pd_nested():
            return PD__With_Nested()

        with self.session as _:
            _.measure__quick(create_pd_nested)
            self.capture_result('F_03__pydantic__with_nested', _.result)

    def test_perf__F_04__pydantic__with_collections(self):                                    # Pydantic: with Python collections
        def create_pd_collections():
            return PD__With_Collections()

        with self.session as _:
            _.measure__quick(create_pd_collections)
            self.capture_result('F_04__pydantic__with_collections', _.result)

    def test_perf__F_05__pydantic__empty_x10(self):                                           # Pydantic: empty 10x
        def create_pd_empty_x10():
            for _ in range(10):
                PD__Empty()

        with self.session as _:
            _.measure__quick(create_pd_empty_x10)
            self.capture_result('F_05__pydantic__empty_x10', _.result)

    def test_perf__F_06__pydantic__empty_x100(self):                                          # Pydantic: empty 100x
        def create_pd_empty_x100():
            for _ in range(100):
                PD__Empty()

        with self.session as _:
            _.measure__quick(create_pd_empty_x100)
            self.capture_result('F_06__pydantic__empty_x100', _.result)

    def test_perf__F_07__pydantic__with_primitives_x10(self):                                 # Pydantic: with primitives 10x
        def create_pd_primitives_x10():
            for _ in range(10):
                PD__With_Primitives()

        with self.session as _:
            _.measure__quick(create_pd_primitives_x10)
            self.capture_result('F_07__pydantic__with_primitives_x10', _.result)

    def test_perf__F_08__pydantic__with_nested_x10(self):                                     # Pydantic: with nested 10x
        def create_pd_nested_x10():
            for _ in range(10):
                PD__With_Nested()

        with self.session as _:
            _.measure__quick(create_pd_nested_x10)
            self.capture_result('F_08__pydantic__with_nested_x10', _.result)