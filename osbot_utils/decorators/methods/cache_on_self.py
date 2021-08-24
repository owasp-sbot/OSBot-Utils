import inspect
from functools import wraps

from osbot_utils.utils.Misc import str_md5

#from osbot_utils.utils.Dev import pprint

CACHE_ON_SELF_KEY_PREFIX = 'cache_on_self'
CACHE_ON_SELF_TYPES      = [int, float, bytearray, bytes, bool,
                            complex, str]

# not supported for now (need to understand side effect, )
# - set, dict, range,, tuple, list      : cloud have inner objects
# - memoryview                          : returns unique memory location value


def cache_on_self(function):
    """
    Use this for cases where we want the cache to be tied to the Class instance (i.e. not global for all executions)
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        if len(args) == 0 or inspect.isclass(type(args[0])) is False:
            raise Exception("In Method_Wrappers.cache_on_self could not find self")

        self = args[0]                                              # get self
        cache_id = cache_on_self_get_cache_in_key(function, args, kwargs)
        if hasattr(self, cache_id) is False:                        # check if return_value has been set
            setattr(self, cache_id, function(*args, **kwargs))      # invoke function and capture the return value
        return getattr(self, cache_id)                              # return the return value
    return wrapper

def cache_on_self__args_to_str(args):
    args_values_as_str = ''
    if args:
        for arg in args:
            if type(arg) in CACHE_ON_SELF_TYPES:
                args_values_as_str += str(arg)
    return args_values_as_str

def cache_on_self__kwargs_to_str(kwargs):
    kwargs_values_as_str = ''
    if kwargs:
        for key,value in kwargs.items():
            if type(value) in CACHE_ON_SELF_TYPES:
                kwargs_values_as_str += f'{key}:{value}|'
    return kwargs_values_as_str

def cache_on_self_get_cache_in_key(function, args=None, kwargs=None):
        key_name   = function.__name__
        args_md5   = ''
        kwargs_md5 = ''
        args_values_as_str   = cache_on_self__args_to_str(args)
        kwargs_values_as_str = cache_on_self__kwargs_to_str(kwargs)
        if args_values_as_str:
            args_md5 = str_md5(args_values_as_str)
        if kwargs_values_as_str:
            kwargs_md5 = str_md5(kwargs_values_as_str)
        return f'{CACHE_ON_SELF_KEY_PREFIX}_{key_name}_{args_md5}_{kwargs_md5}'

        # class_name = self_obj.__class__.__name__
        #
        # function_name = function_obj.__name__
        # if params:
        #     params_as_string = '_'.join(str(x) for x in params).replace('/',' ')
        #     params_md5       = str_md5(params_as_string)
        #     return f'{class_name}_{function_name}_{params_md5}.gz'
        # else:
        #     return f'{class_name}_{function_name}.gz'