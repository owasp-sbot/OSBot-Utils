# ═══════════════════════════════════════════════════════════════════════════════
# Field__Schema - Schema for a Single Field in a Type_Safe Class
# Describes how to create a field's value during fast object creation
# ═══════════════════════════════════════════════════════════════════════════════
#
# FIELD MODES:
#   'static'  - Immutable value, can share reference (str, int, bool, None)
#   'factory' - Mutable, needs fresh instance each time (List, Dict, Set)
#   'nested'  - Nested Type_Safe object, recursive fast_create
#
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                       import Any, Callable, Optional, Type


# ═══════════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════════

FIELD_MODE__STATIC  = 'static'                                                    # Immutable, share reference
FIELD_MODE__FACTORY = 'factory'                                                   # Mutable, create fresh each time
FIELD_MODE__NESTED  = 'nested'                                                    # Nested Type_Safe, recursive create


# ═══════════════════════════════════════════════════════════════════════════════
# Field__Schema
# ═══════════════════════════════════════════════════════════════════════════════

class Field__Schema:                                                              # Schema for a single field
    __slots__ = ('name'        ,                                                  # Field name
                 'mode'        ,                                                  # Creation mode (static/factory/nested)
                 'static_value',                                                  # Value for static fields
                 'factory_func',                                                  # Callable for factory fields
                 'nested_class')                                                  # Class for nested Type_Safe fields

    def __init__(self                                    ,
                 name         : str                      ,
                 mode         : str                      ,
                 static_value : Any            = None    ,
                 factory_func : Callable       = None    ,
                 nested_class : Optional[Type] = None    ):
        self.name         = name
        self.mode         = mode
        self.static_value = static_value
        self.factory_func = factory_func
        self.nested_class = nested_class

    def __repr__(self):
        return f"<Field__Schema {self.name}: {self.mode}>"