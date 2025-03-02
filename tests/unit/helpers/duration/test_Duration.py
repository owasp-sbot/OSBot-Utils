from unittest                               import TestCase
from datetime                               import timedelta, datetime
from osbot_utils.helpers.duration.Duration  import Duration
from osbot_utils.testing.Stdout             import Stdout
from osbot_utils.utils.Misc                 import wait, time_delta_to_str


class test_Duration(TestCase):

    def test_duration_context_manager(self):  # Test basic context manager functionality
        with Stdout() as stdout:
            with Duration() as duration:
                wait(0.0001)  # Small wait to ensure measurable duration

        duration_str = time_delta_to_str(duration.duration)
        assert stdout.value() == f'\nDuration: {duration_str}\n'
        assert duration.start_time is not None
        assert duration.end_time is not None
        assert duration.duration is not None
        assert isinstance(duration.duration, timedelta)

    def test_duration_with_custom_prefix(self):  # Test custom prefix
        with Stdout() as stdout:
            with Duration(prefix="Test time:") as duration:
                wait(0.0001)

        duration_str = time_delta_to_str(duration.duration)
        assert stdout.value() == f'Test time: {duration_str}\n'

    def test_duration_without_print(self):  # Test with print_result=False
        with Stdout() as stdout:
            with Duration(print_result=False) as duration:
                wait(0.0001)

        assert stdout.value() == ""  # Nothing should be printed
        assert duration.duration is not None  # But duration should be calculated

    def test_duration_manual_calls(self):  # Test manual start/end calls
        duration = Duration(print_result=False)
        duration.start()
        wait(0.0001)
        duration.end()

        assert duration.start_time is not None
        assert duration.end_time is not None
        assert duration.duration is not None
        assert duration.duration.total_seconds() > 0

    def test_duration_print_with_manual_calls(self):  # Test manual calls with printing
        with Stdout() as stdout:
            duration = Duration()
            duration.start()
            wait(0.0001)
            duration.end()

        duration_str = time_delta_to_str(duration.duration)
        assert stdout.value() == f'\nDuration: {duration_str}\n'

    def test_duration_milliseconds(self):  # Test milliseconds method
        duration = Duration(print_result=False)
        duration.start()
        wait(0.0001)
        duration.end()

        milliseconds = duration.milliseconds()
        assert milliseconds > 0  # Should be positive
        assert milliseconds >= 0.1  # Should be at least 25ms (wait time)

    def test_duration_seconds(self):  # Test seconds method
        duration = Duration(print_result=False)
        duration.start()
        wait(0.0001)
        duration.end()

        seconds = duration.seconds()
        assert seconds > 0  # Should be positive
        assert seconds >= 0.0001  # Should be at least 0.03s (wait time)

    def test_duration_set_duration(self):  # Test set_duration method
        duration = Duration(print_result=False)
        returned_duration = duration.set_duration(42)

        assert duration.duration        == timedelta(seconds=42)  # Duration should be 42 seconds
        assert returned_duration        == duration  # Should return self for chaining
        assert duration.seconds()       == 42  # Seconds method should return 42
        assert duration.milliseconds()  == 42000  # Milliseconds should return 42000

    def test_duration_with_call_stack(self):  # Test with print_stack=True
        with Stdout() as stdout:
            with Duration(print_stack=True) as duration:
                wait(0.0001)

        output = stdout.value()
        duration_str = time_delta_to_str(duration.duration)

        assert output == ("\n"
                          f"Duration: {duration_str}\n"
                          "\x1b[0m─ test_Duration.test_duration_with_call_stack\x1b[0m"
                          "\n")

    def test_duration_use_utc_false(self):  # Test with use_utc=False
        duration_utc = Duration(print_result=False, use_utc=True)
        duration_local = Duration(print_result=False, use_utc=False)

        duration_utc.start()
        duration_local.start()
        wait(0.0001)
        duration_utc.end()
        duration_local.end()

        # Both should have valid durations
        assert duration_utc.duration is not None
        assert duration_local.duration is not None

        # Start times might be different depending on time zone
        # but both should represent valid datetime objects
        assert duration_utc.start_time is not None
        assert duration_local.start_time is not None

    def test_data_basic(self):                                                               # Test basic data() functionality
        duration = Duration(print_result=False)
        duration.start()
        wait(0.0001)                                                                                  # Small wait for measurable duration
        duration.end()

        data = duration.data()

        assert data.utc               == duration.use_utc                                         # Check schema fields match duration object
        assert data.timestamp_start   == duration.start_time.timestamp()
        assert data.timestamp_end     == duration.end_time  .timestamp()
        assert data.duration_seconds  == duration.seconds()
        assert isinstance(data.duration_seconds, float)

    def test_data_with_set_duration(self):                                                          # Test data() with set_duration
        duration = Duration(print_result=False)
        duration.start_time = datetime.now()
        duration.end_time   = datetime.now()
        duration.set_duration(42)                                                                   # Set a specific duration

        data = duration.data()

        assert data.duration_seconds == 42                                                        # Duration should be exactly 42 seconds

    def test_data_with_use_utc_false(self):                                                         # Test data() with use_utc=False
        duration = Duration(print_result=False, use_utc=False)
        duration.start()
        wait(0.0001)
        duration.end()

        data = duration.data()

        assert data.utc == False                                                                  # UTC flag should be False

    def test_data_before_end(self):                                                                 # Test data() before calling end()
        duration = Duration(print_result=False)
        duration.start()

        with self.assertRaises(ValueError) as context:                                              # Should raise ValueError
            duration.data()

        assert "Duration has not been calculated yet" in str(context.exception)                     # Check error message

    def test_data_type_safety(self):                                                                # Test type safety of Schema__Duration
        duration = Duration(print_result=False)
        duration.start()
        wait(0.0001)
        duration.end()

        data = duration.data()

        # Type checks
        assert isinstance(data.utc, bool)
        assert isinstance(data.timestamp_start, float)
        assert isinstance(data.timestamp_end, float)
        assert isinstance(data.duration_seconds, float)

        # Verify data consistency
        assert data.timestamp_end > data.timestamp_start                                          # End time should be after start time
        assert data.duration_seconds > 0                                                          # Duration should be positive
        assert abs(data.duration_seconds - (data.timestamp_end - data.timestamp_start)) < 0.001   # Duration should match time difference