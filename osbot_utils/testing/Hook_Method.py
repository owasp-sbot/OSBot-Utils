from osbot_utils.helpers.Print_Table import Print_Table
from osbot_utils.utils.Call_Stack import Call_Stack

from osbot_utils.testing.Duration import Duration

class Hook_Method:

    def __init__(self, target_module, target_method, raise_exception=True):
        self.target_module   = target_module
        self.target_method   = target_method
        self.raise_exception = raise_exception                              # todo: figure out the impact of raising this by default
        self.target          = getattr(target_module, target_method)
        self.wrapper_method  = None
        self.calls           = []
        self.on_before_call  = []
        self.on_after_call   = []
        self.mock_call       = None


    def __enter__(self):
        self.wrap()
        return self

    def __exit__(self, type, value, traceback):
        self.unwrap()

    def add_on_after_call(self, on_after_call):
        """
        method to be after before the Hooked call

        method signature: def on_after_call(return_value,  *args, **kwargs):
        should return: return_value
        """
        self.on_after_call.append(on_after_call)
        return self

    def add_on_before_call(self, on_before_call):
        """
        method to be called before the Hooked call

        method signature: def on_after_call(*args, **kwargs):
        should return: (args, kwargs)
        """
        self.on_before_call.append(on_before_call)
        return self

    def calls_count(self):
        return len(self.calls)

    def calls_last_one(self):
        if len(self.calls) > 0:
            return self.calls[-1]

    def after_call(self, return_value, *args, **kwargs):
        """
        call all methods added via `add_on_after_call` with the params: return_value, *args, **kwargs
        return value from each on_after_call will on override existing return_value
        """
        for method in self.on_after_call:
            return_value = method(return_value, *args, **kwargs)
        return return_value

    def before_call(self, *args, **kwargs):
        """
        call all methods added via `add_on_before_call` with the params: *args, **kwargs
        return value is expected to be args and kwargs on each on_after_call which will on override existing args and kwargs values
        """
        for method in self.on_before_call:
            (args, kwargs) = method(*args, **kwargs)
        return (args, kwargs)

    def print(self):
        print()
        print()
        with Print_Table() as _:
            _.print(self.calls)

    def set_mock_call(self, mock_call):
        """
        Use this to simulate a call to the Hooked Method (the
        """
        self.mock_call = mock_call

    def wrap(self):

        def wrapper_method(*args, **kwargs):
            call_stack= Call_Stack().capture()
            with Duration(print_result=False) as duration:
                exception = None
                if self.mock_call:
                    return_value = self.mock_call(*args,**kwargs)
                else:
                    (args, kwargs) = self.before_call(*args, **kwargs)
                    try:
                        return_value   = self.target(*args, **kwargs)
                        return_value   = self.after_call(return_value, args, kwargs)
                    except Exception as error:
                        return_value = None
                        exception = error
                        #raise error

            call = {
                        'args'        : args                ,
                        'call_stack'  : call_stack          ,
                        'exception'   : exception           ,
                        'kwargs'      : kwargs              ,
                        'return_value': return_value        ,
                        'index'       : len(self.calls)     ,
                        'duration'    : int(duration.seconds()*1000)
                    }
            self.calls.append(call)
            if self.raise_exception and exception:
                raise exception
            return call['return_value']

        self.wrapper_method = wrapper_method
        setattr(self.target_module, self.target_method, self.wrapper_method)
        return self.wrapper_method

    def unwrap(self):
        setattr(self.target_module, self.target_method, self.target)

