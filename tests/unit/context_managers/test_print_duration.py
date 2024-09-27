from unittest import TestCase

from osbot_utils.context_managers.print_duration import print_duration
from osbot_utils.testing.Stdout import Stdout


class test_print_duration(TestCase):

    def test__exit__(self):
        with Stdout() as stdout:
            with print_duration() as _:
                pass
        assert stdout.value() == f'\naction took: {_.seconds} seconds\n'