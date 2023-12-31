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

    def test_context__with_args(self):
        def the_answer(value):
            assert value == 42
            return "it's 42"
        def exec_before(value):
            assert value == 'before_and_after'
        def exec_after(value):
            assert value == 'before_and_after'

        with context(the_answer, 'before_and_after', exec_before=exec_before, exec_after=exec_after) as target:     # value can be passed as a param
            assert target(42) == "it's 42"
        args = ['before_and_after']
        with context(the_answer, *args, exec_before=exec_before, exec_after=exec_after) as target:  # or as an *args object at the start
            assert target(42) == "it's 42"
        with context(the_answer, exec_before=exec_before, exec_after=exec_after, *args) as target: # or as an *args object at the end
            assert target(42) == "it's 42"

    def test_context__with_kwargs(self):
        value_before_and_after = {'before_and_after': 42}
        value_target           = {'target': 42}
        return_value           = "value was value_target"

        def an_dict(value):
            assert value == value_target
            return return_value
        def exec_before(value):
            assert value == value_before_and_after
        def exec_after(value):
            assert value == value_before_and_after

        with context(an_dict, value_before_and_after, exec_before=exec_before, exec_after=exec_after) as target:     # value can be passed as a param
            assert target(value_target) == return_value

        an_dict = {'answer': 42}

        def target(value):
            assert value == an_dict
            return context

        def exec_before(value):
            assert value == an_dict

        def exec_after(value):
            assert value == an_dict

        with context(target, an_dict, exec_before=exec_before, exec_after=exec_after) as target:  # value can be passed as a param
            assert target(an_dict) == context

    def test_context__with_kwargs_as_locals(self):
        """
        shows an example of how to use the kwargs to pass data to the target function
        """
        def target(data):
            assert data == {'in_exec_before': 2, 'raw_data': 1}
            data['in_target'] = 3
            return data

        def exec_before(data):
            assert data == {'raw_data': 1}
            data['in_exec_before']  = 2

        def exec_after(data):
            assert data == {'in_exec_before': 2, 'in_target': 3, 'raw_data': 1}
            data['in_exec_after'] = 4

        raw_data = {'raw_data': 1}
        with context(target, raw_data, exec_before=exec_before, exec_after=exec_after) as target:
            assert target(raw_data) == {'in_exec_before': 2, 'in_target': 3, 'raw_data': 1}
        assert raw_data ==  {'in_exec_before': 2, 'in_target': 3, 'in_exec_after': 4, 'raw_data': 1}

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



