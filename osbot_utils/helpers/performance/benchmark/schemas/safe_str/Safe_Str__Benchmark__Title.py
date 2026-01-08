import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

class Safe_Str__Benchmark__Title(Safe_Str):                                      # Benchmark session title
    max_length = 200
    regex      = re.compile(r'[^a-zA-Z0-9_ ()\-:,.v\s]')                         # Clean title chars

    # Supports titles like:
    # - "Type_Safe Performance Benchmarks v4"
    # - "Python Baseline Tests"
    # - "Skip __setattr__ Optimization (Phase 2)"
    # - "MGraph-AI: Cache Layer Benchmarks"