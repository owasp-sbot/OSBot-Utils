import re

import pytest
from unittest                                                                   import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Str                             import Safe_Str
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version import Safe_Str__Version


class test_Safe_Str__Version(TestCase):

    def test_valid_versions(self):
        # Valid version strings
        assert str(Safe_Str__Version("v0.0.1"))     == "v0.0.1"
        assert str(Safe_Str__Version("v1.2.3"))     == "v1.2.3"
        assert str(Safe_Str__Version("v123.456.789")) == "v123.456.789"
        assert str(Safe_Str__Version("v999.999.999")) == "v999.999.999"

        # Trimming whitespace
        assert str(Safe_Str__Version("  v1.2.3  ")) == "v1.2.3"

        # Type conversion
        assert str(Safe_Str__Version(Safe_Str__Version("v2.3.4"))) == "v2.3.4"
        assert str(Safe_Str__Version("v000.001.002")) == "v000.001.002"

    def test_invalid_versions(self):
        expected_error_message = re.escape("in Safe_Str__Version, value does not match required pattern: ^v?\\d{1,3}(?:\\.\\d{1,3}){0,2}$")

        # Exceeds max digits per segment
        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1000")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1.1000")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1.1.1000")

        # Too many segments
        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("1.2.3.4")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1.2.3.4")

        # Malformed formats
        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("1.")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("1..0")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1..3")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("1.0-beta")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("vx.y.z")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("version1.2.3")

        # Empty / None allowed
        assert Safe_Str__Version(None) == ''
        assert Safe_Str__Version("") == ''

        # Exceeds max length
        with pytest.raises(ValueError, match="exceeds maximum length"):
            Safe_Str__Version("v123.456.7890")


    def test__safe_str__version_string_representation(self):
        version = Safe_Str__Version("v3.4.5")
        assert str(version)       == "v3.4.5"
        assert f"Version: {version}" == "Version: v3.4.5"
        assert repr(version)      == "Safe_Str__Version('v3.4.5')"

    def test__concat_behavior(self):
        version = Safe_Str__Version("v1.0.0")

        # Concat loses subclass type
        result = version + "-release"
        assert type(result) is str              # we lose the type safety, or we wouldn't be able to use the version value anywhere
        assert str(result) == "v1.0.0-release"

        result = "version: " + version
        assert type(result) is str              # we lose the type safety,  or we wouldn't be able to use the version value anywhere
        assert str(result) == "version: v1.0.0"

        # Check fallback to str
        generic = Safe_Str("extra")
        result = version + generic
        assert type(result) is str
        assert str(result) == "v1.0.0extra"

        # TypeError on invalid concat
        with pytest.raises(TypeError, match="can only concatenate str"):
            _ = version + 1


    def test_valid_single_segment_versions(self):
        assert str(Safe_Str__Version("1"))   == "1"
        assert str(Safe_Str__Version("2"))   == "2"
        assert str(Safe_Str__Version("999")) == "999"

        assert str(Safe_Str__Version("v1"))   == "v1"
        assert str(Safe_Str__Version("v999")) == "v999"

    def test_valid_two_segment_versions(self):
        assert str(Safe_Str__Version("1.0"))     == "1.0"
        assert str(Safe_Str__Version("10.20"))   == "10.20"
        assert str(Safe_Str__Version("999.999")) == "999.999"

        assert str(Safe_Str__Version("v1.0"))     == "v1.0"
        assert str(Safe_Str__Version("v10.20"))   == "v10.20"
        assert str(Safe_Str__Version("v999.999")) == "v999.999"


    def test_valid_three_segment_versions(self):
        assert str(Safe_Str__Version("1.2.3"))       == "1.2.3"
        assert str(Safe_Str__Version("000.001.002")) == "000.001.002"

        assert str(Safe_Str__Version("v1.2.3"))       == "v1.2.3"
        assert str(Safe_Str__Version("v000.001.002")) == "v000.001.002"

    def test_whitespace_trimming_across_modes(self):
        assert str(Safe_Str__Version("  1  "))     == "1"
        assert str(Safe_Str__Version("  1.0  "))   == "1.0"
        assert str(Safe_Str__Version("  v1.0.0 ")) == "v1.0.0"
