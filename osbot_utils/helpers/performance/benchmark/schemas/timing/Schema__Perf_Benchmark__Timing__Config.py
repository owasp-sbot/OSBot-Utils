# ═══════════════════════════════════════════════════════════════════════════════
# Perf_Benchmark__Timing__Config - Configuration for benchmark sessions
# Pure data schema with settings for timing, output, and display
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Description import Safe_Str__Benchmark__Description
from osbot_utils.helpers.performance.benchmark.schemas.safe_str.Safe_Str__Benchmark__Title       import Safe_Str__Benchmark__Title
from osbot_utils.type_safe.Type_Safe                                                             import Type_Safe
from osbot_utils.helpers.performance.benchmark.schemas.collections.Dict__Benchmark__Legend       import Dict__Benchmark__Legend
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Time_Unit                     import Enum__Time_Unit
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Name                import Safe_Str__File__Name
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path                import Safe_Str__File__Path


class Schema__Perf_Benchmark__Timing__Config(Type_Safe):                                 # Benchmark configuration
    title                   : Safe_Str__Benchmark__Title                         # Session title
    description             : Safe_Str__Benchmark__Description                   # Optional subtitle
    output_path             : Safe_Str__File__Path                               # Base path for outputs
    output_prefix           : Safe_Str__File__Name                               # Filename prefix
    legend                  : Dict__Benchmark__Legend                            # Section descriptions
    time_unit               : Enum__Time_Unit = Enum__Time_Unit.NANOSECONDS      # Display unit
    print_to_console        : bool            = True                             # Print on completion
    auto_save_on_completion : bool            = False                            # Save in stop()/__exit__
