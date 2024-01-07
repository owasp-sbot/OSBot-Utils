from unittest import TestCase

from osbot_utils.utils.Misc import random_string, random_int

from osbot_utils.utils.trace.Trace_Call__Stack_Node import Trace_Call__Stack_Node


class test_Trace_Call__Stack_Node(TestCase):

    def setUp(self):
        self.stack_node = Trace_Call__Stack_Node()

    def test___locals__(self):
        expected_values = { 'call_duration'         : 0   ,
                            'call_end'              : 0   ,
                            'call_index'            : 0   ,
                            'call_start'            : 0   ,
                            'children'              : []  ,
                            'frame'                 : None,
                            'func_name'             : ''  ,
                            'locals'                : {}  ,
                            'name'                  : ''  ,
                            'module'                : ''  ,
                            'source_code'           : ''  ,
                            'source_code_caller'    : ''  ,
                            'source_code_location'  : ''  }
        assert self.stack_node.__cls_kwargs__    () == expected_values
        assert self.stack_node.__default_kwargs__() == expected_values
        assert self.stack_node.__kwargs__        () == expected_values
        assert self.stack_node.__locals__        () == expected_values

    def test_data(self):
        name        = random_string()
        call_index  = random_int()
        assert type(name     ) is str
        assert type(call_index) is int

        stack_node  = Trace_Call__Stack_Node(call_index=call_index, name=name)

        assert stack_node.__locals__() == { 'call_duration'       : 0          ,
                                            'call_end'            : 0          ,
                                            'call_index'          : call_index ,
                                            'call_start'          : 0          ,
                                            "name"                : name       ,
                                            'locals'              : {}         ,
                                            'frame'               : None       ,
                                            "children"            : []         ,
                                            'func_name'           : ''         ,
                                            'module'              : ''         ,
                                            'source_code'         : ''         ,
                                            'source_code_caller'  : ''         ,
                                            'source_code_location': ''         }

        assert stack_node.__locals__() == stack_node.data()