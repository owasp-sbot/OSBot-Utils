from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local import Sqlite__DB__Local
from osbot_utils.helpers.sqlite.domains.schemas.Schema__Table__Requests import Schema__Table__Requests

SQLITE_TABLE__REQUESTS = 'requests'

class Sqlite__DB__Requests(Sqlite__DB__Local):
    db_name     : str
    table_name  : str
    table_schema: type

    def __init__(self,db_path=None):
        self.table_name  = SQLITE_TABLE__REQUESTS
        self.table_schema = Schema__Table__Requests
        super().__init__(db_path=db_path)
