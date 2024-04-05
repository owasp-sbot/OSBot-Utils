from osbot_utils.utils.Misc import str_md5

from osbot_utils.utils.Files import temp_folder_current, path_combine, folder_create

from osbot_utils.utils.Json import json_load_file_gz, json_save_file_gz

#todo: add feature to only cache for some time (for example 2 minutes or 2 hours)
#      this will solve a number of probs with the current usability of this data

class cache_on_tmp:
    """
    Caches the return value of the wrapped method in tmp folder
    Takes into account the request params to create the file name used for caching
    """
    def __init__(self, reload_data=False, return_cache_key=False):
        self.cache_folder_name = "osbot_cache_on_tmp"
        self.cache_folder      = path_combine(temp_folder_current(), self.cache_folder_name)
        self.last_cache_path   = None
        self.return_cache_key  = return_cache_key
        self.reload_data       = reload_data
        folder_create(self.cache_folder)
        #print(self.last_cache_path)

    def __call__(self, function):
        def wrapper(*args,**kwargs):
            params     = list(args)
            if len(params) > 0:
                self_obj   = params.pop(0)
            else:
                self_obj = self                  # has the side effect that the cache key is only locked to the method name
            cache_path = self.get_cache_in_tmp_path(self_obj, function, params)
            if self.return_cache_key:
                return cache_path
            data       = self.get_cache_in_tmp_data(cache_path)
            if data and self.reload_data is False:
               return data

            function_data = function(*args,**kwargs)
            return self.save_cache_in_tmp_data(cache_path,function_data)

        return wrapper

    def get_cache_in_tmp_key(self, self_obj, function_obj, params):
        class_name = self_obj.__class__.__name__
        # if function_obj.__class__.__name__ == 'str':      # todo: check if this is needed
        #     function_name = function_obj
        # else:
        #     function_name = function_obj.__name__
        function_name = function_obj.__name__
        if params:
            params_as_string = '_'.join(str(x) for x in params).replace('/',' ')
            params_md5       = str_md5(params_as_string)
            return f'{class_name}_{function_name}_{params_md5}.gz'
        else:
            return f'{class_name}_{function_name}.gz'

    def get_cache_in_tmp_path(self, self_obj, function_obj, params):
        cache_key            = self.get_cache_in_tmp_key(self_obj, function_obj, params)
        cache_path           = path_combine(self.cache_folder,cache_key)
        self.last_cache_path = cache_path
        return cache_path
        #return '/tmp/cache_in_tmp_{0}.gz'.format(cache_key)

    # todo: refactor to use pickle for data load
    def get_cache_in_tmp_data(self, cache_path):
        return json_load_file_gz(path=cache_path)

    # todo: refactor to use pickle for data save
    def save_cache_in_tmp_data(self, cache_path, data):
        json_save_file_gz(path=cache_path, python_object=data)
        return data