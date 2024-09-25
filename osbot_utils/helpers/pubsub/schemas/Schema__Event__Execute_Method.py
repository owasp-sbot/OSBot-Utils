import types
from osbot_utils.helpers.pubsub.schemas.Schema__Event import Schema__Event

class Schema__Event__Execute_Method(Schema__Event):
    event_type       : str                 = 'execute-method'
    execution_result : object              = None
    method_target    : types.MethodType
    method_args      : list
    method_kwargs    : dict


    def execute(self):
        self.execution_result = self.method_target(*self.method_args, **self.method_kwargs)
        return self.execution_result