class remove_return_value:          # removes the field from the return value of the function (if it exists)

    def __init__(self, field_name):
        self.field_name = field_name                                # field to remove

    def __call__(self, function):
        from functools import wraps

        @wraps(function)                                            # makes __name__ work ok
        def wrapper(*args,**kwargs):                                # wrapper function
            data = function(*args,**kwargs)                         # calls wrapped function with original params
            if data and hasattr(data,'get'):                        # if it is set and has .get method
                if data.get(self.field_name) is not None:           # check if field_name exists in data
                    del data[self.field_name]                       # if it does, delete it
            return data                                             # return data received
        return wrapper                                              # return wrapper function

#todo: check usages and remove legacy method
remove      = remove_return_value