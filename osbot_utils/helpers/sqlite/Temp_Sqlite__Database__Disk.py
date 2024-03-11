from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database, SQLITE_DATABASE_PATH__IN_MEMORY


class Temp_Sqlite__Database__Disk(Kwargs_To_Self):
    database : Sqlite__Database

    def __init__(self):
        super().__init__()
        self.database.in_memory = False

    def __enter__(self):
        self.database.connect()
        return self.database

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.database.delete()
