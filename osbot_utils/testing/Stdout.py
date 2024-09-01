import io
from contextlib import redirect_stdout


class Stdout:
    def __init__(self):
        self.output          = io.StringIO()
        self.redirect_stdout = redirect_stdout(self.output)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop(*args, **kwargs)

    def start(self):
        self.redirect_stdout.__enter__()

    def stop(self, exc_type=None, exc_inst=None, exc_tb=None):
        self.redirect_stdout.__exit__(exc_type, exc_inst, exc_tb)

    def value(self):
        return self.output.getvalue()

