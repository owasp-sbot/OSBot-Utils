# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Step__Fast_Create - Fast Object Creation Using Pre-Computed Schema
# Populates object __dict__ directly, bypassing normal Type_Safe.__init__ flow
# ═══════════════════════════════════════════════════════════════════════════════
#
# HOW IT WORKS:
#   1. Get cached schema for the class
#   2. Start with static_dict.copy() (very fast)
#   3. Call factory functions for mutable fields
#   4. Recursively fast_create nested Type_Safe objects
#   5. Apply kwargs overrides
#   6. Set __dict__ directly via object.__setattr__
#
# PERFORMANCE:
#   Normal path: ~15,000-70,000 ns (MRO walk, validation, conversions)
#   Fast path:   ~800-4,000 ns (schema lookup + dict operations)
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                  import Any
from Type_Safe__Fast_Create__Cache           import type_safe_fast_create_cache


# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Step__Fast_Create
# ═══════════════════════════════════════════════════════════════════════════════

class Type_Safe__Step__Fast_Create:                                               # Fast object creation step

    def create(self, target: Any, **kwargs) -> None:                              # Populate target's __dict__ using schema
        cls    = type(target)
        schema = type_safe_fast_create_cache.get_schema(cls)

        new_dict = schema.static_dict.copy()                                      # Start with static values (fast!)

        for field in schema.factory_fields:                                       # Add factory-created values
            if field.name not in kwargs:
                new_dict[field.name] = field.factory_func()

        for field in schema.nested_fields:                                        # Handle nested Type_Safe objects
            if field.name not in kwargs:
                nested_obj = object.__new__(field.nested_class)                   # Create empty shell
                self.create(nested_obj)                                           # Recursive fast_create
                new_dict[field.name] = nested_obj

        new_dict.update(kwargs)                                                   # Apply user kwargs (override defaults)

        object.__setattr__(target, '__dict__', new_dict)                          # Set dict directly (bypasses __setattr__)


# ═══════════════════════════════════════════════════════════════════════════════
# Module Singleton
# ═══════════════════════════════════════════════════════════════════════════════

type_safe_step_fast_create = Type_Safe__Step__Fast_Create()