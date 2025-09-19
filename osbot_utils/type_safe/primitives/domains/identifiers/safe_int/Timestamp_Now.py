from datetime                                   import datetime, timezone, UTC
from osbot_utils.type_safe.Type_Safe__Primitive import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Int import Safe_Int


# note that this timestemp value returns an Int, since it uses
#    int(datetime.now(UTC).timestamp() * 1000)
#    i.e. we don't have the fraction section (this is done becasue some data stores don't support floats)

class Timestamp_Now(Safe_Int, int):
    def __new__(cls, value=None):
        if value is None:
            value = cls.timestamp_utc_now()                                                 # Returns milliseconds
        elif isinstance(value, str):
            value = cls.parse_string_value(value)
        elif isinstance(value, float):
            value = int(value * 1000)                                              # Convert seconds to milliseconds

        return int.__new__(cls, value)

    @classmethod
    def parse_string_value(cls, value_str: str) -> int:                                 # Convert string to timestamp preserving precision
        if not value_str:
            return cls.timestamp_utc_now()                                              # Empty string returns current time

        try:
            num_value = float(value_str)
            if '.' in value_str:                                                        # Has decimal part - seconds with fraction
                return int(num_value * 1000)                                            # Convert to milliseconds like datetime.timestamp()
            else:
                return int(num_value)                                                   # Integer string - preserve as-is

        except ValueError:
            pass

        try:                                                                            # Try ISO format parsing
            if value_str.endswith('Z'):
                value_str = value_str[:-1] + '+00:00'                                   # Convert Z to timezone offset

            dt = datetime.fromisoformat(value_str)

            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)                                    # Assume UTC if no timezone

            return int(dt.timestamp() * 1000)                                           # Convert to milliseconds for consistency
        except ValueError:
            raise ValueError(f"Could not parse '{value_str}' as timestamp or ISO date. "
                           f"Format: YYYY-MM-DD[THH:MM:SS][+HH:MM|Z] "
                           f"(assumes UTC if no timezone specified)")

    @classmethod
    def timestamp_utc_now(cls):
        return int(datetime.now(UTC).timestamp() * 1000)

    def __str__(self):
        return str(int(self))

    def __repr__(self):
        return f"Timestamp_Now({int(self)})"