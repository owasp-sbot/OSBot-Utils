import types


class Type_Safe__Step__Deserialize_Type:

    def using_value(self, value):         # TODO: Check the security implications of this deserialisation
        if value:
            try:
                module_name, type_name = value.rsplit('.', 1)
                if module_name == 'builtins' and type_name == 'NoneType':                       # Special case for NoneType (which serialises as builtins.* , but it actually in types.* )
                    value = types.NoneType
                else:
                    module = __import__(module_name, fromlist=[type_name])
                    value = getattr(module, type_name)
                    if isinstance(value, type) is False:
                        raise ValueError(f"Security alert, in deserialize_type__using_value only classes are allowed")

            except (ValueError, ImportError, AttributeError) as e:
                raise ValueError(f"Could not reconstruct type from '{value}': {str(e)}")
        return value

type_safe_step_deserialize_type = Type_Safe__Step__Deserialize_Type()