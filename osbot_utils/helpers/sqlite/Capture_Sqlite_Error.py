import sqlite3
from functools import wraps
from osbot_utils.utils.Dev import pprint

def capture_sqlite_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return_value = None
        with Capture_Sqlite_Error() as error_capture:
            try:
                return_value = func(*args, **kwargs)
            except Exception as e:
                raise e
        if error_capture.error_details:
            print()
            pprint('****** SQLITE ERROR DETECTED ******')
            pprint(error_capture.error_details)
        return return_value

    return wrapper

class Capture_Sqlite_Error:
    def __init__(self):
        self.error_details = {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:  # Check if an exception occurred
            if isinstance(exc_val, sqlite3.ProgrammingError):  # Check for SQLite ProgrammingError
                self.process_programming_error(exc_val)
                return True  # Prevent the exception from propagating
            elif isinstance(exc_val, sqlite3.Error):  # Handle other generic sqlite3 errors
                self.process_generic_sqlite_error(exc_val)
                return True
        return False  # Allow exceptions not handled here to propagate

    def process_programming_error(self, exc_val):
        error_message = str(exc_val)
        self.error_details = {
            'error_code': 'ProgrammingError',
            'error_message': error_message
        }

    def process_generic_sqlite_error(self, exc_val):
        error_message = str(exc_val)
        self.error_details = {
            'error_code': type(exc_val).__name__,
            'error_message': error_message
        }