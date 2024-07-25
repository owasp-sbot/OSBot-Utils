from typing import Dict, Type

from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Config import Sqlite__Table__Config, SQLITE__TABLE_NAME__CONFIG, \
    Schema__Table__Config


class Sqlite__DB(Sqlite__Database):

    # methods to override
    def tables_to_add(self):            # use this to define the tables that should be automatically created on setup
        return {}

    def db_not_configured(self):
        return self.tables_names() == []

    @cache_on_self
    def table_config(self):
        return Sqlite__Table__Config(database=self)



    def tables_names(self, include_sqlite_master=False, include_indexes=False):
        return super().tables_names(include_sqlite_master=include_sqlite_master, include_indexes=include_indexes)

    def setup(self):
        if self.db_not_configured():
            self.table_config().setup()
            for table_name, row_schema in self.tables_to_add().items():
                table = self.table(table_name)
                table.row_schema = row_schema
                table.create()
        return self
