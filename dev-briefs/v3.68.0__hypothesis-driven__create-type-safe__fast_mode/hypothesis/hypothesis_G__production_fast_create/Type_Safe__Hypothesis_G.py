# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Hypothesis_G - Production-Ready Fast Object Creation
# Minimal changes to Type_Safe to enable schema-based fast creation
# ═══════════════════════════════════════════════════════════════════════════════
#
# CHANGES FROM Type_Safe:
#   __init__    - Check config, delegate to fast_create or normal path
#   __setattr__ - Check config, bypass validation when skip_validation=True
#
# USAGE:
#   # Normal creation (full validation)
#   obj = MyClass(name='test')
#
#   # Fast creation (schema-based, ~10-20x faster)
#   with Type_Safe__Config(fast_create=True):
#       obj = MyClass(name='test')
#
#   # Fast creation + fast mutations
#   with Type_Safe__Config(fast_create=True, skip_validation=True):
#       obj = MyClass(name='test')
#       obj.name = 'updated'  # Also fast
#
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Set_Attr   import type_safe_step_set_attr
from Type_Safe__Config                                                      import get_active_config
from Type_Safe__Step__Fast_Create                                           import type_safe_step_fast_create
from Type_Safe__Fast_Create__Cache                                          import type_safe_fast_create_cache


# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Hypothesis_G
# ═══════════════════════════════════════════════════════════════════════════════

class Type_Safe__Hypothesis_G(Type_Safe):                                         # Type_Safe with fast creation support

    def __init__(self, **kwargs):
        config = get_active_config()

        if config and config.fast_create:
            if type_safe_fast_create_cache.is_generating(type(self)) is False:    # Not during schema generation
                type_safe_step_fast_create.create(self, **kwargs)
                return

        super().__init__(**kwargs)                                                # Normal path

    def __setattr__(self, name, value):
        config = get_active_config()

        if config and config.skip_validation:
            object.__setattr__(self, name, value)                                 # Direct bypass
        else:
            type_safe_step_set_attr.setattr(super(), self, name, value)           # Normal validation