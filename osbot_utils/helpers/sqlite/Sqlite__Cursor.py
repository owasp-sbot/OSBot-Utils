from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache import cache
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.utils.Status import status_ok, status_error, status_exception


class Sqlite__Cursor(Kwargs_To_Self):
    database : Sqlite__Database

    @cache_on_self
    def cursor(self):
        return self.connection().cursor()

    def commit(self):
        self.connection().commit()
        return self

    def connection(self):
        return self.database.connection()

    def execute(self, sql_query, *params):
        try:
            self.cursor().execute(sql_query, *params)
            return status_ok()
        except Exception as error:
            return status_exception(error=f'{error}')

    def execute__fetch_all(self,sql_query):
        self.execute(sql_query=sql_query)
        return self.cursor().fetchall()

    def fetchone(self):
        return self.cursor().fetchone()

    def table_create(self, table_name, fields):
        if table_name and fields:
            sql_query = f"CREATE TABLE {table_name} ({', '.join(fields)})"
            return self.execute(sql_query=sql_query)
        return status_error(message='table_name, fields cannot be empty')

    def table_delete(self, table_name):
        sql_query = f"DROP TABLE IF EXISTS {table_name};"
        return  self.execute(sql_query=sql_query)

    def table_exists(self, table_name):
        self.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return self.cursor().fetchone() is not None

    def table_schema(self, table_name):
        sql_query = f"PRAGMA table_info({table_name});"
        self.execute(sql_query)
        columns   = self.cursor().fetchall()
        return columns

    def table__sqlite_master(self):                            # todo: refactor into separate class
        sql_query = "SELECT * FROM sqlite_master"
        self.execute(sql_query)
        return self.cursor().fetchall()

    def tables(self):
        sql_query = "SELECT * FROM sqlite_master WHERE type='table';"                   # Query to select all table names from the sqlite_master table
        self.execute(sql_query)
        return self.cursor().fetchall()