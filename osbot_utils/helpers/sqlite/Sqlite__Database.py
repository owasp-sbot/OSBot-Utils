import sqlite3

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache import cache
from osbot_utils.decorators.methods.cache_on_self import cache_on_self

from osbot_utils.utils.Files import current_temp_folder, path_combine, folder_create, file_exists, file_delete
from osbot_utils.utils.Misc import  random_filename

SQLITE_DATABASE_PATH__IN_MEMORY = ':memory:'
FOLDER_NAME_TEMP_DATABASES      = '_temp_sqlite_databases'
TEMP_DATABASE__FILE_NAME_PREFIX = 'random_sqlite_db__'
TEMP_DATABASE__FILE_EXTENSION   = '.sqlite'

class Sqlite__Database(Kwargs_To_Self):
    db_path   : str  = None
    closed    : bool = False
    connected : bool = False
    deleted   : bool = False
    in_memory : bool = True                     # default to an in-memory database

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.db_path:                        # if self.db_path is set via the ctor (then it means that this is not in memory)
            self.in_memory = False              # todo: see if this is not better done with a direct method for a getter/setter

    def close(self):
        if self.closed is False:
            self.connection().close()
            self.closed    = True
            self.connected = False
            return True
        return False

    @cache_on_self
    def connect(self):
        connection_string      = self.connection_string()
        connection             = sqlite3.connect(connection_string)
        connection.row_factory = self.dict_factory                      # this returns a dict as the row value of every query
        self.connected         = True
        return connection

    def connection(self):
        return self.connect()

    def connection_string(self):
        if self.in_memory:
            return SQLITE_DATABASE_PATH__IN_MEMORY
        if not self.db_path:
            self.db_path = self.path_temp_database()
        return self.db_path

    @cache_on_self
    def cursor(self):
        from osbot_utils.helpers.sqlite.Sqlite__Cursor import Sqlite__Cursor
        return Sqlite__Cursor(database=self)

    def delete(self):
        if self.in_memory:          # can't delete an in-memory database
            return False
        if self.deleted:
            return False
        self.close()
        if file_delete(self.db_path):
            self.deleted = True
            return True
        return False

    def dict_factory(self, cursor, row):                        # from https://docs.python.org/3/library/sqlite3.html#how-to-create-and-use-row-factories
        fields = [column[0] for column in cursor.description]
        return {key: value for key, value in zip(fields, row)}

    def exists(self):
        if self.in_memory:
            return True
        return file_exists(self.db_path)

    def path_temp_database(self, file_name=None):
        if file_name is None:
            file_name = TEMP_DATABASE__FILE_NAME_PREFIX + random_filename(extension=TEMP_DATABASE__FILE_EXTENSION)
        return path_combine(self.path_temp_databases(), file_name)

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
        from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table              # need to import here due to circular imports
        return Sqlite__Table(database=self, table_name=table_name)

    def table__sqlite_master(self):
        return self.table('sqlite_master')

    def tables(self):
        from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table             # todo: add support for Type_Registry
        tables = []
        for table_data in self.tables_raw():
            table_name = table_data.get('name')
            table = Sqlite__Table(database=self, table_name=table_name)
            tables.append(table)
        return tables

    def tables_raw(self):
        return self.cursor().tables()

    def tables_names(self):
        return self.table__sqlite_master().field_data('name')




