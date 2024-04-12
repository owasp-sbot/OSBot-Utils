import inspect
from functools import wraps

from osbot_utils.utils.Misc import str_md5

CACHE_ON_SELF_KEY_PREFIX = 'cache_on_function'
CACHE_ON_SELF_TYPES      = [int, float, bytearray, bytes, bool,
                            complex, str]

# todo: refactor with cache_on_self (since there is quite a lot of shared code)
def cache_on_function(function):
    """
    Use this for cases where we want the cache to be tied to the function instance or static method
    """
    @wraps(function)
    def wrapper(*args, **kwargs):
        target = function                                                   # use function as the cache target
        if 'reload_cache' in kwargs:                                        # if the reload parameter is set to True
            reload_cache = True                                             # set reload to True
            del kwargs['reload_cache']                                      # remove the reload parameter from the kwargs
        else:
            reload_cache = False                                            # otherwise set reload to False
        cache_id = cache_on_self__get_cache_in_key(function, args, kwargs)
        if reload_cache is True or hasattr(target, cache_id) is False:        # check if return_value has been set or if reload is True
            return_value = function(*args, **kwargs)                        # invoke function and capture the return value
            setattr(target, cache_id,return_value)                            # set the return value
        return getattr(target, cache_id)                                      # return the return value
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

def cache_on_self__get_cache_in_key(function, args=None, kwargs=None):
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