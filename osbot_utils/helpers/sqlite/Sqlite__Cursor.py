from sqlite3 import Cursor

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache import cache
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database


class Sqlite__Cursor(Kwargs_To_Self):
    database : Sqlite__Database

    def db_name(self):
        return self.database.db_name

    def cursor(self):
        return self.database.sqlite.cursor(self.db_name())

    def execute(self, sql_query, *params):
        return self.cursor().execute(sql_query, *params)

    def execute__fetch_all(self,sql_query):
        return self.execute(sql_query=sql_query).fetchall()

    def table_create(self, table_name, fields):
        sql_query = f"CREATE TABLE {table_name} ({', '.join(fields)})"
        return self.execute(sql_query=sql_query)

    def table_delete(self, table_name):
        sql_query = f"DROP TABLE IF EXISTS {table_name};"
        return  self.execute(sql_query=sql_query)

    def table_exists(self, table_name):
        self.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
        return self.cursor().fetchone() is not None

    def table_schema(self, table_name):
        sql_query = f"PRAGMA table_info({table_name});"
        cursor    = self.execute(sql_query)
        columns   = cursor.fetchall()
        return columns

    def table__sqlite_master(self):                            # todo: refactor into separate class
        sql_query = "SELECT * FROM sqlite_master"
        cursor     = self.execute(sql_query)
        return cursor.fetchall()

    def tables(self):
        sql_query = "SELECT * FROM sqlite_master WHERE type='table';"                   # Query to select all table names from the sqlite_master table
        self.execute(sql_query)
        return self.cursor().fetchall()