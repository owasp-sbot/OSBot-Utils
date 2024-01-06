from contextlib import contextmanager

@contextmanager
def context(target, *args, exec_before=None, exec_after=None, **kwargs):
    if exec_before:
        exec_before(*args, **kwargs)
    try:
        yield target
    finally:
        if exec_after:
            exec_after(*args, **kwargs)
