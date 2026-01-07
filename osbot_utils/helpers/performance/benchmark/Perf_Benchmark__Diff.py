# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Benchmark__Diff - Multi-session comparison and evolution tracking
# Load and compare benchmark sessions from saved JSON files
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Comparison      import Schema__Perf__Benchmark__Comparison
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Evolution       import Schema__Perf__Benchmark__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Result          import Schema__Perf__Benchmark__Result
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Benchmark__Session         import Schema__Perf__Benchmark__Session
from osbot_utils.helpers.performance.benchmark.schemas.benchmark.Schema__Perf__Comparison__Two            import Schema__Perf__Comparison__Two
from osbot_utils.type_safe.Type_Safe                                                                      import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Float                                                     import Safe_Float
from osbot_utils.type_safe.primitives.core.Safe_UInt                                                      import Safe_UInt
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                         import Safe_Str__File__Path
from osbot_utils.utils.Files                                                                              import file_exists, files_list, file_extension
from osbot_utils.utils.Json                                                                               import json_load_file
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Sessions               import List__Benchmark_Sessions
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Comparisons            import List__Benchmark_Comparisons
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Benchmark_Evolutions             import List__Benchmark_Evolutions
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Titles                           import List__Titles
from osbot_utils.helpers.performance.benchmark.schemas.collections.List__Scores                           import List__Scores
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark_Results                import Dict__Benchmark_Results
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Evolution                            import Schema__Perf__Evolution
from osbot_utils.helpers.performance.benchmark.schemas.Schema__Perf__Statistics                           import Schema__Perf__Statistics
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Comparison__Status                     import Enum__Comparison__Status
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Benchmark__Trend                       import Enum__Benchmark__Trend


