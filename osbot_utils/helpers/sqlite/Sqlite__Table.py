from osbot_utils.base_classes.Kwargs_To_Self     import Kwargs_To_Self
from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database

class Sqlite__Table(Kwargs_To_Self):
    database     : Sqlite__Database
    table_name   : str
    table_fields : list

    def add_record(self, record):
        schema        = self.fields__cached()                                               # Retrieve the schema from the cached fields
        filtered_data = {key: value for key, value in record.items() if key in schema}      # Filter the data dictionary to include only keys that are valid column names according to the schema
        columns       = ', '.join(filtered_data.keys())                                     # Construct column names and placeholders
        placeholders  = ', '.join(['?' for _ in filtered_data.values()])
        sql = f'INSERT INTO {self.table_name} ({columns}) VALUES ({placeholders})'          # Construct the SQL statement
        self.cursor().execute(sql, list(filtered_data.values()))                        #    Execute the SQL statement with the filtered data values
        return self

    def create(self):
        result = self.cursor().table_create(table_name=self.table_name, fields=self.table_fields)
        return result.get('status') == 'ok'

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

    def fields(self):
        return self.schema(index_by='name')

    @cache_on_self
    def fields__cached(self):
        return self.fields()

    def not_exists(self):
        return self.exists() is False

    def rows(self):
        sql_query = f"Select * from {self.table_name}"
        return self.cursor().execute__fetch_all(sql_query)

    @index_by
    def schema(self):
        return self.cursor().table_schema(self.table_name)

    def size(self):
        var_name = 'size'
        self.cursor().execute(f'SELECT COUNT(*) as {var_name} FROM {self.table_name}')
        result = self.cursor().fetchone()
        return result.get(var_name)
