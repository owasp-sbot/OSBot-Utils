from osbot_utils.base_classes.Type_Safe                                     import Type_Safe
from osbot_utils.helpers.sqlite.Sqlite__Table                               import Sqlite__Table
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Row          import Sqlite__Cache__Requests__Row
from osbot_utils.utils.Json import json_dumps
from osbot_utils.utils.Misc import str_sha256


class Sqlite__Cache__Requests__Actions(Type_Safe):
    cache_table      : Sqlite__Table
    cache_row        : Sqlite__Cache__Requests__Row

    def cache_add(self, request_data, response_data):
        new_row_obj = self.cache_row.create_new_cache_obj(request_data, response_data)
        return self.cache_table.row_add_and_commit(new_row_obj)

    def cache_delete(self, request_data):
        request_data        = json_dumps(request_data)
        request_data_sha256 = str_sha256(request_data)
        return self.cache_table.rows_delete_where(request_hash=request_data_sha256)


    # def create_new_cache_obj(self, request_data, response_data):
    #     new_row_data = self.create_new_cache_row_data(request_data, response_data)
    #     new_row_obj = self.cache_table.new_row_obj(new_row_data)
    #     return new_row_obj

    def create_new_cache_row_data(self, request_data, response_data):
        new_row_data        = self.cache_row.create_new_cache_row_data(request_data, response_data)
        return new_row_data
