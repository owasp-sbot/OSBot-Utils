# ═══════════════════════════════════════════════════════════════════════════════
# QA__Benchmark__Test_Data - Shared test data and fixtures for benchmark tests
# Contains sample data, target functions, and helper methods
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark_Id                    import Safe_Str__Benchmark_Id
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Section              import Safe_Str__Benchmark__Section
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Index                import Safe_Str__Benchmark__Index
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result          import Schema__Perf__Benchmark__Result
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Session         import Schema__Perf__Benchmark__Session
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results                import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark__Legend                import Dict__Benchmark__Legend


class QA__Benchmark__Test_Data(Type_Safe):                                       # Shared test data


    # ═══════════════════════════════════════════════════════════════════════════════
    # Sample Benchmark IDs
    # ═══════════════════════════════════════════════════════════════════════════════

    benchmark_id_1       : str = 'A_01__python__nop'
    benchmark_id_2       : str = 'A_02__python__class_empty'
    benchmark_id_3       : str = 'B_01__type_safe__empty'
    benchmark_id_4       : str = 'B_02__type_safe__primitives'
    benchmark_id_5       : str = 'C_01__complex__nested'
    benchmark_id_invalid : str = 'invalid'                                       # No section/index


    # ═══════════════════════════════════════════════════════════════════════════════
    # Sample Sections and Indices
    # ═══════════════════════════════════════════════════════════════════════════════

    section_a : str = 'A'
    section_b : str = 'B'
    section_c : str = 'C'
    index_01  : str = '01'
    index_02  : str = '02'


    # ═══════════════════════════════════════════════════════════════════════════════
    # Sample Scores
    # ═══════════════════════════════════════════════════════════════════════════════

    score_100_ns  : int = 100
    score_500_ns  : int = 500
    score_1_kns   : int = 1_000
    score_5_kns   : int = 5_000
    score_10_kns  : int = 10_000
    score_100_kns : int = 100_000


    # ═══════════════════════════════════════════════════════════════════════════════
    # Test Type_Safe Classes
    # ═══════════════════════════════════════════════════════════════════════════════

    # ═══════════════════════════════════════════════════════════════════════════════
    # Base Scores for Session Creation
    # ═══════════════════════════════════════════════════════════════════════════════

    base_score_1 : int = 1000                                                    # A_01 baseline
    base_score_2 : int = 500                                                     # A_02 baseline
    base_score_3 : int = 2000                                                    # B_01 baseline

    class TS__Empty(Type_Safe):                                                  # Empty Type_Safe
        pass

    class TS__With_Primitives(Type_Safe):                                        # Type_Safe with primitives
        name  : str
        value : int


    # ═══════════════════════════════════════════════════════════════════════════════
    # Target Functions for Benchmarking
    # ═══════════════════════════════════════════════════════════════════════════════

    def target_nop(self):                                                        # No-op function
        pass

    def target_simple(self):                                                     # Simple operation
        x = 1 + 1
        return x

    def target_list(self):                                                       # List comprehension
        return [i for i in range(10)]


    # ═══════════════════════════════════════════════════════════════════════════════
    # Factory Methods for Test Data
    # ═══════════════════════════════════════════════════════════════════════════════

    def create_benchmark_result(self                                        ,    # Create sample result
                                benchmark_id : str = None                   ,
                                section      : str = None                   ,
                                index        : str = None                   ,
                                name         : str = None                   ,
                                final_score  : int = None                   ,
                                raw_score    : int = None                   ) -> Schema__Perf__Benchmark__Result:

        return Schema__Perf__Benchmark__Result(benchmark_id = Safe_Str__Benchmark_Id(benchmark_id or self.benchmark_id_1)     ,
                                               section      = Safe_Str__Benchmark__Section(section or self.section_a)         ,
                                               index        = Safe_Str__Benchmark__Index(index or self.index_01)              ,
                                               name         = name or 'python__nop'                                           ,
                                               final_score  = Safe_UInt(final_score if final_score is not None else 100)      ,
                                               raw_score    = Safe_UInt(raw_score if raw_score is not None else 87)           )

    def create_results_dict(self                                            ,    # Create results dict
                            count: int = 3                                  ) -> Dict__Benchmark_Results:

        results = Dict__Benchmark_Results()

        if count >= 1:
            results[Safe_Str__Benchmark_Id(self.benchmark_id_1)] = self.create_benchmark_result(
                benchmark_id = self.benchmark_id_1                                                                            ,
                section      = self.section_a                                                                                 ,
                index        = self.index_01                                                                                  ,
                name         = 'python__nop'                                                                                  ,
                final_score  = self.score_100_ns                                                                              ,
                raw_score    = 87                                                                                             )

        if count >= 2:
            results[Safe_Str__Benchmark_Id(self.benchmark_id_2)] = self.create_benchmark_result(
                benchmark_id = self.benchmark_id_2                                                                            ,
                section      = self.section_a                                                                                 ,
                index        = self.index_02                                                                                  ,
                name         = 'python__class_empty'                                                                          ,
                final_score  = self.score_500_ns                                                                              ,
                raw_score    = 456                                                                                            )

        if count >= 3:
            results[Safe_Str__Benchmark_Id(self.benchmark_id_3)] = self.create_benchmark_result(
                benchmark_id = self.benchmark_id_3                                                                            ,
                section      = self.section_b                                                                                 ,
                index        = self.index_01                                                                                  ,
                name         = 'type_safe__empty'                                                                             ,
                final_score  = self.score_1_kns                                                                               ,
                raw_score    = 876                                                                                            )

        return results

    def create_legend(self) -> Dict__Benchmark__Legend:                          # Create sample legend
        legend = Dict__Benchmark__Legend()
        legend[Safe_Str__Benchmark__Section(self.section_a)] = 'Python Baselines'
        legend[Safe_Str__Benchmark__Section(self.section_b)] = 'Type_Safe Creation'
        return legend

    def create_session(self                                                 ,    # Create sample session
                       title       : str = 'Test Session'                   ,
                       result_count: int = 3                                ) -> Schema__Perf__Benchmark__Session:

        return Schema__Perf__Benchmark__Session(title       = title                                 ,
                                                description = 'Test description'                    ,
                                                results     = self.create_results_dict(result_count),
                                                legend      = self.create_legend()         )




    # ═══════════════════════════════════════════════════════════════════════════════
    # Session with Score Multiplier
    # ═══════════════════════════════════════════════════════════════════════════════

    def create_session_with_scores(self                                     ,    # Create session with scaled scores
                                   title            : str   = 'Test Session',
                                   score_multiplier : float = 1.0           ) -> Schema__Perf__Benchmark__Session:

        results = Dict__Benchmark_Results()

        results[Safe_Str__Benchmark_Id(self.benchmark_id_1)] = self.create_benchmark_result(
            benchmark_id = self.benchmark_id_1                                                            ,
            section      = self.section_a                                                                 ,
            index        = self.index_01                                                                  ,
            name         = 'python__nop'                                                                  ,
            final_score  = int(self.base_score_1 * score_multiplier)                                      ,
            raw_score    = int(self.base_score_1 * score_multiplier * 0.87)                               )

        results[Safe_Str__Benchmark_Id(self.benchmark_id_2)] = self.create_benchmark_result(
            benchmark_id = self.benchmark_id_2                                                            ,
            section      = self.section_a                                                                 ,
            index        = self.index_02                                                                  ,
            name         = 'python__class_empty'                                                          ,
            final_score  = int(self.base_score_2 * score_multiplier)                                      ,
            raw_score    = int(self.base_score_2 * score_multiplier * 0.91)                               )

        results[Safe_Str__Benchmark_Id(self.benchmark_id_3)] = self.create_benchmark_result(
            benchmark_id = self.benchmark_id_3                                                            ,
            section      = self.section_b                                                                 ,
            index        = self.index_01                                                                  ,
            name         = 'type_safe__empty'                                                             ,
            final_score  = int(self.base_score_3 * score_multiplier)                                      ,
            raw_score    = int(self.base_score_3 * score_multiplier * 0.88)                               )

        return Schema__Perf__Benchmark__Session(title       = title               ,
                                                description = 'Test description'  ,
                                                results     = results             ,
                                                legend      = self.create_legend())
    # ═══════════════════════════════════════════════════════════════════════════════
    # Benchmark Runner Helper
    # ═══════════════════════════════════════════════════════════════════════════════

    def run_sample_benchmarks(self, timing):                                     # Run sample benchmarks
        timing.benchmark(Safe_Str__Benchmark_Id(self.benchmark_id_1), self.target_nop)
        timing.benchmark(Safe_Str__Benchmark_Id(self.benchmark_id_2), self.target_simple)
