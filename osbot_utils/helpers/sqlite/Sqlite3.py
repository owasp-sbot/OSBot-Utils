import sqlite3
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

class Sqlite3(Kwargs_To_Self):

    @cache_on_self
    def connect(self, db_name):
        return sqlite3.connect(db_name)

    @cache_on_self
    def cursor(self,db_name):
        return self.connect(db_name).cursor()

    def execute(self, db_name, sql_query):
        return self.cursor(db_name).execute(sql_query)

    # def create(self):
    #     conn = sqlite3.connect('example.db')
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

    def tables(self, db_name):
        sql_query = "SELECT * FROM sqlite_master WHERE type='table';"
        cursor    = self.execute(db_name, sql_query)                    # Query to select all table names from the sqlite_master table
        tables    = []
        for table in cursor.fetchall():                                   # Fetch all results
            (type, name, tbl_name, rootpage, sql) = table
            table_data = {"type": type, "name": name, "rootpage": rootpage, "table": tbl_name,"sql": sql}
            tables.append(table_data)
        return tables


        return tables
