from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local               import Sqlite__DB__Local
from osbot_utils.helpers.sqlite.domains.schemas.Schema__Table__Requests import Schema__Table__Requests
from osbot_utils.utils.Misc import random_text

SQLITE_TABLE__REQUESTS = 'requests'

class Sqlite__DB__Requests(Sqlite__DB__Local):
    table_name  : str
    table_schema: type

    def __init__(self,db_path=None, db_name=None, table_name=None):
        self.table_name   = table_name or SQLITE_TABLE__REQUESTS
        self.table_schema = Schema__Table__Requests
        super().__init__(db_path=db_path, db_name=db_name)
        self.setup()

    @cache_on_self
    def table_requests(self):
        return self.table(self.table_name)

    def table_requests__create(self):
        with self.table_requests() as _:
            _.row_schema = self.table_schema                    # set the table_class
            if _.exists() is False:
                _.create()                                          # create if it doesn't exist
                _.index_create('request_hash')                      # add index to the request_hash field
                return True
        return False

    def table_requests__reset(self):
        self.table_requests().delete()
        return self.table_requests__create()

    def setup(self):
        self.table_requests__create()
        return self