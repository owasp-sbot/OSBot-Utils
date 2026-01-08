# # ═══════════════════════════════════════════════════════════════════════════════
# # Performance Baselines for Type_Safe__Config (v2 - using Perf_Benchmark)
# # Captures baseline measurements for config creation and stack discovery
# # ═══════════════════════════════════════════════════════════════════════════════
# #
# # LEGEND:
# #   A = Python Baselines (raw Python operations for reference)
# #   B = Type_Safe__Config Creation & Operations
# #   C = find_type_safe_config Stack Discovery
# #   D = Type_Safe Object Creation (various complexity levels)
# #   E = Python @dataclass Object Creation (for comparison)
# #   F = Pydantic BaseModel Object Creation (for comparison)
# #
# # ═══════════════════════════════════════════════════════════════════════════════
#
# from dataclasses                                                                              import dataclass, field
# from typing                                                                                   import List, Dict
# from unittest                                                                                 import TestCase
# from osbot_utils.helpers.performance.benchmark.Perf_Benchmark__Timing                         import Perf_Benchmark__Timing
# from osbot_utils.helpers.performance.benchmark.schemas.timing.Schema__Perf_Benchmark__Timing__Config import Schema__Perf_Benchmark__Timing__Config
# from osbot_utils.type_safe.primitives.core.Safe_Str                                           import Safe_Str
# from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                             import Safe_Id
# from osbot_utils.utils.Env                                                                    import not_in_github_action
# from osbot_utils.utils.Files                                                                  import path_combine
# from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
# from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import Type_Safe__Config
# from osbot_utils.type_safe.type_safe_core.config.static_methods.find_type_safe_config         import find_type_safe_config
#
#
# # ═══════════════════════════════════════════════════════════════════════════════
# # Reference Classes for Python Baselines (Section A)
# # ═══════════════════════════════════════════════════════════════════════════════
#
# class Empty_Class:                                                                            # Plain Python class with no attributes
#     pass
#
# class Class_With_Init:                                                                        # Plain Python class with __init__
#     def __init__(self):
#         self.a = 1
#         self.b = 2
#         self.c = 3
#
# class Class_With_Slots:                                                                       # Python class with __slots__
#     __slots__ = ('a', 'b', 'c')
#     def __init__(self):
#         self.a = 1
#         self.b = 2
#         self.c = 3
#
#
# def empty_function():                                                                         # Empty function for invocation baseline
#     pass
#
#
# # ═══════════════════════════════════════════════════════════════════════════════
# # Type_Safe Test Classes (Section D)
# # ═══════════════════════════════════════════════════════════════════════════════
#
# class TS__Empty(Type_Safe):                                                                   # Empty Type_Safe class
#     pass
#
# class TS__With_Primitives(Type_Safe):                                                         # Type_Safe with Python primitives
#     name   : str  = ''
#     count  : int  = 0
#     active : bool = False
#
# class TS__With_Safe_Types(Type_Safe):                                                         # Type_Safe with type-safe primitives
#     id     : Safe_Id
#     name   : Safe_Str
#     label  : Safe_Str
#
# class TS__Inner(Type_Safe):                                                                   # Inner class for nesting tests
#     value : str = ''
#
# class TS__With_Nested(Type_Safe):                                                             # Type_Safe with nested Type_Safe
#     inner  : TS__Inner
#     name   : str = ''
#
# class TS__With_Python_Collections(Type_Safe):                                                 # Type_Safe with Python collections
#     items : list
#     data  : dict
#
# class TS__With_TypeSafe_Collections(Type_Safe):                                               # Type_Safe with Type_Safe collections
#     items : List[str]
#     data  : Dict[str, str]
#
#
# # ═══════════════════════════════════════════════════════════════════════════════
# # @dataclass Test Classes (Section E)
# # ═══════════════════════════════════════════════════════════════════════════════
#
# @dataclass
# class DC__Empty:                                                                              # Empty dataclass
#     pass
#
# @dataclass
# class DC__With_Primitives:                                                                    # Dataclass with Python primitives
#     name   : str  = ''
#     count  : int  = 0
#     active : bool = False
#
# @dataclass
# class DC__Inner:                                                                              # Inner dataclass for nesting tests
#     value : str = ''
#
# @dataclass
# class DC__With_Nested:                                                                        # Dataclass with nested dataclass
#     inner  : DC__Inner = field(default_factory=DC__Inner)
#     name   : str       = ''
#
# @dataclass
# class DC__With_Collections:                                                                   # Dataclass with Python collections
#     items : List[str]       = field(default_factory=list)
#     data  : Dict[str, int]  = field(default_factory=dict)
#
#
# # ═══════════════════════════════════════════════════════════════════════════════
# # Pydantic BaseModel Test Classes (Section F) - Optional
# # ═══════════════════════════════════════════════════════════════════════════════
#
# try:
#     from pydantic import BaseModel
#     HAS_PYDANTIC = True
#
#     class PD__Empty(BaseModel):                                                               # Empty Pydantic model
#         pass
#
#     class PD__With_Primitives(BaseModel):                                                     # Pydantic with Python primitives
#         name   : str  = ''
#         count  : int  = 0
#         active : bool = False
#
#     class PD__Inner(BaseModel):                                                               # Inner Pydantic model
#         value : str = ''
#
#     class PD__With_Nested(BaseModel):                                                         # Pydantic with nested model
#         inner  : PD__Inner = PD__Inner()
#         name   : str       = ''
#
#     class PD__With_Collections(BaseModel):                                                    # Pydantic with Python collections
#         items : List[str]       = []
#         data  : Dict[str, int]  = {}
#
# except ImportError:
#     HAS_PYDANTIC = False
#
#
# # ═══════════════════════════════════════════════════════════════════════════════
# # Time Thresholds (in nanoseconds)
# # ═══════════════════════════════════════════════════════════════════════════════
#
# time_100_ns  =     100                                                                        # Sub-microsecond
# time_500_ns  =     500                                                                        # Half microsecond
# time_1_kns   =   1_000                                                                        # 1 microsecond
# time_2_kns   =   2_000                                                                        # 2 microseconds
# time_5_kns   =   5_000                                                                        # 5 microseconds
# time_10_kns  =  10_000                                                                        # 10 microseconds
# time_20_kns  =  20_000                                                                        # 20 microseconds
# time_50_kns  =  50_000                                                                        # 50 microseconds
#
#
# # ═══════════════════════════════════════════════════════════════════════════════
# # Stack Depth Helper Functions for Section C
# # ═══════════════════════════════════════════════════════════════════════════════
#
# def depth_1():
#     return find_type_safe_config()
#
# def depth_2():
#     return depth_1()
#
# def depth_3():
#     return depth_2()
#
# def depth_4():
#     return depth_3()
#
# def depth_5():
#     return depth_4()
#
# def depth_6():
#     return depth_5()
#
# def depth_7():
#     return depth_6()
#
# def depth_8():
#     return depth_7()
#
# def depth_9():
#     return depth_8()
#
# def depth_10():
#     return depth_9()
#
#
# class test_perf__Type_Safe__Config(TestCase):
#
#     def test__run_all_benchmarks(self):
#         asserts_enabled = False
#         output_path     = path_combine(__file__, '../type-safe__config-stats/')
#         config          = Schema__Perf_Benchmark__Timing__Config(title           = 'Type_Safe__Config Performance Baselines',
#                                                                  output_path     = output_path                              ,
#                                                                  asserts_enabled = asserts_enabled                          )
#
#         with Perf_Benchmark__Timing(config=config) as timing:
#
#             # ═══════════════════════════════════════════════════════════════════
#             # Section A: Python Baselines
#             # ═══════════════════════════════════════════════════════════════════
#
#             timing.benchmark('A_01__python__nop'                   , lambda: None                                     )
#             timing.benchmark('A_02__python__var_assignment'        , lambda: 42                                       )
#             timing.benchmark('A_03__python__function_invocation'   , empty_function                                   )
#             timing.benchmark('A_04__python__function_invocation_x10', lambda: [empty_function() for _ in range(10)]   )
#             timing.benchmark('A_05__python__class_empty'           , Empty_Class                                      )
#             timing.benchmark('A_06__python__class_with_init'       , Class_With_Init                                  )
#             timing.benchmark('A_07__python__class_with_slots'      , Class_With_Slots                                 )
#             timing.benchmark('A_08__python__class_with_init_x10'   , lambda: [Class_With_Init() for _ in range(10)]   )
#             timing.benchmark('A_09__python__class_with_init_x100'  , lambda: [Class_With_Init() for _ in range(100)]  )
#
#             # ═══════════════════════════════════════════════════════════════════
#             # Section B: Type_Safe__Config Creation & Operations
#             # ═══════════════════════════════════════════════════════════════════
#
#             timing.benchmark('B_01__config_creation__default'      , Type_Safe__Config                                            , assert_less_than=time_2_kns)
#             timing.benchmark('B_02__config_creation__single_flag'  , lambda: Type_Safe__Config(skip_validation=True)              , assert_less_than=time_2_kns)
#             timing.benchmark('B_03__config_creation__all_flags'    , lambda: Type_Safe__Config(skip_setattr     = True,
#                                                                                                skip_validation  = True,
#                                                                                                skip_conversion  = True,
#                                                                                                skip_mro_walk    = True,
#                                                                                                on_demand_nested = True,
#                                                                                                fast_collections = True)           , assert_less_than=time_2_kns)
#             timing.benchmark('B_04__factory__fast_mode'            , Type_Safe__Config.fast_mode                                  , assert_less_than=time_2_kns)
#             timing.benchmark('B_05__factory__on_demand_mode'       , Type_Safe__Config.on_demand_mode                             , assert_less_than=time_2_kns)
#             timing.benchmark('B_06__factory__bulk_load_mode'       , Type_Safe__Config.bulk_load_mode                             , assert_less_than=time_2_kns)
#
#             config_for_repr = Type_Safe__Config.fast_mode()
#             timing.benchmark('B_07__config__repr'                  , lambda: repr(config_for_repr)                                , assert_less_than=time_2_kns)
#
#             config1, config2 = Type_Safe__Config.fast_mode(), Type_Safe__Config.fast_mode()
#             timing.benchmark('B_08__config__equality'              , lambda: config1 == config2                                   , assert_less_than=time_1_kns)
#
#             timing.benchmark('B_09__context_manager__overhead'     , lambda: Type_Safe__Config().__enter__() or True              , assert_less_than=time_2_kns)
#
#             # ═══════════════════════════════════════════════════════════════════
#             # Section C: find_type_safe_config Stack Discovery
#             # ═══════════════════════════════════════════════════════════════════
#
#             timing.benchmark('C_01__find_config__no_config'        , find_type_safe_config                                        , assert_less_than=time_2_kns)
#
#             _type_safe_config_ = Type_Safe__Config()                                          # Config in local scope for stack discovery
#             with _type_safe_config_:
#                 timing.benchmark('C_02__find_config__depth_1'      , find_type_safe_config                                        , assert_less_than=time_2_kns)
#                 timing.benchmark('C_03__find_config__depth_3'      , depth_3                                                      , assert_less_than=time_5_kns)
#                 timing.benchmark('C_04__find_config__depth_5'      , depth_5                                                      , assert_less_than=time_5_kns)
#                 timing.benchmark('C_05__find_config__depth_10'     , depth_10                                                     , assert_less_than=time_10_kns)
#                 timing.benchmark('C_06__find_config__repeated_x3'  , lambda: (find_type_safe_config(),
#                                                                              find_type_safe_config(),
#                                                                              find_type_safe_config())                             , assert_less_than=time_5_kns)
#
#             timing.benchmark('C_07__find_config__no_config_x3'     , lambda: (find_type_safe_config(),
#                                                                              find_type_safe_config(),
#                                                                              find_type_safe_config())                             , assert_less_than=time_5_kns)
#
#             timing.benchmark('C_08__full_pattern__create_and_lookup', lambda: Type_Safe__Config(skip_validation=True).__enter__() and find_type_safe_config(), assert_less_than=time_5_kns)
#
#             # ═══════════════════════════════════════════════════════════════════
#             # Section D: Type_Safe Object Creation
#             # ═══════════════════════════════════════════════════════════════════
#
#             timing.benchmark('D_01__type_safe__empty'              , TS__Empty                                                    , assert_less_than=time_10_kns )
#             timing.benchmark('D_02__type_safe__with_primitives'    , TS__With_Primitives                                          , assert_less_than=time_20_kns )
#             timing.benchmark('D_03__type_safe__with_safe_types'    , TS__With_Safe_Types                                          , assert_less_than=time_50_kns )
#             timing.benchmark('D_04__type_safe__with_nested'        , TS__With_Nested                                              , assert_less_than=time_50_kns )
#             timing.benchmark('D_05__type_safe__with_python_collections'  , TS__With_Python_Collections                            , assert_less_than=time_50_kns )
#             timing.benchmark('D_06__type_safe__with_typesafe_collections', TS__With_TypeSafe_Collections                          , assert_less_than=time_50_kns )
#             timing.benchmark('D_07__type_safe__empty_x10'          , lambda: [TS__Empty() for _ in range(10)]                                                   )
#             timing.benchmark('D_08__type_safe__empty_x100'         , lambda: [TS__Empty() for _ in range(100)]                                                  )
#             timing.benchmark('D_09__type_safe__with_primitives_x10', lambda: [TS__With_Primitives() for _ in range(10)]                                         )
#             timing.benchmark('D_10__type_safe__with_nested_x10'    , lambda: [TS__With_Nested() for _ in range(10)]                                             )
#
#             # ═══════════════════════════════════════════════════════════════════
#             # Section E: @dataclass Object Creation
#             # ═══════════════════════════════════════════════════════════════════
#
#             timing.benchmark('E_01__dataclass__empty'              , DC__Empty                                                    )
#             timing.benchmark('E_02__dataclass__with_primitives'    , DC__With_Primitives                                          )
#             timing.benchmark('E_03__dataclass__with_nested'        , DC__With_Nested                                              )
#             timing.benchmark('E_04__dataclass__with_collections'   , DC__With_Collections                                         )
#             timing.benchmark('E_05__dataclass__empty_x10'          , lambda: [DC__Empty() for _ in range(10)]                     )
#             timing.benchmark('E_06__dataclass__empty_x100'         , lambda: [DC__Empty() for _ in range(100)]                    )
#             timing.benchmark('E_07__dataclass__with_primitives_x10', lambda: [DC__With_Primitives() for _ in range(10)]           )
#             timing.benchmark('E_08__dataclass__with_nested_x10'    , lambda: [DC__With_Nested() for _ in range(10)]               )
#
#             # ═══════════════════════════════════════════════════════════════════
#             # Section F: Pydantic BaseModel Object Creation (if available)
#             # ═══════════════════════════════════════════════════════════════════
#
#             if HAS_PYDANTIC:
#                 timing.benchmark('F_01__pydantic__empty'               , PD__Empty                                                )
#                 timing.benchmark('F_02__pydantic__with_primitives'     , PD__With_Primitives                                      )
#                 timing.benchmark('F_03__pydantic__with_nested'         , PD__With_Nested                                          )
#                 timing.benchmark('F_04__pydantic__with_collections'    , PD__With_Collections                                     )
#                 timing.benchmark('F_05__pydantic__empty_x10'           , lambda: [PD__Empty() for _ in range(10)]                 )
#                 timing.benchmark('F_06__pydantic__empty_x100'          , lambda: [PD__Empty() for _ in range(100)]                )
#                 timing.benchmark('F_07__pydantic__with_primitives_x10' , lambda: [PD__With_Primitives() for _ in range(10)]       )
#                 timing.benchmark('F_08__pydantic__with_nested_x10'     , lambda: [PD__With_Nested() for _ in range(10)]           )
#
#             # ═══════════════════════════════════════════════════════════════════
#             # Save Results
#             # ═══════════════════════════════════════════════════════════════════
#
#             if not_in_github_action():
#                 timing.reporter().print_summary()
#                 timing.reporter().save_all()                                                  # Saves .json, .txt, .md, .html