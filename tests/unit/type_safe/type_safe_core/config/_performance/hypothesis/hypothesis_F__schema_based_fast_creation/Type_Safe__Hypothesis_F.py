# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Hypothesis_F - Schema-Based Fast Object Creation
# Bypasses Type_Safe.__init__ entirely using pre-computed schema
# ═══════════════════════════════════════════════════════════════════════════════
#
# HOW IT WORKS:
#
# 1. First time a class is seen: generate schema (expensive, cached)
# 2. Subsequent creates: use schema to build __dict__ directly (cheap!)
#
# NORMAL PATH:
#   cls(**kwargs)
#   └─► __init__()
#       └─► __cls_kwargs__()      # Walk MRO, compute defaults
#       └─► type_safe_step_init() # Loop fields, validate each
#           └─► __setattr__()     # Per-field validation
#
# FAST PATH:
#   fast_create(cls, **kwargs)
#   └─► object.__new__(cls)       # Create empty shell
#   └─► schema.static_dict.copy() # Copy pre-computed statics
#   └─► factory_func()            # Create mutables
#   └─► object.__setattr__(__dict__, new_dict)  # Single assignment
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import Any, Dict, Type
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import get_active_config

from Type_Safe__Fast_Create__Schema                                                           import (
    Class__Creation__Schema,
    Field__Schema,
    FIELD_MODE__STATIC,
    FIELD_MODE__FACTORY,
    FIELD_MODE__NESTED,
    get_or_create_schema,
    clear_schema_cache,
    _generating_schema,
)


# ═══════════════════════════════════════════════════════════════════════════════
# Fast Create Function
# ═══════════════════════════════════════════════════════════════════════════════

def fast_create(cls: type, **kwargs) -> Any:
    """Create a Type_Safe instance using pre-computed schema.

    This bypasses Type_Safe.__init__ entirely, directly constructing
    the object's __dict__ from a cached schema.

    Args:
        cls: The Type_Safe class to instantiate
        **kwargs: Field values to set (override defaults)

    Returns:
        New instance of cls with all fields set
    """
    # Get or create schema (cached per class)
    schema = get_or_create_schema(cls)

    # Create empty shell (no __init__ called!)
    obj = object.__new__(cls)

    # Start with static values (single dict.copy - very fast)
    new_dict = schema.static_dict.copy()

    # Add factory-created values (only for fields not in kwargs)
    for field in schema.factory_fields:
        if field.name not in kwargs:
            new_dict[field.name] = field.factory_func()

    # Handle nested Type_Safe objects (recursive fast_create)
    for field in schema.nested_fields:
        if field.name not in kwargs:
            new_dict[field.name] = fast_create(field.nested_class)

    # Apply user kwargs (override defaults)
    new_dict.update(kwargs)

    # Set dict directly (bypasses __init__ and __setattr__)
    object.__setattr__(obj, '__dict__', new_dict)

    return obj


# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe Subclass with Fast Create Support
# ═══════════════════════════════════════════════════════════════════════════════


class Type_Safe__Hypothesis_F(Type_Safe):
    """
    HYPOTHESIS F: Schema-Based Fast Create

    When fast_create=True in config, uses pre-computed schema to create
    objects ~20-25x faster than normal Type_Safe.__init__.
    """

    def __new__(cls, **kwargs):
        config = get_active_config()

        # Use fast_create if enabled AND not currently generating schema for this class
        if config and config.fast_create and cls not in _generating_schema:
            return fast_create(cls, **kwargs)

        # Normal creation path
        return super().__new__(cls)

    def __init__(self, **kwargs):
        config = get_active_config()

        # If fast_create was used, __new__ already set up __dict__
        # Skip __init__ entirely
        if config and config.fast_create and type(self) not in _generating_schema:
            return

        # Normal init path
        super().__init__(**kwargs)


# ═══════════════════════════════════════════════════════════════════════════════
# Utility Functions
# ═══════════════════════════════════════════════════════════════════════════════

def warm_schema_cache(cls: type):
    """Pre-warm the schema cache for a class (and its nested classes).

    Call this during startup for classes you know will be created frequently.
    """
    schema = get_or_create_schema(cls)

    # Recursively warm nested classes
    for field in schema.nested_fields:
        if field.nested_class:
            warm_schema_cache(field.nested_class)