import inspect
from weakref                                                    import WeakKeyDictionary
from osbot_utils.type_safe.shared.Type_Safe__Not_Cached         import type_safe_not_cached
from osbot_utils.type_safe.shared.Type_Safe__Shared__Variables  import IMMUTABLE_TYPES


class Type_Safe__Cache:

    _cls__annotations_cache  : WeakKeyDictionary
    _cls__immutable_vars     : WeakKeyDictionary
    _cls__kwargs_cache       : WeakKeyDictionary
    _obj__annotations_cache  : WeakKeyDictionary
    _type__get_origin_cache  : WeakKeyDictionary
    _mro_cache               : WeakKeyDictionary
    _valid_vars_cache        : WeakKeyDictionary

    cache__miss__cls__annotations   : int = 0
    cache__miss__cls__kwargs        : int = 0
    cache__miss__cls__immutable_vars: int = 0
    cache__miss__obj__annotations   : int = 0
    cache__miss__type__get_origin   : int = 0
    cache__miss__mro                : int = 0
    cache__miss__valid_vars         : int = 0

    cache__hit__cls__annotations    : int  = 0
    cache__hit__cls__kwargs         : int  = 0
    cache__hit__cls__immutable_vars : int  = 0
    cache__hit__obj__annotations    : int  = 0
    cache__hit__type__get_origin    : int  = 0
    cache__hit__mro                 : int  = 0
    cache__hit__valid_vars          : int  = 0
    skip_cache                      : bool = False


    # Caching system for Type_Safe methods
    def __init__(self):
        self._cls__annotations_cache  = WeakKeyDictionary()                                        # Cache for class annotations
        self._cls__immutable_vars     = WeakKeyDictionary()                                        # Cache for class immutable vars
        self._cls__kwargs_cache       = WeakKeyDictionary()                                        # Cache for class kwargs
        self._obj__annotations_cache  = WeakKeyDictionary()                                        # Cache for object annotations
        self._type__get_origin_cache  = WeakKeyDictionary()                                        # Cache for tp (type) get_origin results
        self._mro_cache               = WeakKeyDictionary()                                        # Cache for Method Resolution Order
        self._valid_vars_cache        = WeakKeyDictionary()

    def get_cls_kwargs(self, cls):
        cls_kwargs = self._cls__kwargs_cache.get(cls)

        if cls_kwargs is None:
            self.cache__miss__cls__kwargs += 1
        else:
            self.cache__hit__cls__kwargs += 1
        return cls_kwargs

    def get_obj_annotations(self, target):
        if target is None:
            return {}
        annotations_key = target.__class__
        annotations = self._obj__annotations_cache.get(annotations_key)                          # this is a more efficient cache retrieval pattern (we only get the data from the dict once)
        if self.skip_cache or annotations is None:
            annotations = dict(type_safe_not_cached.all_annotations(target).items())
            self._obj__annotations_cache[annotations_key] = annotations
            self.cache__miss__obj__annotations += 1
        else:
            self.cache__hit__obj__annotations += 1
        return annotations

    def get_class_annotations(self, cls):
        annotations = self._cls__annotations_cache.get(cls)                          # this is a more efficient cache retrieval pattern (we only get the data from the dict once)
        if self.skip_cache or annotations is None:                                                     # todo: apply this to the other cache getters
            annotations = type_safe_not_cached.all_annotations__in_class(cls).items()
            self._cls__annotations_cache[cls] = annotations
            self.cache__miss__cls__annotations +=1
        else:
            self.cache__hit__cls__annotations += 1
        return annotations

    def get_class_immutable_vars(self, cls):
        immutable_vars = self._cls__immutable_vars.get(cls)
        if self.skip_cache or immutable_vars is None:
            annotations                            = self.get_class_annotations(cls)
            immutable_vars                         = {key: value for key, value in annotations if value in IMMUTABLE_TYPES}
            self._cls__immutable_vars[cls]         = immutable_vars
            self.cache__miss__cls__immutable_vars += 1
        else:
            self.cache__hit__cls__immutable_vars   += 1
        return immutable_vars

    def get_class_mro(self, cls):
        if self.skip_cache or cls not in self._mro_cache:
            self._mro_cache[cls]   = inspect.getmro(cls)
            self.cache__miss__mro += 1
        else:
            self.cache__hit__mro   += 1
        return self._mro_cache[cls]


    def get_origin(self, var_type):                                                             # Cache expensive get_origin calls
        if self.skip_cache or var_type not in self._type__get_origin_cache:
            origin = type_safe_not_cached.get_origin(var_type)
            try:                                                                                # this is needed for the edge case when we can't create a key from the var_type in WeakKeyDictionary (see test test__regression__type_safe_is_not_enforced_on_dict_and_Dict for an example)
                self._type__get_origin_cache[var_type] = origin
            except TypeError:
                pass
            self.cache__miss__type__get_origin    += 1
        else:
            origin = self._type__get_origin_cache[var_type]
            self.cache__hit__type__get_origin      += 1
        return origin

    # todo: see if we have cache misses and invalid hits based on the validator (we might need more validator specific methods)
    def get_valid_class_variables(self, cls, validator):
        if self.skip_cache or cls not in self._valid_vars_cache:
            valid_variables = {}
            for name, value in vars(cls).items():
                if not validator(name, value):
                    valid_variables[name] = value
            self._valid_vars_cache[cls]   = valid_variables
            self.cache__miss__valid_vars += 1
        else:
            self.cache__hit__valid_vars  += 1
        return self._valid_vars_cache[cls]

    def set_cache__cls_kwargs(self, cls, kwargs):
        if self.skip_cache is False:
            self._cls__kwargs_cache[cls] = kwargs
        return kwargs

    def print_cache_hits(self):
        print()
        print("###### Type_Safe_Cache Hits ########")
        print()
        print( "  cache name          | hits   | miss  |  size |")
        print( "----------------------|--------|-------|-------|")
        print(f"  annotations         | {self.cache__hit__cls__annotations   :5}  | {self.cache__miss__cls__annotations    :5} | {len(self._obj__annotations_cache) :5} |")
        print(f"  cls__kwargs         | {self.cache__hit__cls__kwargs        :5}  | {self.cache__miss__cls__kwargs         :5} | {len(self._cls__kwargs_cache     ) :5} |")
        print(f"  cls__immutable_vars | {self.cache__hit__cls__immutable_vars:5}  | {self.cache__miss__cls__immutable_vars :5} | {len(self._cls__immutable_vars   ) :5} |")
        print(f"  obj__annotations    | {self.cache__hit__obj__annotations   :5}  | {self.cache__miss__obj__annotations    :5} | {len(self._obj__annotations_cache) :5} |")
        print(f"  type__get_origin    | {self.cache__hit__type__get_origin   :5}  | {self.cache__miss__type__get_origin    :5} | {len(self._type__get_origin_cache) :5} |")
        print(f"  mro                 | {self.cache__hit__mro                :5}  | { self.cache__miss__mro                :5} | {len(self._mro_cache             ) :5} |")
        print(f"  valid_vars          | {self.cache__hit__valid_vars         :5}  | {self.cache__miss__valid_vars          :5} | {len(self._valid_vars_cache      ) :5} |")

type_safe_cache = Type_Safe__Cache()

