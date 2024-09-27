from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.testing.Stdout import Stdout


class test_capture_exception(TestCase):

    def test__capture_exception(self):
        from osbot_utils.decorators.methods.capture_exception import capture_exception

        @capture_exception
        def an_method():
            pass

        @capture_exception
        def an_method__with_exception():
            raise Exception('test exception')

        with Stdout() as stdout_1:
            an_method__with_exception()

        assert stdout_1.value() == ('\n'
                                  '****** EXCEPTION DETECTED ******\n'
                                  '\n'
                                  "{ 'exception_type': 'Exception',\n"
                                  "  'last_frame': { 'file': "
                                  f"'{__file__}',\n"
                                  "                  'line': 19},\n"
                                 "  'message': 'test exception'}\n")

        with Stdout() as stdout_2:
            an_method()

        assert stdout_2.value() == ''
