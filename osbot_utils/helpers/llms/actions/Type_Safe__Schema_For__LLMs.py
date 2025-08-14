import re
from typing                                                         import Type, Any, List, Dict, Tuple, Set, Optional, Union, get_origin, get_args
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe      import type_safe
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Cache   import type_safe_cache
from osbot_utils.type_safe.validators.Type_Safe__Validator          import Type_Safe__Validator
from osbot_utils.type_safe.validators.Validator__Min                import Validator__Min
from osbot_utils.type_safe.validators.Validator__Max                import Validator__Max
from osbot_utils.type_safe.validators.Validator__Regex              import Validator__Regex
from osbot_utils.type_safe.validators.Validator__One_Of             import Validator__One_Of
from osbot_utils.helpers.python_compatibility.python_3_8            import Annotated
import inspect


class Type_Safe__Schema_For__LLMs(Type_Safe):

    @type_safe
    def export(self, target : Type[Type_Safe]) -> dict:                                 # Target Type_Safe class to convert, Returns JSON Schema object
        return self.export__type_safe(target)

    def export__type_safe(self, target: Type[Type_Safe]) -> dict:                       # Target Type_Safe class to convert, Returns JSON Schema object
        annotations = type_safe_cache.get_class_annotations(target)
        properties  = {}
        required    = []

        schema = { "type"      : "object"   ,
                   "properties": properties }

        if target.__doc__:                                                              # Add description if available and requested
            schema["description"] = self.clean_docstring(target.__doc__)

        for var_name, var_type in annotations:                                          # Process all annotated fields

            prop_schema          = self.get_property_schema(target, var_name, var_type)
            properties[var_name] = prop_schema

            if self.is_required_property(target, var_name, var_type):                # Check if property is required
                required.append(var_name)

        if required:                                                                  # Add required fields if any
            schema["required"] = required

        return schema

    def clean_docstring(self, docstring: str) -> str:                                   # Cleans up a docstring
        if not docstring:
            return ""
        lines = docstring.splitlines()

        while lines and not lines[0].strip():                                           # Remove empty lines at the beginning
            lines.pop(0)

        while lines and not lines[-1].strip():                                          # Remove empty lines at the end
            lines.pop()

        indent = min((len(line) - len(line.lstrip())                                    # Find minimum indentation
                     for line in lines if line.strip()), default=0)

        return '\n'.join(line[indent:] for line in lines)                               # Remove indentation and join lines

    def get_property_schema(self, target_cls : Type ,                                   # Class containing the property
                                  var_name   : str  ,                                   # Name of the property
                                  var_type   : Any  ,                                   # Type annotation of the property
                               ) -> dict:                                               # Returns JSON Schema for property
        validators = []
        origin     = get_origin(var_type)

        if origin is Annotated:                                                         # Handle Annotated types
            args        = get_args(var_type)
            base_type   = args[0]
            validators  = [arg for arg in args[1:] if isinstance(arg, Type_Safe__Validator)]
            var_type    = base_type
            origin      = get_origin(base_type)         # todo: see if we need this field (which is not being used at the moment)

        schema = self.get_type_schema(var_type)                                         # Get basic type schema

        #if target_cls.__doc__:                                                          # Add description if available
        doc = self.get_attribute_doc(target_cls, var_name)
        if doc:
            schema["description"] = doc

        for validator in validators:                                                    # Apply validators
            self._apply_validator(schema, validator)

        return schema

    def get_attribute_doc(self, cls     : Type ,                                        # Class to extract docs from
                                attr_name: str
                           ) -> Optional[str]:                                           # Returns attribute documentation
        if cls.__doc__:                                                                  # Try class docstring first
            lines = cls.__doc__.splitlines()
            for i, line in enumerate(lines):
                if f"{attr_name}:" in line or f"{attr_name} :" in line:
                    parts = line.split(":", 1)
                    if len(parts) > 1:
                        return parts[1].strip()
                    if i + 1 < len(lines) and lines[i + 1].strip():
                        return lines[i + 1].strip()

        try:                                                                            # if nor available Try source code comments next
            source = inspect.getsource(cls)
            lines  = source.splitlines()
            for line in lines:
                normal_case  = f"{attr_name}:" in line or f"{attr_name} :" in line       # Handle the normal case and the aligned case with variable spacing
                aligned_case = re.search(fr"\b{attr_name}\s*:", line)

                if normal_case or aligned_case:
                    if "#" in line:
                        return line.split("#", 1)[1].strip()
                if f"{attr_name} :" in line or f"{attr_name}:" in line:
                    if "#" in line:
                        return line.split("#", 1)[1].strip()
        except (TypeError, OSError):
            pass

        return None

    def get_type_schema(self, type_hint: Any) -> dict:                                  # Convert Python type to JSON Schema
        origin = get_origin(type_hint)

        if   type_hint is str       : return {"type": "string"  }                       # Handle primitive types
        elif type_hint is int       : return {"type": "integer" }
        elif type_hint is float     : return {"type": "number"  }
        elif type_hint is bool      : return {"type": "boolean" }
        elif type_hint is None      : return {"type": "null"    }
        elif type_hint is type(None): return {"type": "null"    }


        if origin in (list, List):                                                      # Handle container types
            args      = get_args(type_hint)
            item_type = args[0] if args else Any
            return { "type" : "array",
                     "items": self.get_type_schema(item_type) }
        elif origin in (dict, Dict):
            args = get_args(type_hint)
            if len(args) >= 2:
                key_type, value_type = args[0], args[1]
                return { "type"                : "object",
                         "additionalProperties": self.get_type_schema(value_type) }
            else:
                return {"type": "object"}
        elif origin in (tuple, Tuple):
            args = get_args(type_hint)
            if args:
                return { "type"    : "array"                                    ,
                         "items"   : [self.get_type_schema(arg) for arg in args],
                         "minItems": len(args)                                  ,
                         "maxItems": len(args)                                  }
            else:
                return {"type": "array"}
        elif origin in (set, Set):
            args = get_args(type_hint)
            item_type = args[0] if args else Any
            return { "type"       : "array"                         ,
                     "items"      : self.get_type_schema(item_type) ,
                     "uniqueItems": True                            }

        elif origin is Union:                                                       # Handle union types (Optional is Union[type, None])
            args = get_args(type_hint)
            if len(args) == 2 and type(None) in args:
                non_none_type = next(arg for arg in args if arg is not type(None))
                schema = self.get_type_schema(non_none_type)
                if "type" in schema and isinstance(schema["type"], str):
                    schema["type"] = [schema["type"], "null"]
                return schema
            else:
                return { "anyOf": [self.get_type_schema(arg) for arg in args] }


        elif inspect.isclass(type_hint) and issubclass(type_hint, Type_Safe):       # Handle custom Type_Safe classes (nested objects)
            return self.export__type_safe(type_hint)                                # Recursive call for nested objects

        return {"type": "object"}                                                   # Default fallback

    def _apply_validator(self, schema   : dict               ,                      # Schema to modify
                               validator: Type_Safe__Validator
                          ) -> None:                                                # Applies validator constraints
        if isinstance(validator, Validator__Min):
            if   schema.get("type") in ["integer", "number"]: schema["minimum"  ] = validator.min_value
            elif schema.get("type") == "string"             : schema["minLength"] = validator.min_value
            elif schema.get("type") == "array"              : schema["minItems" ] = validator.min_value

        elif isinstance(validator, Validator__Max):
            if   schema.get("type") in ["integer", "number"]: schema["maximum"  ] = validator.max_value
            elif schema.get("type") == "string"             : schema["maxLength"] = validator.max_value
            elif schema.get("type") == "array"              : schema["maxItems" ] = validator.max_value

        elif isinstance(validator, Validator__Regex):
            if schema.get("type") == "string":
                schema["pattern"] = validator.pattern
                if validator.description:
                    if "description" not in schema:
                        schema["description"] = validator.description
                    else:
                        schema["description"] += f" (Pattern: {validator.description})"

        elif isinstance(validator, Validator__One_Of):
            schema["enum"] = validator.allowed

    def is_required_property(self, target_cls: Type ,                                   # Class containing the property
                                   var_name  : str  ,                                   # Name of the property
                                   var_type  : Any
                              ) -> bool:                                                # Returns True if property is required
        origin = get_origin(var_type)                                                   # Check if the type is Optional
        if origin is Union:
            args = get_args(var_type)
            if type(None) in args:
                return False

        if hasattr(target_cls, var_name):                                               # Check if there's a default value in the class
            return getattr(target_cls, var_name) is None

        return True                                                                     # By default, consider it required