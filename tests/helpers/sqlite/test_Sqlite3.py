from sqlite3 import Connection
from unittest import TestCase


from osbot_utils.helpers.sqlite.Capture_Sqlite_Error import capture_sqlite_error, Capture_Sqlite_Error
from osbot_utils.helpers.sqlite.Sqlite3 import Sqlite3
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import list_set
from osbot_utils.utils.Objects import obj_data


class test_Sqlite3(TestCase):

    def setUp(self):
        self.db_name = ':memory:'               # create an in-memory database    #'test_Sqlite3.db'
        self.sqlite3 = Sqlite3()

    def test_connect(self):
        connection = self.sqlite3.connect(self.db_name)
        assert type(connection) is Connection
        assert list_set(obj_data(connection)) == [ 'DataError', 'DatabaseError', 'Error', 'IntegrityError', 'InterfaceError', 'InternalError',
                                                   'NotSupportedError', 'OperationalError', 'ProgrammingError', 'Warning',
                                                   'autocommit', 'backup', 'blobopen', 'close', 'commit', 'create_aggregate', 'create_collation',
                                                   'create_function', 'create_window_function', 'cursor', 'deserialize', 'execute', 'executemany',
                                                   'executescript', 'getconfig', 'getlimit', 'in_transaction', 'interrupt', 'isolation_level',
                                                   'iterdump', 'rollback', 'row_factory', 'serialize', 'set_authorizer', 'set_progress_handler',
                                                   'set_trace_callback', 'setconfig', 'setlimit', 'text_factory', 'total_changes']
        assert connection.autocommit     == -1
        assert connection.in_transaction is False
        assert connection.row_factory    is None
        assert connection.total_changes   == 0

        assert connection == self.sqlite3.connect(self.db_name)         # confirm @cache is working since we get the same object every time
        assert connection == self.sqlite3.connect(self.db_name)

    #@capture_sqlite_error
    def test_execute(self):
        with Capture_Sqlite_Error() as error:
            self.sqlite3.execute(self.db_name, '')
        assert error.error_details == {'error_code': 'ProgrammingError',
                                       'error_message': 'parameters are of unsupported type'}

#         """CREATE TABLE users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT UNIQUE NOT NULL
# );"""