# ═══════════════════════════════════════════════════════════════════════════════
# find_type_safe_config - Fast config discovery using thread-local storage
# Performance: ~75 ns (vs ~2,200 ns for stack walking)
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                         import Optional
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                  import Type_Safe__Config
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                  import get_active_config


# ═══════════════════════════════════════════════════════════════════════════════
# find_type_safe_config
# ═══════════════════════════════════════════════════════════════════════════════

def find_type_safe_config() -> Optional[Type_Safe__Config]:                         # ~75 ns lookup!
    return get_active_config()