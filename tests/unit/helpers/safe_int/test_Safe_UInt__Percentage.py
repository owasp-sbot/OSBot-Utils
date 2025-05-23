import pytest
from unittest                                             import TestCase
from osbot_utils.helpers.safe_int.Safe_UInt__Percentage   import Safe_UInt__Percentage, TYPE_SAFE_UINT__PERCENTAGE__MIN_VALUE, TYPE_SAFE_UINT__PERCENTAGE__MAX_VALUE
from osbot_utils.type_safe.Type_Safe                      import Type_Safe


class test_Safe_UInt__Percentage(TestCase):

    def test_Safe_UInt__Percentage_class(self):
        # Valid percentages
        assert int(Safe_UInt__Percentage(0)) == 0
        assert int(Safe_UInt__Percentage(1)) == 1
        assert int(Safe_UInt__Percentage(25)) == 25
        assert int(Safe_UInt__Percentage(50)) == 50
        assert int(Safe_UInt__Percentage(75)) == 75
        assert int(Safe_UInt__Percentage(99)) == 99
        assert int(Safe_UInt__Percentage(100)) == 100

        # String conversion
        assert int(Safe_UInt__Percentage('0')) == 0
        assert int(Safe_UInt__Percentage('50')) == 50
        assert int(Safe_UInt__Percentage('100')) == 100

        assert Safe_UInt__Percentage(None) == 0
        assert Safe_UInt__Percentage() == 0
        assert Safe_UInt__Percentage(0) == 0

        # Out of range - too high
        with pytest.raises(ValueError, match="Safe_UInt__Percentage must be <= 100, got 101"):
            Safe_UInt__Percentage(101)
        with pytest.raises(ValueError, match="Safe_UInt__Percentage must be <= 100, got 150"):
            Safe_UInt__Percentage(150)
        with pytest.raises(ValueError, match="Safe_UInt__Percentage must be <= 100, got 200"):
            Safe_UInt__Percentage(200)

        # Out of range - negative
        with pytest.raises(ValueError, match="Safe_UInt__Percentage must be >= 0, got -1"):
            Safe_UInt__Percentage(-1)
        with pytest.raises(ValueError, match="Safe_UInt__Percentage must be >= 0, got -50"):
            Safe_UInt__Percentage(-50)

        # Invalid types
        with pytest.raises(TypeError, match="Safe_UInt__Percentage requires an integer value, got float"):
            Safe_UInt__Percentage(50.5)
        with pytest.raises(ValueError, match="Cannot convert 'half' to integer"):
            Safe_UInt__Percentage('half')
        with pytest.raises(TypeError, match="Safe_UInt__Percentage does not allow boolean values"):
            Safe_UInt__Percentage(True)


    def test_common_percentage_values(self):
        """Test common percentage values used in practice."""
        # Quarters
        assert int(Safe_UInt__Percentage(0)) == 0    # 0%
        assert int(Safe_UInt__Percentage(25)) == 25   # 1/4
        assert int(Safe_UInt__Percentage(50)) == 50   # 1/2
        assert int(Safe_UInt__Percentage(75)) == 75   # 3/4
        assert int(Safe_UInt__Percentage(100)) == 100  # 100%

        # Thirds (rounded)
        assert int(Safe_UInt__Percentage(33)) == 33   # ~1/3
        assert int(Safe_UInt__Percentage(67)) == 67   # ~2/3

        # Fifths
        assert int(Safe_UInt__Percentage(20)) == 20   # 1/5
        assert int(Safe_UInt__Percentage(40)) == 40   # 2/5
        assert int(Safe_UInt__Percentage(60)) == 60   # 3/5
        assert int(Safe_UInt__Percentage(80)) == 80   # 4/5

        # Tenths
        assert int(Safe_UInt__Percentage(10)) == 10   # 1/10
        assert int(Safe_UInt__Percentage(30)) == 30   # 3/10
        assert int(Safe_UInt__Percentage(70)) == 70   # 7/10
        assert int(Safe_UInt__Percentage(90)) == 90   # 9/10

    def test_usage_in_Type_Safe(self):
        class Progress_Status(Type_Safe):
            download_progress : Safe_UInt__Percentage = Safe_UInt__Percentage(0)
            upload_progress   : Safe_UInt__Percentage = Safe_UInt__Percentage(0)
            cpu_usage        : Safe_UInt__Percentage
            memory_usage     : Safe_UInt__Percentage

        status = Progress_Status(
            cpu_usage=Safe_UInt__Percentage(45),
            memory_usage=Safe_UInt__Percentage(62)
        )

        assert int(status.download_progress) == 0
        assert int(status.upload_progress) == 0
        assert int(status.cpu_usage) == 45
        assert int(status.memory_usage) == 62

        # Update progress
        status.download_progress = Safe_UInt__Percentage(25)
        status.upload_progress = Safe_UInt__Percentage(75)
        assert int(status.download_progress) == 25
        assert int(status.upload_progress) == 75

        # Complete
        status.download_progress = Safe_UInt__Percentage(100)
        assert int(status.download_progress) == 100

        # Invalid percentage
        with pytest.raises(ValueError, match="Safe_UInt__Percentage must be <= 100, got 110"):
            status.cpu_usage = Safe_UInt__Percentage(110)

        # Serialization
        status_json = status.json()
        assert status_json == {
            'download_progress': 100,
            'upload_progress': 75,
            'cpu_usage': 45,
            'memory_usage': 62
        }

        status_restored = Progress_Status.from_json(status_json)
        assert type(status_restored.cpu_usage) is Safe_UInt__Percentage
        assert int(status_restored.download_progress) == 100

    def test_arithmetic_operations(self):
        pct1 = Safe_UInt__Percentage(25)
        pct2 = Safe_UInt__Percentage(30)

        # Addition that stays in range
        result = pct1 + pct2
        assert type(result) is Safe_UInt__Percentage
        assert int(result) == 55

        # Addition that exceeds 100
        pct3 = Safe_UInt__Percentage(60)
        pct4 = Safe_UInt__Percentage(50)
        result = pct3 + pct4  # 110 > 100
        assert type(result) is int  # Falls back to regular int
        assert result == 110

        # Subtraction
        result = pct4 - pct1
        assert type(result) is Safe_UInt__Percentage
        assert int(result) == 25

        # Subtraction that goes negative
        result = pct1 - pct4
        assert type(result) is int  # Falls back to regular int
        assert result == -25

    def test_boundary_values(self):
        # Minimum boundary
        assert int(Safe_UInt__Percentage(TYPE_SAFE_UINT__PERCENTAGE__MIN_VALUE)) == 0

        # Maximum boundary
        assert int(Safe_UInt__Percentage(TYPE_SAFE_UINT__PERCENTAGE__MAX_VALUE)) == 100

        # Just outside boundaries
        with pytest.raises(ValueError):
            Safe_UInt__Percentage(TYPE_SAFE_UINT__PERCENTAGE__MIN_VALUE - 1)
        with pytest.raises(ValueError):
            Safe_UInt__Percentage(TYPE_SAFE_UINT__PERCENTAGE__MAX_VALUE + 1)

    def test_percentage_calculations(self):
        """Test using percentages in calculations."""
        # Calculate percentage of a value
        total = 200
        pct = Safe_UInt__Percentage(25)
        result = (int(pct) / 100) * total
        assert result == 50.0

        # Multiple percentages
        discount1 = Safe_UInt__Percentage(10)
        discount2 = Safe_UInt__Percentage(5)
        # Total discount is not 15% but rather applying them sequentially
        price = 100
        after_discount1 = price * (100 - int(discount1)) / 100
        after_discount2 = after_discount1 * (100 - int(discount2)) / 100
        assert after_discount1 == 90.0
        assert after_discount2 == 85.5