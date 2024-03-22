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

    def sql_command_delete_table(self):
        return f'DELETE FROM {self.table.table_name}'

    def sql_command_for_insert(self, record):
        valid_field_names = self.table.fields_names__cached()
        if type(record) is dict:
            if record:
                field_names   = record.keys()
                params        =  list(record.values())
                for field_name in field_names:
                    if field_name not in valid_field_names:
                        raise ValueError(f'in sql_command_for_insert, there was a field_name "{field_name}" that did exist in the current table')

                columns       = ', '.join(field_names)                                                         # Construct column names and placeholders
                placeholders  = ', '.join(['?' for _ in field_names])
                sql_command   = f'INSERT INTO {self.table.table_name} ({columns}) VALUES ({placeholders})'    # Construct the SQL statement
                return sql_command, params

    def sql_query_for_fields(self, field_names: list = None):
        return self.select_for_fields(field_names)

    def sql_query_for_select_field_name(self, field_name):
        if field_name:
            return f"SELECT {field_name} FROM {self.table.table_name};"  # Construct the SQL query

    def sql_query_for_size(self, var_name):
        if var_name:
            return f'SELECT COUNT(*) as {var_name} FROM {self.table.table_name}'

    def sql_query_select_fields_with_conditions(self, return_fields, query_conditions):
        target_table = self.table.table_name
        self.validate_query_fields(target_table, return_fields, query_conditions)
        if target_table and return_fields and query_conditions:
            where_fields     = list(query_conditions.keys())
            params           = list(query_conditions.values())
            fields_to_return = ', '.join(return_fields)                                               # Join the select_fields list into a comma-separated string
            where_clause     = ' AND '.join([f"{field}=?" for field in where_fields])                 # Dynamically construct the WHERE clause based on condition_fields
            sql_query        = f"SELECT {fields_to_return} FROM {target_table} WHERE {where_clause}"  # Construct the full SQL query
            return sql_query, params

    def sql_query_for_select_rows_where(self, **kwargs):
        valid_fields  = self.table.fields__cached()                                                               # Get a list of valid field names from the cached schema
        params        = []                                                                                  # Initialize an empty list to hold query parameters
        where_clauses = []                                                                                  # Initialize an empty list to hold parts of the WHERE clause
        for field_name, query_value in kwargs.items():                                                      # Iterate over each keyword argument and its value
            if field_name not in valid_fields:                                                              # Check if the provided field name is valid
                raise ValueError(f'in select_rows_where, the provided field is not valid: {field_name}')
            params.append(query_value)                                                                      # Append the query value to the parameters list
            where_clauses.append(f"{field_name} = ?")                                                       # Append the corresponding WHERE clause part, using a placeholder for the value
        where_clause = ' AND '.join(where_clauses)                                                          # Join the individual parts of the WHERE clause with 'AND'


        sql_query = f"SELECT * FROM {self.table.table_name} WHERE {where_clause}" # Construct the full SQL query
        return sql_query, params

    def validate_query_fields(self, target_table, return_fields, query_conditions):
        valid_fields = self.table.fields_names__cached(include_star_field=True)
        if target_table not in self.table.database.tables_names(include_sqlite_master=True):
            raise ValueError(f'in validate_query_fields, invalid target_table name: "{target_table}"')
        if type(return_fields) is not list:
            raise ValueError(f'in validate_query_fields, return_fields value must be a list, and it was "{type(return_fields)}"')
        for return_field in return_fields:
            if return_field not in valid_fields:
                raise ValueError(f'in validate_query_fields, invalid, invalid return_field: "{return_field}"')
        if type(query_conditions) is not dict:
            raise ValueError(f'in validate_query_fields, query_conditions value must be a dict, and it was "{type(query_conditions)}"')
        for where_field in query_conditions.keys():
            if where_field not in valid_fields:
                raise ValueError(f'in validate_query_fields, invalid, invalid return_field: "{where_field}"')