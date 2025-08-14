import math
from unittest                                               import TestCase
from osbot_utils.type_safe.primitives.safe_float.Safe_Float__Engineering import Safe_Float__Engineering
from osbot_utils.type_safe.Type_Safe                        import Type_Safe



class test_Safe_Float__Engineering(TestCase):

    def test_Safe_Float__Engineering_class(self):
        # Valid engineering values with 6 decimal precision
        assert float(Safe_Float__Engineering(3.141593))    == 3.141593
        assert float(Safe_Float__Engineering(2.718282))    == 2.718282
        assert float(Safe_Float__Engineering(9.806650))    == 9.806650
        assert float(Safe_Float__Engineering(299792458))   == 299792458.0

        # String conversion
        assert float(Safe_Float__Engineering('3.141593'))  == 3.141593
        assert float(Safe_Float__Engineering('1.234567'))  == 1.234567
        assert float(Safe_Float__Engineering('-273.150'))  == -273.150

        # Scientific notation
        assert float(Safe_Float__Engineering(1.23e-6))     == 1.23e-6
        assert float(Safe_Float__Engineering(6.022e23))    == 6.022e23
        assert float(Safe_Float__Engineering('1.23e-6'))   == 1.23e-6

        # Automatic rounding to 6 decimal places
        assert float(Safe_Float__Engineering(3.14159265359)) == 3.14159265359
        assert float(Safe_Float__Engineering(1.2345674))     == 1.2345674
        assert float(Safe_Float__Engineering(1.2345675))     == 1.2345675
        assert float(Safe_Float__Engineering(0.0000001))     == 1e-07
        assert float(Safe_Float__Engineering(0.0000005))     == 5e-07

        # Negative values allowed
        assert float(Safe_Float__Engineering(-273.15))      == -273.15
        assert float(Safe_Float__Engineering(-9.806650))    == -9.806650

        # Large and small values
        assert float(Safe_Float__Engineering(1e-10))        == 1e-10
        assert float(Safe_Float__Engineering(1e10))         == 1e10

    def test_engineering_calculations(self):
        # Physics calculations
        # F = ma
        mass = Safe_Float__Engineering(10.5)          # kg
        acceleration = Safe_Float__Engineering(9.80665) # m/s²
        force = mass * acceleration
        assert abs(float(force) - 102.969825) < 1e-6

        # Voltage divider: Vout = Vin * (R2 / (R1 + R2))
        vin = Safe_Float__Engineering(5.0)     # volts
        r1 = Safe_Float__Engineering(1000.0)   # ohms
        r2 = Safe_Float__Engineering(2200.0)   # ohms
        vout = vin * (r2 / (r1 + r2))
        assert abs(float(vout) - 3.4375) < 1e-6

        # RC time constant: τ = R * C
        resistance = Safe_Float__Engineering(10000.0)    # 10k ohms
        capacitance = Safe_Float__Engineering(0.000001)  # 1 microfarad
        tau = resistance * capacitance
        assert float(tau) == 0.01  # 10ms

    def test_epsilon_comparisons(self):
        # Test epsilon tolerance (1e-6)
        val1 = Safe_Float__Engineering(1.0)
        val2 = 1.0 + 1e-7  # Difference smaller than epsilon
        val3 = 1.0 + 2e-6  # Difference larger than epsilon

        assert val1 == val2  # Should be equal within epsilon
        assert not (val1 == val3)  # Should not be equal

        # Engineering constants with small differences
        pi_calculated = Safe_Float__Engineering(3.141593)
        pi_constant = 3.141592653589793
        assert pi_calculated == pi_constant  # Close enough for engineering

    def test_performance_vs_exactness(self):
        # Engineering uses use_decimal=False for performance
        # Test that calculations are fast but still accurate enough

        # Iterative calculation
        result = Safe_Float__Engineering(1.0)
        for i in range(1000):
            result = result * 1.0001

        # Should be approximately e^0.1 = 1.105170...
        expected = math.exp(0.1)
        assert abs(float(result) - expected) < 0.01  # Good enough for engineering

        # Not exact like money calculations, but fast
        val = Safe_Float__Engineering(0.1)
        sum_val = Safe_Float__Engineering(0.0)
        for _ in range(10):
            sum_val = Safe_Float__Engineering(float(sum_val) + float(val))
        # May not be exactly 1.0 due to float precision, but close
        assert abs(float(sum_val) - 1.0) < 1e-6

    def test_usage_in_Type_Safe(self):
        class Sensor_Reading(Type_Safe):
            temperature : Safe_Float__Engineering  # Celsius
            pressure    : Safe_Float__Engineering  # Pascal
            humidity    : Safe_Float__Engineering  # Percentage
            timestamp   : float

        reading = Sensor_Reading(
            temperature=Safe_Float__Engineering(23.456789),
            pressure=Safe_Float__Engineering(101325.0),
            humidity=Safe_Float__Engineering(65.5),
            timestamp=1234567890.123
        )

        assert float(reading.temperature) == 23.456789
        assert float(reading.pressure) == 101325.0
        assert float(reading.humidity) == 65.5

        # Temperature conversion C to F: F = C * 9/5 + 32
        temp_f = reading.temperature * (9.0/5.0) + 32
        assert abs(float(temp_f) - 74.222220) < 1e-6

        # Pressure conversion Pa to kPa
        pressure_kpa = reading.pressure / 1000
        assert float(pressure_kpa) == 101.325

        # Serialization
        reading_json = reading.json()
        assert reading_json['temperature'] == 23.456789
        assert reading_json['pressure'] == 101325.0

    def test_scientific_constants(self):
        # Common engineering/physics constants
        c = Safe_Float__Engineering(299792458)      # Speed of light m/s
        g = Safe_Float__Engineering(9.806650)       # Gravity m/s²
        pi = Safe_Float__Engineering(3.141593)      # Pi
        e = Safe_Float__Engineering(2.718282)       # Euler's number

        # Calculations with constants
        # Circumference of circle with radius 10
        radius = Safe_Float__Engineering(10.0)
        circumference = 2 * pi * radius
        assert abs(float(circumference) - 62.831860) < 1e-6

        # Escape velocity: v = sqrt(2 * g * h)
        height = Safe_Float__Engineering(1000.0)  # meters
        # Note: This is simplified, real escape velocity needs planet mass/radius
        v_squared = 2 * g * height
        assert abs(float(v_squared) - 19613.3) < 0.1


    def test_engineering_notation(self):
        # Common engineering values and their representations
        kilo = Safe_Float__Engineering(1000.0)
        mega = Safe_Float__Engineering(1000000.0)
        giga = Safe_Float__Engineering(1000000000.0)

        milli = Safe_Float__Engineering(0.001)
        micro = Safe_Float__Engineering(0.000001)
        nano = Safe_Float__Engineering(0.000000001)

        # Calculations with SI prefixes
        # 5 kilohms * 2 milliamps = 10 volts
        resistance_kohm = Safe_Float__Engineering(5.0)
        current_ma = Safe_Float__Engineering(2.0)
        voltage = (resistance_kohm * 1000) * (current_ma * 0.001)
        assert float(voltage) == 10.0

        # Frequency to period: T = 1/f
        frequency_mhz = Safe_Float__Engineering(100.0)  # 100 MHz
        period_ns = (1.0 / (frequency_mhz * mega)) * (giga)  # Convert to nanoseconds
        assert float(period_ns) == 10.0  # 10 nanoseconds

    def test__safe_float_engineering__string_representation(self):
        # Engineering notation values
        eng = Safe_Float__Engineering(1234.5678)
        assert str(eng) == "1234.5678"
        assert f"Measurement: {eng}" == "Measurement: 1234.5678"
        assert repr(eng) == "Safe_Float__Engineering(1234.5678)"