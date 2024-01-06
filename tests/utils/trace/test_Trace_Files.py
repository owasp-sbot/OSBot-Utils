from unittest import TestCase

import pytest

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Lists import unique
from osbot_utils.utils.Misc import str_md5
from osbot_utils.utils.Objects import print_obj_data_as_dict, obj_data_aligned, print_obj_data_aligned, obj_info
from osbot_utils.utils.ast.Ast_Merge import Ast_Merge
from osbot_utils.utils.trace.Trace_Call import Trace_Call
from osbot_utils.utils.trace.Trace_Files import Trace_Files


class test_Trace_Files(TestCase):

    def setUp(self):
        self.kwargs = {}

    def test___default_kwargs__(self):
        expected_values = { 'capture_source_code'      : False ,
                            'capture_start_with'       : []    ,
                            'files'                    : []    ,
                            'ignore_start_with'        : []    ,
                            'print_locals'             : False ,
                            'print_max_string_length'  : 100   ,
                            'print_on_exit'            : False ,
                            'show_caller'              : False ,
                            'show_method_parent'       : False ,
                            'show_parent_info'         : True  ,
                            'show_source_code_path'    : False ,
                            'title'                    : ''    }
        assert Trace_Files.__default_kwargs__() == expected_values
        assert Trace_Files().__default_kwargs__() == expected_values
        trace_files = Trace_Files()
        assert trace_files.__locals__() == {**expected_values,
                                            'prev_trace_function'       : None                                                          ,
                                            'stack'                     : [{'call_index': 0, 'children': [], 'name': 'Trace Session'}]  ,
                                            'trace_call_handler'        : trace_files.trace_call_handler                                ,
                                            'trace_call_print_traces'   : trace_files.trace_call_print_traces                           ,
                                            'trace_call_view_model'     : trace_files.trace_call_view_model                             }

    def test___init__(self):
        assert Trace_Files.__cls_kwargs__() == {'files': []}
        assert Trace_Files().files == []

        assert Trace_Files(files=[]       ).files == []
        assert Trace_Files(files=['a,b,c']).files == ['a,b,c']

    @pytest.mark.skip("needs fixing after the refactoring of the Trace_Call__Handler")
    def test_trace_call(self):

        def method_a():
            method_b()

        def method_b() :
            print('in method_b')

        kwargs = {"capture_start_with": ['t','o']}
        with Trace_Files(**kwargs) as trace_file:
            #trace_file.print_traces_on_exit = True                          # To hit the 'print_traces' line in __exit__
            pprint(str_md5('aaa'))
            method_a()
            method_b()

        assert len(unique(trace_file.files)) > 1

        # #pprint(unique(trace_file.files))
        #
        # ast_merge = Ast_Merge()
        # for file in unique(trace_file.files):
        #     print(file)
        #     ast_merge.merge_file(file)
        #
        # print(ast_merge.source_code())







