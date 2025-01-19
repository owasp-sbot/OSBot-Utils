# from unittest                             import TestCase
# from osbot_utils.helpers.trace.Trace_Call import trace_calls
# from osbot_utils.type_safe.Type_Safe      import Type_Safe
#
# class test__perf__Type_Safe__tracing(TestCase):
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