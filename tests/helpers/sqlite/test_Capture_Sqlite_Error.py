import sqlite3
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from osbot_utils.helpers.sqlite.Capture_Sqlite_Error import capture_sqlite_error
from osbot_utils.utils.Dev import pprint

class test_Capture_Sqlite_Error(TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_decorator(self, sys_stdout):
        expected_output = ('\n'
                           '\n'
                           "'****** SQLITE ERROR DETECTED ******'\n"
                           '\n'
                           '{\'error_code\': \'OperationalError\', \'error_message\': \'near "aaaa": '
                           "syntax error'}\n")
        @capture_sqlite_error
        def trigger_error():
            with sqlite3.connect(':memory:') as conn:
                cursor = conn.cursor()
                result = cursor.execute('aaaa')
                pprint(result)

        trigger_error()

        assert sys_stdout.getvalue() == expected_output