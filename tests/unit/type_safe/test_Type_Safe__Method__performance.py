from unittest                                                   import TestCase
from typing                                                     import List, Dict, Optional, Union, Any, Type
from dataclasses                                                import dataclass
from enum                                                       import Enum
from osbot_utils.helpers.duration.decorators.capture_duration   import capture_duration
from osbot_utils.type_safe.decorators.type_safe                 import type_safe
from osbot_utils.type_safe.Type_Safe                            import Type_Safe
from osbot_utils.helpers.Safe_Id                                import Safe_Id
from osbot_utils.helpers.Random_Guid                            import Random_Guid


# class StatusEnum(Enum):
#     ACTIVE = "active"
#     INACTIVE = "inactive"
#     PENDING = "pending"
#
#
# @dataclass
# class DataClass:
#     name: str
#     value: int
#
#
# class CustomType(Type_Safe):
#     id: str
#     data: Dict[str, Any]


class test__decorator__type_safe__performance(TestCase):

    def setUp(self):
        self.iterations = 10000
        self.warmup_iterations = 10

    def _calculate_overhead(self, no_check_time: float, with_check_time: float) -> float:
        """Calculate overhead ratio and print results"""
        overhead = with_check_time / no_check_time if no_check_time > 0 else float('inf')
        # print(f"\n  No check: {no_check_time:.6f}s ({no_check_time/self.iterations*1000:.3f}ms per call)")
        # print(f"  With check: {with_check_time:.6f}s ({with_check_time/self.iterations*1000:.3f}ms per call)")
        # print(f"  Overhead: {overhead:.1f}x")
        return overhead

    def test__performance__no_parameters(self):
        """Test performance for methods with no parameters (best case)"""
        class NoParamClass:
            def no_check(self):
                return 42

            @type_safe
            def with_check(self):
                return 42

        obj = NoParamClass()

        # Warmup
        for _ in range(self.warmup_iterations):
            obj.no_check()
            obj.with_check()

        with capture_duration(precision=5) as duration_no_check:
            for _ in range(self.iterations):
                obj.no_check()

        with capture_duration(precision=5) as duration_with_check:
            for _ in range(self.iterations):
                obj.with_check()

        overhead = self._calculate_overhead(duration_no_check.seconds, duration_with_check.seconds)
        # print()
        # print('duration_no_check    :' , duration_no_check.seconds)
        # print('duration_with_check  :', duration_with_check.seconds)
        # print('overhead             :', overhead)
        #assert overhead < 250  # Current baseline which is really high
        #assert overhead < 70  # Current baseline which is really high
        assert overhead < 5  # Current baseline which is really high





