import types
from osbot_utils.base_classes.Type_Safe                                     import Type_Safe
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Actions      import Sqlite__Cache__Requests__Actions
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Data         import Sqlite__Cache__Requests__Data
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Row__Config  import Sqlite__Cache__Requests__Row__Config
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Row          import Sqlite__Cache__Requests__Row
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Requests                import Sqlite__DB__Requests
from osbot_utils.utils.Json                                                 import json_dumps, json_loads
from osbot_utils.utils.Misc                                                 import str_sha256, timestamp_utc_now, bytes_sha256
from osbot_utils.utils.Objects                                              import pickle_save_to_bytes, pickle_load_from_bytes
from osbot_utils.utils.Toml                                                 import toml_to_dict


class Sqlite__Cache__Requests(Type_Safe):
    add_timestamp     : bool                 = True
    add_source_location:bool                 = True
    enabled           : bool                 = True
    update_mode       : bool                 = False
    cache_only_mode   : bool                 = False
    sqlite_requests   : Sqlite__DB__Requests = None
    pickle_response   : bool                 = False
    capture_exceptions: bool                 = False                # once this is working, it might be more useful to have this set to true
    exception_classes : list
    on_invoke_target  : types.FunctionType

    def __init__(self, db_path=None, db_name=None, table_name=None):
        self.sqlite_requests = Sqlite__DB__Requests(db_path=db_path, db_name=db_name, table_name=table_name)
        super().__init__()
        kwargs__cache_table    = dict(                        cache_table        = self.cache_table())
        kwargs__cache_data     = dict(**kwargs__cache_table,  cache_request_data = self.cache_request_data )
        kwargs__cache_row      = dict(**kwargs__cache_table,  config             = self.cache_row_config() )

        self.cache_row       = Sqlite__Cache__Requests__Row    (**kwargs__cache_row      )
        self.cache_data      = Sqlite__Cache__Requests__Data   (**kwargs__cache_data     )

        kwargs__cache_actions = dict(**kwargs__cache_table, cache_row=self.cache_row)

        self.cache_actions   = Sqlite__Cache__Requests__Actions(**kwargs__cache_actions  )


        self.apply_refactoring_paches()

    def apply_refactoring_paches(self):
        self.cache_add                      = self.cache_actions.cache_add
        self.cache_delete                   = self.cache_actions.cache_delete
        self.cache_entries                  = self.cache_data.cache_entries
        self.cache_entry                    = self.cache_data.cache_entry
        self.cache_entry_comments           = self.cache_data.cache_entry_comments
        self.cache_entry_comments_update    = self.cache_data.cache_entry_comments_update
        self.cache_entry_for_request_params = self.cache_data.cache_entry_for_request_params
        self.create_new_cache_obj           = self.cache_row.create_new_cache_obj
        self.create_new_cache_row_data      = self.cache_actions.create_new_cache_row_data


    # this is the method that is current overwritten to create custom request data
    def cache_request_data(self, *args, **target_kwargs):
        return {'args': list(args), 'kwargs': target_kwargs}                                # convert the args tuple to a list since that is what it will be once it is serialised

    def cache_row_config(self):
        kwargs = dict(pickle_response = self.pickle_response ,
                      add_timestamp   = self.add_timestamp )
        config  = Sqlite__Cache__Requests__Row__Config(**kwargs)
        return config



    def cache_table(self):
        return self.sqlite_requests.table_requests()

    def cache_table__clear(self):
        return self.cache_table().clear()



    def delete_where_request_data(self, request_data):                                      # todo: check if it is ok to use the request_data as a query target, or if we should use the request_hash variable
        if type(request_data) is dict:                                                      # if we get an request_data obj
            request_data = json_dumps(request_data)                                         # convert it to the json dump
        if type(request_data) is str:                                                       # make sure we have a string
            if len(self.rows_where__request_data(request_data)) > 0:                        # make sure there is at least one entry to delete
                self.cache_table().rows_delete_where(request_data=request_data)             # delete it
                return len(self.rows_where__request_data(request_data)) == 0                # confirm it was deleted
        return False                                                                        # if anything was not right, return False

    def disable(self):
        self.enabled = False
        return self

    def enable(self):
        self.enabled = True
        return self

    def invoke(self, target, target_args, target_kwargs):
        return self.invoke_with_cache(target, target_args, target_kwargs)

    def invoke_target(self, target, target_args, target_kwargs):
        if self.on_invoke_target:
            raw_response = self.on_invoke_target(target, target_args, target_kwargs)
        else:
            raw_response = target(*target_args, **target_kwargs)
        return self.transform_raw_response(raw_response)

    def invoke_with_cache(self, target, target_args, target_kwargs, request_data=None):
        if self.enabled is False:
            if self.cache_only_mode:
                return None
            return self.invoke_target(target, target_args, target_kwargs)
        if request_data is None:
            request_data  = self.cache_request_data(*target_args, **target_kwargs)
        cache_entry   = self.cache_entry(request_data)
        if cache_entry:
            if self.update_mode is True:
                self.cache_delete(request_data)
            else:
                return self.response_data_deserialize(cache_entry)
        if self.cache_only_mode is False:
            return self.invoke_target__and_add_to_cache(request_data, target, target_args, target_kwargs)


    def invoke_target__and_add_to_cache(self,request_data, target, target_args, target_kwargs):
        try:
            response_data_obj = self.invoke_target(target, target_args, target_kwargs)
            response_data     = self.response_data_serialize(response_data_obj)
            self.cache_add(request_data=request_data, response_data=response_data)
            return response_data_obj
        except Exception as exception:
            if self.capture_exceptions:
                response_data     = self.response_data_serialize(exception)
                self.cache_add(request_data=request_data, response_data=response_data)
            raise exception

    def only_from_cache(self, value=True):
        self.cache_only_mode = value
        return self

    def response_data_deserialize(self, cache_entry):
        if self.pickle_response:
            response_bytes = cache_entry.get('response_bytes')
            response_data_obj =  pickle_load_from_bytes(response_bytes)
        else:
            response_data = cache_entry.get('response_data')
            response_data_obj = json_loads(response_data)
        if self.capture_exceptions:
            if (type(response_data_obj) is Exception or                     # raise if it is an exception
                type(response_data_obj) in self.exception_classes):         # or if one of the types that have been set as being exception classes
                    raise response_data_obj
            # else:
            #     pprint(type(response_data_obj))
        return response_data_obj

    def response_data_serialize(self, response_data):
        if self.pickle_response:
            return pickle_save_to_bytes(response_data)
        return response_data

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



    def rows_where(self, **kwargs):
        return self.cache_table().select_rows_where(**kwargs)

    def rows_where__request_data(self, request_data):
        return self.rows_where(request_data=request_data)

    def rows_where__request_hash(self, request_hash):
        return self.rows_where(request_hash=request_hash)

    def transform_raw_response(self, raw_response):
        return raw_response

    def update(self, value=True):
        self.update_mode = value
        return self

    def set__add_timestamp(self, value):
        self.add_timestamp                                = value
        self.cache_row.config.add_timestamp = value  # todo: remove this temp fix for passing in the timestamp
        return self