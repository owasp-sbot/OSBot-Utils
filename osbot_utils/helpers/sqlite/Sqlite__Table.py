from osbot_utils.base_classes.Kwargs_To_Self     import Kwargs_To_Self
from osbot_utils.decorators.methods.capture_status import apply_capture_status
from osbot_utils.helpers.sqlite.Sqlite import Sqlite
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database

class Sqlite__Table(Kwargs_To_Self):
    database     : Sqlite__Database
    table_name   : str
    table_fields : list

    def create(self):
        if self.table_name and self.table_fields:
            self.cursor().table_create(table_name=self.table_name, fields=self.table_fields)
            return self.exists()
        return False

    def cursor(self):
        return self.database.cursor()

    def delete(self):
        return self.cursor().table_delete(self.table_name)

    def exists(self):
        return self.cursor().table_exists(self.table_name)




