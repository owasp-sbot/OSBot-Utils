from osbot_utils.base_classes.Kwargs_To_Self     import Kwargs_To_Self
from osbot_utils.decorators.lists.filter_list import filter_list
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.Print_Table import Print_Table
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set

DEFAULT_FIELD_NAME__ID = 'id'

class Sqlite__Table(Kwargs_To_Self):
    database     : Sqlite__Database
    table_name   : str

    def create(self, fields=None):
        from osbot_utils.helpers.sqlite.Sqlite__Table__Create import Sqlite__Table__Create
        table_create       = Sqlite__Table__Create(self.table_name)         # todo: fix this workflow
        table_create.table = self                                           #       since it is weird to have to overwrite the table vale of Sqlite__Table__Create
        table_create.add_fields(fields)
        return table_create.create_table()

    def cursor(self):
        return self.database.cursor()

    def connection(self):
        return self.database.connection()

    def delete(self):
        if self.exists() is False:                                  # if table doesn't exist
            return False                                            # return False
        self.cursor().table_delete(self.table_name)                 # delete table
        return self.exists() is False                               # confirm table does not exist

    def exists(self):
        return self.cursor().table_exists(self.table_name)

    def field_data(self, field_name):                               # todo: fix SQL injection
        sql_query  = f"SELECT {field_name} FROM {self.table_name};"  # Construct the SQL query
        all_rows   = self.cursor().execute__fetch_all(sql_query)      # Execute the SQL query and get all rows
        all_values = [row[field_name] for row in all_rows]          # Extract the desired field from each row in the result set
        return all_values

    def fields(self):
        return self.schema(index_by='name')

    @cache_on_self
    def fields__cached(self):
        return self.fields()

    def fields_names__cached(self, execute_id=False):
        field_names = list_set(self.fields__cached())
        if execute_id:
            field_names.remove(DEFAULT_FIELD_NAME__ID)
        return field_names

    def not_exists(self):
        return self.exists() is False

    def print(self, **kwargs):
        return Print_Table(**kwargs).print(self.rows())

    def row_add(self, record):
        schema        = self.fields__cached()                                               # Retrieve the schema from the cached fields
        filtered_data = {key: value for key, value in record.items() if key in schema}      # Filter the data dictionary to include only keys that are valid column names according to the schema
        columns       = ', '.join(filtered_data.keys())                                     # Construct column names and placeholders
        placeholders  = ', '.join(['?' for _ in filtered_data.values()])
        sql = f'INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})'          # Construct the SQL statement
        self.cursor().execute(sql, list(filtered_data.values()))                            # Execute the SQL statement with the filtered data values
        return self

    def rows_add(self, records, commit=True):
        for record in records:
            self.row_add(record)
        if commit:
            self.cursor().commit()
        return self


    def rows(self, fields_names=None):
        sql_query = self.sql_query_for_fields(fields_names)
        return self.cursor().execute__fetch_all(sql_query)


    @index_by
    def schema(self):
        return self.cursor().table_schema(self.table_name)

    @filter_list
    def schema__by_name_type(self):
        return {item.get('name'): item.get('type') for item in self.schema()}

    def size(self):
        var_name = 'size'
        self.cursor().execute(f'SELECT COUNT(*) as {var_name} FROM {self.table_name}')
        result = self.cursor().fetchone()
        return result.get(var_name)

    def sql_query_for_fields(self, field_names: list = None):               # todo: refactor this into an SQL_Builder class
        valid_fields = self.fields_names__cached()
        if field_names is None:
            field_names = valid_fields
        elif isinstance(field_names, list) is False:
            raise ValueError(f"in sql_query_for_fields, field_names must be a list, it was :{field_names}")

        invalid_field_names = [name for name in field_names if name not in valid_fields]    # If no valid field names are provided, raise an error or return a default query
        if invalid_field_names:                                                             # If there are any invalid field names, raise an exception listing them
            message = f"Invalid field names provided: {', '.join(invalid_field_names)}"
            raise ValueError(message)

        fields_str = ', '.join(field_names)                         # Construct the SQL query string
        sql_query = f"SELECT {fields_str} FROM {self.table_name};"  # Join the valid field names with commas
        return sql_query


