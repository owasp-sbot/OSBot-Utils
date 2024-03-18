from osbot_utils.base_classes.Kwargs_To_Self     import Kwargs_To_Self
from osbot_utils.decorators.lists.filter_list import filter_list
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.Print_Table import Print_Table
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.models.Sqlite__Field__Type import Sqlite__Field__Type
from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Objects import base_types, default_value
from osbot_utils.utils.Status import status_error
from osbot_utils.utils.Str import str_cap_snake_case

DEFAULT_FIELD_NAME__ID             = 'id'
ROW_BASE_CLASS                     = Kwargs_To_Self
SQL_TABLE__MODULE_NAME__ROW_SCHEMA = 'Dynamic_Class__Sqlite__Table'

class Sqlite__Table(Kwargs_To_Self):
    database  : Sqlite__Database
    table_name: str
    row_schema: type

    def _table_create(self):                        # todo: Sqlite__Table__Create needs to be refactored (since that was created before we had support for table_class )
        from osbot_utils.helpers.sqlite.Sqlite__Table__Create import Sqlite__Table__Create
        table_create = Sqlite__Table__Create(self.table_name)                               # todo: fix this workflow
        table_create.table = self
        return table_create                                                                            #       since it is weird to have to overwrite the table vale of Sqlite__Table__Create

    def add_row(self, **row_data):
        new_row  = self.new_row_obj(row_data)
        return self.row_add(new_row)

    def clear(self):
        sql_query = f'DELETE FROM {self.table_name}'
        return self.cursor().execute_and_commit(sql_query)

    def create(self):
        table_create = self._table_create()
        return table_create.create_table__from_row_schema(self.row_schema)

    def commit(self):
        return self.cursor().commit()

    def connection(self):
        return self.database.connection()

    def cursor(self):
        return self.database.cursor()

    def delete(self):
        if self.exists() is False:                                  # if table doesn't exist
            return False                                            # return False
        self.cursor().table_delete(self.table_name)                 # delete table
        return self.exists() is False                               # confirm table does not exist

    def exists(self):
        return self.cursor().table_exists(self.table_name)

    def fields(self):
        return self.schema(index_by='name')

    @cache_on_self
    def fields__cached(self):
        return self.fields()

    def fields_types__cached(self, exclude_id=False):
        fields_types = {}
        for field_name, field_data in self.fields__cached().items():
            if exclude_id and field_name == DEFAULT_FIELD_NAME__ID:
                continue
            sqlite_field_type = field_data['type']
            field_type = Sqlite__Field__Type.enum_map().get(sqlite_field_type)
            fields_types[field_name] = field_type
        return fields_types

    def fields_names__cached(self, exclude_id=False):
        field_names = list_set(self.fields__cached())
        if exclude_id:
            field_names.remove(DEFAULT_FIELD_NAME__ID)
        return field_names

    def index_create(self, index_field):
        if index_field not in self.fields_names__cached():
            raise ValueError(f"in index_create, invalid target_field: {index_field}")

        index_name = self.index_name(index_field)
        sql_query = f'CREATE INDEX IF NOT EXISTS {index_name} ON {self.table_name}({index_field});'
        return self.cursor().execute_and_commit(sql_query)

    def index_delete(self, index_name):
        sql_query = f'DROP INDEX IF EXISTS {index_name};'
        return self.cursor().execute_and_commit(sql_query)

    def index_exists(self, index_field):
        index_name = self.index_name(index_field)
        return index_name in self.indexes()

    def index_name(self, index_field):
        return f'idx__{self.table_name}__{index_field}'

    def list_from_fetch(self, rows, field_name):
        return [row[field_name] for row in rows]

    def indexes(self):
        field_name  = 'name'
        table_name  = 'sqlite_master'
        table_type  = 'index'
        field_query = 'tbl_name'
        sql_query   = f"SELECT {field_name} FROM {table_name} WHERE type='{table_type}' AND {field_query}=?"
        rows        = self.cursor().execute__fetch_all(sql_query, (self.table_name,))
        return self.list_from_fetch(rows, field_name)

    def new_row_obj(self, row_data=None):
        if self.row_schema:
            new_obj = self.row_schema()
            if row_data and ROW_BASE_CLASS in base_types(new_obj):
                new_obj.update_from_kwargs(**row_data)
            return new_obj

    def not_exists(self):
        return self.exists() is False

    def print(self, **kwargs):
        return Print_Table(**kwargs).print(self.rows())

    def row_add(self, row_obj=None):
        invalid_reason = self.validate_row_obj(row_obj)
        if invalid_reason:
            raise Exception(f"in row_add the provided row_obj is not valid: {invalid_reason}")
        # if type(row_data) is self.table_class:
        #     new_row = row_data
        # else:
        #     new_row = self.new_row_obj(row_data)

        return self.row_add_record(row_obj.__dict__)
        # if self.table_class:                                         # todo: see if we need the type checks below
        #     if type(row_obj) is self.table_class:
        #         if Kwargs_To_Self in base_types(row_obj):
        #             return self.row_add_record(row_obj.json())
        # return status_error('in row_add, row_obj had the wrong format', data=row_obj)

    def row_add_record(self, record):
        schema        = self.fields__cached()                                               # Retrieve the schema from the cached fields
        filtered_data = {key: value for key, value in record.items() if key in schema}      # Filter the data dictionary to include only keys that are valid column names according to the schema
        columns       = ', '.join(filtered_data.keys())                                     # Construct column names and placeholders
        placeholders  = ', '.join(['?' for _ in filtered_data.values()])
        sql = f'INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})'          # Construct the SQL statement
        return self.cursor().execute(sql, list(filtered_data.values()))                            # Execute the SQL statement with the filtered data values

    def rows_add(self, records, commit=True):           # todo: refactor to use row_add
        for record in records:
            self.row_add_record(record)
        if commit:
            self.cursor().commit()
        return self

    def row_schema__create_from_current_field_types(self):
        exclude_field_id                 = True                                                                 # don't include the id field since in most cases the row_schema doesn't include it
        field_types                      = self.fields_types__cached(exclude_id=exclude_field_id)               # mapping with field name to field type (in python)
        caps_table_name                  = str_cap_snake_case(self.table_name)
        dynamic_class_name               = f'Row_Schema__{caps_table_name}'                                    # name that we will give to the dynamic class generated
        dynamic_class_dict               = { k: default_value(v) for k, v in field_types.items()}              # assign the field values its default value (for that type)
        dynamic_class_dict['__module__'] = SQL_TABLE__MODULE_NAME__ROW_SCHEMA                                            # set the module name
        Dynamic_Class                    = type(dynamic_class_name, (ROW_BASE_CLASS,), dynamic_class_dict)     # Create the dynamic class
        Dynamic_Class.__annotations__    = field_types                                                         # Set annotations of the new Dynamic_Class to be the mappings we have from field_types
        return Dynamic_Class                                                                                   # return the Dynamic class (whose fields should match the field_types)

    def row_schema__set_from_field_types(self):
        self.row_schema = self.row_schema__create_from_current_field_types()
        return self


    def rows(self, fields_names=None):
        sql_query = self.sql_query_for_fields(fields_names)
        return self.cursor().execute__fetch_all(sql_query)

    def select_rows_where(self, **kwargs):
        valid_fields  = self.fields__cached()                               # Get a list of valid field names from the cached schema
        params        = []                                                  # Initialize an empty list to hold query parameters
        where_clauses = []                                                  # Initialize an empty list to hold parts of the WHERE clause
        for field_name, query_value in kwargs.items():                      # Iterate over each keyword argument and its value
            if field_name not in valid_fields:                              # Check if the provided field name is valid
                raise ValueError(f'in select_rows_where, the provided field is not valid: {field_name}')
            params.append(query_value)                                      # Append the query value to the parameters list
            where_clauses.append(f"{field_name} = ?")                       # Append the corresponding WHERE clause part, using a placeholder for the value
        where_clause = ' AND '.join(where_clauses)                          # Join the individual parts of the WHERE clause with 'AND'


        sql_query = f"SELECT * FROM {self.table_name} WHERE {where_clause}" # Construct the full SQL query

        # Execute the query and return the results
        return self.cursor().execute__fetch_all(sql_query, params)

    def select_field_values(self, field_name):
        if field_name not in self.fields__cached():
            raise ValueError(f'in select_all_vales_from_field, the provide field_name "{field_name}" does not exist in the current table "{self.table_name}"')
        sql_query  = f"SELECT {field_name} FROM {self.table_name};"     # Construct the SQL query
        all_rows   = self.cursor().execute__fetch_all(sql_query)        # Execute the SQL query and get all rows
        all_values = [row[field_name] for row in all_rows]              # Extract the desired field from each row in the result set
        return all_values

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

    def validate_row_obj(self, row_obj):
        field_types = self.fields_types__cached()
        invalid_reason = ""
        if self.row_schema:
            if row_obj:
                if issubclass(type(row_obj), ROW_BASE_CLASS):
                    for field_name, field_type in row_obj.__annotations__.items():
                        if field_name not in field_types:
                            invalid_reason = f'provided row_obj has a field that is not part of the current table: {field_name}'
                            break

                        if field_type != field_types[field_name]:
                            invalid_reason = f'provided row_obj has a field {field_name} that has a field type {field_type} that does not match the current tables type of that field: {field_types[field_name]}'
                            break
                    if invalid_reason  is '':
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
            invalid_reason = f'there is no row_schema defined for this table {self.table_name}'
        return invalid_reason

