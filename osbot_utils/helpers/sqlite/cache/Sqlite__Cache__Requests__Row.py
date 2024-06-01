from osbot_utils.base_classes.Type_Safe                                     import Type_Safe
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Row__Config  import Sqlite__Cache__Requests__Row__Config
from osbot_utils.utils.Json                                                 import json_dumps
from osbot_utils.utils.Misc                                                 import str_sha256, timestamp_utc_now, bytes_sha256



class Sqlite__Cache__Requests__Row(Type_Safe):
    config : Sqlite__Cache__Requests__Row__Config


    def create_new_cache_row_data(self, request_data, response_data):       # todo refactor this method into sub methods (one that map the request and one that maps the response)
        request_data_json  = json_dumps(request_data)
        request_data_hash  = str_sha256(request_data_json)
        if self.config.add_timestamp:
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
        return cache_cata