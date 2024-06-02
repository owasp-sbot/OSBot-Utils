from unittest import TestCase

from osbot_utils.context_managers.disable_root_loggers import disable_root_loggers
from osbot_utils.helpers.cache_requests.flows.flow__Cache__Requests import flow__Cache_Requests


class test_flow__Cache__Requests(TestCase):

    def setUp(self):
        print()
        print()
        self.flow = flow__Cache_Requests()

    def test_invoke_function(self):
        def an_function(a,b):
            print('...in an_function')
            return a + b

        with disable_root_loggers():
            assert self.flow.invoke_function(an_function, 40, 2) == 42
