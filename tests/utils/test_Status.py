from unittest import TestCase

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import obj_data
from osbot_utils.utils.Status import osbot_logger, status_error


class test_Status(TestCase):

    def setUp(self):
        pass

    def test__osbot_logger(self):
        pprint(obj_data(osbot_logger))


    def test_status_error(self):
        kwargs = dict(message = 'an error message'   ,
                      data    = {'an': 'error'}      ,
                      error   = Exception('an error'))
        result = kwargs.copy()
        result['status'] = 'error'
        assert status_error(**kwargs) == result

