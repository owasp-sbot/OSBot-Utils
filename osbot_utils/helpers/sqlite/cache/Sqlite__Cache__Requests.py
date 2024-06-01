import types
from osbot_utils.base_classes.Type_Safe                                     import Type_Safe
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Actions      import Sqlite__Cache__Requests__Actions
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Config       import Sqlite__Cache__Requests__Config
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Data         import Sqlite__Cache__Requests__Data
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Invoke import Sqlite__Cache__Requests__Invoke
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Row          import Sqlite__Cache__Requests__Row
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Sqlite       import Sqlite__Cache__Requests__Sqlite
from osbot_utils.utils.Json                                                 import json_loads
from osbot_utils.utils.Objects                                              import pickle_save_to_bytes, pickle_load_from_bytes


class Sqlite__Cache__Requests(Type_Safe):

    def __init__(self, db_path=None, db_name=None, table_name=None):
        super().__init__()

        # todo refactor this whole section to a DI (DependencyInjection / Type_Registry class, which is the one responsible for creating these objects in the right order of dependency)

        self.cache_config       = Sqlite__Cache__Requests__Config()
        self.config             = self.cache_config

        kwargs__cache_sqlite   = dict(config=self.cache_config, db_path=db_path, db_name=db_name, table_name=table_name)
        self.cache_sqlite      = Sqlite__Cache__Requests__Sqlite (**kwargs__cache_sqlite)
        self.sqlite_requests   = self.cache_sqlite.sqlite_requests
        self.cache_table       = self.cache_sqlite.cache_table



        kwargs__cache_table    = dict(                        cache_table        = self.cache_sqlite.cache_table())
        kwargs__cache_data     = dict(**kwargs__cache_table,  cache_request_data = self.cache_request_data        )
        kwargs__cache_row      = dict(**kwargs__cache_table,  config             = self.cache_config              )

        self.cache_row       = Sqlite__Cache__Requests__Row    (**kwargs__cache_row   )
        self.cache_data      = Sqlite__Cache__Requests__Data   (**kwargs__cache_data  )


        kwargs__cache_actions = dict(**kwargs__cache_table, cache_row=self.cache_row)
        self.cache_actions    = Sqlite__Cache__Requests__Actions(**kwargs__cache_actions  )

        kwargs__cache_invoke  = dict(cache_data       = self.cache_data         ,
                                     cache_actions    = self.cache_actions      ,
                                     config           = self.cache_config       )
        self.cache_invoke     = Sqlite__Cache__Requests__Invoke(**kwargs__cache_invoke)

        self.apply_refactoring_patches()

    def apply_refactoring_patches(self):
        self.cache_add                       = self.cache_actions.cache_add
        self.cache_delete                    = self.cache_actions.cache_delete
        self.create_new_cache_row_data       = self.cache_actions.create_new_cache_row_data

        self.cache_entries                   = self.cache_data.cache_entries
        self.cache_entry                     = self.cache_data.cache_entry
        self.cache_entry_comments            = self.cache_data.cache_entry_comments
        self.cache_entry_comments_update     = self.cache_data.cache_entry_comments_update
        self.cache_entry_for_request_params  = self.cache_data.cache_entry_for_request_params

        self.create_new_cache_obj            = self.cache_row.create_new_cache_obj

        self.cache_table__clear              = self.cache_sqlite.cache_table__clear
        self.delete_where_request_data       = self.cache_sqlite.delete_where_request_data
        self.rows_where                      = self.cache_sqlite.rows_where
        self.rows_where__request_data        = self.cache_sqlite.rows_where__request_data
        self.rows_where__request_hash        = self.cache_sqlite.rows_where__request_hash

        self.disable                         = self.cache_config.disable
        self.enable                          = self.cache_config.enable

        self.invoke                          = self.cache_invoke.invoke
        self.invoke_target                   = self.cache_invoke.invoke_target
        self.invoke_with_cache               = self.cache_invoke.invoke_with_cache
        self.invoke_target__and_add_to_cache = self.cache_invoke.invoke_target__and_add_to_cache
        self.transform_raw_response          = self.cache_invoke.transform_raw_response
        self.response_data_deserialize       = self.cache_invoke.response_data_deserialize
        self.response_data_serialize         = self.cache_invoke.response_data_serialize


    # FOR NOW: these methods cannot be refactored

    # this is the method that is current overwritten to create custom request data
    def cache_request_data(self, *args, **target_kwargs):
        return {'args': list(args), 'kwargs': target_kwargs}                                # convert the args tuple to a list since that is what it will be once it is serialised


    def set_on_invoke_target(self, on_invoke_target  : types.FunctionType):
        self.cache_invoke.on_invoke_target = on_invoke_target


    # methods to refactor


    def only_from_cache(self, value=True):
        self.config.cache_only_mode = value
        return self

    def response_data_for__request_hash(self, request_hash):
        rows = self.rows_where__request_hash(request_hash)
        if len(rows) > 0:
            cache_entry       = rows[0]
            response_data_obj = self.response_data_deserialize(cache_entry)
            return response_data_obj
        return {}

    def requests_data__all(self):
        requests_data = []
        for row in self.cache_table().rows():
            req_id           = row.get('id')
            request_data     = row.get('request_data')
            request_hash     = row.get('request_hash')
            request_comments = row.get('comments')

            request_data_obj = dict(request_data = request_data    ,
                                    _id          = req_id          ,
                                    _hash        =  request_hash   ,
                                    _comments    = request_comments)

            requests_data.append(request_data_obj)
        return requests_data

    def response_data__all(self):
        responses_data = []
        for row in self.cache_table().rows():
            response_data_obj = self.convert_row__to__response_data_obj(row)
            responses_data.append(response_data_obj)
        return responses_data

    def convert_row__to__response_data_obj(self, row):
        row_id            = row.get('id'           )
        comments          = row.get('comments'     )
        request_hash      = row.get('request_hash' )
        response_hash     = row.get('response_hash')
        response_data     = self.response_data_deserialize(row)
        response_data_obj = dict( comments      = comments      ,
                                  row_id        = row_id        ,
                                  request_hash  = request_hash  ,
                                  response_hash = response_hash ,
                                  response_data = response_data )
        return response_data_obj



    def update(self, value=True):
        self.config.update_mode = value
        return self

    def set__add_timestamp(self, value):
        self.config.add_timestamp = value
        return self