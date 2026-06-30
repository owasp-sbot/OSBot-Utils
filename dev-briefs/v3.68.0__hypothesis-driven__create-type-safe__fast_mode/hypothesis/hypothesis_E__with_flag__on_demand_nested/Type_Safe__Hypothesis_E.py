# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Hypothesis_E - On-Demand Nested Object Creation
# Creates nested Type_Safe objects only when first accessed
# ═══════════════════════════════════════════════════════════════════════════════
#
# APPROACH: Integrate Type_Safe__On_Demand behavior with Type_Safe__Config
#
# Normal flow:
#   MGraph__Index() → creates edges_index → creates Schema__Data → creates Dicts...
#   (Cascade of object creation even if never accessed)
#
# With on_demand_nested=True:
#   MGraph__Index() → stores types in _on_demand__types, sets attrs to None
#   index.edges_index → created NOW (on first access)
#   index.nodes_index → never created if never accessed!
#
# Key insight: We only check config in __init__. The __getattribute__ override
# just checks if _on_demand__types exists - no config lookup per access.
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import Any, Type, Union, get_origin, get_args
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                               import Type_Safe__Primitive
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                         import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                         import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set                          import Type_Safe__Set
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import get_active_config


class Type_Safe__Hypothesis_E(Type_Safe):
    """
    HYPOTHESIS E: on_demand_nested Flag Implementation

    Change: When on_demand_nested=True, nested Type_Safe objects are created
            only when first accessed, not during __init__.

    Expected: Major improvement for classes with nested Type_Safe attributes
              (20x faster reported in Type_Safe__On_Demand docs)

    This is adapted from Type_Safe__On_Demand but uses Type_Safe__Config.
    """

    def __init__(self, **kwargs):
        config = get_active_config()

        if config and config.on_demand_nested:
            self._init_on_demand(**kwargs)
        else:
            super().__init__(**kwargs)

    def _init_on_demand(self, **kwargs):
        """Initialize with on-demand creation for nested Type_Safe attributes."""

        # Set flags FIRST to prevent premature on-demand creation
        object.__setattr__(self, '_on_demand__init_complete', False)
        object.__setattr__(self, '_on_demand__types', {})

        on_demand_types = {}

        # Walk MRO to find all Type_Safe-typed attributes
        for base_cls in type(self).__mro__:
            if base_cls is object:
                continue
            if not hasattr(base_cls, '__annotations__'):
                continue

            for var_name, var_type in base_cls.__annotations__.items():
                if var_name.startswith('_'):                                                  # Skip private attributes
                    continue
                if var_name in kwargs:                                                        # Skip if caller provided value
                    continue
                if var_name in on_demand_types:                                               # Skip if already marked
                    continue

                # Check if class defines an explicit default value
                if var_name in base_cls.__dict__:
                    value = base_cls.__dict__[var_name]
                    if value is not None:
                        continue                                                              # Has explicit non-None default

                # Check if this type should be on-demand
                if self._should_create_on_demand(var_type):
                    on_demand_types[var_name] = var_type
                    kwargs[var_name] = None                                                   # Prevent Type_Safe auto-creation

        # Store on-demand types for later creation
        object.__setattr__(self, '_on_demand__types', on_demand_types)

        # Call parent init with modified kwargs
        super().__init__(**kwargs)

        # Enable on-demand creation now that init is complete
        object.__setattr__(self, '_on_demand__init_complete', True)

    @staticmethod
    def _should_create_on_demand(var_type: Type) -> bool:
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
                return Type_Safe__Hypothesis_E._should_create_on_demand(non_none[0])
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

    def __getattribute__(self, name: str) -> Any:
        """Override to create Type_Safe objects on first access."""

        # Fast path for internal/private attributes
        if name.startswith('_'):
            return object.__getattribute__(self, name)

        # Don't trigger on-demand creation during __init__
        try:
            init_complete = object.__getattribute__(self, '_on_demand__init_complete')
            if not init_complete:
                return object.__getattribute__(self, name)
        except AttributeError:
            # _on_demand__init_complete doesn't exist - not in on-demand mode
            return object.__getattribute__(self, name)

        # Check if this is a pending on-demand attribute
        try:
            on_demand_types = object.__getattribute__(self, '_on_demand__types')
            if name in on_demand_types:
                var_type = on_demand_types.pop(name)                                          # Remove from pending
                new_value = var_type()                                                        # Create now!
                object.__setattr__(self, name, new_value)                                     # Set directly (bypass validation)
                return new_value
        except AttributeError:
            pass

        return object.__getattribute__(self, name)

    def __repr__(self) -> str:
        """String representation showing on-demand status."""
        try:
            pending_count = len(object.__getattribute__(self, '_on_demand__types'))
            if pending_count > 0:
                return f"<{type(self).__name__} ({pending_count} attrs pending)>"
        except AttributeError:
            pass
        return f"<{type(self).__name__}>"