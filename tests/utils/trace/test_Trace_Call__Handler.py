from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Objects import base_classes

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.trace.Trace_Call__Handler import Trace_Call__Handler


class test_Trace_Call__Handler(TestCase):

    def setUp(self):
        self.handler = Trace_Call__Handler()

    def test___default_kwargs(self):
        assert Trace_Call__Handler.__default_kwargs__() == dict(call_index                  = 0     ,
                                                                stack                       = None  ,
                                                                title                       = None  ,
                                                                trace_capture_all           = False ,
                                                                trace_capture_source_code   = False ,
                                                                trace_capture_start_with    = None  ,
                                                                trace_ignore_internals      = True ,
                                                                trace_ignore_start_with     = None )


    def test___init__(self):
        assert Kwargs_To_Self in base_classes(Trace_Call__Handler)
        assert self.handler.__locals__() == { **self.handler.__default_kwargs__(),
                                                 'call_index'                   : 0,
                                                 'stack'                        : [{'call_index': 0, 'children': [], 'name': 'Trace Session'}],
                                                 'trace_capture_all'            : False,
                                                 'trace_capture_source_code'    : False,
                                                 'trace_capture_start_with'     : [],
                                                 'trace_ignore_internals'       : True,
                                                 'trace_ignore_start_with'      : [],
                                                 'trace_title'                  : 'Trace Session'}