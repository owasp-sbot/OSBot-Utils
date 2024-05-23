from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Globals import ROW_BASE_CLASS
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table


class SQL_Builder(Kwargs_To_Self):
    table      : Sqlite__Table
    limit      : int            = None                  # set it to None to make it explict that the limit is not set

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
        sql_query = f"SELECT {fields_str} FROM {self.table.table_name}{self.sql_limit()};"  # Join the valid field names with commas
        return sql_query

    def command__delete_table(self):
        return f'DELETE FROM {self.table.table_name}'

    def command__delete_where(self, query_conditions):
        self.validator().validate_query_fields(self.table, [],query_conditions)      # todo: add method to validate_query_fields to handle just the query section (so that we don't need to provide a empty list for the return values)
        target_table = self.table.table_name
        where_fields = list(query_conditions.keys())
        params       = list(query_conditions.values())
        where_clause = ' AND '.join([f"{field}=?" for field in where_fields])                   # todo: refactor into method that just handle the WHERE statements
        sql_query    = f"DELETE FROM {target_table} WHERE {where_clause}"                       # todo: refactor into a method that creates the final statement from a number of other objects (or strings)
        return sql_query, params

    def command_for_insert(self, record):
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

    def query_for_fields(self, field_names: list = None):
        return self.select_for_fields(field_names)

    def query_for_size(self):
        return f'SELECT COUNT(*) as size FROM {self.table.table_name}'

    def sql_limit(self):
        if self.limit is not None:
            return f" LIMIT {int(self.limit)}"
        return ""

    def query_select_fields_with_conditions(self, return_fields, query_conditions):
        self.validator().validate_query_fields(self.table , return_fields, query_conditions)
        target_table = self.table.table_name
        if target_table and return_fields and query_conditions:
            where_fields     = list(query_conditions.keys())
            params           = list(query_conditions.values())
            fields_to_return = ', '.join(return_fields)                                               # Join the select_fields list into a comma-separated string
            where_clause     = ' AND '.join([f"{field}=?" for field in where_fields])                 # Dynamically construct the WHERE clause based on condition_fields
            sql_query        = f"SELECT {fields_to_return} FROM {target_table} WHERE {where_clause}"  # Construct the full SQL query
            return sql_query, params

    def query_for_select_rows_where(self, **kwargs):
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

    def sql_query_update_with_conditions(self, update_fields, query_conditions):
        update_keys     = list(update_fields.keys())            # todo: refactor self.validate_query_fields to use a more generic value for these fields
        condition_keys  = list(query_conditions.keys())
        self.validator().validate_query_fields(self.table, update_keys, query_conditions)
        target_table = self.table.table_name
        if target_table and update_fields and query_conditions:
            update_clause   = ', '.join([f"{key}=?" for key in update_keys])
            where_clause    = ' AND '.join([f"{field}=?" for field in condition_keys])
            sql_query       = f"UPDATE {target_table} SET {update_clause} WHERE {where_clause}"

            # The parameters for the SQL execution must include both the update values and the condition values, in the correct order.
            params = list(update_fields.values()) + list(query_conditions.values())
            return sql_query, params

    def validate_row_obj(self, row_obj):
        field_types = self.table.fields_types__cached()
        invalid_reason = ""
        if self.table.row_schema:
            if row_obj:
                if issubclass(type(row_obj), ROW_BASE_CLASS):
                    for field_name, field_type in row_obj.__annotations__.items():
                        if field_name not in field_types:
                            invalid_reason = f'provided row_obj has a field that is not part of the current table: {field_name}'
                            break

                        if field_type != field_types[field_name]:
                            invalid_reason = f'provided row_obj has a field {field_name} that has a field type {field_type} that does not match the current tables type of that field: {field_types[field_name]}'
                            break
                    if invalid_reason  == '':
                        for field_name, field_value in row_obj.__locals__().items():
                            if field_name not in field_types:
                                invalid_reason = f'provided row_obj has a field that is not part of the current table: {field_name}'
                                break
                            if type(field_value) != field_types.get(field_name):
                                invalid_reason = f'provided row_obj has a field {field_name} that has a field value {field_value} value that has a type {type(field_value)} that does not match the current tables type of that field: {field_types.get(field_name)}'
                                break
                else:
                    invalid_reason = f'provided row_obj ({type(row_obj)}) is not a subclass of {ROW_BASE_CLASS}'
            else:
                invalid_reason = f'provided row_obj was None'
        else:
            invalid_reason = f'there is no row_schema defined for this table {self.table.table_name}'
        return invalid_reason

    def validator(self):
        return SQL_Query__Validator()

class SQL_Query__Validator:

    # todo: refactor this method to use a more generic value for these return_fields since it is already being used in two use cases: return fields and update fields
    def validate_query_fields(self, table, return_fields, query_conditions):
        target_table = table.table_name
        valid_fields = table.fields_names__cached(include_star_field=True)
        if target_table not in table.database.tables_names(include_sqlite_master=True):
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

        return self