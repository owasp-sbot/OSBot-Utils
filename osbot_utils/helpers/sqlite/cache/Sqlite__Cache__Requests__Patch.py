import types

from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests   import Sqlite__Cache__Requests
from osbot_utils.utils.Misc                                     import random_text


class Sqlite__Cache__Requests__Patch(Sqlite__Cache__Requests):
    db_name             : str                = random_text('requests_cache_')
    table_name          : str                = random_text('requests_table_')
    pickle_response     : bool               = True                                     # todo: move this from this file since the pickle setting is not relevant to Sqlite__Cache__Requests__Patch (it should be set by who needs it )
    target_function     : types.FunctionType
    target_class        : object
    target_function_name: str

    def __init__(self, db_path=None):
        super().__init__(db_path=db_path, db_name=self.db_name, table_name=self.table_name)

    def __enter__(self):
        self.patch_apply()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.patch_restore()
        return

    def delete(self):
        return self.sqlite_requests.delete()

    def proxy_method(self, *args, **kwargs):
        request_data  = self.request_data (*args, **kwargs)
        target_kwargs = self.target_kwargs(*args, **kwargs)
        target_args   = self.target_args  (*args, **kwargs)

        invoke_kwargs = dict(target       = self.target_function,
                             target_args   = target_args        ,
                             target_kwargs = target_kwargs      ,
                             request_data  = request_data       )

        return self.invoke_with_cache(**invoke_kwargs)

    def patch_apply(self):
        if (type(self.target_class)   is object or
            self.target_function      is None   or
            self.target_function_name  == ''     ):
                raise ValueError('target_function, target_object and target_function_name must be set')
        def proxy(*args, **kwargs):
            return self.proxy_method(*args, **kwargs)
        setattr(self.target_class, self.target_function_name, proxy)
        return self

    def patch_restore(self):
        setattr(self.target_class, self.target_function_name, self.target_function)

    def request_data(self, *args, **kwargs):
        return {'args'  : args   ,
                'kwargs': kwargs }

    def target_args(self, *args, **kwargs):
        return args

    def target_kwargs(self, *args, **kwargs):
        return kwargs
