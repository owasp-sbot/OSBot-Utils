class Type_Safe__Step__Init:

    def init(self, __self         ,
                   __class_kwargs ,
                   **kwargs
             )                   -> None:

        for (key, value) in __class_kwargs.items():                             # assign all default values to target
            if hasattr(__self, key):
                existing_value = getattr(__self, key)
                if existing_value is not None:
                    setattr(__self, key, existing_value)
                    continue
            setattr(__self, key, value)

        for (key, value) in kwargs.items():                                     # overwrite with values provided in ctor
            if hasattr(__self, key):
                if value is not None:                                           # prevent None values from overwriting existing values, which is quite common in default constructors
                    setattr(__self, key, value)
            else:
                raise ValueError(f"{__self.__class__.__name__} has no attribute '{key}' and cannot be assigned the value '{value}'. "
                                 f"Use {__self.__class__.__name__}.__default_kwargs__() see what attributes are available")

type_safe_step_init = Type_Safe__Step__Init()