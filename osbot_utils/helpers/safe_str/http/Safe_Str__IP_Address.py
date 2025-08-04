import ipaddress
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive


class Safe_Str__IP_Address(Type_Safe__Primitive, str):

    def __new__(cls, value: str = None):
        if value is not None:                                                                   # check that it is not None
            if not isinstance(value, str):                                                      # check that it is a string
                raise TypeError(f"Value provided must be a string, and it was {type(value)}")
            else:
                value = value.strip()                                                           # trim/strip the value since there could be some leading spaces (which are easy to fix here)

        if not value:                                                                           # allow empty or null values
            return str.__new__(cls, "")

        try:
            ip_obj = ipaddress.ip_address(value)                                                # validate IP address using ipaddress module
            value = str(ip_obj)                                                                 # Use the canonical representation
        except ValueError as e:
            raise ValueError(f"Invalid IP address: {value}") from e

        return str.__new__(cls, value)

    def __add__(self, other):                                           # Concatenation returns regular str, not Safe_Str__IP_Address
        return str.__add__(self, other)

    def __radd__(self, other):                                          # Reverse concatenation also returns regular str"""
        return str.__add__(other, self)