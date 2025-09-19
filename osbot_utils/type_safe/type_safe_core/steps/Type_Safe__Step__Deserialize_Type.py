import re
import types
from osbot_utils.type_safe.Type_Safe            import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive

TYPE_SAFE__DESERIALIZATION__ALLOWED_MODULES           = { 'builtins'       ,                                # Core allowed modules (always safe)
                                                          'types'          ,
                                                          'typing'         ,
                                                          'enum'           ,
                                                          'decimal'        ,
                                                          'datetime'       ,
                                                          'collections'    ,
                                                          'collections.abc'}


TYPE_SAFE__DESERIALIZATION__ALLOWED_TYPE_SAFE_MODULES = { 'osbot_utils.type_safe'            ,              # Type_Safe framework modules
                                                          'osbot_utils.type_safe.primitives' }

TYPE_SAFE__DESERIALIZATION__DANGEROUS_TYPES           = { 'eval', 'exec', 'compile', '__import__' ,         # Dangerous built-in types to block
                                                          'open', 'input', 'breakpoint', 'help'   ,
                                                          'globals', 'locals', 'vars', 'dir'      }

TYPE_SAFE__DESERIALIZATION__VALID_NAME_PATTERN = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*(\.[a-zA-Z_][a-zA-Z0-9_]*)*$')

class Type_Safe__Step__Deserialize_Type:

    def __init__(self, allow_type_safe_subclasses=True):    # Initialize deserializer with security settings.

        self.allowed_modules = (TYPE_SAFE__DESERIALIZATION__ALLOWED_MODULES          |
                                TYPE_SAFE__DESERIALIZATION__ALLOWED_TYPE_SAFE_MODULES)
        self.allow_type_safe_subclasses = allow_type_safe_subclasses                        # If True, allow any class that inherits from Type_Safe

    def is_module_allowed(self, module_name: str) -> bool:                                  # Check if a module is in the allow listed.
        if module_name in self.allowed_modules:
            return True

        for allowed in self.allowed_modules:
            if module_name.startswith(allowed + '.'):
                return True

        return False

    def is_type_safe_class(self, cls) -> bool:                          # Check if a class inherits from Type_Safe or Type_Safe__Primitive.
        try:
            if issubclass(cls, (Type_Safe, Type_Safe__Primitive)):
                return True
        except (ImportError, TypeError):
            pass
        return False

    def is_typing_generic(self, obj) -> bool:           # Check if an object is a valid typing generic type construct.
        # Check for typing module special forms and generic aliases
        if hasattr(obj, '__module__') and obj.__module__ == 'typing':
            #obj_name = getattr(obj, '__name__', str(obj))                               # These are the typing constructs that are valid for type annotations but aren't regular classes

            if type(obj).__name__ == '_SpecialGenericAlias':                            # Check for _SpecialGenericAlias types (List, Dict, Set, Tuple, etc.)
                return True

            if type(obj).__name__ == '_SpecialForm':                                    # Check for _SpecialForm types (Optional, Union, Any, etc.)
                return True

            if type(obj).__name__ in ('_GenericAlias', '_UnionGenericAlias',            # Check for other typing constructs
                                      '_TupleType', '_CallableType'):
                return True
        return False

    def using_value(self, value):
        if not value:
            return None

        if not isinstance(value, str):
            raise ValueError("Type reference must be a string")

        try:            
            if '.' not in value:                                                        # Check format
                raise ValueError(f"Type reference must include module: '{value}'")

            if not TYPE_SAFE__DESERIALIZATION__VALID_NAME_PATTERN.match(value):
                raise ValueError(f"Invalid type reference format: '{value}'")

            module_name, type_name = value.rsplit('.', 1)
            
            if module_name == 'builtins' and type_name == 'NoneType':                   # Special case for NoneType
                return types.NoneType
            
            if type_name in TYPE_SAFE__DESERIALIZATION__DANGEROUS_TYPES:                # Check deny list
                raise ValueError(f"Type '{type_name}' is deny listed for security")
            
            module_allowed = self.is_module_allowed(module_name)                        # Check module allow listed
            if not module_allowed and not self.allow_type_safe_subclasses:
                allowed_sorted = sorted(self.allowed_modules)
                raise ValueError(f"Module '{module_name}' is not in allowed modules. "
                                 f"Allowed: {allowed_sorted}"                         )

            try:                                                                        # Try import
                module = __import__(module_name, fromlist=[type_name])
            except ImportError as e:
                raise ValueError(f"Could not import module '{module_name}': {str(e)}")

            if not hasattr(module, type_name):                                          # Check type exists
                raise ValueError(f"Type '{type_name}' not found in module '{module_name}'")

            cls = getattr(module, type_name)
            if self.is_typing_generic(cls):
                return cls                                                              # These are valid for type annotations

            if not isinstance(cls, type):                                               # Verify it's a class (for non-typing objects)
                raise ValueError(f"Security alert, in deserialize_type__using_value only classes are allowed, "
                                 f"got {type(cls).__name__} for '{module_name}.{type_name}'")

            if not module_allowed:                                                      # If module wasn't allowed, check Type_Safe
                if not self.is_type_safe_class(cls):
                    allowed_sorted = sorted(self.allowed_modules)
                    raise ValueError(f"Module '{module_name}' is not in allowed modules and "
                                     f"'{type_name}' does not inherit from Type_Safe. "
                                     f"Allowed modules: {allowed_sorted}")

            return cls

        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Could not reconstruct type from '{value}': {str(e)}")        # This should rarely be reached now

type_safe_step_deserialize_type = Type_Safe__Step__Deserialize_Type()