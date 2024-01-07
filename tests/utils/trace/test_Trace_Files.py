from unittest import TestCase

import pytest

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Lists import unique
from osbot_utils.utils.Misc import str_md5
from osbot_utils.utils.Objects import print_obj_data_as_dict, obj_data_aligned, print_obj_data_aligned, obj_info
from osbot_utils.utils.ast.Ast_Merge import Ast_Merge
from osbot_utils.utils.trace.Trace_Call import Trace_Call
from osbot_utils.utils.trace.Trace_Call__Handler import DEFAULT_ROOT_NODE_NODE_TITLE
from osbot_utils.utils.trace.Trace_Call__Stack_Node import Trace_Call__Stack_Node
from osbot_utils.utils.trace.Trace_Files import Trace_Files


class test_Trace_Files(TestCase):

    def setUp(self):
        self.kwargs = {}

    def test___default_kwargs__(self):
        trace_files = Trace_Files()
        assert trace_files.__kwargs__() == {'config': trace_files.config ,
                                                    'files' : []                 }

        assert trace_files.__locals__() == { **trace_files.__kwargs__()                                                                 ,
                                            'prev_trace_function'       : None                                                          ,
                                            'stack'                     : trace_files.stack                  ,
                                            'trace_call_handler'        : trace_files.trace_call_handler     ,
                                            'trace_call_print_traces'   : trace_files.trace_call_print_traces,
                                            'trace_call_view_model'     : trace_files.trace_call_view_model  }

        assert len(trace_files.stack)   ==1
        assert trace_files.stack[0]     == Trace_Call__Stack_Node(name=DEFAULT_ROOT_NODE_NODE_TITLE)

    def test___init__(self):
        assert Trace_Files.__cls_kwargs__() == {'files': []}
        assert Trace_Files().files == []

        assert Trace_Files(files=[]       ).files == []
        assert Trace_Files(files=['a,b,c']).files == ['a,b,c']





