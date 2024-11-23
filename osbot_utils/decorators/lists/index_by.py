# todo: find way to also allow the used of function().index_by(key) to working
#     : maybe using Fluent_List


def index_by(function):                                 # returns the list provided indexed by the key provided in index_by
    from functools import wraps
    from osbot_utils.fluent.Fluent_Dict import Fluent_Dict

    def apply(key, values):
        if key:
            results = {}
            for item in values:
                if type(item) is dict:
                    results[item.get(key)] = item
            return Fluent_Dict(results)
        return values

    @wraps(function)
    def wrapper(*args,**kwargs):
        key = None
        if 'index_by' in kwargs:
            key = kwargs.get('index_by')
            del kwargs['index_by']
        values = function(*args,**kwargs)

        return apply(key,values)
    return wrapper