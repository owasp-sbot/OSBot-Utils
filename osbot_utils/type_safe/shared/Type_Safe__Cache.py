import inspect
from typing                                                     import get_origin
from weakref                                                    import WeakKeyDictionary
from osbot_utils.type_safe.shared.Type_Safe__Shared__Variables  import IMMUTABLE_TYPES
from osbot_utils.utils.Objects                                  import all_annotations__in_class


class Type_Safe__Cache:

    _cls__annotations_cache : WeakKeyDictionary
    _cls__immutable_vars    : WeakKeyDictionary
    _cls__kwargs_cache      : WeakKeyDictionary
    _get_origin_cache       : WeakKeyDictionary
    _mro_cache              : WeakKeyDictionary
    _valid_vars_cache       : WeakKeyDictionary

    cache_hit__cls__annotations   : int  = 0
    cache_hit__cls__kwargs        : int  = 0
    cache_hit__cls__immutable_vars: int  = 0
    cache_hit__get_origin         : int  = 0
    cache_hit__mro                : int  = 0
    cache_hit__valid_vars         : int  = 0
    skip_cache                    : bool = False


    # Caching system for Type_Safe methods
    def __init__(self):
        self._cls__annotations_cache = WeakKeyDictionary()                                        # Cache for class annotations
        self._cls__immutable_vars    = WeakKeyDictionary()                                        # Cache for class immutable vars
        self._cls__kwargs_cache      = WeakKeyDictionary()                                        # Cache for class kwargs
        self._get_origin_cache       = WeakKeyDictionary()                                        # Cache for get_origin results
        self._mro_cache              = WeakKeyDictionary()                                        # Cache for Method Resolution Order
        self._valid_vars_cache       = WeakKeyDictionary()

    def get_cls_kwargs(self, cls):
        if self.skip_cache or cls not in self._cls__kwargs_cache:
            return None
        else:
            self.cache_hit__cls__kwargs += 1
        return self._cls__kwargs_cache.get(cls)

    def get_class_annotations(self, cls):
        annotations = self._cls__annotations_cache.get(cls)                          # this is a more efficient cache retrieval pattern (we only get the data from the dict once)
        if not annotations:                                                     # todo: apply this to the other cache getters
            if self.skip_cache or cls not in self._cls__annotations_cache:
                annotations = all_annotations__in_class(cls).items()
                self._cls__annotations_cache[cls] = annotations
        else:
            self.cache_hit__cls__annotations += 1
        return annotations

    def get_class_immutable_vars(self, cls):
        immutable_vars = self._cls__immutable_vars.get(cls)
        if self.skip_cache or not immutable_vars:
            annotations                    = self.get_class_annotations(cls)
            immutable_vars                 = {key: value for key, value in annotations if value in IMMUTABLE_TYPES}
            self._cls__immutable_vars[cls] = immutable_vars
        else:
            self.cache_hit__cls__immutable_vars += 1
        return immutable_vars

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

    def set_cache__cls_kwargs(self, cls, kwargs):
        self._cls__kwargs_cache[cls] = kwargs
        return kwargs

    def print_cache_hits(self):
        print()
        print("###### Type_Safe_Cache Hits ########")
        print()
        print(f"  annotations        : {self.cache_hit__cls__annotations    }")
        print(f"  cls__kwargs        : {self.cache_hit__cls__kwargs         }")
        print(f"  cls__immutable_vars: {self.cache_hit__cls__immutable_vars }")
        print(f"  get_origin         : {self.cache_hit__get_origin          }")
        print(f"  mro                : {self.cache_hit__mro                 }")
        print(f"  valid_vars         : {self.cache_hit__valid_vars          }")

type_safe_cache = Type_Safe__Cache()