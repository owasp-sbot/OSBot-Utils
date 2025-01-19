import types
import inspect

class Type_Safe__Step__Default_Kwargs:

    def default_kwargs(self, _self):
        kwargs = {}
        cls = type(_self)
        for base_cls in inspect.getmro(cls):                                                    # Traverse the inheritance hierarchy and collect class-level attributes
            if base_cls is object:                                                              # Skip the base 'object' class
                continue
            for k, v in vars(base_cls).items():
                if not k.startswith('__') and not isinstance(v, types.FunctionType):            # remove instance functions
                    if not isinstance(v, classmethod):
                        kwargs[k] = v
            # add the vars defined with the annotations
            if hasattr(base_cls,'__annotations__'):                                             # can only do type safety checks if the class does not have annotations
                for var_name, var_type in base_cls.__annotations__.items():
                    var_value        = getattr(_self, var_name)
                    kwargs[var_name] = var_value

        return kwargs

type_safe_step_default_kwargs = Type_Safe__Step__Default_Kwargs()

