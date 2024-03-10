import sqlite3

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache import cache
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from osbot_utils.utils.Files import current_temp_folder, path_combine, folder_create
from osbot_utils.utils.Misc import  random_filename

SQLITE_DATABASE_PATH__IN_MEMORY = ':memory:'
FOLDER_NAME_TEMP_DATABASES      = '_temp_sqlite_databases'
TEMP_DATABASE__FILE_NAME_PREFIX = 'random_sqlite_db__'
TEMP_DATABASE__FILE_EXTENSION   = '.sqlite'

class Sqlite__Database(Kwargs_To_Self):
    in_memory : bool = True                     # default to an in-memory database
    db_path   : str

    @cache_on_self
    def connect(self):
        connection_string = self.connection_string()
        connection        = sqlite3.connect(connection_string)
        connection.row_factory = self.dict_factory                      # this returns a dict as the row value of every query
        return connection

    def connection(self):
        return self.connect()

    def connection_string(self):
        if self.in_memory:
            return SQLITE_DATABASE_PATH__IN_MEMORY
        if self.db_path:
            return self.db_path
        return self.path_temp_database()

    @cache
    def cursor(self):
        from osbot_utils.helpers.sqlite.Sqlite__Cursor import Sqlite__Cursor
        return Sqlite__Cursor(database=self)

    def dict_factory(self, cursor, row):                        # from https://docs.python.org/3/library/sqlite3.html#how-to-create-and-use-row-factories
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    def path_temp_database(self):
        random_file_name = TEMP_DATABASE__FILE_NAME_PREFIX + random_filename(extension=TEMP_DATABASE__FILE_EXTENSION)
        return random_file_name

    def path_temp_databases(self):
        path_temp_databases  = path_combine(current_temp_folder(), FOLDER_NAME_TEMP_DATABASES)      # use current temp folder has the parent folder
        folder_create(path_temp_databases)                                                          # make sure it exists
        return path_temp_databases

    def save_to(self, path):
        connection = self.connection()
        file_conn  = sqlite3.connect(path)
        connection.backup(file_conn)
        file_conn.close()
        return path


    def table(self, table_name):
        from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
        return Sqlite__Table(database=self, table_name=table_name)

    def tables(self):
        return self.cursor().tables()




