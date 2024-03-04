from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache import cache
from osbot_utils.helpers.sqlite.Sqlite import Sqlite



class Sqlite__Database(Kwargs_To_Self):
    db_name : str = ':memory:'              # default to an in-memory database
    sqlite  : Sqlite

    @cache
    def cursor(self):
        from osbot_utils.helpers.sqlite.Sqlite__Cursor import Sqlite__Cursor
        return Sqlite__Cursor(database=self)

    def table(self, table_name):
        from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
        return Sqlite__Table(database=self, table_name=table_name)

    def tables(self):
        return self.cursor().tables()



