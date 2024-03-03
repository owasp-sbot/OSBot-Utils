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

    def execute(self, db_name, sql_query, params=None):
        return self.cursor(db_name).execute(sql_query, params)

    # def create(self):
    #     conn = sqlite3.connect('example.db')