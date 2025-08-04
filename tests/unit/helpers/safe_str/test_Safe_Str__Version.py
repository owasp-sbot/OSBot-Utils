import re

import pytest
from unittest                                      import TestCase
from osbot_utils.helpers.safe_str.Safe_Str__Version import Safe_Str__Version
from osbot_utils.helpers.safe_str.Safe_Str          import Safe_Str


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
        expected_error_message = re.escape("Value does not match required pattern: ^v(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})$")
        # Exceeds max digits
        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1000.1.1")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1.1000.1")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1.1.1000")

        # Incorrect format
        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("1.2.3")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1.2")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1.2.3.4")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1.2.alpha")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("vx.y.z")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("version1.2.3")

        with pytest.raises(ValueError, match=expected_error_message):
            Safe_Str__Version("v1..3")

        # Empty or None
        with pytest.raises(ValueError, match="in Safe_Str__Version, value cannot be None when allow_empty is False"):
            Safe_Str__Version(None)

        with pytest.raises(ValueError, match="Value cannot be empty when allow_empty is False"):
            Safe_Str__Version("")

        # Exceeds max length
        with pytest.raises(ValueError, match="exceeds maximum length"):
            Safe_Str__Version("v123.456.7890")  # 12 characters, too long

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
