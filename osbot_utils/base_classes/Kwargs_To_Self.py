# todo: find a way to add these documentations strings to a separate location so that
#       the code is not polluted with them (like in the example below)
#       the data is avaiable in IDE's code complete
import inspect
import types

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import default_value


class Kwargs_To_Self:
    """
    A mixin class to strictly assign keyword arguments to pre-defined instance attributes during initialization.

    This base class provides an __init__ method that assigns values from keyword
    arguments to instance attributes. If an attribute with the same name as a key
    from the kwargs is defined in the class, it will be set to the value from kwargs.
    If the key does not match any predefined attribute names, an exception is raised.

    This behavior enforces strict control over the attributes of instances, ensuring
    that only predefined attributes can be set at the time of instantiation and avoids
    silent attribute creation which can lead to bugs in the code.

    Usage:
        class MyConfigurableClass(Kwargs_To_Self):
            attribute1 = 'default_value'
            attribute2 = True
            attribute3 : str
            attribute4 : list
            attribute4 : int = 42

            # Other methods can be added here

        # Correctly override default values by passing keyword arguments
        instance = MyConfigurableClass(attribute1='new_value', attribute2=False)

        # This will raise an exception as 'attribute3' is not predefined
        # instance = MyConfigurableClass(attribute3='invalid_attribute')

        this will also assign the default value to any variable that has a type defined.
        In the example above the default values (mapped by __default__kwargs__ and __locals__) will be:
            attribute1 = 'default_value'
            attribute2 = True
            attribute3 = ''             # default value of str
            attribute4 = []             # default value of list
            attribute4 = 42             # defined value in the class

    Note:
        It is important that all attributes which may be set at instantiation are
        predefined in the class. Failure to do so will result in an exception being
        raised.

        Also important is that attributes tyeps

    Methods:
        __init__(**kwargs): The initializer that handles the assignment of keyword
                            arguments to instance attributes. It enforces strict
                            attribute assignment rules, only allowing attributes
                            that are already defined in the class to be set.
    """

    def __init__(self, **kwargs):
        """
        Initialize an instance of the derived class, strictly assigning provided keyword
        arguments to corresponding instance attributes.

        Parameters:
            **kwargs: Variable length keyword arguments.

        Raises:
            Exception: If a key from kwargs does not correspond to any attribute
                       pre-defined in the class, an exception is raised to prevent
                       setting an undefined attribute.

        """
        for (key, value) in self.__default_kwargs__().items():                  # assign all default values to self
            setattr(self, key, value)

        for (key, value) in kwargs.items():                             # overwrite with values provided in ctor
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise Exception(f"{self.__class__.__name__} has no attribute '{key}' and cannot be assigned the value '{value}'. "
                                f"Use {self.__class__.__name__}.__default_kwargs__() see what attributes are available")

    def __enter__(self): return self
    def _exit__(self, exc_type, exc_val, exc_tb): pass

    @classmethod
    def __cls_kwargs__(cls):
        """Return current class dictionary of class level variables and their values."""
        kwargs = {}

        for k, v in vars(cls).items():
            if not k.startswith('__') and not isinstance(v, types.FunctionType):  # remove instance functions
                kwargs[k] = v

        for var_name, var_type in cls.__annotations__.items():
            if hasattr(cls, var_name) is False:                         # only add if it has not already been defined
                var_value = default_value(var_type)
                kwargs[var_name] = var_value
            else:
                var_value = getattr(cls, var_name)
                if not isinstance(var_value, var_type):
                    exception_message = f"variable '{var_name}' is defined as type '{var_type}' but has value '{var_value}' of type '{type(var_value)}'"
                    raise Exception(exception_message)
        return kwargs

    @classmethod
    def __default_kwargs__(cls):
        """Return entire (including base classes) dictionary of class level variables and their values."""
        kwargs = {}

        for base_cls in inspect.getmro(cls):                  # Traverse the inheritance hierarchy and collect class-level attributes
            if base_cls is object:  # Skip the base 'object' class
                continue
            for k, v in vars(base_cls).items():
                if not k.startswith('__') and not isinstance(v, types.FunctionType):    # remove instance functions
                    kwargs[k] = v

            # add the vars defined with the annotations
            for var_name, var_type in base_cls.__annotations__.items():
                if hasattr(cls, var_name) is False:                         # only add if it has not already been defined
                    var_value = default_value(var_type)
                    kwargs[var_name] = var_value
                else:
                    var_value = getattr(cls, var_name)
                    if not isinstance(var_value, var_type):
                        exception_message = f"variable '{var_name}' is defined as type '{var_type}' but has value '{var_value}' of type '{type(var_value)}'"
                        raise Exception(exception_message)

        return kwargs

    def __kwargs__(self):
        """Return a dictionary of the current instance's attribute values including inherited class defaults."""
        kwargs = {}
        # Update with instance-specific values

        for key, value in self.__default_kwargs__().items():
            if hasattr(self, key):
                kwargs[key] = self.__getattribute__(key)
            else:
                kwargs[key] = value
        return kwargs


    def __locals__(self):
        """Return a dictionary of the current instance's attribute values."""
        kwargs = self.__kwargs__()

        for k, v in vars(self).items():
            if not isinstance(v, types.FunctionType):
                kwargs[k] = v
        return kwargs