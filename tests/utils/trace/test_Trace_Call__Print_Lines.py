from unittest import TestCase

from osbot_utils.utils.Files import folder_exists, current_temp_folder

from osbot_utils.utils.trace.Trace_Call import Trace_Call
from osbot_utils.utils.trace.Trace_Call__Config import Trace_Call__Config

from osbot_utils.utils.trace.Trace_Call__Print_Lines import Trace_Call__Print_Lines


class test_Trace_Call__Print_Lines(TestCase):

    def setUp(self):
        self.config      = Trace_Call__Config()
        self.trace_call  = Trace_Call(config=self.config)

    def create_view_model(self):
        with self.config as _:
            _.trace_capture_lines = True
            _.trace_capture_all   = True

        with self.trace_call:
            def an_method():
                temp_folder = current_temp_folder()
                folder_exists(current_temp_folder())
            an_method()

        return self.trace_call.create_view_model()

    def test_print_lines(self):
        view_model = self.create_view_model()
        print_lines = Trace_Call__Print_Lines(config=self.config, view_model=view_model)
        print()
        print_lines.print_lines()
        #self.trace_call.print()