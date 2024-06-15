import sys
from unittest import TestCase

import pytest

from osbot_utils.testing.Patch_Print import Patch_Print


class test_Patch_Print(TestCase):

    @classmethod
    def setUpClass(cls):
        if sys.version_info < (3, 8):
            pytest.skip("Skipping tests that don't work on 3.7 or lower")

    def setUp(self):
        self.patch_print = Patch_Print()

    def test__init__(self):
        assert self.patch_print.__locals__() == {'enabled'       : True                          ,
                                                 'expected_calls': []                            ,
                                                 'mocked_print'  : self.patch_print.mocked_print ,
                                                 'patched_print' : None                          ,
                                                 'print_calls'   : False                         }


    def test__enter__exit__(self):
        with self.patch_print as _:
            print('in test__enter__exit__',12,1)
            print("aaaa", end='__end__')

        assert _.calls() == [(('in test__enter__exit__', 12, 1), {}), (('aaaa',), {'end': '__end__'})]

    def test_calls(self):
        with self.patch_print as _:
            print('simple print')
            print('with only text')

        assert _.calls() == ['simple print', 'with only text']




