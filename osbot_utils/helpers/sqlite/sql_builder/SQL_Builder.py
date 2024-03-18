from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table


class SQL_Builder(Kwargs_To_Self):
    table      : Sqlite__Table

    def validate_query_data(self):
        if self.table.row_schema is None:
            raise ValueError("in SQL_Builder, there was no row_schema defined in the mapped table")