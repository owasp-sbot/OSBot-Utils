import types
from osbot_utils.base_classes.Kwargs_To_Self                    import Kwargs_To_Self
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Requests    import Sqlite__DB__Requests
from osbot_utils.utils.Json                                     import json_dumps, json_loads
from osbot_utils.utils.Misc                                     import str_sha256, timestamp_utc_now
from osbot_utils.utils.Objects                                  import pickle_save_to_bytes, pickle_load_from_bytes
from osbot_utils.utils.Toml import toml_to_dict


class Sqlite__Cache__Requests(Kwargs_To_Self):
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

    def cache_add(self, request_data, response_data):
        new_row_obj = self.create_new_cache_obj(request_data, response_data)
        return self.cache_table().row_add_and_commit(new_row_obj)

    def cache_delete(self, request_data):
        request_data        = json_dumps(request_data)
        request_data_sha256 = str_sha256(request_data)
        return self.cache_table().rows_delete_where(request_hash=request_data_sha256)

    def cache_entries(self):
        return self.cache_table().rows()

    def cache_entry(self, request_data):
        request_data        = json_dumps(request_data)
        request_data_sha256 = str_sha256(request_data)
        data                = self.cache_table().select_rows_where(request_hash=request_data_sha256)
        if len(data) > 0:                       # todo: add logic to handle (or log), where there are multiple entries with the same hash
            return data[0]
        return {}

    def cache_entry_comments(self, model_id, body):
        cache_entry = self.cache_entry_for_request_params(model_id=model_id, body=body)
        return cache_entry.get('comments')

    def cache_entry_comments_update(self, model_id, body, new_comments):
        cache_entry      = self.cache_entry_for_request_params(model_id=model_id, body=body)
        request_hash     = cache_entry.get('request_hash')
        update_fields    = dict(comments=new_comments)
        query_conditions = dict(request_hash=request_hash)
        result           = self.cache_table().row_update(update_fields, query_conditions)
        return result

    def cache_entry_for_request_params(self, *args, **target_kwargs):
        request_data = self.cache_request_data(*args, **target_kwargs)
        return self.cache_entry(request_data)

    def create_new_cache_data(self, request_data, response_data):
        request_data_json  = json_dumps(request_data)
        request_data_hash  = str_sha256(request_data_json)
        if self.add_timestamp:
            timestamp = timestamp_utc_now()
        else:
            timestamp = 0
        cache_cata = dict(comments       = ''                  ,
                          metadata       = ''                  ,
                          request_data   = request_data_json   ,
                          request_hash   = request_data_hash   ,
                          request_type   = ''                  ,
                          response_bytes = b''                 ,
                          response_data  = ''                  ,
                          response_hash  = ''                  ,
                          response_type  = ''                  ,
                          source         = ''                  ,
                          timestamp      = timestamp           )
        if self.pickle_response:
            cache_cata['response_bytes'] = response_data
        else:
            response_data_json = json_dumps(response_data)
            response_data_hash = str_sha256(response_data_json)
            cache_cata['response_data'] = response_data_json
            cache_cata['response_hash'] = response_data_hash
        return cache_cata

    def create_new_cache_obj(self, request_data, response_data):
        new_row_data = self.create_new_cache_data(request_data, response_data)
        new_row_obj = self.cache_table().new_row_obj(new_row_data)
        return new_row_obj

    def cache_table(self):
        return self.sqlite_requests.table_requests()

    def cache_table__clear(self):
        return self.cache_table().clear()

    def cache_request_data(self, *args, **target_kwargs):
        return {'args': list(args), 'kwargs': target_kwargs}                                # convert the args tuple to a list since that is what it will be once it is serialised


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
            req_id           = row.get('id')
            response_data     = row.get('response_data')
            response_hash     = row.get('response_hash')

            response_data_obj = dict(response_data = response_data    ,
                                    _id            = req_id          ,
                                    _hash          = response_hash   )

            responses_data.append(response_data_obj)
        return responses_data



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