# import time
# import statistics
# from unittest                                import TestCase
# from typing                                  import List, Dict, Optional, Union, Any, Type
# from osbot_utils.type_safe.Type_Safe__Method import Type_Safe__Method
#
#
# class test_Type_Safe__Method__performance(TestCase):
#
#     def setUp(self):                                                                     # Setup performance test environment
#         self.iterations = 1000                                                           # Number of iterations for performance tests
#
#     def measure_execution_time(self, func, *args, **kwargs):                            # Measure execution time of a function over multiple iterations
#         times = []
#         for _ in range(self.iterations):
#             start = time.perf_counter()
#             func(*args, **kwargs)
#             end   = time.perf_counter()
#             times.append(end - start)
#
#         return { 'mean'  : statistics.mean(times)                     ,
#                  'median': statistics.median(times)                   ,
#                  'stdev' : statistics.stdev(times) if len(times) > 1 else 0,
#                  'min'   : min(times)                                 ,
#                  'max'   : max(times)                                 }
#
#     def test_simple_function_performance(self):                                          # Test performance with simple function signatures
#         def simple_func(a : int   ,
#                         b : str   ,
#                         c : float
#                    ) -> None:
#             pass
#
#         checker = Type_Safe__Method(simple_func)
#
#         # Measure validation time
#         def validate():
#             bound_args = checker.handle_type_safety((1, "test", 3.14), {})
#
#         stats = self.measure_execution_time(validate)
#
#         print(f"\nSimple function validation performance:")
#         print(f"  Mean: {stats['mean']*1000:.3f}ms")
#         print(f"  Median: {stats['median']*1000:.3f}ms")
#         print(f"  Min: {stats['min']*1000:.3f}ms")
#         print(f"  Max: {stats['max']*1000:.3f}ms")
#
#     def test_complex_function_performance(self):                                         # Test performance with complex type signatures
#         def complex_func(simple      : str                      ,
#                         optional    : Optional[int]      = None ,
#                         union       : Union[str, int, float] = 0     ,
#                         list_param  : List[str]              = None  ,
#                         dict_param  : Dict[str, Any]         = None  ,
#                         type_param  : Type[object]           = object
#                        ) -> None:
#             pass
#
#         checker = Type_Safe__Method(complex_func)
#
#         # Measure validation time with all parameters
#         def validate():
#             bound_args = checker.handle_type_safety(
#                 ("test",),
#                 { 'optional'  : 42                              ,
#                   'union'     : 3.14                            ,
#                   'list_param': ["a", "b", "c"]                 ,
#                   'dict_param': {"key1": "value1", "key2": 2}  ,
#                   'type_param': str                             }
#             )
#
#         stats = self.measure_execution_time(validate)
#
#         print(f"\nComplex function validation performance:")
#         print(f"  Mean: {stats['mean']*1000:.3f}ms")
#         print(f"  Median: {stats['median']*1000:.3f}ms")
#         print(f"  Min: {stats['min']*1000:.3f}ms")
#         print(f"  Max: {stats['max']*1000:.3f}ms")
#
#     def test_list_validation_performance(self):                                          # Test performance of list validation with varying sizes
#         def list_func(items: List[int]) -> None:
#             pass
#
#         checker = Type_Safe__Method(list_func)
#
#         for size in [10, 100, 1000]:
#             test_list = list(range(size))
#
#             def validate():
#                 bound_args = checker.handle_type_safety((test_list,), {})
#
#             stats = self.measure_execution_time(validate)
#
#             print(f"\nList validation performance (size={size}):")
#             print(f"  Mean: {stats['mean']*1000:.3f}ms")
#             print(f"  Per item: {stats['mean']*1000/size:.3f}ms")
#
#     def test_dict_validation_performance(self):                                          # Test performance of dict validation with varying sizes
#         def dict_func(data: Dict[str, int]) -> None:
#             pass
#
#         checker = Type_Safe__Method(dict_func)
#
#         for size in [10, 100, 1000]:
#             test_dict = {f"key{i}": i for i in range(size)}
#
#             def validate():
#                 bound_args = checker.handle_type_safety((test_dict,), {})
#
#             stats = self.measure_execution_time(validate)
#
#             print(f"\nDict validation performance (size={size}):")
#             print(f"  Mean: {stats['mean']*1000:.3f}ms")
#             print(f"  Per item: {stats['mean']*1000/size:.3f}ms")
#
#     def test_caching_impact(self):                                                       # Test if repeated validations benefit from any caching
#         def cached_func(a : int       ,
#                        b : str       ,
#                        c : List[int]
#                       ) -> None:
#             pass
#
#         checker   = Type_Safe__Method(cached_func)
#         test_args = (42, "test", [1, 2, 3])
#
#         # First run (cold)
#         cold_times = []
#         for _ in range(100):
#             start = time.perf_counter()
#             checker.handle_type_safety(test_args, {})
#             end   = time.perf_counter()
#             cold_times.append(end - start)
#
#         # Subsequent runs (potentially cached)
#         warm_times = []
#         for _ in range(100):
#             start = time.perf_counter()
#             checker.handle_type_safety(test_args, {})
#             end   = time.perf_counter()
#             warm_times.append(end - start)
#
#         cold_mean = statistics.mean(cold_times)
#         warm_mean = statistics.mean(warm_times)
#
#         print(f"\nCaching impact:")
#         print(f"  Cold mean: {cold_mean*1000:.3f}ms")
#         print(f"  Warm mean: {warm_mean*1000:.3f}ms")
#         print(f"  Improvement: {((cold_mean - warm_mean) / cold_mean * 100):.1f}%")
#
#     def test_type_checking_overhead(self):                                               # Compare overhead of type checking vs no checking
#         def typed_func(a : int   ,
#                       b : str   ,
#                       c : float
#                      ) -> float:
#             return a + len(b) + c
#
#         def untyped_func(a, b, c):
#             return a + len(b) + c
#
#         checker = Type_Safe__Method(typed_func)
#         args    = (42, "test", 3.14)
#
#         # Measure typed function with checking
#         def with_checking():
#             bound_args = checker.handle_type_safety(args, {})
#             return typed_func(**bound_args.arguments)
#
#         # Measure direct call
#         def without_checking():
#             return untyped_func(*args)
#
#         typed_stats   = self.measure_execution_time(with_checking)
#         untyped_stats = self.measure_execution_time(without_checking)
#
#         overhead = (typed_stats['mean'] - untyped_stats['mean']) / untyped_stats['mean'] * 100
#
#         print(f"\nType checking overhead:")
#         print(f"  Without checking: {untyped_stats['mean']*1000:.3f}ms")
#         print(f"  With checking: {typed_stats['mean']*1000:.3f}ms")
#         print(f"  Overhead: {overhead:.1f}%")
#
#     def test_error_handling_performance(self):                                           # Test performance impact of error handling
#         def strict_func(value: int) -> None:
#             pass
#
#         checker = Type_Safe__Method(strict_func)
#
#         # Measure successful validation
#         def valid_case():
#             try:
#                 checker.handle_type_safety((42,), {})
#             except:
#                 pass
#
#         # Measure failed validation
#         def invalid_case():
#             try:
#                 checker.handle_type_safety(("not an int",), {})
#             except ValueError:
#                 pass
#
#         valid_stats   = self.measure_execution_time(valid_case)
#         invalid_stats = self.measure_execution_time(invalid_case)
#
#         print(f"\nError handling performance:")
#         print(f"  Valid case: {valid_stats['mean']*1000:.3f}ms")
#         print(f"  Invalid case: {invalid_stats['mean']*1000:.3f}ms")
#         print(f"  Error overhead: {((invalid_stats['mean'] - valid_stats['mean']) / valid_stats['mean'] * 100):.1f}%")
#
#
# class OptimizedType_Safe__Method(Type_Safe__Method):                                     # Example of potential optimizations
#
#     def __init__(self, func):
#         super().__init__(func)
#         # Cache for type checking results
#         self._type_cache = {}
#
#     def validate_direct_type(self, param_name : str ,                                   # Simple caching of type validation results
#                                    param_value : Any ,
#                                    expected_type : Any
#                             ) -> bool:
#         cache_key = (type(param_value), expected_type)
#         if cache_key in self._type_cache:
#             if not self._type_cache[cache_key]:
#                 raise ValueError(f"Cached: Parameter '{param_name}' expected type {expected_type}, but got {type(param_value)}")
#             return True
#
#         try:
#             result                       = super().validate_direct_type(param_name, param_value, expected_type)
#             self._type_cache[cache_key]  = True
#             return result
#         except ValueError:
#             self._type_cache[cache_key]  = False
#             raise
#
#
# class test_Optimized_Type_Safe__Method(TestCase):                                        # Test potential optimizations
#
#     def test_optimization_comparison(self):                                              # Compare original vs optimized implementation
#         def test_func(a : int   ,
#                      b : str   ,
#                      c : float
#                     ) -> None:
#             pass
#
#         original   = Type_Safe__Method(test_func)
#         optimized  = OptimizedType_Safe__Method(test_func)
#
#         args       = (42, "test", 3.14)
#         iterations = 1000
#
#         # Test original
#         start = time.perf_counter()
#         for _ in range(iterations):
#             original.handle_type_safety(args, {})
#         original_time = time.perf_counter() - start
#
#         # Test optimized
#         start = time.perf_counter()
#         for _ in range(iterations):
#             optimized.handle_type_safety(args, {})
#         optimized_time = time.perf_counter() - start
#
#         improvement = (original_time - optimized_time) / original_time * 100
#
#         print(f"\nOptimization comparison:")
#         print(f"  Original: {original_time*1000:.3f}ms")
#         print(f"  Optimized: {optimized_time*1000:.3f}ms")
#         print(f"  Improvement: {improvement:.1f}%")