import types
from osbot_utils.base_classes.Type_Safe                                     import Type_Safe
from osbot_utils.helpers.cache_requests.Cache__Requests__Config             import Cache__Requests__Config
from osbot_utils.helpers.cache_requests.Cache__Requests__Table              import Cache__Requests__Table
from osbot_utils.utils.Json                                                 import json_dumps, json_loads
from osbot_utils.utils.Misc                                                 import str_sha256
from osbot_utils.utils.Objects                                              import pickle_save_to_bytes, pickle_load_from_bytes


class Cache__Requests__Data(Type_Safe):
    cache_table        : Cache__Requests__Table
    cache_request_data : types.MethodType
    config             : Cache__Requests__Config

    def cache_entries(self):
        return self.cache_table.rows()

    def cache_entry(self, request_data):
        request_data        = json_dumps(request_data)
        request_data_sha256 = str_sha256(request_data)
        data                = self.cache_table.select_rows_where(request_hash=request_data_sha256)

        if len(data) > 0:                                   # todo: add logic to handle (or log), where there are multiple entries with the same hash
            return data[0]
        return {}

    def cache_entry_comments(self, *args, **target_kwargs):
        cache_entry = self.cache_entry_for_request_params(*args, **target_kwargs)
        return cache_entry.get('comments')

    def cache_entry_comments_update(self, new_comments, *args, **target_kwargs):
        cache_entry      = self.cache_entry_for_request_params(*args, **target_kwargs)
        request_hash     = cache_entry.get('request_hash')
        update_fields    = dict(comments=new_comments)
        query_conditions = dict(request_hash=request_hash)
        result           = self.cache_table.row_update(update_fields, query_conditions)
        return result

    def cache_entry_for_request_params(self, *args, **target_kwargs):
        request_data = self.cache_request_data(*args, **target_kwargs)
        return self.cache_entry(request_data)



    def response_data_for__request_hash(self, request_hash):
        rows = self.cache_table.rows_where__request_hash(request_hash)
        if len(rows) > 0:
            cache_entry       = rows[0]
            response_data_obj = self.response_data_deserialize(cache_entry)
            return response_data_obj
        return {}

    def requests_data__all(self):
        requests_data = []
        for row in self.cache_table.rows():
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
        for row in self.cache_table.rows():
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

    def response_data_deserialize(self, cache_entry):
        if self.config.pickle_response:                                             # todo: refactor our this logic, since this needs to be done in sync with the response_type value
            response_bytes = cache_entry.get('response_bytes')
            response_data_obj =  pickle_load_from_bytes(response_bytes)
        else:
            response_data = cache_entry.get('response_data')
            response_data_obj = json_loads(response_data)                           # todo: review the other scenarios of response_type
        if self.config.capture_exceptions:
            if (type(response_data_obj) is Exception or                             # raise if it is an exception
                type(response_data_obj) in self.config.exception_classes):          # or if one of the types that have been set as being exception classes
                    raise response_data_obj
        return response_data_obj

    def response_data_serialize(self, response_data):
        if self.config.pickle_response:
            try:
                return pickle_save_to_bytes(response_data)
            except:                                         # todo: look at a better way to handle this and any possible side effects (saw this with a couple boto3 class)
                return None
        return response_data