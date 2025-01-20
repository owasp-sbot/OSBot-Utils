import types
from enum                                                           import EnumMeta
from typing                                                         import Dict, Any, Type, get_origin, Annotated, get_args
from osbot_utils.type_safe.steps.Type_Safe__Cache                   import Type_Safe__Cache, type_safe_cache
from osbot_utils.type_safe.steps.Type_Safe__Raise_Exception         import type_safe_raise_exception
from osbot_utils.type_safe.steps.Type_Safe__Step__Default_Value     import type_safe_step_default_value
from osbot_utils.type_safe.steps.Type_Safe__Validation              import IMMUTABLE_TYPES
from osbot_utils.utils.Objects                                      import obj_is_type_union_compatible

class Type_Safe__Step__Class_Kwargs:                                      # Cache for class-level keyword arguments and related information."""

    type_safe_cache : Type_Safe__Cache

    def __init__(self):
        self.type_safe_cache = type_safe_cache

    def get_cls_kwargs(self, cls: Type, include_base_classes: bool = True) -> Dict[str, Any]:
        if not hasattr(cls, '__mro__'):
            return {}

        base_classes = type_safe_cache.get_class_mro(cls)
        if not include_base_classes:
            base_classes = base_classes[:1]

        kwargs = {}
        for base_cls in base_classes:
            self.process_mro_class  (base_cls, kwargs)
            self.process_annotations(cls, base_cls, kwargs)
        return kwargs

    def handle_undefined_var(self, cls, kwargs, var_name, var_type):                              # Handle variables not yet defined in base class
        if var_name in kwargs:
            return
        var_value                = type_safe_step_default_value.default_value(cls, var_type)
        kwargs[var_name]         = var_value

    def handle_defined_var(self, base_cls, var_name, var_type):                                   # Handle variables already defined in base class
        var_value = getattr(base_cls, var_name)
        if var_value is None:                                                                     # Allow None assignments on constructor
            return

        if self.should_skip_type_check(var_type):
            return

        self.validate_variable_type    (var_name, var_type, var_value)
        self.validate_type_immutability(var_name, var_type)

    def process_annotation(self, cls, base_cls, kwargs, var_name, var_type):                       # Process type annotations for class variables
        if not hasattr(base_cls, var_name):
            self.handle_undefined_var(cls, kwargs, var_name, var_type)
        else:
            self.handle_defined_var(base_cls, var_name, var_type)

    def process_annotations(self, cls, base_cls, kwargs):
        if hasattr(base_cls,'__annotations__'):                                                         # can only do type safety checks if the class does not have annotations
            for var_name, var_type in type_safe_cache.get_class_annotations(base_cls):
                self.process_annotation(cls, base_cls, kwargs, var_name, var_type)

    def process_mro_class(self, base_cls, kwargs):
        if base_cls is object:                                                            # Skip the base 'object' class
            return

        class_variables = type_safe_cache.get_valid_class_variables(base_cls, self.should_skip_var)

        for name, value in class_variables.items():
            if name not in kwargs:
                kwargs[name] = value

    def should_skip_var(self, var_name: str, var_value: Any) -> bool:                     # Determines if variable should be skipped during MRO processing
        if var_name.startswith('__'):                                                      # skip internal variables
            return True
        if isinstance(var_value, types.FunctionType):                                      # skip instance functions
            return True
        if isinstance(var_value, classmethod):                                            # skip class methods
            return True
        if isinstance(var_value, property):                                               # skip property descriptors
            return True
        return False

    def should_skip_type_check(self, var_type):                                                   # Determine if type checking should be skipped
        return (get_origin(var_type) is Annotated or
                get_origin(var_type) is type)




    def validate_type_immutability(self, var_name: str, var_type: Any) -> None:                         # Validates that type is immutable or in supported format
        if var_type not in IMMUTABLE_TYPES and var_name.startswith('__') is False:                          # if var_type is not one of the IMMUTABLE_TYPES or is an __ internal
            if obj_is_type_union_compatible(var_type, IMMUTABLE_TYPES) is False:                            # if var_type is not something like Optional[Union[int, str]]
                if var_type not in IMMUTABLE_TYPES or type(var_type) not in IMMUTABLE_TYPES:
                    if not isinstance(var_type, EnumMeta):
                        type_safe_raise_exception.immutable_type_error(var_name, var_type)

    def validate_variable_type(self, var_name, var_type, var_value):                                # Validate type compatibility
        if var_type and not isinstance(var_value, var_type):
            type_safe_raise_exception.type_mismatch_error(var_name, var_type, var_value)


# Create singleton instance
type_safe_step_class_kwargs = Type_Safe__Step__Class_Kwargs()