from unittest.mock import patch, MagicMock, _patch
from osbot_utils.utils.Dev import pprint
from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


class Patch_Print(Kwargs_To_Self):
    enabled        : bool      = True
    expected_calls : list
    mocked_print   : MagicMock
    patched_print  : _patch
    print_calls    : bool


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __enter__(self):
        if self.enabled:
            self.patched_print = patch('builtins.print')
            self.mocked_print = self.patched_print.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.enabled:
            self.patched_print.stop()

            if self.print_calls:
                pprint(self.calls())
                #print(self.mocked_print.call_args_list)

            if self.expected_calls:
                assert self.calls() == self.expected_calls

    def call_args_list(self):
        if self.mocked_print:
            return self.mocked_print.call_args_list
        return []

    def calls(self):
        calls_data = []
        if self.mocked_print:
            for call in self.mocked_print.call_args_list:
                if len(call.args) == 0 and call.kwargs == {}:
                    call_data = ''
                elif len(call.args) == 1 and call.kwargs == {}:
                    call_data = call.args[0]
                else:
                    call_data = (call.args,  call.kwargs)
                calls_data.append(call_data)
        return calls_data


