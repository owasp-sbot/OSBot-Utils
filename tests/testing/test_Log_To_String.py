import logging
from unittest import TestCase

from osbot_utils.testing.Log_To_String import Log_To_String


class test_Log_To_String(TestCase):

    def setUp(self) -> None:
        self.logger = logging.getLogger()

    def add_test_log_entires(self):
        self.logger.critical('critical message')        # level 50
        self.logger.error   ('error message'   )        # level 40
        self.logger.warning ('warning message' )        # level 30
        self.logger.info    ('info message'    )        # level 20
        self.logger.debug   ('debug message'   )        # level 10


    def test__enter____leave__(self):
        with Log_To_String(self.logger) as log_to_string:
            log_to_string.set_level_warning()
            self.add_test_log_entires()
            assert log_to_string.contents() == "critical message\nerror message\nwarning message\n"
            self.logger.exception("an exception")

    def test_set_level_critical(self):
        with Log_To_String(self.logger) as log_to_string:
            log_to_string.set_level_critical()
            self.add_test_log_entires()
            assert log_to_string.contents() == "critical message\n"

    def test_set_level_debug(self):
        with Log_To_String(self.logger) as log_to_string:
            log_to_string.set_level_debug()
            self.add_test_log_entires()
            assert log_to_string.contents() == "critical message\nerror message\nwarning message\ninfo message\ndebug message\n"

    def test_set_level_error(self):
        with Log_To_String(self.logger) as log_to_string:
            log_to_string.set_level_error()
            self.add_test_log_entires()
            assert log_to_string.contents() == "critical message\nerror message\n"

    def test_set_level_info(self):
        with Log_To_String(self.logger) as log_to_string:
            log_to_string.set_level_info()
            self.add_test_log_entires()
            assert log_to_string.contents() == "critical message\nerror message\nwarning message\ninfo message\n"

    def test_set_level_warning(self):
        with Log_To_String(self.logger) as log_to_string:
            log_to_string.set_level_warning()
            self.add_test_log_entires()
            assert log_to_string.contents() == "critical message\nerror message\nwarning message\n"

    def test__logging_an_exception(self):
        with Log_To_String(self.logger) as log_to_string:
            try:
                print(10/0)
            except:
                self.logger.exception('this should not work')
            assert 'this should not work'                in log_to_string.contents()
            assert 'Traceback (most recent call last):'  in log_to_string.contents()
            assert 'ZeroDivisionError: division by zero' in log_to_string.contents()