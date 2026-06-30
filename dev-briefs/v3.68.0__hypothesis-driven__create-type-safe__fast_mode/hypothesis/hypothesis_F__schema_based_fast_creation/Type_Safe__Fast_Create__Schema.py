# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Fast_Create__Schema - Schema Classes for Fast Object Creation
# Defines the structure that describes how to quickly create Type_Safe objects
# ═══════════════════════════════════════════════════════════════════════════════
#
# FIELD MODES:
#
# 'static'    - Immutable value, can share reference (str, int, bool, None)
# 'factory'   - Mutable, needs fresh instance (List, Dict, Set, Obj_Id)
# 'nested'    - Nested Type_Safe, recursive fast_create
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import Any, Dict, List, Type, Union, get_origin, get_args
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                               import Type_Safe__Primitive
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                         import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                         import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set                          import Type_Safe__Set


# ═══════════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════════

FIELD_MODE__STATIC    = 'static'                                                              # Immutable, share reference
FIELD_MODE__FACTORY   = 'factory'                                                             # Mutable, create fresh each time
FIELD_MODE__NESTED    = 'nested'                                                              # Nested Type_Safe, recursive create

IMMUTABLE_TYPES = (str, int, float, bool, type(None), bytes, tuple, frozenset)


# ═══════════════════════════════════════════════════════════════════════════════
# Schema Classes
# ═══════════════════════════════════════════════════════════════════════════════

class Field__Schema:
    """Schema for a single field - describes how to create its value"""
    __slots__ = ['name', 'mode', 'static_value', 'factory_func', 'nested_class']

    def __init__(self,
                 name         : str,
                 mode         : str,
                 static_value : Any      = None,
                 factory_func : callable = None,
                 nested_class : type     = None):
        self.name         = name
        self.mode         = mode
        self.static_value = static_value
        self.factory_func = factory_func                                                      # Callable that creates fresh instance
        self.nested_class = nested_class

    def __repr__(self):
        return f"<Field__Schema {self.name}: {self.mode}>"


class Class__Creation__Schema:
    """Schema for a Type_Safe class - describes how to create instances quickly"""
    __slots__ = ['target_class', 'fields', 'static_dict', 'factory_fields', 'nested_fields']

    def __init__(self,
                 target_class   : type,
                 fields         : List[Field__Schema],
                 static_dict    : Dict[str, Any],
                 factory_fields : List[Field__Schema],
                 nested_fields  : List[Field__Schema]):
        self.target_class   = target_class
        self.fields         = fields
        self.static_dict    = static_dict
        self.factory_fields = factory_fields
        self.nested_fields  = nested_fields

    def __repr__(self):
        return f"<Class__Creation__Schema {self.target_class.__name__}: {len(self.fields)} fields>"


    def print_schema(self):
        """Print a formatted view of this schema"""
        lines = []
        lines.append(f"")
        lines.append(f"╔═══════════════════════════════════════════════════════════════════════════════")
        lines.append(f"║ SCHEMA: {self.target_class.__name__}")
        lines.append(f"╠═══════════════════════════════════════════════════════════════════════════════")
        lines.append(f"║ Total fields: {len(self.fields)}")
        lines.append(f"║   - Static:  {len(self.static_dict)} (shared immutable values)")
        lines.append(f"║   - Factory: {len(self.factory_fields)} (fresh instance each time)")
        lines.append(f"║   - Nested:  {len(self.nested_fields)} (recursive fast_create)")
        lines.append(f"╠═══════════════════════════════════════════════════════════════════════════════")

        # Static fields
        if self.static_dict:
            lines.append(f"║ STATIC FIELDS (copy reference):")
            for name, value in self.static_dict.items():
                value_repr = repr(value) if len(repr(value)) < 40 else repr(value)[:37] + "..."
                lines.append(f"║   • {name}: {type(value).__name__} = {value_repr}")

        # Factory fields
        if self.factory_fields:
            lines.append(f"║ FACTORY FIELDS (create fresh):")
            for field in self.factory_fields:
                func_name = getattr(field.factory_func, '__name__', str(field.factory_func))
                if hasattr(field.factory_func, '__closure__') and field.factory_func.__closure__:
                    # Lambda with closure - try to get more info
                    func_name = f"λ → {field.factory_func()!r}"[:50]
                lines.append(f"║   • {field.name}: {func_name}")

        # Nested fields
        if self.nested_fields:
            lines.append(f"║ NESTED FIELDS (recursive fast_create):")
            for field in self.nested_fields:
                lines.append(f"║   • {field.name}: {field.nested_class.__name__}")

        lines.append(f"╚═══════════════════════════════════════════════════════════════════════════════")
        lines.append(f"")

        print("\n".join(lines))
