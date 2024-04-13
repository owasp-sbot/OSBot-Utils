from os import environ

from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.utils.Files import current_temp_folder, path_combine

ENV_NAME_PATH_LOCAL_DBS        = 'PATH_LOCAL_DBS'

class Sqlite__DB__Local(Sqlite__Database):
    db_name     : str
    table_name  : str
    table_schema: type

    def __init__(self, db_path=None):
        super().__init__(db_path=db_path or self.path_local_db())
        if not self.table_name:
            self.table_name = 'temp_table'
        self.setup()

    def path_db_folder(self):
        return environ.get(ENV_NAME_PATH_LOCAL_DBS) or current_temp_folder()

    def path_local_db(self):
        return path_combine(self.path_db_folder(), self.db_name)

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