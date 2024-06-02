import functools

from osbot_utils.helpers.flows.Flow import flow


class flow__Cache_Requests:

    @flow()
    def invoke_function(self, function, *args, **kwargs):
        print('in invoke function')
        return function(*args, **kwargs)