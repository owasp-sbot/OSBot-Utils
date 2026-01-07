# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Hypothesis_A - Config Lookup Integration
# Tests overhead of adding find_type_safe_config() to Type_Safe.__init__
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.type_safe.type_safe_core.config.static_methods.find_type_safe_config         import find_type_safe_config


class Type_Safe__Hypothesis_A(Type_Safe):                                                     # Hypothesis: add config lookup to init
    """
    HYPOTHESIS A: Config Lookup Integration

    Change: Add find_type_safe_config() call to __init__
    Expected: +200-500ns overhead when no config present
    Purpose: Enable downstream optimizations (skip_setattr, skip_validation, etc.)

    This class is for benchmarking only - do not use in production.
    """

    # For Hypothesis A: just capture config, don't act on it yet
    # Future hypotheses will use config flags to skip expensive operations
    def __init__(self, **kwargs):
        config = find_type_safe_config()                                                      # THE CHANGE: lookup config from stack

        object.__setattr__(self, "__hypothesis_config__", config)                             # Store for inspection (temporary)

        super().__init__(**kwargs)


