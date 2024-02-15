import io
from contextlib import redirect_stdout


class Stdout:
    def __init__(self):
        self.output          = io.StringIO()
        self.redirect_stdout = redirect_stdout(self.output)

    def __enter__(self):
        self.redirect_stdout.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.redirect_stdout.__exit__(exc_type, exc_val, exc_tb)

    def value(self):
        return self.output.getvalue()

