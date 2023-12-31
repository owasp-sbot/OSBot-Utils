from contextlib import contextmanager

@contextmanager
def context(target, exec_before=None, exec_after=None):
    if exec_before:
        exec_before()
    try:
        yield target
    finally:
        if exec_after:
            exec_after()