class Perf_Benchmark__Diff(Type_Safe):                                           # Multi-session comparison
    sessions : List__Benchmark_Sessions                                          # Loaded sessions


    # ═══════════════════════════════════════════════════════════════════════════════
    # Loading Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def load_session(self                                                   ,
                     filepath: Safe_Str__File__Path                         ) -> 'Perf_Benchmark__Diff':
        if file_exists(filepath) is False:
            return self

        data = json_load_file(filepath)
        if data is None:
            return self

        session = self.parse_session_data(data)
        if session is not None:
            self.sessions.append(session)

        return self

    def load_folder(self                                                    ,
                    folder_path: Safe_Str__File__Path                       ) -> 'Perf_Benchmark__Diff':
        all_files  = files_list(folder_path)
        json_files = [f for f in all_files if file_extension(f) == '.json']

        for filepath in sorted(json_files):
            self.load_session(filepath)

        return self

    def parse_session_data(self, data: dict) -> Schema__Perf__Benchmark__Session:

        results = Dict__Benchmark_Results()

        for benchmark_id, result_data in data.get('results', {}).items():
            result = Schema__Perf__Benchmark__Result.from_json(result_data)
            results[benchmark_id] = result

        return Schema__Perf__Benchmark__Session(title       = data.get('title', '')      ,
                                                description = data.get('description', ''),
                                                results     = results                    )


    # ═══════════════════════════════════════════════════════════════════════════════
    # Trend Calculation
    # ═══════════════════════════════════════════════════════════════════════════════

    def calculate_trend(self, change_pct: float) -> Enum__Benchmark__Trend:      # Determine trend
        if change_pct > 10:
            return Enum__Benchmark__Trend.STRONG_IMPROVEMENT
        if change_pct > 0:
            return Enum__Benchmark__Trend.IMPROVEMENT
        if change_pct < -10:
            return Enum__Benchmark__Trend.STRONG_REGRESSION
        if change_pct < 0:
            return Enum__Benchmark__Trend.REGRESSION
        return Enum__Benchmark__Trend.UNCHANGED


    # ═══════════════════════════════════════════════════════════════════════════════
    # Comparison Methods
    # ═══════════════════════════════════════════════════════════════════════════════

    def compare_two(self                                               ,
                    session_a: Schema__Perf__Benchmark__Session = None ,
                    session_b: Schema__Perf__Benchmark__Session = None ) -> Schema__Perf__Comparison__Two:

        if session_a is None and session_b is None:
            if len(self.sessions) == 0:
                return Schema__Perf__Comparison__Two(status = Enum__Comparison__Status.ERROR_NO_SESSIONS          ,
                                                     error  = 'No sessions loaded'                                )
            if len(self.sessions) < 2:
                return Schema__Perf__Comparison__Two(status = Enum__Comparison__Status.ERROR_INSUFFICIENT_SESSIONS,
                                                     error  = 'Need at least 2 sessions to compare'               )
            session_a = self.sessions[0]
            session_b = self.sessions[-1]

        comparisons = List__Benchmark_Comparisons()
        all_ids     = set(session_a.results.keys()) | set(session_b.results.keys())

        for benchmark_id in sorted(all_ids):
            result_a = session_a.results.get(benchmark_id)
            result_b = session_b.results.get(benchmark_id)

            if result_a is None or result_b is None:
                continue

            score_a = int(result_a.final_score)
            score_b = int(result_b.final_score)

            if score_a > 0:
                change_pct = ((score_a - score_b) / score_a) * 100
            else:
                change_pct = 0.0

            comparison = Schema__Perf__Benchmark__Comparison(benchmark_id   = benchmark_id             ,
                                                             name           = result_b.name            ,
                                                             score_a        = Safe_UInt(score_a)       ,
                                                             score_b        = Safe_UInt(score_b)       ,
                                                             change_percent = Safe_Float(change_pct)   ,
                                                             trend          = self.calculate_trend(change_pct))
            comparisons.append(comparison)

        if len(comparisons) == 0:
            return Schema__Perf__Comparison__Two(status = Enum__Comparison__Status.ERROR_NO_COMMON_BENCHMARKS,
                                                 error  = 'No common benchmarks between sessions'            )

        title_a = session_a.title or 'Session A'
        title_b = session_b.title or 'Session B'

        return Schema__Perf__Comparison__Two(status      = Enum__Comparison__Status.SUCCESS,
                                             title_a     = title_a                         ,
                                             title_b     = title_b                         ,
                                             comparisons = comparisons                     )

    def compare_all(self) -> Schema__Perf__Evolution:                            # Multi-session evolution
        if len(self.sessions) == 0:
            return Schema__Perf__Evolution(status = Enum__Comparison__Status.ERROR_NO_SESSIONS,
                                           error  = 'No sessions loaded'                      )

        if len(self.sessions) < 2:
            return Schema__Perf__Evolution(status = Enum__Comparison__Status.ERROR_INSUFFICIENT_SESSIONS,
                                           error  = 'Need at least 2 sessions for comparison'           )

        titles = List__Titles()
        for i, session in enumerate(self.sessions):
            title = session.title or f'Session {i+1}'
            titles.append(title)

        all_ids = set()
        for session in self.sessions:
            all_ids.update(session.results.keys())

        evolutions = List__Benchmark_Evolutions()

        for benchmark_id in sorted(all_ids):
            scores = List__Scores()
            name   = ''
            first  = None
            last   = None

            for session in self.sessions:
                result = session.results.get(benchmark_id)
                if result is not None:
                    if not name:
                        name = result.name
                    score = int(result.final_score)
                    scores.append(Safe_UInt(score))
                    if first is None:
                        first = score
                    last = score
                else:
                    scores.append(Safe_UInt(0))

            if first is not None and last is not None and first > 0:
                change_pct = ((first - last) / first) * 100
            else:
                change_pct = 0.0

            evolution = Schema__Perf__Benchmark__Evolution(benchmark_id   = benchmark_id                  ,
                                                           name           = name or benchmark_id          ,
                                                           scores         = scores                        ,
                                                           first_score    = Safe_UInt(first or 0)         ,
                                                           last_score     = Safe_UInt(last or 0)          ,
                                                           change_percent = Safe_Float(change_pct)        ,
                                                           trend          = self.calculate_trend(change_pct))
            evolutions.append(evolution)

        return Schema__Perf__Evolution(status        = Enum__Comparison__Status.SUCCESS     ,
                                       session_count = Safe_UInt(len(self.sessions))        ,
                                       titles        = titles                               ,
                                       evolutions    = evolutions                           )

    def statistics(self) -> Schema__Perf__Statistics:                            # Summary statistics
        if len(self.sessions) == 0:
            return Schema__Perf__Statistics(status = Enum__Comparison__Status.ERROR_NO_SESSIONS,
                                            error  = 'No sessions loaded'                      )

        if len(self.sessions) < 2:
            return Schema__Perf__Statistics(status = Enum__Comparison__Status.ERROR_INSUFFICIENT_SESSIONS,
                                            error  = 'Need at least 2 sessions for statistics'           )

        first_session = self.sessions[0]
        last_session  = self.sessions[-1]

        improvements = []
        regressions  = []

        all_ids = set(first_session.results.keys()) & set(last_session.results.keys())

        for benchmark_id in all_ids:
            first_score = int(first_session.results[benchmark_id].final_score)
            last_score  = int(last_session.results[benchmark_id].final_score)

            if first_score > 0:
                change_pct = ((first_score - last_score) / first_score) * 100
                name       = last_session.results[benchmark_id].name

                comparison = Schema__Perf__Benchmark__Comparison(benchmark_id   = benchmark_id                  ,
                                                                 name           = name                          ,
                                                                 score_a        = Safe_UInt(first_score)        ,
                                                                 score_b        = Safe_UInt(last_score)         ,
                                                                 change_percent = Safe_Float(change_pct)        ,
                                                                 trend          = self.calculate_trend(change_pct))

                if change_pct > 0:
                    improvements.append(comparison)
                elif change_pct < 0:
                    regressions.append(comparison)

        avg_improvement = 0.0
        best_improvement = None
        if improvements:
            avg_improvement  = sum(c.change_percent for c in improvements) / len(improvements)
            best_improvement = max(improvements, key=lambda c: c.change_percent)

        avg_regression   = 0.0
        worst_regression = None
        if regressions:
            avg_regression   = sum(abs(c.change_percent) for c in regressions) / len(regressions)
            worst_regression = min(regressions, key=lambda c: c.change_percent)

        return Schema__Perf__Statistics(status            = Enum__Comparison__Status.SUCCESS     ,
                                        session_count     = Safe_UInt(len(self.sessions))        ,
                                        benchmark_count   = Safe_UInt(len(all_ids))              ,
                                        improvement_count = Safe_UInt(len(improvements))         ,
                                        regression_count  = Safe_UInt(len(regressions))          ,
                                        avg_improvement   = Safe_Float(avg_improvement)          ,
                                        avg_regression    = Safe_Float(avg_regression)           ,
                                        best_improvement  = best_improvement                     ,
                                        worst_regression  = worst_regression                     )