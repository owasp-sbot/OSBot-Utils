# todo: find a way to add these documentations strings to a separate location so that
#       the data is available in IDE's code complete
from osbot_utils.type_safe.shared.Type_Safe__Validation             import type_safe_validation
from osbot_utils.type_safe.steps.Type_Safe__Step__Class_Kwargs      import type_safe_step_class_kwargs
from osbot_utils.type_safe.steps.Type_Safe__Step__Default_Kwargs    import type_safe_step_default_kwargs
from osbot_utils.type_safe.steps.Type_Safe__Step__Default_Value     import type_safe_step_default_value
from osbot_utils.type_safe.steps.Type_Safe__Step__Init              import type_safe_step_init
from osbot_utils.type_safe.steps.Type_Safe__Step__Set_Attr          import type_safe_step_set_attr
from osbot_utils.utils.Objects                                      import serialize_to_dict

class Type_Safe:

    def __init__(self, **kwargs):

        class_kwargs = self.__cls_kwargs__()
        type_safe_step_init.init(self, class_kwargs, **kwargs)


    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

    def __setattr__(self, name, value):
        type_safe_step_set_attr.setattr(super(), self, name, value)

    def __attr_names__(self):
        from osbot_utils.utils.Misc import list_set

        return list_set(self.__locals__())

    @classmethod
    def __cls_kwargs__(cls):                                                # Return current class dictionary of class level variables and their values
        return type_safe_step_class_kwargs.get_cls_kwargs(cls)

    @classmethod
    def __default__value__(cls, var_type):
        return type_safe_step_default_value.default_value(cls, var_type)

    def __default_kwargs__(self):                                           # Return entire (including base classes) dictionary of class level variables and their values.
        return type_safe_step_default_kwargs.default_kwargs(self)

    def __kwargs__(self):                                                   # Return a dictionary of the current instance's attribute values including inherited class defaults.
        return type_safe_step_default_kwargs.kwargs(self)


    def __locals__(self):                                                   # Return a dictionary of the current instance's attribute values.
        return type_safe_step_default_kwargs.locals(self)

    # global methods added to any class that base classes this
    # todo: see if there should be a prefix on these methods, to make it easier to spot them
    #       of if these are actually that useful that they should be added like this
    # todo: these methods should not be here
    # def bytes(self):
    #     from osbot_utils.utils.Json import json_to_bytes
    #
    #     return json_to_bytes(self.json())
    #
    # def bytes_gz(self):
    #     from osbot_utils.utils.Json import json_to_gz
    #
    #     return json_to_gz(self.json())

    def json(self):
        return self.serialize_to_dict()

    def json__compress(self):                                           # todo: see if this is the best place to put these Type_Safe__Json_Compressor methods
        from osbot_utils.type_safe.shared.Type_Safe__Json_Compressor import Type_Safe__Json_Compressor
        return Type_Safe__Json_Compressor().compress(self)

    # todo: see if we still need this. now that Type_Safe handles base types, there should be no need for this
    def merge_with(self, target):
        original_attrs = {k: v for k, v in self.__dict__.items() if k not in target.__dict__}       # Store the original attributes of self that should be retained.
        self.__dict__ = target.__dict__                                                             # Set the target's __dict__ to self, now self and target share the same __dict__.
        self.__dict__.update(original_attrs)                                                        # Reassign the original attributes back to self.
        return self

    # def locked(self, value=True):                                   # todo: figure out best way to do this (maybe???)
    #     self.__lock_attributes__ = value                            #     : update, with the latest changes were we don't show internals on __locals__() this might be a good way to do this
    #     return self

    def reset(self):
        for k,v in self.__cls_kwargs__().items():
            setattr(self, k, v)

    # todo: see if we still need this here in this class
    def update_from_kwargs(self, **kwargs):                         # Update instance attributes with values from provided keyword arguments.

        for key, value in kwargs.items():
            if value is not None:
                if hasattr(self,'__annotations__'):  # can only do type safety checks if the class does not have annotations
                    if type_safe_validation.check_if__type_matches__obj_annotation__for_attr(self, key, value) is False:
                        raise ValueError(f"Invalid type for attribute '{key}'. Expected '{self.__annotations__.get(key)}' but got '{type(value)}'")
                setattr(self, key, value)
        return self

    def obj(self):
        from osbot_utils.utils.Objects import dict_to_obj

        return dict_to_obj(self.json())

    def serialize_to_dict(self):                                        # todo: see if we need this method or if the .json() is enough
        return serialize_to_dict(self)

    def print(self):
        from osbot_utils.utils.Dev import pprint

        pprint(serialize_to_dict(self))

    @classmethod
    def from_json(cls, json_data, raise_on_not_found=False):
        from osbot_utils.type_safe.steps.Type_Safe__Step__From_Json import type_safe_step_from_json     # circular dependency on Type_Safe
        return type_safe_step_from_json.from_json(cls, json_data, raise_on_not_found)

    @classmethod
    def from_json__compressed(cls, json_data):                          # todo: see if this is the best place to put these Type_Safe__Json_Compressor methods
        from osbot_utils.type_safe.shared.Type_Safe__Json_Compressor import Type_Safe__Json_Compressor
        json_data__decompressed = Type_Safe__Json_Compressor().decompress(json_data)
        return cls.from_json(json_data__decompressed)
