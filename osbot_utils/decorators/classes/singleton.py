
def singleton(cls):
    assert type(cls) == type             # make sure the singleton decorator was added to class/type (vs a function)
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance