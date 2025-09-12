import pytest
from unittest                                                                                   import TestCase
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.numerical.safe_float.Safe_Float__Percentage_Exact import Safe_Float__Percentage_Exact


class test_Safe_Float__Percentage_Exact(TestCase):

    def test_Safe_Float__Percentage_Exact_class(self):
        # Valid percentages
        assert float(Safe_Float__Percentage_Exact(0.0))   == 0.0
        assert float(Safe_Float__Percentage_Exact(0.01))  == 0.01
        assert float(Safe_Float__Percentage_Exact(25.0))  == 25.0
        assert float(Safe_Float__Percentage_Exact(50.0))  == 50.0
        assert float(Safe_Float__Percentage_Exact(75.5))  == 75.5
        assert float(Safe_Float__Percentage_Exact(99.99)) == 99.99
        assert float(Safe_Float__Percentage_Exact(100.0)) == 100.0

        # String conversion with decimal precision
        assert float(Safe_Float__Percentage_Exact('33.33')) == 33.33
        assert float(Safe_Float__Percentage_Exact('66.67')) == 66.67
        assert float(Safe_Float__Percentage_Exact('0.01'))  == 0.01

        # Integer conversion
        assert float(Safe_Float__Percentage_Exact(0))   == 0.0
        assert float(Safe_Float__Percentage_Exact(50))  == 50.0
        assert float(Safe_Float__Percentage_Exact(100)) == 100.0

        # Automatic rounding to 2 decimal places
        assert float(Safe_Float__Percentage_Exact(33.333))  == 33.33
        assert float(Safe_Float__Percentage_Exact(66.666))  == 66.67
        assert float(Safe_Float__Percentage_Exact(99.999))  == 100.00
        assert float(Safe_Float__Percentage_Exact(0.001))   == 0.00
        assert float(Safe_Float__Percentage_Exact(0.005))   == 0.01

        # Out of range
        with pytest.raises(ValueError, match="Safe_Float__Percentage_Exact must be >= 0.0, got -0.01"):
            Safe_Float__Percentage_Exact(-0.01)
        with pytest.raises(ValueError, match="Safe_Float__Percentage_Exact must be <= 100.0, got 100.01"):
            Safe_Float__Percentage_Exact(100.01)
        with pytest.raises(ValueError, match="Safe_Float__Percentage_Exact must be <= 100.0, got 150.0"):
            Safe_Float__Percentage_Exact(150.0)

    def test_exact_percentage_arithmetic(self):
        # Test exact decimal arithmetic for percentages

        # Adding percentages
        pct1 = Safe_Float__Percentage_Exact(33.33)
        pct2 = Safe_Float__Percentage_Exact(33.33)
        pct3 = Safe_Float__Percentage_Exact(33.34)
        total = Safe_Float__Percentage_Exact(float(pct1) + float(pct2) + float(pct3))
        assert float(total) == 100.00  # Exactly 100%

        # Percentage of a percentage
        base = Safe_Float__Percentage_Exact(50.0)
        reduction = Safe_Float__Percentage_Exact(10.0)  # 10% of 50%
        result = base * (reduction / 100)
        assert float(result) == 5.00

        # Dividing percentages equally
        total_pct = Safe_Float__Percentage_Exact(100.0)
        thirds = total_pct / 3
        assert float(thirds) == 33.33

    def test_percentage_calculations(self):
        # Test score calculation
        score = 85
        total = 100
        percentage = Safe_Float__Percentage_Exact((score / total) * 100)
        assert float(percentage) == 85.00

        # Growth rate calculation
        old_value = 100
        new_value = 125
        growth = Safe_Float__Percentage_Exact(((new_value - old_value) / old_value) * 100)
        assert float(growth) == 25.00

        # Discount stacking
        original_discount = Safe_Float__Percentage_Exact(20.0)
        additional_discount = Safe_Float__Percentage_Exact(10.0)

        # Not 30% total, but 20% then 10% of remaining
        remaining_after_first = 100 - float(original_discount)  # 80%
        second_discount_amount = remaining_after_first * (float(additional_discount) / 100)  # 8%
        total_discount = Safe_Float__Percentage_Exact(float(original_discount) + second_discount_amount)
        assert float(total_discount) == 28.00

    def test_common_percentage_scenarios(self):
        # Grade boundaries
        grades = {
            'A+': Safe_Float__Percentage_Exact(97.0),
            'A':  Safe_Float__Percentage_Exact(93.0),
            'A-': Safe_Float__Percentage_Exact(90.0),
            'B+': Safe_Float__Percentage_Exact(87.0),
            'B':  Safe_Float__Percentage_Exact(83.0),
            'B-': Safe_Float__Percentage_Exact(80.0),
        }

        student_score = Safe_Float__Percentage_Exact(85.5)
        assert float(grades['B+']) > float(student_score) >= float(grades['B'])

        # Progress tracking
        completed = 237
        total = 300
        progress = Safe_Float__Percentage_Exact((completed / total) * 100)
        assert float(progress) == 79.00

        # Battery level
        battery_reading = 0.856  # Raw value
        battery_percent = Safe_Float__Percentage_Exact(battery_reading * 100)
        assert float(battery_percent) == 85.60

    def test_usage_in_Type_Safe(self):
        class Performance_Metrics(Type_Safe):
            cpu_usage    : Safe_Float__Percentage_Exact
            memory_usage : Safe_Float__Percentage_Exact
            disk_usage   : Safe_Float__Percentage_Exact = Safe_Float__Percentage_Exact(0.0)
            gpu_usage    : Safe_Float__Percentage_Exact = Safe_Float__Percentage_Exact(0.0)

        metrics = Performance_Metrics(
            cpu_usage=Safe_Float__Percentage_Exact(45.25),
            memory_usage=Safe_Float__Percentage_Exact(62.80)
        )

        assert float(metrics.cpu_usage) == 45.25
        assert float(metrics.memory_usage) == 62.80
        assert float(metrics.disk_usage) == 0.00

        # Update metrics
        metrics.disk_usage = Safe_Float__Percentage_Exact(78.50)
        metrics.gpu_usage = Safe_Float__Percentage_Exact(92.15)

        # Check if any metric is critical (>90%)
        critical_threshold = 90.0
        is_gpu_critical = float(metrics.gpu_usage) > critical_threshold
        assert is_gpu_critical == True

        # Average usage
        total = (float(metrics.cpu_usage) +
                float(metrics.memory_usage) +
                float(metrics.disk_usage) +
                float(metrics.gpu_usage))
        average = Safe_Float__Percentage_Exact(total / 4)
        assert float(average) == 69.68

        # Serialization
        metrics_json = metrics.json()
        assert metrics_json == {
            'cpu_usage': 45.25,
            'memory_usage': 62.80,
            'disk_usage': 78.50,
            'gpu_usage': 92.15
        }

    def test_percentage_edge_cases(self):
        # Very small percentages
        tiny = Safe_Float__Percentage_Exact(0.01)
        assert float(tiny) == 0.01

        # Rounding at boundaries
        assert float(Safe_Float__Percentage_Exact(99.994)) == 99.99
        assert float(Safe_Float__Percentage_Exact(99.995)) == 100.00
        assert float(Safe_Float__Percentage_Exact(99.999)) == 100.00

        # Ensure 100% is valid
        full = Safe_Float__Percentage_Exact(100.0)
        assert float(full) == 100.00

        # # Just over 100% is invalid
        with pytest.raises(ValueError):
            Safe_Float__Percentage_Exact(100.004)  # Would round to 100.00 but checked before rounding
        # print()
        # assert Safe_Float__Percentage_Exact(100.004) == 100.0

        with pytest.raises(ValueError):
            assert Safe_Float__Percentage_Exact(101.004) == 100.0

    def test__safe_float__percentage_constraints(self):
        # Percentage (0-100)
        percent1 = Safe_Float__Percentage_Exact(50.0)
        percent2 = Safe_Float__Percentage_Exact(30.0)

        result = percent1 + percent2
        assert type(result) is Safe_Float__Percentage_Exact
        assert result == 80.0

        # Should fall back when exceeding 100
        percent3 = Safe_Float__Percentage_Exact(90.0)
        result = percent3 + 20.0  # Would be 110
        assert type(result) is float  # Falls back to float
        assert result == 110.0

    def test__safe_float_percentage__string_representation(self):
        # Percentage values
        percent = Safe_Float__Percentage_Exact(75.50)
        assert str(percent) == "75.50"
        assert f"{percent}%" == "75.50%"
        assert repr(percent) == "Safe_Float__Percentage_Exact(75.50)"

        # Whole number percentage
        whole = Safe_Float__Percentage_Exact(100.0)
        assert str(whole) == "100.00"
        assert f"Complete: {whole}%" == "Complete: 100.00%"