from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table


class SQL_Builder(Kwargs_To_Self):
    table      : Sqlite__Table

    def validate_query_data(self):
        if self.table.row_schema is None:
            raise ValueError("in SQL_Builder, there was no row_schema defined in the mapped table")

    def select_for_fields(self,  field_names: list = None):
        valid_fields = self.table.fields_names__cached()
        if field_names is None:
            field_names = valid_fields
        elif isinstance(field_names, list) is False:
            raise ValueError(f"in sql_query_for_fields, field_names must be a list, it was :{field_names}")

        invalid_field_names = [name for name in field_names if name not in valid_fields]    # If no valid field names are provided, raise an error or return a default query
        if invalid_field_names:                                                             # If there are any invalid field names, raise an exception listing them
            message = f"Invalid field names provided: {', '.join(invalid_field_names)}"
            raise ValueError(message)

        fields_str = ', '.join(field_names)                         # Construct the SQL query string
        sql_query = f"SELECT {fields_str} FROM {self.table.table_name};"  # Join the valid field names with commas
        return sql_query