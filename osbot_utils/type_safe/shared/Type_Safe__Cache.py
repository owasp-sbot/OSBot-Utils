import inspect
from weakref import WeakKeyDictionary


class Type_Safe__Cache:

    _annotations_cache : WeakKeyDictionary
    _mro_cache         : WeakKeyDictionary
    _valid_vars_cache  : WeakKeyDictionary

    # Caching system for Type_Safe methods
    def __init__(self):
        self._annotations_cache = WeakKeyDictionary()                                       # Cache for class annotations
        self._mro_cache         = WeakKeyDictionary()                                        # Cache for Method Resolution Order
        self._valid_vars_cache  = WeakKeyDictionary()

    def get_class_annotations(self, cls):
        if cls not in self._annotations_cache:
            self._annotations_cache[cls] =  cls.__annotations__.items()
        return self._annotations_cache[cls]

    def get_class_mro(self, cls):
        if cls not in self._mro_cache:
            self._mro_cache[cls] = inspect.getmro(cls)
        return self._mro_cache[cls]

    # todo: see if we have cache misses and invalid hits based on the validator (we might need more validator specific methods)
    def get_valid_class_variables(self, cls, validator):                                   # Returns a dictionary of valid class variables that should be processed. Filters out internal variables, methods, and other non-data attributes.
        if cls not in self._valid_vars_cache:
            valid_variables = {}
            for name, value in vars(cls).items():
                if not validator(name, value):
                    valid_variables[name] = value
            self._valid_vars_cache[cls] = valid_variables
        return self._valid_vars_cache[cls]

type_safe_cache = Type_Safe__Cache()