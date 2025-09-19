import time
import pytest
from datetime                                                                    import datetime, timezone
from typing                                                                      import List
from unittest                                                                    import TestCase
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                  import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Int                              import Safe_Int
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now import Timestamp_Now
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List            import Type_Safe__List
from osbot_utils.utils.Misc                                                      import timestamp_now
from osbot_utils.utils.Objects                                                   import base_types


class test_Timestamp_Now(TestCase):

    def test__init__(self):                                                    # Test basic initialization
        with Timestamp_Now() as _:
            current_time = timestamp_now()

            assert type(_)         is Timestamp_Now
            assert type(int(_))    is int
            assert base_types(_)   == [Safe_Int, int, Type_Safe__Primitive, int, object, object, object]

            # Should be close to current time (within 1 second)
            assert abs(_ - current_time) <= 1

            # Should be a valid timestamp
            assert _ > 0
            assert _ < 2000000000 * 1000                                     # Before year 2033

            assert isinstance(_, int)
            assert isinstance(_, Type_Safe__Primitive)

    def test_auto_generation_behavior(self):                                  # Test that Timestamp_Now generates current time
        timestamp1 = Timestamp_Now()
        time.sleep(0.001)                                                      # Small delay
        timestamp2 = Timestamp_Now()
        time.sleep(0.001)
        timestamp3 = Timestamp_Now()

        # Timestamps should increase with time
        assert timestamp2 >= timestamp1
        assert timestamp3 >= timestamp2

        # But should be very close (within a 5 miliseconds)
        assert timestamp3 - timestamp1 < 5

    def test_with_explicit_int_value(self):                                   # Test providing explicit timestamp
        explicit_timestamp = 1234567890

        with Timestamp_Now(explicit_timestamp) as _:
            assert _ == explicit_timestamp
            assert type(_) is Timestamp_Now

        # Edge case: zero timestamp (Unix epoch)
        epoch = Timestamp_Now(0)
        assert epoch == 0

        # Future timestamp
        future = Timestamp_Now(2000000000)
        assert future == 2000000000

    def test_with_float_value(self):                                          # Test float timestamp conversion
        float_timestamp = 1234567890.123456

        with Timestamp_Now(float_timestamp) as _:
            assert _ == 1234567890123
            assert type(_) is Timestamp_Now

    def test_with_string_timestamp(self):                                     # Test numeric string timestamps
        with Timestamp_Now("1234567890") as _:
            assert _ == 1234567890
            assert type(_) is Timestamp_Now

        with Timestamp_Now("1234567890.999") as _:
            assert _ == 1234567890999                                            # Truncated

    def test_with_iso_date_strings(self):                                     # Test ISO date string parsing
        # Basic date
        with Timestamp_Now("2024-01-15") as _:
            dt = datetime(2024, 1, 15, tzinfo=timezone.utc)
            assert _ == int(dt.timestamp() * 1000)

        # Date with time
        with Timestamp_Now("2024-01-15T10:30:45") as _:
            dt = datetime(2024, 1, 15, 10, 30, 45, tzinfo=timezone.utc)
            assert _ == int(dt.timestamp() * 1000)

        # Date with Z (UTC)
        with Timestamp_Now("2024-01-15T10:30:45Z") as _:
            dt = datetime(2024, 1, 15, 10, 30, 45, tzinfo=timezone.utc)
            assert _ == int(dt.timestamp() * 1000)

        # Date with timezone offset
        with Timestamp_Now("2024-01-15T10:30:45+05:00") as _:
            # This is 05:30:45 UTC
            dt = datetime(2024, 1, 15, 5, 30, 45, tzinfo=timezone.utc)
            assert _ == int(dt.timestamp() * 1000)

    def test_invalid_string_formats(self):                                    # Test error handling for bad formats
        error_pattern = r"Could not parse .* as timestamp or ISO date"

        with pytest.raises(ValueError, match=error_pattern):
            Timestamp_Now("not-a-date")

        with pytest.raises(ValueError, match=error_pattern):
            Timestamp_Now("2024-13-45")                                       # Invalid date

        with pytest.raises(ValueError, match=error_pattern):
            Timestamp_Now("15/01/2024")                                       # Wrong format (not ISO)

    def test_timezone_handling(self):                                         # Test timezone assumptions
        # No timezone = UTC assumed
        naive_date = "2024-01-15T12:00:00"
        with Timestamp_Now(naive_date) as ts1:
            dt_utc = datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
            assert ts1 == int(dt_utc.timestamp() * 1000)

        # Explicit UTC
        utc_date = "2024-01-15T12:00:00Z"
        with Timestamp_Now(utc_date) as ts2:
            assert ts2 == ts1                                                   # Same as naive (both UTC)

        # Different timezone
        est_date = "2024-01-15T12:00:00-05:00"                                  # EST
        with Timestamp_Now(est_date) as ts3:
            assert ts3 == ts1 + (5 * 3600) * 1000                               # 5 hours later in UTC

    def test_str_representation(self):                                          # Test string conversion
        explicit = Timestamp_Now(1234567890)

        assert str(explicit) == "1234567890"
        assert repr(explicit) == "Timestamp_Now(1234567890)"

        # Formatting
        assert f"Time: {explicit}" == "Time: 1234567890"
        assert "{:d}".format(explicit) == "1234567890"

    def test_arithmetic_operations(self):                                     # Test arithmetic with timestamps
        base = Timestamp_Now(1000000000)

        # Addition
        result = base + 3600                                                  # Add 1 hour
        assert result == 1000003600
        assert type(result) is Timestamp_Now

        # Subtraction
        result = base - 3600                                                  # Subtract 1 hour
        assert result == 999996400
        assert type(result) is Timestamp_Now

        # Difference between timestamps
        ts1 = Timestamp_Now(1000000000)
        ts2 = Timestamp_Now(1000003600)
        diff = ts2 - ts1
        assert diff == 3600
        assert type(diff) is Timestamp_Now

    def test_comparison_operations(self):                                     # Test comparisons
        ts1 = Timestamp_Now(1000000000)
        ts2 = Timestamp_Now(1000003600)
        ts3 = Timestamp_Now(1000000000)

        assert ts1 < ts2
        assert ts2 > ts1
        assert ts1 <= ts3
        assert ts1 >= ts3
        assert ts1 == ts3
        assert ts1 != ts2

        # Compare with integers
        assert ts1 == 1000000000
        assert ts1 < 1000003600
        assert ts2 > 1000000000

    def test_in_type_safe_schema(self):                                       # Test usage in Type_Safe classes
        class Schema__Event(Type_Safe):
            created_at  : Timestamp_Now                                       # Auto-generates current time
            updated_at  : Timestamp_Now = None                               # Explicitly nullable
            scheduled_at: Timestamp_Now

        with Schema__Event() as _:
            current = timestamp_now()

            # Auto-generated timestamps
            assert type(_.created_at) is Timestamp_Now
            assert type(_.scheduled_at) is Timestamp_Now
            assert abs(_.created_at - current) <= 1                          # Recent
            assert abs(_.scheduled_at - current) <= 1

            # Nullable field
            assert _.updated_at is None

            # Can set explicit value
            _.updated_at = Timestamp_Now(1234567890)
            assert _.updated_at == 1234567890

            # Can set from string
            _.scheduled_at = "2025-12-31T23:59:59Z"
            dt = datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
            assert _.scheduled_at == int(dt.timestamp()) * 1000

    def test_json_serialization_in_schema(self):                              # Test JSON round-trip
        class Schema__Record(Type_Safe):
            timestamp   : Timestamp_Now
            modified    : Timestamp_Now
            expires     : Timestamp_Now

        original = Schema__Record()
        original.expires = Timestamp_Now("2025-01-01T00:00:00Z")

        # Serialize
        json_data = original.json()
        assert 'timestamp' in json_data
        assert 'modified' in json_data
        assert 'expires' in json_data

        # All should be integers
        assert type(json_data['timestamp']) is int
        assert type(json_data['modified']) is int
        assert type(json_data['expires']) is int

        # Deserialize
        restored = Schema__Record.from_json(json_data)

        # Should preserve exact values
        assert restored.timestamp == original.timestamp
        assert restored.modified == original.modified
        assert restored.expires == original.expires

        # Types should be preserved
        assert type(restored.timestamp) is Timestamp_Now
        assert type(restored.modified) is Timestamp_Now
        assert type(restored.expires) is Timestamp_Now

    def test_hashability(self):                                               # Test use as dict key
        ts1 = Timestamp_Now(1000000000)
        ts2 = Timestamp_Now(1000003600)
        ts3 = Timestamp_Now(1000007200)

        # Should work as dict keys
        mapping = {
            ts1: 'early',
            ts2: 'middle',
            ts3: 'late'
        }

        assert mapping[ts1] == 'early'
        assert mapping[ts2] == 'middle'
        assert mapping[ts3] == 'late'
        assert len(mapping) == 3

        # Should work in sets
        ts_set = {ts1, ts2, ts3}
        assert len(ts_set) == 3
        assert ts1 in ts_set

    def test_use_in_collections(self):                                        # Test in Type_Safe collections
        class Schema__Timeline(Type_Safe):
            start      : Timestamp_Now
            checkpoints: List[Timestamp_Now]

        with Schema__Timeline() as _:
            assert type(_.start) is Timestamp_Now
            assert type(_.checkpoints) is Type_Safe__List

            # Add checkpoints
            _.checkpoints.append(Timestamp_Now())
            time.sleep(0.01)
            _.checkpoints.append(Timestamp_Now())
            time.sleep(0.01)
            _.checkpoints.append(Timestamp_Now())

            # Should be in chronological order
            for i in range(len(_.checkpoints) - 1):
                assert _.checkpoints[i] <= _.checkpoints[i + 1]

    def test_conversion_to_datetime(self):                                    # Test converting back to datetime
        ts = Timestamp_Now(1234567890)

        # Can convert to datetime
        dt = datetime.fromtimestamp(int(ts), tz=timezone.utc)
        assert dt.year == 2009
        assert dt.month == 2
        assert dt.day == 13

        # Round trip through datetime
        dt2 = datetime(2024, 1, 15, 10, 30, 45, tzinfo=timezone.utc)
        ts2 = Timestamp_Now(int(dt2.timestamp()))
        dt3 = datetime.fromtimestamp(int(ts2), tz=timezone.utc)
        assert dt3 == dt2

    def test_inheritance_chain(self):                                         # Test type hierarchy
        ts = Timestamp_Now()

        # Check inheritance
        assert base_types(ts) == [Safe_Int, int, Type_Safe__Primitive, int, object, object, object]
        assert isinstance(ts, Timestamp_Now       )
        assert isinstance(ts, Safe_Int            )
        assert isinstance(ts, Type_Safe__Primitive)
        assert isinstance(ts, int                 )

        # Should work in integer contexts
        assert ts + 100 > ts
        assert ts * 1 == ts
        assert ts // 1 == ts

    def test_edge_cases(self):                                                # Test edge behaviors
        # Very old timestamp
        old = Timestamp_Now(1)
        assert old == 1

        # Unix epoch
        epoch = Timestamp_Now(0)
        assert epoch == 0

        # Year 2038 problem boundary (32-bit systems)
        year_2038 = Timestamp_Now(2147483647)
        assert year_2038 == 2147483647

        # Empty string should generate current time
        with Timestamp_Now('') as _:
            current = timestamp_now()
            assert abs(_ - current) <= 1

    def test_precision_handling(self):                                        # Test sub-second precision is truncated
        # Microsecond precision in ISO format
        iso_with_micro = "2024-01-15T10:30:45.123456"
        with Timestamp_Now(iso_with_micro) as _:
            dt = datetime(2024, 1, 15, 10, 30, 45, tzinfo=timezone.utc)
            assert _ == 1705314645123

        # Float with decimals
        float_ts = 1234567890.999999
        with Timestamp_Now(float_ts) as _:
            assert _ == 1234567890999

    def test_rapid_generation(self):                                          # Test generating many timestamps quickly
        timestamps = []
        for _ in range(100):
            timestamps.append(Timestamp_Now())

        # Should all be very close (within 1 second)
        assert max(timestamps) - min(timestamps) < 1

        # Should be non-decreasing
        for i in range(len(timestamps) - 1):
            assert timestamps[i] <= timestamps[i + 1]

    def test_default_behavior_in_function_params(self):                       # Test as default parameter
        def process_event(timestamp: Timestamp_Now = None):
            if timestamp is None:
                timestamp = Timestamp_Now()
            return timestamp

        # Without providing timestamp
        ts1 = process_event()
        ts2 = process_event()
        assert abs(ts2 - ts1) < 1                                            # Both recent

        # With providing timestamp
        specific_ts = Timestamp_Now(1234567890)
        ts3 = process_event(specific_ts)
        assert ts3 == specific_ts

    def test_real_world_date_formats(self):                                  # Test common real-world formats
        # API responses often use these formats
        test_cases = [("2024-01-15"               , datetime(2024, 1, 15            , tzinfo=timezone.utc)),
                      ("2024-01-15T10:30:45"      , datetime(2024, 1, 15, 10, 30, 45, tzinfo=timezone.utc)),
                      ("2024-01-15T10:30:45Z"     , datetime(2024, 1, 15, 10, 30, 45, tzinfo=timezone.utc)),
                      ("2024-01-15T10:30:45+00:00", datetime(2024, 1, 15, 10, 30, 45, tzinfo=timezone.utc)),]

        for date_str, expected_dt in test_cases:
            with Timestamp_Now(date_str) as ts:
                assert ts == int(expected_dt.timestamp() * 1000)