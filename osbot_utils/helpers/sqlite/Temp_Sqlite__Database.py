from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database, SQLITE_DATABASE_PATH__IN_MEMORY


class Temp_Sqlite__Database(Kwargs_To_Self):
    path    : str = SQLITE_DATABASE_PATH__IN_MEMORY             # default to in-memory database
    database: Sqlite__Database