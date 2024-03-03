import sqlite3
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

class Sqlite3(Kwargs_To_Self):

    @cache_on_self
    def connect(self, db_name):
        connection             = sqlite3.connect(db_name)
        connection.row_factory = self.dict_factory              # this returns a dict as the row value of every query
        return connection

    @cache_on_self
    def cursor(self,db_name):
        return self.connect(db_name).cursor()

    def dict_factory(self, cursor, row):                        # from https://docs.python.org/3/library/sqlite3.html#how-to-create-and-use-row-factories
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    def execute(self, db_name, sql_query):
        return self.cursor(db_name).execute(sql_query)

    def execute__fetch_all(self, db_name, sql_query):
        return self.execute(db_name,sql_query).fetchall()

    def table_create(self, db_name, table_name, fields):
        sql_query = f"CREATE TABLE {table_name} ({', '.join(fields)})"
        return self.execute(db_name, sql_query)

    def table_delete(self, db_name, table_name):
        sql_query = f"DROP TABLE IF EXISTS {table_name};"
        cursor = self.execute(db_name, sql_query)
        return cursor

    def table__sqlite_master(self, db_name):
        sql_query = "SELECT * FROM sqlite_master"
        cursor     = self.execute(db_name, sql_query)
        return cursor.fetchall()

    def table__schema(self, db_name, table_name):
        sql_query = f"PRAGMA table_info({table_name});"
        cursor = self.execute(db_name, sql_query)
        columns = cursor.fetchall()
        return columns
        schema = []
        for col in columns:
            col_info = { "cid"          : col[0] ,
                         "name"         : col[1] ,
                         "type"         : col[2] ,
                         "notnull"      : col[3] ,
                         "default_value": col[4] ,
                         "pk"           : col[5] }
            schema.append(col_info)
        return schema

    def tables(self, db_name):
        sql_query = "SELECT * FROM sqlite_master WHERE type='table';"
        cursor    = self.execute(db_name, sql_query)                    # Query to select all table names from the sqlite_master table
        return cursor.fetchall()