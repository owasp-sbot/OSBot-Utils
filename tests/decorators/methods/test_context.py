from unittest import TestCase
from unittest.mock import MagicMock

from osbot_utils.decorators.methods.context import context


class test_context(TestCase):

    def test_context(self):
        before_mock = MagicMock()
        after_mock = MagicMock()
        def the_answer():
            return 42
        def exec_before():
            before_mock()
        def exec_after():
            after_mock()

        with context(the_answer, exec_before=exec_before, exec_after=exec_after) as target:
            assert target() == 42

        before_mock.assert_called_once()
        after_mock.assert_called_once()

    def test_exec_before_and_after_called(self):
        before_mock = MagicMock()
        after_mock = MagicMock()
        target_value = "test_target"

        with context(target_value, exec_before=before_mock, exec_after=after_mock) as target:
            before_mock.assert_called_once()
            after_mock.assert_not_called()
            self.assertEqual(target, target_value)

        after_mock.assert_called_once()

    def test_confirm_yield_is_target(self):
        target_value = "test_target"
        with context(target_value) as target:               # No before or after functions provided, should run without errors
            self.assertEqual(target, target_value)


    def test_exec_after_called_even_if_exception_raised(self):
        after_mock = MagicMock()

        with self.assertRaises(ValueError):
            with context("test_target", exec_after=after_mock) as target:
                raise ValueError("An error occurred inside the with block.")

        after_mock.assert_called_once()

        after_mock_2 = MagicMock()
        def throw_exception():
            raise ValueError("An error occurred inside the with block.")

        with self.assertRaises(ValueError):
            with context(throw_exception, exec_after=after_mock_2) as target:
                target()

        after_mock_2.assert_called_once()



