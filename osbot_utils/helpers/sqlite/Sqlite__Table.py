from osbot_utils.base_classes.Kwargs_To_Self     import Kwargs_To_Self
from osbot_utils.decorators.methods.capture_status import apply_capture_status
from osbot_utils.helpers.sqlite.Sqlite import Sqlite
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database

class Sqlite__Table(Kwargs_To_Self):
    database     : Sqlite__Database
    table_name   : str
    table_fields : list

    def create(self):
        result = self.cursor().table_create(table_name=self.table_name, fields=self.table_fields)
        return result.get('status') == 'ok'

    def cursor(self):
        return self.database.cursor()

    def delete(self):
        if self.exists() is False:                                  # if table doesn't exist
            return False                                            # return False
        self.cursor().table_delete(self.table_name)                 # delete table
        return self.exists() is False                               # confirm table does not exist

    def exists(self):
        return self.cursor().table_exists(self.table_name)

    def schema(self):
        return self.cursor().table_schema(self.table_name)


