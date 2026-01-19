# ═══════════════════════════════════════════════════════════════════════════════
# Class__Schema - Schema for a Type_Safe Class
# Describes how to quickly create instances using pre-computed field information
# ═══════════════════════════════════════════════════════════════════════════════
#
# STRUCTURE:
#   target_class   - The Type_Safe class this schema describes
#   fields         - All Field__Schema instances
#   static_dict    - Pre-built dict of static field values (copied on create)
#   factory_fields - Fields requiring fresh instances
#   nested_fields  - Fields requiring recursive fast_create
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                              import Any, Dict, List, Type
from .Field__Schema                      import Field__Schema


# ═══════════════════════════════════════════════════════════════════════════════
# Class__Schema
# ═══════════════════════════════════════════════════════════════════════════════

class Class__Schema:                                                              # Schema for fast object creation
    __slots__ = ('target_class'  ,                                                # The class this schema describes
                 'fields'        ,                                                # All fields
                 'static_dict'   ,                                                # Pre-built dict of static values
                 'factory_fields',                                                # Fields needing fresh instances
                 'nested_fields' )                                                # Fields needing recursive create

    def __init__(self                                      ,
                 target_class   : Type                     ,
                 fields         : List[Field__Schema]      ,
                 static_dict    : Dict[str, Any]           ,
                 factory_fields : List[Field__Schema]      ,
                 nested_fields  : List[Field__Schema]      ):
        self.target_class   = target_class
        self.fields         = fields
        self.static_dict    = static_dict
        self.factory_fields = factory_fields
        self.nested_fields  = nested_fields

    def __repr__(self):
        return f"<Class__Schema {self.target_class.__name__}: {len(self.fields)} fields>"

    def print_schema(self):                                                       # Print formatted schema view
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

        if self.static_dict:
            lines.append(f"║ STATIC FIELDS (copy reference):")
            for name, value in self.static_dict.items():
                value_repr = repr(value) if len(repr(value)) < 40 else repr(value)[:37] + "..."
                lines.append(f"║   • {name}: {type(value).__name__} = {value_repr}")

        if self.factory_fields:
            lines.append(f"║ FACTORY FIELDS (create fresh):")
            for field in self.factory_fields:
                func_name = getattr(field.factory_func, '__name__', str(field.factory_func))
                if hasattr(field.factory_func, '__closure__') and field.factory_func.__closure__:
                    func_name = f"λ → {field.factory_func()!r}"[:50]
                lines.append(f"║   • {field.name}: {func_name}")

        if self.nested_fields:
            lines.append(f"║ NESTED FIELDS (recursive fast_create):")
            for field in self.nested_fields:
                lines.append(f"║   • {field.name}: {field.nested_class.__name__}")

        lines.append(f"╚═══════════════════════════════════════════════════════════════════════════════")
        lines.append(f"")

        print("\n".join(lines))