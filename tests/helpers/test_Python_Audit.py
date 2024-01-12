import sys
from unittest import TestCase
from unittest.mock import call, patch

import pytest

from osbot_utils.testing.Patch_Print import Patch_Print
from osbot_utils.utils.Dev import pprint

from osbot_utils.testing.Temp_File import Temp_File

from osbot_utils.utils.Files import current_temp_folder, folder_exists

from osbot_utils.helpers.Python_Audit import Python_Audit


class test_Python_Audit(TestCase):

    def setUp(self):
        self.python_audit = Python_Audit()

    def test___init__(self):
        expected_locals = { 'audit_events'      : [] }
        assert self.python_audit.__locals__() == expected_locals


    def test_hook_callback(self):
        current_frame = sys._getframe()
        assert self.python_audit.audit_events == []
        self.python_audit.hook_callback('event-1', 'args-1')
        assert self.python_audit.audit_events == [('event-1', 'args-1', current_frame)]
        self.python_audit.hook_callback('event-2', 'args-2')
        assert self.python_audit.audit_events == [('event-1', 'args-1', current_frame), ('event-2', 'args-2', current_frame)]

        assert self.python_audit.data() == [{'args': 'args-1', 'event': 'event-1', 'index': 0, 'stack': current_frame},
                                            {'args': 'args-2', 'event': 'event-2', 'index': 1, 'stack': current_frame},]

        assert self.python_audit.events() == self.python_audit.audit_events
        assert self.python_audit.events_by_type() == {'event-1': 1, 'event-2': 1}

        with Patch_Print() as _:
            self.python_audit.print()

        assert _.call_args_list() == [call(),
                                      call( '┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐'),
                                      call( '│ index │ event   │ args   │ stack                                                                                                                                                              │'),
                                      call( '├───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤'),
                                      call(f"│ 0     │ event-1 │ args-1 │ {str(current_frame).replace('line 44', 'line 42')} │"),
                                      call(f"│ 1     │ event-2 │ args-2 │ {str(current_frame).replace('line 44', 'line 42')} │"),
                                      call( '└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘')]


    def test_start(self):
        with patch("sys.addaudithook") as add_audit_hook:
            assert self.python_audit.start() is self.python_audit
            assert add_audit_hook.call_args_list == [call(self.python_audit.hook_callback)]

    @pytest.mark.skip("this can't be run in CI since there isn't a way to remove the audit callback method")
    def test_start_skipped(self):

        assert self.python_audit.start() is self.python_audit
        with Temp_File():
            pass
            #requests.get("https://www.google.com/404")

        #self.python_audit.print()

        assert self.python_audit.events_by_type() == { 'open'            : 2,
                                                       'os.mkdir'        : 1,
                                                       'os.remove'       : 1,
                                                       'os.rmdir'        : 1,
                                                       'os.scandir'      : 1,
                                                       'shutil.rmtree'   : 1,
                                                       'tempfile.mkdtemp': 1}

