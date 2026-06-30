# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Hypothesis_E_v2 - Simplified On-Demand Nested Object Creation
# No permanent per-object tracking - uses temporary flag during __init__ only
# ═══════════════════════════════════════════════════════════════════════════════
#
# SIMPLIFIED APPROACH:
#
# 1. In __init__: Set kwargs[var_name] = None for Type_Safe attrs (prevents creation)
# 2. Set _on_demand__init_complete at START of __init__, DELETE at END
# 3. In __getattribute__: If flag exists → in init → don't auto-create
#                         If flag doesn't exist → after init → auto-create
#
# NO NEED FOR:
# - _on_demand__types dict (per object)
# - Permanent _on_demand__init_complete flag
# - _on_demand__clean_json hack
#
# WHY THIS WORKS:
# - The flag only exists DURING __init__
# - After init completes, flag is deleted
# - json(), from_json(), obj() never see the flag
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import Type, Union, get_origin, get_args
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                               import Type_Safe__Primitive
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                         import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                         import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set                          import Type_Safe__Set
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import get_active_config


def should_create_on_demand(var_type: Type) -> bool:                                          # Module-level to avoid recursion in __getattribute__
    """Determine if a type should be created on demand.

    Returns True for Type_Safe subclasses, excluding:
    - Type_Safe__Primitive (cheap to create)
    - Type_Safe__List/Dict/Set (cheap to create)
    """
    # Handle Optional[X] and Union[X, None]
    origin = get_origin(var_type)
    if origin is Union:
        args = get_args(var_type)
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return should_create_on_demand(non_none[0])
        return False

    # Must be a concrete type
    if not isinstance(var_type, type):
        return False

    # Must be a Type_Safe subclass
    if not issubclass(var_type, Type_Safe):
        return False

    # Exclude Type_Safe__Primitive - they're cheap
    if issubclass(var_type, Type_Safe__Primitive):
        return False

    # Exclude Type_Safe collections - they're also cheap
    if issubclass(var_type, (Type_Safe__List, Type_Safe__Dict, Type_Safe__Set)):
        return False

    return True


class Type_Safe__Hypothesis_E_v2(Type_Safe):
    """
    HYPOTHESIS E v2: Simplified on_demand_nested Implementation

    Strategy:
    1. Set _on_demand__init_complete flag at START of __init__
    2. Set kwargs[var_name] = None for Type_Safe attrs (prevents creation)
    3. DELETE flag at END of __init__
    4. In __getattribute__: Flag exists → in init → don't auto-create
                            Flag gone → after init → auto-create

    No permanent per-object attributes needed!
    """

    def __init__(self, **kwargs):
        config = get_active_config()

        if config and config.on_demand_nested:
            # Set flag to prevent auto-creation during init
            object.__setattr__(self, '_on_demand__init_complete', False)

            try:
                # Walk MRO and set kwargs[var_name] = None for Type_Safe attrs
                for base_cls in type(self).__mro__:
                    if base_cls is object:
                        continue

                    annotations = getattr(base_cls, '__annotations__', {})
                    for var_name, var_type in annotations.items():
                        if var_name.startswith('_'):                                          # Skip private
                            continue
                        if var_name in kwargs:                                                # User provided value
                            continue

                        # Check for explicit default value in class
                        if var_name in base_cls.__dict__:
                            if base_cls.__dict__[var_name] is not None:
                                continue                                                      # Has explicit non-None default

                        if should_create_on_demand(var_type):
                            kwargs[var_name] = None                                           # Prevent auto-creation

                super().__init__(**kwargs)
            finally:
                # Delete flag - now auto-creation is allowed
                try:
                    object.__delattr__(self, '_on_demand__init_complete')
                except AttributeError:
                    pass
        else:
            super().__init__(**kwargs)

    def __getattribute__(self, name: str):
        # Fast path for internal/private attributes
        if name.startswith('_'):
            return object.__getattribute__(self, name)

        # Check if we're still in __init__ (flag exists)
        try:
            object.__getattribute__(self, '_on_demand__init_complete')
            # Flag exists - we're in init, don't auto-create
            return object.__getattribute__(self, name)
        except AttributeError:
            pass  # Flag doesn't exist - we're NOT in init, continue to auto-create logic

        value = object.__getattribute__(self, name)

        # Fast path - most common case (value already exists)
        if value is not None:
            return value

        # Value is None - check if we should auto-create
        # Look up annotation type from class hierarchy
        cls = object.__getattribute__(self, '__class__')

        for base_cls in cls.__mro__:
            if base_cls is object:
                continue
            annotations = getattr(base_cls, '__annotations__', {})
            if name in annotations:
                var_type = annotations[name]
                if should_create_on_demand(var_type):
                    new_value = var_type()                                                    # Create NOW
                    object.__setattr__(self, name, new_value)                                 # Set directly
                    return new_value
                break                                                                         # Found annotation but not Type_Safe

        return value                                                                          # Return None