from osbot_utils.base_classes.Type_Safe                         import Type_Safe
from osbot_utils.helpers.cache_requests.Cache__Requests__Config import Cache__Requests__Config
from osbot_utils.helpers.sqlite.cache.Sqlite__DB__Requests      import Sqlite__DB__Requests


class Sqlite__Cache__Requests__Sqlite(Type_Safe):
    sqlite_requests : Sqlite__DB__Requests              = None
    config          : Cache__Requests__Config
    db_path         : str
    db_name         : str
    table_name      : str
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sqlite_requests = Sqlite__DB__Requests(db_path=self.db_path, db_name=self.db_name, table_name=self.table_name)

    def cache_table(self):
        return self.sqlite_requests.table_requests()

