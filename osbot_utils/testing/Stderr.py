import io
from contextlib import redirect_stderr


class Stderr:               # todo: refactor with Stdout whose code is 90% the same as this one. Add class to capture both at the same time
    def __init__(self):
        self.output          = io.StringIO()
        self.redirect_stderr = redirect_stderr(self.output)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args, **kwargs):
        self.stop(*args, **kwargs)

    def start(self):
        self.redirect_stderr.__enter__()

    def stop(self, exc_type=None, exc_inst=None, exc_tb=None):
        self.redirect_stderr.__exit__(exc_type, exc_inst, exc_tb)

    def value(self):
        return self.output.getvalue()

