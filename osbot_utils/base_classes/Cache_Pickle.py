import os
from functools import wraps

from osbot_utils.utils.Files import path_combine, folder_create, temp_folder_current, file_exists, \
    pickle_load_from_file, pickle_save_to_file, files_list, files_recursive
from osbot_utils.utils.Misc import str_md5
from osbot_utils.utils.Python_Logger import logger_info



class Cache_Pickle:

    _cache__FOLDER_CACHE_ROOT_FOLDER = '_cache_pickle'
    _cache__SUPPORTED_PARAMS_TYPES   = [int, float, bytearray, bytes, bool, complex, str]

    def __init__(self):
        self._cache_enabled = True
        #self.log_info      = logger_info()
        self._cache_setup()              # make sure the cache folder exists

    def __enter__(self): return self
    def __exit__ (self, type, value, traceback): pass

    def __getattribute__(self, name):
        if name.startswith('_cache_') or name.startswith('__'):                 # if the method is a method from Cache_Pickleor a private method
            return super().__getattribute__(name)                               # just return it's value
        target = super().__getattribute__(name)                                 # get the target
        if not callable(target):                                                # if it is not a function
            return target                                                       # just return it
        return self._cache_data(target)                                         # if it is a function, create a wrapper around it

    def _cache_clear(self):
        cache_dir = self._cache_path()
        for filename in os.listdir(cache_dir):
            if filename.endswith('.pickle'):
                os.remove(os.path.join(cache_dir, filename))
        return self

    def _cache_data(self, func):

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
            cache_file_name = self._cache_resolve_file_name(func, args, kwargs)

            # path_file = path_combine(self._cache_path(), f'{caller_name}.pickle')
            path_file = path_combine(self._cache_path(), cache_file_name)

            if use_cache is True and reload_cache is False and file_exists(path_file):
                return pickle_load_from_file(path_file)
            else:
                data = func(*args, **kwargs)
                if data and use_cache is True:
                    caller_name = func.__name__
                    #print(f"Saving cache file data for: {caller_name}")
                    pickle_save_to_file(data, path_file)
                return data
        return wrapper

    def _cache_disable(self):
        self._cache_enabled = False
        return self

    def _cache_path(self):
        class_name  = self.__class__.__name__
        module_name = self.__class__.__module__
        folder_name = f'{self._cache__FOLDER_CACHE_ROOT_FOLDER}/{module_name.replace(".", "/")}'
        if not module_name.endswith(class_name):
            folder_name += f'/{class_name}'
        return path_combine(temp_folder_current(), folder_name)

    def _cache_files(self):
        return files_recursive(self._cache_path())

    def _cache_setup(self):
        folder_create(self._cache_path())
        return self

    def _cache_kwargs_to_str(self, kwargs):
        kwargs_values_as_str = ''
        if kwargs:
            if type(kwargs) is not dict:
                return str(kwargs)
            for key, value in kwargs.items():
                if value and type(value) not in self._cache__SUPPORTED_PARAMS_TYPES:
                    value = '(...)'
                kwargs_values_as_str += f'{key}:{value}|'
        return kwargs_values_as_str

    def _cache_args_to_str(self, args):
        args_values_as_str = ''
        if args:
            if type(args) is not list:
                return str(args)
            for arg in args:
                if not arg or type(arg) in self._cache__SUPPORTED_PARAMS_TYPES:
                    arg_value = str(arg)
                else:
                    arg_value = '(...)'
                args_values_as_str += f'{arg_value}|'
        return args_values_as_str

    def _cache_resolve_file_name(self, function, args=None, kwargs=None):
        key_name               = function.__name__
        args_md5               = ''
        kwargs_md5             = ''
        args_values_as_str     = self._cache_args_to_str(args)
        kwargs_values_as_str   = self._cache_kwargs_to_str(kwargs)
        if args_values_as_str  : args_md5   = '_' + str_md5(args_values_as_str  )[:10]
        if kwargs_values_as_str: kwargs_md5 = '_' + str_md5(kwargs_values_as_str)[:10]
        cache_file_name        = f'{key_name}{args_md5}{kwargs_md5}'
        cache_file_name       += '.pickle'
        return cache_file_name