# ═══════════════════════════════════════════════════════════════════════════════
# Schema Generation
# ═══════════════════════════════════════════════════════════════════════════════

def is_immutable(value: Any) -> bool:
    """Check if a value is immutable and can be safely shared"""
    if value is None:
        return True
    if isinstance(value, IMMUTABLE_TYPES):
        return True
    return False


def is_type_safe_collection(value: Any) -> bool:
    """Check if value is a Type_Safe collection"""
    return isinstance(value, (Type_Safe__List, Type_Safe__Dict, Type_Safe__Set, list, dict, set))


def is_nested_type_safe(value: Any) -> bool:
    """Check if value is a nested Type_Safe object (not primitive, not collection)"""
    if not isinstance(value, Type_Safe):
        return False
    if isinstance(value, Type_Safe__Primitive):
        return False
    if isinstance(value, (Type_Safe__List, Type_Safe__Dict, Type_Safe__Set)):
        return False
    return True


def get_factory_function(value: Any):
    """Get a factory function to create a fresh instance with same config.

    For Type_Safe__List/Dict/Set, we need to preserve the expected_type info.
    Returns a callable that creates a new instance with the same configuration.
    """
    if isinstance(value, Type_Safe__List):
        expected_type = value.expected_type
        return lambda: Type_Safe__List(expected_type=expected_type)

    if isinstance(value, Type_Safe__Dict):
        expected_key_type = value.expected_key_type
        expected_value_type = value.expected_value_type
        return lambda: Type_Safe__Dict(expected_key_type=expected_key_type,
                                        expected_value_type=expected_value_type)

    if isinstance(value, Type_Safe__Set):
        expected_type = value.expected_type
        return lambda: Type_Safe__Set(expected_type=expected_type)

    if isinstance(value, list):
        return list
    if isinstance(value, dict):
        return dict
    if isinstance(value, set):
        return set

    # For Type_Safe__Primitive and other types, use the type
    value_type = type(value)
    return lambda: value_type()


def generate_schema(cls: type) -> Class__Creation__Schema:
    """Generate a creation schema for a Type_Safe class.

    This is called once per class (cached). It creates a template instance
    to discover the default values, then classifies each field.

    Args:
        cls: The Type_Safe class to generate schema for

    Returns:
        Class__Creation__Schema describing how to fast-create instances
    """
    # Mark this class as being generated (prevents recursion)
    _generating_schema.add(cls)

    try:
        # Create one instance normally to get defaults
        # This is expensive but only done once per class
        template = cls()
        template_dict = template.__dict__.copy()

        fields         = []
        static_dict    = {}
        factory_fields = []
        nested_fields  = []

        for name, value in template_dict.items():
            if name.startswith('_'):                                                              # Skip private attributes
                continue

            # Classify the field
            if is_immutable(value):
                field = Field__Schema(
                    name         = name,
                    mode         = FIELD_MODE__STATIC,
                    static_value = value
                )
                static_dict[name] = value

            elif is_nested_type_safe(value):
                field = Field__Schema(
                    name         = name,
                    mode         = FIELD_MODE__NESTED,
                    nested_class = type(value)
                )
                nested_fields.append(field)

            else:  # Mutable (collections, primitives, etc.)
                field = Field__Schema(
                    name         = name,
                    mode         = FIELD_MODE__FACTORY,
                    factory_func = get_factory_function(value)
                )
                factory_fields.append(field)

            fields.append(field)

        return Class__Creation__Schema(
            target_class   = cls,
            fields         = fields,
            static_dict    = static_dict,
            factory_fields = factory_fields,
            nested_fields  = nested_fields
        )
    finally:
        # Remove from generating set
        _generating_schema.discard(cls)


# ═══════════════════════════════════════════════════════════════════════════════
# Schema Cache
# ═══════════════════════════════════════════════════════════════════════════════

_schema_cache: Dict[type, Class__Creation__Schema] = {}

# Flag to prevent recursion during schema generation
_generating_schema: set = set()


def get_or_create_schema(cls: type) -> Class__Creation__Schema:
    """Get cached schema or create new one"""
    if cls not in _schema_cache:
        _schema_cache[cls] = generate_schema(cls)
        #_schema_cache[cls].print_schema()

    return _schema_cache[cls]


def clear_schema_cache():
    """Clear the schema cache (useful for testing)"""
    _schema_cache.clear()
    _generating_schema.clear()