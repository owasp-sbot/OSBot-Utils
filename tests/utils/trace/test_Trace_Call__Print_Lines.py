from unittest import TestCase
from unittest.mock import patch, call

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
            #_.trace_capture_all   = True
            _.trace_capture_start_with = ['test', 'osbot']

        with self.trace_call:
            def an_method():
                temp_folder = current_temp_folder()
                folder_exists(current_temp_folder())
            an_method()

        return self.trace_call.create_view_model()

    def test_print_lines(self):
        view_model = self.create_view_model()
        print_lines = Trace_Call__Print_Lines(config=self.config, view_model=view_model)
        # print()
        # print_lines.print_lines()
        # return

        with patch('builtins.print') as builtins_print:
            print_lines.print_lines()
            assert builtins_print.call_args_list == [call('┌─────┬──────────────────────────────────────────────────────────────┬───────────────────────────────────────────────┬──────┬──────┬───────┐   '),
                                                     call('│ #   │ Source code                                                  │ Method Class and Name                         │ Self object │ Line │ Depth │   '),
                                                     call('├─────┼──────────────────────────────────────────────────────────────┼───────────────────────────────────────────────┼──────┼──────┼───────┤   '),
                                                     call('│ \x1b[90m1\x1b[0m   │ \x1b[1m\x1b[92m  def an_method():\x1b[0m                                           │ test_Trace_Call__Print_Lines.an_method        │      │   25 │     1 │'),
                                                     call('│ \x1b[90m2\x1b[0m   │ \x1b[1m\x1b[38;2;120;120;120m      temp_folder = current_temp_folder()\x1b[0m                    │ test_Trace_Call__Print_Lines.an_method        │      │   26 │     1 │'),
                                                     call('│ \x1b[90m3\x1b[0m   │   \x1b[1m\x1b[92m        def temp_folder_current():\x1b[0m                         │ osbot_utils.utils.Files.temp_folder_current   │      │  387 │     2 │'),
                                                     call('│ \x1b[90m4\x1b[0m   │   \x1b[1m\x1b[38;2;120;120;120m            return tempfile.gettempdir()\x1b[0m                   │ osbot_utils.utils.Files.temp_folder_current   │      │  388 │     2 │'),
                                                     call('│ \x1b[90m5\x1b[0m   │ \x1b[1m\x1b[38;2;120;120;120m      folder_exists(current_temp_folder())\x1b[0m                   │ test_Trace_Call__Print_Lines.an_method        │      │   27 │     1 │'),
                                                     call('│ \x1b[90m6\x1b[0m   │   \x1b[1m\x1b[92m        def temp_folder_current():\x1b[0m                         │ osbot_utils.utils.Files.temp_folder_current   │      │  387 │     2 │'),
                                                     call('│ \x1b[90m7\x1b[0m   │   \x1b[1m\x1b[38;2;120;120;120m            return tempfile.gettempdir()\x1b[0m                   │ osbot_utils.utils.Files.temp_folder_current   │      │  388 │     2 │'),
                                                     call('│ \x1b[90m8\x1b[0m   │   \x1b[1m\x1b[92m        def folder_exists(path):\x1b[0m                           │ osbot_utils.utils.Files.folder_exists         │      │  166 │     2 │'),
                                                     call('│ \x1b[90m9\x1b[0m   │   \x1b[1m\x1b[38;2;120;120;120m            return is_folder(path)\x1b[0m                         │ osbot_utils.utils.Files.folder_exists         │      │  167 │     2 │'),
                                                     call('│ \x1b[90m10\x1b[0m  │     \x1b[1m\x1b[92m              def is_folder(target):\x1b[0m                     │ osbot_utils.utils.Files.is_folder             │      │  264 │     3 │'),
                                                     call('│ \x1b[90m11\x1b[0m  │     \x1b[1m\x1b[38;2;120;120;120m                  if isinstance(target, Path):\x1b[0m           │ osbot_utils.utils.Files.is_folder             │      │  265 │     3 │'),
                                                     call('│ \x1b[90m12\x1b[0m  │     \x1b[1m\x1b[38;2;120;120;120m                  if type(target) is str:\x1b[0m                │ osbot_utils.utils.Files.is_folder             │      │  267 │     3 │'),
                                                     call('│ \x1b[90m13\x1b[0m  │     \x1b[1m\x1b[38;2;120;120;120m                      return os.path.isdir(target)\x1b[0m       │ osbot_utils.utils.Files.is_folder             │      │  268 │     3 │'),
                                                     call('└─────┴──────────────────────────────────────────────────────────────┴───────────────────────────────────────────────┴──────┴──────┴───────┘')]


        #print_lines.print_lines()
        #self.trace_call.print()

