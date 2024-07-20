from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local import Sqlite__DB__Local
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Files import Sqlite__Table__Files


class Sqlite__DB__Files(Sqlite__DB__Local):

    def __init__(self, db_path=None, db_name=None):
        super().__init__(db_path=db_path, db_name=db_name)

    def add_file(self, path, contents=None, metadata=None):
        return self.table_files().add_file(path, contents, metadata)

    def clear_table(self):
        self.table_files().clear()

    def delete_file(self, path):
        return self.table_files().delete_file(path)

    def file(self, path, include_contents=False):
        return self.table_files().file(path, include_contents=include_contents)

    def file_contents(self, path):
        return self.table_files().file_contents(path)

    def file__with_content(self, path):
        return self.file(path, include_contents=True)

    def file_exists(self, path):
        return self.table_files().file_exists(path)

    def file_names(self):
        return self.table_files().select_field_values('path')

    @cache_on_self
    def table_files(self):
        return Sqlite__Table__Files(database=self).setup()

    @index_by
    def files(self,include_contents=False):
        return self.table_files().files(include_contents=include_contents)

    def files__with_content(self):
        return self.files(include_contents=True)

    def files__by_path(self):
        return self.files(index_by='path')

    def setup(self):
        self.table_files()
        return self