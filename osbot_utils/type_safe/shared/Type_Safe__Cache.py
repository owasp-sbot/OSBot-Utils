import inspect
from typing  import get_origin
from weakref import WeakKeyDictionary


class Type_Safe__Cache:

    _annotations_cache : WeakKeyDictionary
    _get_origin_cache  : WeakKeyDictionary
    _mro_cache         : WeakKeyDictionary
    _valid_vars_cache  : WeakKeyDictionary

    cache_hit__annotations  : int = 0
    cache_hit__get_origin   : int = 0
    cache_hit__mro          : int = 0
    cache_hit__valid_vars   : int = 0
    skip_cache              : bool = False


    # Caching system for Type_Safe methods
    def __init__(self):
        self._annotations_cache = WeakKeyDictionary()                                        # Cache for class annotations
        self._get_origin_cache  = WeakKeyDictionary()                                        # Cache for get_origin results
        self._mro_cache         = WeakKeyDictionary()                                        # Cache for Method Resolution Order
        self._valid_vars_cache  = WeakKeyDictionary()

    def get_class_annotations(self, cls):
        if self.skip_cache or cls not in self._annotations_cache:
            self._annotations_cache[cls] = cls.__annotations__.items()
        else:
            self.cache_hit__annotations += 1
        return self._annotations_cache[cls]

    def get_class_mro(self, cls):
        if self.skip_cache or cls not in self._mro_cache:
            self._mro_cache[cls] = inspect.getmro(cls)
        else:
            self.cache_hit__mro += 1
        return self._mro_cache[cls]


    def get_origin(self, var_type):                                                             # Cache expensive get_origin calls
        if self.skip_cache or var_type not in self._get_origin_cache:
            self._get_origin_cache[var_type] = get_origin(var_type)
        else:
            self.cache_hit__get_origin += 1
        return self._get_origin_cache[var_type]

    # todo: see if we have cache misses and invalid hits based on the validator (we might need more validator specific methods)
    def get_valid_class_variables(self, cls, validator):
        if self.skip_cache or cls not in self._valid_vars_cache:
            valid_variables = {}
            for name, value in vars(cls).items():
                if not validator(name, value):
                    valid_variables[name] = value
            self._valid_vars_cache[cls] = valid_variables
        else:
            self.cache_hit__valid_vars += 1
        return self._valid_vars_cache[cls]


    def print_cache_hits(self):
        print()
        print("###### Type_Safe_Cache Hits ########")
        print()
        print(f"  annotations : {self.cache_hit__annotations}")
        print(f"  get_origin  : {self.cache_hit__get_origin }")
        print(f"  mro         : {self.cache_hit__mro        }")
        print(f"  valid_vars  : {self.cache_hit__valid_vars }")

type_safe_cache = Type_Safe__Cache()