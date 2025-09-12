import uuid
from osbot_utils.utils.Misc                     import is_guid
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive

GUID__NAMESPACE = uuid.UUID('2cfec064-537a-4ff7-8fdc-2fc9e2606f3d')

class Guid(Type_Safe__Primitive, str):
    def __new__(cls, value: str):
        if not isinstance(value, str):                                                  # Check if the value is a string
            raise ValueError(f'in Guid: value provided was not a string: {value}')      # if not raise a ValueError
        if is_guid(value):
            guid = value
        else:
            guid = uuid.uuid5(GUID__NAMESPACE, value)                                   # Generate a UUID5 using the namespace and value
        return super().__new__(cls, str(guid))                                          # Return a new instance of Guid initialized with the string version of the UUID

    def __str__(self):
        return self