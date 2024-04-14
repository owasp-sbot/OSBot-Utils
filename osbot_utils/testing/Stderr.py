import io
from contextlib import redirect_stderr


class Stderr:
    def __init__(self):
        self.output          = io.StringIO()
        self.redirect_stderr = redirect_stderr(self.output)

    def __enter__(self):
        self.redirect_stderr.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redirect_stderr.__exit__(exc_type, exc_val, exc_tb)

    def value(self):
        return self.output.getvalue()

