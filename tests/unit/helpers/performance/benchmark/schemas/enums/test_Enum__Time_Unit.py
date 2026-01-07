# ═══════════════════════════════════════════════════════════════════════════════
# test_Enum__Time_Unit - Tests for time unit enumeration
# ═══════════════════════════════════════════════════════════════════════════════

from enum                                                                                                 import Enum
from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Time_Unit                              import Enum__Time_Unit


class test_Enum__Time_Unit(TestCase):

    def test__init__(self):                                                      # Test enum values exist
        assert Enum__Time_Unit.NANOSECONDS  is not None
        assert Enum__Time_Unit.MICROSECONDS is not None
        assert Enum__Time_Unit.MILLISECONDS is not None
        assert Enum__Time_Unit.SECONDS      is not None

    def test_values(self):                                                       # Test enum value strings
        assert Enum__Time_Unit.NANOSECONDS.value  == 'ns'
        assert Enum__Time_Unit.MICROSECONDS.value == 'µs'
        assert Enum__Time_Unit.MILLISECONDS.value == 'ms'
        assert Enum__Time_Unit.SECONDS.value      == 's'

    def test_inheritance(self):                                                  # Test inherits from Enum
        assert isinstance(Enum__Time_Unit.NANOSECONDS, Enum)

    def test_members(self):                                                      # Test all members present
        members = list(Enum__Time_Unit)
        assert len(members) == 4
        assert Enum__Time_Unit.NANOSECONDS  in members
        assert Enum__Time_Unit.MICROSECONDS in members
        assert Enum__Time_Unit.MILLISECONDS in members
        assert Enum__Time_Unit.SECONDS      in members

    def test_by_value(self):                                                     # Test lookup by value
        assert Enum__Time_Unit('ns') == Enum__Time_Unit.NANOSECONDS
        assert Enum__Time_Unit('µs') == Enum__Time_Unit.MICROSECONDS
        assert Enum__Time_Unit('ms') == Enum__Time_Unit.MILLISECONDS
        assert Enum__Time_Unit('s')  == Enum__Time_Unit.SECONDS

    def test_by_name(self):                                                      # Test lookup by name
        assert Enum__Time_Unit['NANOSECONDS']  == Enum__Time_Unit.NANOSECONDS
        assert Enum__Time_Unit['MICROSECONDS'] == Enum__Time_Unit.MICROSECONDS
        assert Enum__Time_Unit['MILLISECONDS'] == Enum__Time_Unit.MILLISECONDS
        assert Enum__Time_Unit['SECONDS']      == Enum__Time_Unit.SECONDS

    def test_comparison(self):                                                   # Test equality comparison
        unit_1 = Enum__Time_Unit.NANOSECONDS
        unit_2 = Enum__Time_Unit.NANOSECONDS
        unit_3 = Enum__Time_Unit.MICROSECONDS

        assert unit_1 == unit_2
        assert unit_1 != unit_3
        assert unit_1 is unit_2                                                  # Same instance

    def test_name_attribute(self):                                               # Test name attribute
        assert Enum__Time_Unit.NANOSECONDS.name  == 'NANOSECONDS'
        assert Enum__Time_Unit.MICROSECONDS.name == 'MICROSECONDS'
        assert Enum__Time_Unit.MILLISECONDS.name == 'MILLISECONDS'
        assert Enum__Time_Unit.SECONDS.name      == 'SECONDS'
