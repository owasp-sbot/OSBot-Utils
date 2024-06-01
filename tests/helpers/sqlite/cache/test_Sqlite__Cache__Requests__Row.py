from unittest import TestCase

from osbot_utils.helpers.sqlite.cache.Sqlite__Cache__Requests__Row import Sqlite__Cache__Requests__Row


class test_Sqlite__Cache__Requests__Row(TestCase):

    def setUp(self):
        self.cache_request_row = Sqlite__Cache__Requests__Row()