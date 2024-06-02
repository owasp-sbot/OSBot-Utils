from unittest import TestCase

from osbot_utils.helpers.cache_requests.flows.flow__Cache__Requests import flow__Cache_Requests


class test_flow__Cache__Requests(TestCase):

    def setUp(self):
        print()
        print()
        self.flow = flow__Cache_Requests()

    def test_invoke_function(self):
        def function(a,b):
            return a + b

        assert self.flow.invoke_function(function, 40, 2) == 42
