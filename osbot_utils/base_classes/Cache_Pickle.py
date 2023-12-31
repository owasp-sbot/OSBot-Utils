import os
from functools import wraps

from osbot_utils.utils.Files import path_combine, folder_create, temp_folder_current, file_exists, pickle_load_from_file, pickle_save_to_file
from osbot_utils.utils.Misc import str_md5
from osbot_utils.utils.Python_Logger import logger_info

FOLDER_CACHE_ROOT_FOLDER = '_cache_pickle'
SUPPORTED_PARAMS_TYPES   = [int, float, bytearray, bytes, bool, complex, str]

class Cache_Pickle:

    def __init__(self):
        self.cache_enabled = True
        self.log_info      = logger_info()
        self.cache_setup()              # make sure the cache folder exists


    def __getattribute__(self, name):
        if name.startswith('cache_') or name.startswith('__'):
            return super().__getattribute__(name)

        target = super().__getattribute__(name)
        if not callable(target):
            return target

        return self.cache_data(target)

    def cache_clear(self):
        cache_dir = self.cache_path()
        for filename in os.listdir(cache_dir):
            if filename.endswith('.pickle'):
                os.remove(os.path.join(cache_dir, filename))
        return self

    def cache_data(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            if type(func.__self__) != type(self):       # if the parent type of the function is not self, then just execute it (this happens if a function is set as a variable)
                return func(*args, **kwargs)

            # first check the params that are specific for this cache method (and cannot be propagated)
            if 'reload_cache' in kwargs:                                        # if the reload parameter is set to True
                reload_cache = kwargs['reload_cache']                           # set reload to the value provided
                del kwargs['reload_cache']                                      # remove the reload parameter from the kwargs
            else:
                reload_cache = False                                            # otherwise set reload to False

            if 'use_cache' in kwargs:                                           # see if we want to disable cache
                use_cache = kwargs['use_cache']
                del kwargs['use_cache']
            else:
                use_cache = True
            # after processing these extra params we can resolve the file name and check if it exists
            cache_file_name = self.cache_resolve_file_name(func, args, kwargs)

            # path_file = path_combine(self.cache_path(), f'{caller_name}.pickle')
            path_file = path_combine(self.cache_path(), cache_file_name)

            if use_cache is True and reload_cache is False and file_exists(path_file):
                return pickle_load_from_file(path_file)
            else:
                data = func(*args, **kwargs)
                if data and use_cache is True:
                    caller_name = func.__name__
                    self.log_info(f"Saving cache file data for: {caller_name}")
                    pickle_save_to_file(data, path_file)
                return data
        return wrapper

    def cache_disable(self):
        self.cache_enabled = False

    def cache_path(self):
        module_name = self.__class__.__module__
        folder_name = f'{FOLDER_CACHE_ROOT_FOLDER}/{module_name.replace(".", "/")}'
        return path_combine(temp_folder_current(), folder_name)


    def cache_setup(self):
        folder_create(self.cache_path())
        return self

    def cache_kwargs_to_str(self, kwargs):
        kwargs_values_as_str = ''
        if kwargs:
            for key, value in kwargs.items():
                if type(value) in SUPPORTED_PARAMS_TYPES:
                    kwargs_values_as_str += f'{key}:{value}|'
        return kwargs_values_as_str

    def cache_args_to_str(self, args):
        args_values_as_str = ''
        if args:
            for arg in args:
                if type(arg) in SUPPORTED_PARAMS_TYPES:
                    args_values_as_str += str(arg)
        return args_values_as_str

    def cache_resolve_file_name(self, function, args=None, kwargs=None):
        key_name               = function.__name__
        args_md5               = ''
        kwargs_md5             = ''
        args_values_as_str     = self.cache_args_to_str(args)
        kwargs_values_as_str   = self.cache_kwargs_to_str(kwargs)
        if args_values_as_str  : args_md5   = '_' + str_md5(args_values_as_str  )
        if kwargs_values_as_str: kwargs_md5 = '_' + str_md5(kwargs_values_as_str)
        cache_file_name        = f'{key_name}{args_md5}{kwargs_md5}'
        cache_file_name       += '.pickle'
        return cache_file_name