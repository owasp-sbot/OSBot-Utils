from unittest import TestCase
from osbot_utils.testing.Trace_Call import Trace_Call


def dummy_function():
    pass

def another_function():
    dummy_function()

class test_Trace_Call(TestCase):


    def test_trace_call(self):

        # Test the initialization and its attributes
        trace_call = Trace_Call()
        assert trace_call.prev_trace_function  is None      , "prev_trace_function should be None initially"
        assert trace_call.call_index           == 0         , "call_index should be 0 initially"
        assert trace_call.view_model           == []        , "view_model should be empty initially"
        assert trace_call.print_traces_on_exit is False     , "print_traces_on_exit should be False initially"
        assert trace_call.stack                == [{"name": trace_call.trace_title, "children": [], "call_index": 0}], "Initial stack state not correct"

        # Test the enter and exit methods
        with Trace_Call() as trace_call:
            trace_call.trace_capture_start_with   = ['test_Trace_Call']
            trace_call.print_traces_on_exit = True  # To hit the 'print_traces' line in __exit__
            dummy_function()
            another_function()

        assert len(trace_call.view_model) == 4, "Four function calls should be traced"
        assert trace_call.view_model[0]['method_name'] == trace_call.trace_title    , "First function in view_model should be 'traces'"
        assert trace_call.view_model[1]['method_name'] == 'dummy_function'          , "2nd function in view_model should be 'dummy_function'"
        assert trace_call.view_model[2]['method_name'] == 'another_function'        , "3rd function in view_model should be 'another_function'"
        assert trace_call.view_model[3]['method_name'] == 'dummy_function'          , "4th function in view_model should be 'dummy_function'"

        # Test the create_view_model function
        stack_data = [{"name": "some_function", "children": [{"name": "child_function", "children": []}]}]
        view_model = trace_call.create_view_model(stack_data)
        assert len(view_model) == 2, "Two functions should be in the created view_model"

        # Test fix_view_mode function
        trace_call.view_model = view_model
        trace_call.fix_view_mode()
        assert trace_call.view_model[-1]['prefix'] == '└───', "Last node prefix should be updated"

    # todo: refactor to remove dependency on Html_Parser
    # def test_trace_calls(self):
    #     with Trace_Call('trace 123') as trace_call:
    #         trace_call.trace_ignore_start_with = ['cbr_website_beta.flask', 'cbr_website_beta.apps.dev']
    #         html = Html_Parser('<div id=132> some div</div>')
    #         assert html.with_id('132') == ' some div'
    #
    #     assert len(trace_call.view_model) > 0
    #
    #     trace_call.print_traces()
