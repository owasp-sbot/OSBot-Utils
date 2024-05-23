from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local import Sqlite__DB__Local
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Files import Sqlite__Table__Files


class Sqlite__DB__Files(Sqlite__DB__Local):

    def __init__(self, db_path=None, db_name=None):
        super().__init__(db_path=db_path, db_name=db_name)

    def add_file(self, path, contents=None, metadata=None):
        return self.table_files().add_file(path, contents, metadata)

    @cache_on_self
    def table_files(self):
        return Sqlite__Table__Files(database=self).setup()

    def files(self):
        return self.table_files().files()

    def setup(self):
        self.table_files()
        return self