from osbot_utils.helpers.sqlite.Sqlite__Table                import Sqlite__Table
from osbot_utils.helpers.sqlite.cache.Cache__Requests__Table import Cache__Requests__Table


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
