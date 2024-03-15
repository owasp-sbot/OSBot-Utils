from contextlib import contextmanager


@contextmanager
def obj_as_context(variable):
    yield variable