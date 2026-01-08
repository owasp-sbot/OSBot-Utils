# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Fast_Create__Cache - Schema Generation and Caching for Fast Creation
# Generates Class__Schema once per class, caches for subsequent fast creates
# ═══════════════════════════════════════════════════════════════════════════════
#
# CACHE STRATEGY:
#   - Regular dict (not WeakKeyDictionary) - classes never get GC'd at runtime
#   - One schema per class, generated on first access
#   - Schema describes how to build __dict__ directly without validation
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                         import Any, Dict, Set, Type
from osbot_utils.type_safe.Type_Safe                                                                import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                                     import Type_Safe__Primitive
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                               import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                               import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set                                import Type_Safe__Set
from osbot_utils.type_safe.type_safe_core.fast_create.schemas.Schema__Type_Safe__Fast_Create__Class import Schema__Type_Safe__Fast_Create__Class
from osbot_utils.type_safe.type_safe_core.fast_create.schemas.Schema__Type_Safe__Fast_Create__Field import FIELD_MODE__STATIC, FIELD_MODE__FACTORY, FIELD_MODE__NESTED, Schema__Type_Safe__Fast_Create__Field

# ═══════════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════════

IMMUTABLE_TYPES = (str, int, float, bool, type(None), bytes, tuple, frozenset)    # Types safe to share references


# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Fast_Create__Cache
# ═══════════════════════════════════════════════════════════════════════════════

class Type_Safe__Fast_Create__Cache:                                              # Schema generation and caching

    schema_cache : Dict[Type, Schema__Type_Safe__Fast_Create__Class]              # Class -> Schema mapping
    generating   : Set[Type]                                                      # Guards against recursion

    def __init__(self):
        self.schema_cache = {}                                                    # Regular dict - classes persist
        self.generating   = set()                                                 # Recursion guard

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    # ═══════════════════════════════════════════════════════════════════════════
    # Public API
    # ═══════════════════════════════════════════════════════════════════════════

    def get_schema(self, cls: Type) -> Schema__Type_Safe__Fast_Create__Class:                             # Get cached schema or create new
        if cls not in self.schema_cache:
            self.schema_cache[cls] = self.generate_schema(cls)
        return self.schema_cache[cls]

    def warm_cache(self, cls: Type) -> None:                                      # Pre-warm cache for class and nested
        schema = self.get_schema(cls)
        for field in schema.nested_fields:                                        # Recursively warm nested classes
            if field.nested_class:
                self.warm_cache(field.nested_class)

    def clear_cache(self) -> None:                                                # Clear all cached schemas (for testing)
        self.schema_cache.clear()
        self.generating.clear()

    def is_generating(self, cls: Type) -> bool:                                   # Check if schema generation in progress
        return cls in self.generating

    # ═══════════════════════════════════════════════════════════════════════════
    # Schema Generation
    # ═══════════════════════════════════════════════════════════════════════════

    def generate_schema(self, cls: Type) -> Schema__Type_Safe__Fast_Create__Class:                        # Generate schema for a Type_Safe class
        self.generating.add(cls)                                                  # Mark as generating (recursion guard)

        try:
            template      = cls()                                                 # Create template to get defaults
            template_dict = template.__dict__.copy()

            fields         = []
            static_dict    = {}
            factory_fields = []
            nested_fields  = []

            for name, value in template_dict.items():
                if name.startswith('_'):                                          # Skip private attributes
                    continue

                field = self.classify_field(name, value)
                fields.append(field)

                if field.mode == FIELD_MODE__STATIC:
                    static_dict[name] = field.static_value
                elif field.mode == FIELD_MODE__FACTORY:
                    factory_fields.append(field)
                elif field.mode == FIELD_MODE__NESTED:
                    nested_fields.append(field)

            return Schema__Type_Safe__Fast_Create__Class(target_class   = cls           ,
                                                         fields         = fields        ,
                                                         static_dict    = static_dict   ,
                                                         factory_fields = factory_fields,
                                                         nested_fields  = nested_fields )
        finally:
            self.generating.discard(cls)                                          # Remove from generating set

    def classify_field(self, name: str, value: Any) -> Schema__Type_Safe__Fast_Create__Field:             # Classify field by its value type
        if self.is_immutable(value):
            return Schema__Type_Safe__Fast_Create__Field(name         = name               ,
                                                         mode         = FIELD_MODE__STATIC ,
                                                         static_value = value              )

        if self.is_nested_type_safe(value):
            return Schema__Type_Safe__Fast_Create__Field(name         = name              ,
                                                         mode         = FIELD_MODE__NESTED,
                                                         nested_class = type(value)       )

        return Schema__Type_Safe__Fast_Create__Field(name         = name                          ,
                                                    mode         = FIELD_MODE__FACTORY           ,
                                                    factory_func = self.get_factory_func(value)  )

    # ═══════════════════════════════════════════════════════════════════════════
    # Value Classification Helpers
    # ═══════════════════════════════════════════════════════════════════════════

    def is_immutable(self, value: Any) -> bool:                                   # Check if value is immutable
        if value is None:
            return True
        return isinstance(value, IMMUTABLE_TYPES)

    def is_type_safe_collection(self, value: Any) -> bool:                        # Check if value is Type_Safe collection
        return isinstance(value, (Type_Safe__List, Type_Safe__Dict, Type_Safe__Set, list, dict, set))

    def is_nested_type_safe(self, value: Any) -> bool:                            # Check if value is nested Type_Safe
        if not isinstance(value, Type_Safe):
            return False
        if isinstance(value, Type_Safe__Primitive):                               # Primitives are not nested
            return False
        if isinstance(value, (Type_Safe__List, Type_Safe__Dict, Type_Safe__Set)): # Collections handled separately
            return False
        return True

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Function Generation
    # ═══════════════════════════════════════════════════════════════════════════

    def get_factory_func(self, value: Any):                                       # Get factory function for value

        if isinstance(value, Type_Safe__List):                                    # Preserve expected_type
            expected_type = value.expected_type
            return lambda: Type_Safe__List(expected_type=expected_type)

        if isinstance(value, Type_Safe__Dict):                                    # Preserve key/value types
            expected_key_type   = value.expected_key_type
            expected_value_type = value.expected_value_type
            return lambda: Type_Safe__Dict(expected_key_type   = expected_key_type  ,
                                           expected_value_type = expected_value_type)

        if isinstance(value, Type_Safe__Set):                                     # Preserve expected_type
            expected_type = value.expected_type
            return lambda: Type_Safe__Set(expected_type=expected_type)

        if isinstance(value, list):
            return list
        if isinstance(value, dict):
            return dict
        if isinstance(value, set):
            return set

        value_type = type(value)                                                  # Default: use type constructor
        return lambda: value_type()


# ═══════════════════════════════════════════════════════════════════════════════
# Module Singleton
# ═══════════════════════════════════════════════════════════════════════════════

type_safe_fast_create_cache = Type_Safe__Fast_Create__Cache()