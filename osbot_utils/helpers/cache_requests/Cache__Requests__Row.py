from osbot_utils.type_safe.Type_Safe                         import Type_Safe
from osbot_utils.helpers.cache_requests.Cache__Requests__Config import Cache__Requests__Config
from osbot_utils.helpers.cache_requests.Cache__Requests__Table  import Cache__Requests__Table
from osbot_utils.utils.Json                                     import json_dumps
from osbot_utils.utils.Misc                                     import str_sha256, timestamp_utc_now, bytes_sha256



class Cache__Requests__Row(Type_Safe):
    config      : Cache__Requests__Config
    cache_table : Cache__Requests__Table

    # todo: duplicated method with Sqlite__Cache__Requests (which is the one that is being overwritten)
    #       this need to change to use the 'cache_key' workflow
    def cache_request_data(self, *args, **target_kwargs):
        return {'args'  : list(args)    ,
                'kwargs': target_kwargs }                   # convert the args tuple to a list since that is what it will be once it is serialised

    def create_new_cache_obj(self, request_data, response_data):
        new_row_data = self.create_new_cache_row_data(request_data, response_data)
        new_row_obj = self.cache_table.new_row_obj(new_row_data)
        return new_row_obj

    def create_new_cache_row_data(self, request_data, response_data):       # todo refactor this method into sub methods (one that map the request and one that maps the response)
        request_data_json  = json_dumps(request_data)
        request_data_hash  = str_sha256(request_data_json)
        if self.config.add_timestamp:
            timestamp = timestamp_utc_now()
        else:
            timestamp = 0
        cache_cata = dict(request_data   = request_data_json   ,
                          request_hash   = request_data_hash   ,
                          timestamp      = timestamp           )

        self.map_response_data(cache_cata, response_data)
        return cache_cata

    def map_response_data(self, cache_cata, response_data):
        response_data_str   = ''
        response_data_bytes = b''
        if self.config.pickle_response:
            response_type             = 'pickle'
            response_data_bytes       = response_data
            response_data_hash        = bytes_sha256(response_data_bytes)

        else:
            if type(response_data)   is bytes:
                response_type         = 'bytes'
                response_data_bytes   =  response_data
                response_data_hash    = bytes_sha256(response_data_bytes)
            elif type(response_data) is dict:
                response_type         = 'dict'
                response_data_str     = json_dumps(response_data)
                response_data_hash    = str_sha256(response_data_str)
            else:
                response_type         = 'str'
                response_data_str     = str(response_data)
                response_data_hash    = str_sha256(response_data_str)

        cache_cata['response_bytes'] = response_data_bytes
        cache_cata['response_data' ]  = response_data_str
        cache_cata['response_hash' ]  = response_data_hash
        cache_cata['response_type' ]  = response_type

