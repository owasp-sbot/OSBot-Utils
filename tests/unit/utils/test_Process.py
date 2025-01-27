import sys
from unittest                   import TestCase
from unittest.mock              import patch, call
from osbot_utils.utils.Process  import run_process, exec_open, stop_process


class test_Process(TestCase):

    # def test_chmod_x(self):
    #     temp_exe = temp_file('exe', "aaaa")
    #     assert '-rw-r--r--' in run_process('ls', ['-la', temp_exe])['stdout']
    #     chmod_x(temp_exe)
    #     assert '-rwxr-xr-x' in run_process('ls', ['-la', temp_exe])['stdout']

    def test_run(self):

        assert run_process('echo', ['hello', 'world'])['stdout'] == 'hello world\n'
        assert run_process('echo', 'hello world')['stdout'] == 'hello world\n'

        run_error = run_process('aaaaa_bbbbb')['error']
        assert type(run_error) == FileNotFoundError
        assert str(run_error ) == "[Errno 2] No such file or directory: 'aaaaa_bbbbb'"

    @patch("osbot_utils.utils.Process.Process.run")
    def test_exec_open(self, process_run):
        exec_open("file_path", "cwd")
        assert process_run.mock_calls == [call('open', ['file_path'], 'cwd')]

    @patch("os.kill")
    def test_stop_process(self, os_kill):
        pid = 12345
        stop_process(pid)
        assert str(os_kill.mock_calls) == "[call(12345, <Signals.SIGKILL: 9>)]"


