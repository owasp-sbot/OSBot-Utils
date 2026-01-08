# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Hypothesis_D - Skip Conversion in Init
# Surgical change: bypass convert_value_to_type_safe_objects() when skip_conversion=True
# ═══════════════════════════════════════════════════════════════════════════════
#
# APPROACH: Override __init__ to conditionally skip type conversion for kwargs.
#
# Normal flow (kwargs):
#   MyClass(items=['a', 'b']) → convert_value_to_type_safe_objects() → Type_Safe__List
#
# With skip_conversion=True:
#   MyClass(items=['a', 'b']) → items stays as plain list (no conversion)
#
# IMPORTANT: Default values are NOT affected - they're created via default_value()
#            in __cls_kwargs__, which runs before this init logic.
#
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import get_active_config
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Set_Attr                     import type_safe_step_set_attr
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Init                         import type_safe_step_init


class Type_Safe__Hypothesis_D(Type_Safe):
    """
    HYPOTHESIS D: skip_conversion Flag in Init

    Changes:
    1. skip_validation in __setattr__ (from Hypothesis C)
    2. skip_conversion in __init__ (NEW)

    Expected: Additional savings when providing kwargs
    """

    def __init__(self, **kwargs):
        config = get_active_config()

        if config and config.skip_conversion:
            self._init_skip_conversion(**kwargs)                                              # Fast path - skip conversion
        else:
            super().__init__(**kwargs)                                                        # Normal path - full conversion

    def _init_skip_conversion(self, **kwargs):
        """Init without type conversion for kwargs.

        This is a copy of Type_Safe.__init__ + type_safe_step_init.init()
        but skips the convert_value_to_type_safe_objects() call.

        Default values are still created normally via __cls_kwargs__.
        """
        class_kwargs = self.__cls_kwargs__(provided_kwargs=kwargs)                            # Still process class kwargs normally

        # Set defaults (from type_safe_step_init.init, loop 1)
        for (key, value) in class_kwargs.items():
            if hasattr(self, key):
                existing_value = getattr(self, key)
                if existing_value is not None:
                    setattr(self, key, existing_value)
                    continue
            setattr(self, key, value)

        # Set provided kwargs WITHOUT conversion (from type_safe_step_init.init, loop 2)
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                if value is not None:
                    # SKIP: value = type_safe_step_init.convert_value_to_type_safe_objects(self, key, value)
                    setattr(self, key, value)                                                 # Direct assignment
            else:
                raise ValueError(f"{self.__class__.__name__} has no attribute '{key}' and cannot be assigned the value '{value}'. "
                                 f"Use {self.__class__.__name__}.__default_kwargs__() see what attributes are available") from None

    def __setattr__(self, name, value):
        """From Hypothesis C: skip validation when configured."""
        config = get_active_config()
        if config and config.skip_validation:
            object.__setattr__(self, name, value)                                             # Direct bypass - no validation
        else:
            type_safe_step_set_attr.setattr(super(), self, name, value)                       # Normal path - full validation