# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Hypothesis_B - NOP Config in Context
# Tests overhead when Type_Safe__Config IS present but not acted upon
# ═══════════════════════════════════════════════════════════════════════════════
#
# NOTE: This class is IDENTICAL to Type_Safe__Hypothesis_A
# The difference is in the TEST HARNESS - Hypothesis B runs inside:
#   with Type_Safe__Config(skip_validation=True):
#       obj = Type_Safe__Hypothesis_B()
#
# This isolates the question: "Does having config present add overhead?"
#
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.type_safe.type_safe_core.config.static_methods.find_type_safe_config import find_type_safe_config


class Type_Safe__Hypothesis_B(Type_Safe):                                                     # NOP: find config but don't use it
    """
    HYPOTHESIS B: NOP Type_Safe__Config in Context

    Change: Run inside Type_Safe__Config context (vs outside in Hypothesis A)
    Expected: ~0 ns additional overhead (thread-local returns object vs None)
    Purpose: Establish baseline before actually using config flags

    This class is for benchmarking only - do not use in production.
    """

    def __init__(self, **kwargs):
        config = find_type_safe_config()                                                      # Now returns actual config!
        object.__setattr__(self, "__hypothesis_config__", config)                             # Store for inspection
        super().__init__(**kwargs)