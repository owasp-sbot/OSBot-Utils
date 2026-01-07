# ═══════════════════════════════════════════════════════════════════════════════
# test_Enum__Hypothesis__Status - Tests for hypothesis status enumeration
# ═══════════════════════════════════════════════════════════════════════════════

from enum                                                                                                 import Enum
from unittest                                                                                             import TestCase
from osbot_utils.helpers.performance.benchmark.schemas.enums.Enum__Hypothesis__Status                     import Enum__Hypothesis__Status


class test_Enum__Hypothesis__Status(TestCase):

    def test__init__(self):                                                      # Test enum values exist
        assert Enum__Hypothesis__Status.SUCCESS      is not None
        assert Enum__Hypothesis__Status.FAILURE      is not None
        assert Enum__Hypothesis__Status.INCONCLUSIVE is not None
        assert Enum__Hypothesis__Status.REGRESSION   is not None

    def test_values(self):                                                       # Test enum value strings
        assert Enum__Hypothesis__Status.SUCCESS.value      == 'success'
        assert Enum__Hypothesis__Status.FAILURE.value      == 'failure'
        assert Enum__Hypothesis__Status.INCONCLUSIVE.value == 'inconclusive'
        assert Enum__Hypothesis__Status.REGRESSION.value   == 'regression'

    def test_inheritance(self):                                                  # Test inherits from Enum
        assert isinstance(Enum__Hypothesis__Status.SUCCESS, Enum)

    def test_members(self):                                                      # Test all members present
        members = list(Enum__Hypothesis__Status)
        assert len(members) == 4
        assert Enum__Hypothesis__Status.SUCCESS      in members
        assert Enum__Hypothesis__Status.FAILURE      in members
        assert Enum__Hypothesis__Status.INCONCLUSIVE in members
        assert Enum__Hypothesis__Status.REGRESSION   in members

    def test_by_value(self):                                                     # Test lookup by value
        assert Enum__Hypothesis__Status('success')      == Enum__Hypothesis__Status.SUCCESS
        assert Enum__Hypothesis__Status('failure')      == Enum__Hypothesis__Status.FAILURE
        assert Enum__Hypothesis__Status('inconclusive') == Enum__Hypothesis__Status.INCONCLUSIVE
        assert Enum__Hypothesis__Status('regression')   == Enum__Hypothesis__Status.REGRESSION

    def test_by_name(self):                                                      # Test lookup by name
        assert Enum__Hypothesis__Status['SUCCESS']      == Enum__Hypothesis__Status.SUCCESS
        assert Enum__Hypothesis__Status['FAILURE']      == Enum__Hypothesis__Status.FAILURE
        assert Enum__Hypothesis__Status['INCONCLUSIVE'] == Enum__Hypothesis__Status.INCONCLUSIVE
        assert Enum__Hypothesis__Status['REGRESSION']   == Enum__Hypothesis__Status.REGRESSION

    def test_comparison(self):                                                   # Test equality comparison
        status_1 = Enum__Hypothesis__Status.SUCCESS
        status_2 = Enum__Hypothesis__Status.SUCCESS
        status_3 = Enum__Hypothesis__Status.FAILURE

        assert status_1 == status_2
        assert status_1 != status_3
        assert status_1 is status_2                                              # Same instance

    def test_name_attribute(self):                                               # Test name attribute
        assert Enum__Hypothesis__Status.SUCCESS.name      == 'SUCCESS'
        assert Enum__Hypothesis__Status.FAILURE.name      == 'FAILURE'
        assert Enum__Hypothesis__Status.INCONCLUSIVE.name == 'INCONCLUSIVE'
        assert Enum__Hypothesis__Status.REGRESSION.name   == 'REGRESSION'
