from osbot_utils.base_classes.Type_Safe                                 import Type_Safe
from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Config   import Sqlite__Cache__Requests__Config
from osbot_utils.helpers.sqlite.cache.db.Sqlite__DB__Requests           import Sqlite__DB__Requests
from osbot_utils.utils.Json                                             import json_dumps


class Sqlite__Cache__Requests__Sqlite(Type_Safe):
    sqlite_requests : Sqlite__DB__Requests              = None
    config          : Sqlite__Cache__Requests__Config
    db_path         : str
    db_name         : str
    table_name      : str
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sqlite_requests = Sqlite__DB__Requests(db_path=self.db_path, db_name=self.db_name, table_name=self.table_name)

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

    def rows_where(self, **kwargs):
        return self.cache_table().select_rows_where(**kwargs)

    def rows_where__request_data(self, request_data):
        return self.rows_where(request_data=request_data)

    def rows_where__request_hash(self, request_hash):
        return self.rows_where(request_hash=request_hash)
