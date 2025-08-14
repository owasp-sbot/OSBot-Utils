from typing                                         import Optional, List, Dict, Union
from unittest                                       import TestCase
from osbot_utils.utils.Objects                      import __
from osbot_utils.type_safe.Type_Safe                import Type_Safe


class test__perf__Type_Safe__tracing(TestCase):
#
#     @trace_calls(include=['*'], show_internals=True, show_lines=True, show_types=True, show_class=True,
#                  show_duration=True, duration_padding=150)
#     def test__Python_class__ctor(self):
#         class An_Class():
#             pass
#
#         An_Class()
#
#     @trace_calls(include=['*'], show_internals=True, show_lines=True, show_types=True, show_class=True,
#                  show_duration=True, duration_padding=150)
#     def test__Type_Safe__ctor__no_attr(self):
#         class An_Class(Type_Safe):
#             pass
#
#         An_Class()
#
#     @trace_calls(include=['*'], show_internals=True, show_lines=True, show_types=True, show_class=True,
#                  show_duration=True, duration_padding=150)
#     def test__Type_Safe__ctor__one_attr(self):
#         class An_Class(Type_Safe):
#             an_str:str
#
#         An_Class()


    # @trace_calls(include              = ['osbot'      ],
    #              ignore               = ['typing' ],
    #              show_internals       = False       ,
    #              show_lines           = False       ,
    #              show_types           = False       ,
    #              show_class           = True        ,
    #              show_duration        = True        ,
    #              duration_padding     = 140         ,
    #              #duration_bigger_than = 0.001
    #              )
    def test_complex_types(self):

        class ComplexTypes(Type_Safe):                                          # Multiple complex types
            an_int       : int
            optional_str : Optional [str]
            str_list     : List     [str]
            int_dict     : Dict     [str, int]
            union_field  : Union    [str, int]

        assert ComplexTypes().obj() == __(an_int=0, optional_str=None, str_list=[], int_dict=__(), union_field=None)

        #type_safe_cache.print_cache_hits()













