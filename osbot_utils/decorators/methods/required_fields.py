from functools import wraps

from osbot_utils.utils.Objects import get_missing_fields


class required_fields:
    """checks that required fields are not null in the current object (does not work for for static methods)"""
    def __init__(self, field_names):
        self.field_names = field_names

    def __call__(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            target_obj = args[0]                                                        # self of the caller
            missing_fields = get_missing_fields(target_obj, self.field_names)
            if len(missing_fields) > 0:
                raise  Exception(f'missing fields in {function.__name__}: {missing_fields}')
            return function(*args,**kwargs)
        return wrapper