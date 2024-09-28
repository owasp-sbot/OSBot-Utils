import traceback
from functools              import wraps
from osbot_utils.utils.Dev  import pprint

def capture_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return_value = None
        with Capture_Exception() as context:
            return_value = func(*args, **kwargs)
        if context.error_occurred:
            print("\n****** EXCEPTION DETECTED ******")
            pprint(context.error_details)
        return return_value
    return wrapper

class Capture_Exception:
    error_occurred : bool
    error_details  : dict

    def __enter__(self):
        self.error_occurred = False
        self.error_details = {}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.error_occurred = True
            last_frame = traceback.extract_tb(exc_tb)[-1]
            self.error_details = {
                'exception_type': str(exc_type.__name__),
                'message'       : str(exc_val),
                'last_frame'    :  { 'file': last_frame.filename,
                                    'line': last_frame.lineno  }
            }
            return True
        return False