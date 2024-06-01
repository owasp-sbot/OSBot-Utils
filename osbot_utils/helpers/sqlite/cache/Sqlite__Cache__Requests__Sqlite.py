from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Requests import Sqlite__DB__Requests


class Sqlite__Cache__Requests__Sqlite(Type_Safe):
    sqlite_requests   : Sqlite__DB__Requests = None

    def __init__(self, db_path=None, db_name=None, table_name=None):
        super().__init__()
        self.sqlite_requests = Sqlite__DB__Requests(db_path=db_path, db_name=db_name, table_name=table_name)
