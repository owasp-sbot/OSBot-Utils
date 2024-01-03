from pprint import pprint


class Catch:
    """
    Helper class for cases when the native Python exception traces is too noisy
    """
    def __init__(self, log_exception=False, log_headers=True, logger=None, expected_error=None):
        self.log_exception       = log_exception
        self.log_headers         = log_headers
        self.logger              = logger or print
        self.exception_type      = None
        self.exception_value     = None
        self.exception_traceback = None
        self.execution_complete  = False
        self.expected_error      = expected_error

    def __repr__(self):
        if self.execution_complete:
            return f'Catch: {self.exception_type} : {self.exception_value}'
        else:
            return f'Catch: (not executed yet)'

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.exception_type      = exception_type
        self.exception_value     = exception_value
        self.exception_traceback = exception_traceback
        self.execution_complete  = True
        if self.log_exception:
            if exception_type is not None:
                if self.log_headers:
                    self.log()
                    self.log("********* Catch ***********")
                    self.log(exception_type)
                    self.log()
                self.log(exception_value)
        if self.expected_error:
            self.assert_error_is(self.expected_error)
        return True     # returning true here will prevent the exception to be propagated (which is the objective of this class :) )

    def assert_error_is(self, expected_error):
        assert str(self) == expected_error

    def log(self, message=''):
        self.logger(message)