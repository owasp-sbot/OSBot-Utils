from osbot_utils.base_classes.Kwargs_To_Self     import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite import Sqlite
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database


class Sqlite__Table(Kwargs_To_Self):
    database   : Sqlite__Database
    table_name : str

    def exists(self):
        return self.database.cursor().table_exists(self.table_name)




