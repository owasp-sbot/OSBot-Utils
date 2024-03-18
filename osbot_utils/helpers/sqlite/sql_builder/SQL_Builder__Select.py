from osbot_utils.helpers.sqlite.sql_builder.SQL_Builder import SQL_Builder


class SQL_Builder__Select(SQL_Builder):

    def build(self):
        self.validate_query_data()

        return f"SELECT * FROM *"

    def validate_query_data(self):
        super().validate_query_data()