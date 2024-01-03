# todo: find a way to add these documentations strings to a separate location so that
#       the code is not polluted with them (like in the example below)
#       the data is avaiable in IDE's code complete
import inspect


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

            # Other methods can be added here

        # Correctly override default values by passing keyword arguments
        instance = MyConfigurableClass(attribute1='new_value', attribute2=False)

        # This will raise an exception as 'attribute3' is not predefined
        # instance = MyConfigurableClass(attribute3='invalid_attribute')

    Note:
        It is important that all attributes which may be set at instantiation are
        predefined in the class. Failure to do so will result in an exception being
        raised.

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
        for (key, value) in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise Exception(f"{self.__class__.__name__} has no attribute '{key}' and cannot be assigned the value '{value}'")

    @classmethod
    def __default_kwargs__(cls):
        """Return a dictionary of class level variables and their values."""
        kwargs = {}

        for base_cls in inspect.getmro(cls):                  # Traverse the inheritance hierarchy and collect class-level attributes
            if base_cls is object:  # Skip the base 'object' class
                continue
            for k, v in vars(base_cls).items():
                if not k.startswith('__'):# and not callable(v):
                    kwargs[k] = v

        for k, v in cls.__dict__.items():
            if not k.startswith('_') and not callable(v):
                kwargs[k] = v
        return kwargs

    def __kwargs__(self):
        """Return a dictionary of the current instance's attribute values including inherited class defaults."""
        kwargs = {}


            #kwargs.update({k: v for k, v in vars(cls).items() #if not k.startswith('_') and not callable(v)})

        # Update with instance-specific values
        for key in self.__default_kwargs__().keys():
            kwargs[key] = self.__getattribute__(key)
        return kwargs


    def __locals__(self):
        """Return a dictionary of the current instance's attribute values."""
        return {k: v for k, v in vars(self).items() if not k.startswith('_')}
