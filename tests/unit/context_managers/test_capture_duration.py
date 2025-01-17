from unittest import TestCase

from osbot_utils.testing.Stdout import Stdout

from osbot_utils.context_managers.capture_duration import capture_duration

class test_capture_duration(TestCase):

    def test__init__(self):
        with capture_duration() as _:
            assert _.action_name == ''
            assert _.duration    == 0
            assert _.start_time   > 0
            assert _.end_time    == 0
            assert _.seconds     == 0

    def test__enter__(self):
        with capture_duration() as _:
            assert _.start_time > 0
            assert _.end_time   == 0
            assert _.duration   == 0
            assert _.seconds    == 0

    def test__exit__(self):
        with capture_duration() as _:
            assert _.start_time  > 0
            assert _.end_time   == 0
            assert _.duration   == 0
            assert _.seconds    == 0
        assert _.end_time  > 0
        assert _.duration >= 0
        assert _.seconds  >= 0

    def test_data(self):
        with capture_duration() as _:
            assert _.data() == {'end': 0, 'seconds': 0, 'start': _.start_time}
        assert _.data() == {'end': _.end_time, 'seconds': _.seconds, 'start': _.start_time}

    def test_print(self):
        with Stdout() as stdout_1:
            with capture_duration() as _:
                _.print()
        assert stdout_1.value() == '\naction took: 0.0 seconds\n'

        with Stdout() as stdout_2:
            with capture_duration(action_name='an action') as _:
                _.print()
        assert stdout_2.value() == '\naction "an action" took: 0.0 seconds\n'



    def test__exit__with_exception(self):
        with self.assertRaises(ValueError) as context:
            with capture_duration() as _:
                assert _.start_time > 0
                assert _.end_time   == 0
                assert _.duration   == 0
                assert _.seconds    == 0
                raise ValueError('test exception')
        assert _.end_time > 0
        assert _.duration >= 0
        assert _.seconds  >= 0
        assert context.exception.args[0] == 'test exception'
