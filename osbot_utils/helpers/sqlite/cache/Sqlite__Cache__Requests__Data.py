import types
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.utils.Json import json_dumps
from osbot_utils.utils.Misc import str_sha256


class Sqlite__Cache__Requests__Data(Type_Safe):
    cache_table        : Sqlite__Table
    cache_request_data : types.MethodType

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

    # def cache_request_data(self, *args, **target_kwargs):
    #     return {'args': list(args), 'kwargs': target_kwargs}                                # convert the args tuple to a list since that is what it will be once it is serialised