from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table


class SQL_Builder(Kwargs_To_Self):
    table      : Sqlite__Table
    row_schema : type

    def validate_query_data(self):
        return

class SQL_Builder__Select(SQL_Builder):

    def build(self):
        self.validate_query_data()

        return f"SELECT * FROM *"

    def validate_query_data(self):
        super().validate_query_data()