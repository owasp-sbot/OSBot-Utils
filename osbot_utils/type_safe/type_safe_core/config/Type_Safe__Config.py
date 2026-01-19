# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Config - Configuration for Type_Safe Performance Optimization
# Context-aware configuration using thread-local storage for fast lookup (~75ns)
# ═══════════════════════════════════════════════════════════════════════════════
#
# FLAGS:
#   fast_create     - Use schema-based object creation (bypasses __init__ flow)
#   skip_validation - Bypass __setattr__ validation (for trusted data)
#
# FUTURE FLAGS (not yet implemented):
#   immutable       - Prevent attribute addition after __init__ completes
#
# ═══════════════════════════════════════════════════════════════════════════════

import threading
from typing                                                                       import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# Thread-Local Storage
# ═══════════════════════════════════════════════════════════════════════════════

_thread_local = threading.local()                                                 # Per-thread config storage


def get_active_config() -> Optional['Type_Safe__Config']:                         # Fast lookup (~75 ns)
    return getattr(_thread_local, 'config', None)


def set_active_config(config: Optional['Type_Safe__Config']) -> None:             # Set active config
    _thread_local.config = config

def type_safe__show_detailed_errors() -> bool:
    active_config = get_active_config()
    if active_config:
        return active_config.detailed_errors
    return False

# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Config
# ═══════════════════════════════════════════════════════════════════════════════

class Type_Safe__Config:                                                          # Configuration for Type_Safe optimization

    __slots__ = ('fast_create'     ,                                              # Use schema-based creation
                 'skip_validation' ,                                              # Bypass __setattr__ validation
                 '_previous_config',                                               # For nested context restoration
                 'detailed_errors'
                 )

    def __init__(self                         ,
                 fast_create     : bool = False,
                 skip_validation : bool = False,
                 detailed_errors : bool = False,):
        self.fast_create      = fast_create
        self.skip_validation  = skip_validation
        self.detailed_errors  = detailed_errors
        self._previous_config = None                                              # Stores previous config for nesting

    def __enter__(self):                                                          # Context manager entry
        self._previous_config = get_active_config()                               # Save current (for nested contexts)
        set_active_config(self)                                                   # Set ourselves as active
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):                                # Context manager exit
        set_active_config(self._previous_config)                                  # Restore previous (or None)
        return False

    def __repr__(self):                                                           # String representation
        flags = []
        if self.fast_create     : flags.append('fast_create')
        if self.skip_validation : flags.append('skip_validation')

        if flags:
            return f"Type_Safe__Config({', '.join(flags)})"
        return "Type_Safe__Config(default)"

    def __eq__(self, other):                                                      # Equality comparison
        if not isinstance(other, Type_Safe__Config):
            return False
        return (self.fast_create     == other.fast_create     and
                self.skip_validation == other.skip_validation    )

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Methods
    # ═══════════════════════════════════════════════════════════════════════════

    @classmethod
    def fast_mode(cls) -> 'Type_Safe__Config':                                    # Maximum performance mode
        return cls(fast_create     = True,
                   skip_validation = True)
