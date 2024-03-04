import sqlite3
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

class Sqlite(Kwargs_To_Self):

    @cache_on_self
    def connect(self, db_name):         # todo: refactor this to Sqlite__Connection class
        connection             = sqlite3.connect(db_name)
        connection.row_factory = self.dict_factory              # this returns a dict as the row value of every query
        return connection

    @cache_on_self
    def cursor(self,db_name):
        return self.connect(db_name).cursor()

    def dict_factory(self, cursor, row):                        # from https://docs.python.org/3/library/sqlite3.html#how-to-create-and-use-row-factories
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}