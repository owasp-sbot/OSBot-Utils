from functools import wraps

def filter_list(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        only_show = kwargs.pop('only_show', None)                                               # Directly extract and remove 'only_show' from kwargs if present
        values    = function(*args, **kwargs)                                                   # Call the decorated function
        if only_show:                                                                           # Filter the list of dictionaries to only include specified keys
            return [{key: item[key] for key in only_show if key in item} for item in values]
        return values

    return wrapper
