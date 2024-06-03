from osbot_utils.helpers.cache_requests.Cache__Requests__Table import Cache__Requests__Table
from osbot_utils.helpers.sqlite.Sqlite__Table                  import Sqlite__Table
from osbot_utils.utils.Json import json_dumps


class Sqlite__Cache__Requests__Table(Cache__Requests__Table):
    cache_table : Sqlite__Table

    def __init__(self, **kwargs):
        super().__init__( **kwargs)

        self.table_name           = self.cache_table.table_name
        self._table_create        = self.cache_table._table_create
        self.database             = self.cache_table.database
        self.clear                = self.cache_table.clear
        self.exists               = self.cache_table.exists
        self.indexes              = self.cache_table.indexes
        self.new_row_obj          = self.cache_table.new_row_obj
        self.row_add_and_commit   = self.cache_table.row_add_and_commit
        self.row_update           = self.cache_table.row_update
        self.row_schema           = self.cache_table.row_schema
        self.rows                 = self.cache_table.rows
        self.rows_delete_where    = self.cache_table.rows_delete_where
        self.schema__by_name_type = self.cache_table.schema__by_name_type
        self.select_rows_where    = self.cache_table.select_rows_where
        self.size                 = self.cache_table.size

    def cache_table__clear(self):
        return self.cache_table.clear()

    def delete_where_request_data(self, request_data):                                      # todo: check if it is ok to use the request_data as a query target, or if we should use the request_hash variable
        if type(request_data) is dict:                                                      # if we get an request_data obj
            request_data = json_dumps(request_data)                                         # convert it to the json dump
        if type(request_data) is str:                                                       # make sure we have a string
            if len(self.rows_where__request_data(request_data)) > 0:                        # make sure there is at least one entry to delete
                self.cache_table.rows_delete_where(request_data=request_data)             # delete it
                return len(self.rows_where__request_data(request_data)) == 0                # confirm it was deleted
        return False                                                                        # if anything was not right, return False

    def rows_where(self, **kwargs):
        return self.cache_table.select_rows_where(**kwargs)

    def rows_where__request_data(self, request_data):
        return self.rows_where(request_data=request_data)

    def rows_where__request_hash(self, request_hash):
        return self.rows_where(request_hash=request_hash)

