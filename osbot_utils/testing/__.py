from types                  import SimpleNamespace
from osbot_utils.utils.Dev  import pprint

__SKIP__         = object()
__MISSING__      = object()
__GREATER_THAN__ = lambda x: ('gt', x)
__LESS_THAN__    = lambda x: ('lt', x)
__BETWEEN__      = lambda min_val, max_val: ('between', min_val, max_val)
__CLOSE_TO__     = lambda value, tolerance=0.01: ('close_to', value, tolerance)


class __(SimpleNamespace):
    def __enter__(self)                          : return self
    def __exit__(self, exc_type, exc_val, exc_tb): return False

    def __contains__(self, item):                                                           # Allow 'subset in superset' syntax
        return self.contains(item)

    def __eq__(self, other):                                                                # Enhanced equality that handles SKIP markers for dynamic values
        if not isinstance(other, __):
            return super().__eq__(other)

        for key in set(self.__dict__.keys()) | set(other.__dict__.keys()):
            self_val  = getattr(self, key, None)
            other_val = getattr(other, key, None)

            if self_val is __SKIP__ or other_val is __SKIP__:                              # Skip comparison if either value is a skip marker
                continue

            # Handle comparison operators
            # if isinstance(other_val, tuple) and len(other_val) >= 2:
            #     op = other_val[0]
            if (isinstance(other_val, tuple) and len(other_val) >= 2 and
                not isinstance(self_val, tuple)):  # ← ADD THIS CHECK
                op = other_val[0]
                try:
                    if op == 'gt' and not (self_val > other_val[1]):
                        return False
                    elif op == 'lt' and not (self_val < other_val[1]):
                        return False
                    elif op == 'gte' and not (self_val >= other_val[1]):
                        return False
                    elif op == 'lte' and not (self_val <= other_val[1]):
                        return False
                    elif op == 'between' and not (other_val[1] <= self_val <= other_val[2]):
                        return False
                    elif op == 'close_to' and not (abs(self_val - other_val[1]) <= other_val[2]):
                        return False
                except TypeError:
                    return False                                                        # Comparison not supported (e.g. None > 0)
                continue

            if isinstance(self_val, __) and isinstance(other_val, __):                      # Handle nested __ objects recursively
                if self_val.__eq__(other_val) is False:                                     # Explicit recursive comparison
                    return False
            elif self_val != other_val:
                return False
        return True

    def contains(self, other=None, **kwargs):
        if other is not None and kwargs:
            raise ValueError("Cannot mix positional and keyword arguments in contains(). "
                             "Use either _.contains(__(a=1, b=2)) or _.contains(a=1, b=2), not both.")

        if kwargs:                                          # If kwargs provided, use them instead of 'other'
            other = kwargs

        other_dict = getattr(other, '__dict__', other) if hasattr(other, '__dict__') else other if isinstance(other, dict) else None
        if other_dict is None:
            return False

        for key, expected_value in other_dict.items():
            if expected_value is __SKIP__:                                                  # Skip this field
                continue

            if expected_value is __MISSING__:
                if hasattr(self, key):
                    return False        # Field exists but expected missing
                continue                # Field missing as expected

            if not hasattr(self, key):
                return False
            actual_value = getattr(self, key)

            # Handle comparison operators
            if isinstance(expected_value, tuple) and len(expected_value) >= 2:
                op = expected_value[0]
                try:
                    if op == 'gt' and not (actual_value > expected_value[1]):
                        return False
                    elif op == 'lt' and not (actual_value < expected_value[1]):
                        return False
                    elif op == 'gte' and not (actual_value >= expected_value[1]):
                        return False
                    elif op == 'lte' and not (actual_value <= expected_value[1]):
                        return False
                    elif op == 'between' and not (expected_value[1] <= actual_value <= expected_value[2]):
                        return False
                    elif op == 'close_to' and not (abs(actual_value - expected_value[1]) <= expected_value[2]):
                        return False
                except TypeError:
                    return False                                                        # Comparison not supported (e.g. None > 0)
                continue

            if isinstance(expected_value, __) and isinstance(actual_value, __):
                if not actual_value.contains(expected_value):
                    return False
            elif actual_value != expected_value:
                return False
        return True

    def diff(self, other):                  # Return differences between objects for better test failure messages
        differences = {}
        all_keys = set(self.__dict__.keys()) | set(other.__dict__.keys() if hasattr(other, '__dict__') else other.keys() if isinstance(other, dict) else [])

        for key in all_keys:
            self_val = getattr(self, key, __MISSING__)
            other_val = getattr(other, key, __MISSING__) if hasattr(other, '__dict__') else other.get(key, __MISSING__) if isinstance(other, dict) else __MISSING__

            if self_val is __SKIP__ or other_val is __SKIP__:
                continue

            if self_val != other_val:
                differences[key] = {'actual': self_val, 'expected': other_val}

        #return differences if differences else None
        from osbot_utils.testing.__helpers import dict_to_obj
        return dict_to_obj(differences)


    def excluding(self, *fields):           # Return copy without specified fields for comparison"
        result = __(**self.__dict__)
        for field in fields:
            delattr(result, field) if hasattr(result, field) else None
        return result

    def merge(self, **updates): # Create new instance with updates, handling nested __ objects
        result = __(**self.__dict__)
        for key, value in updates.items():
            if isinstance(value, __) and hasattr(result, key) and isinstance(getattr(result, key), __):
                setattr(result, key, getattr(result, key).merge(**value.__dict__))
            else:
                setattr(result, key, value)
        return result

    def print(self):
        pprint(self)