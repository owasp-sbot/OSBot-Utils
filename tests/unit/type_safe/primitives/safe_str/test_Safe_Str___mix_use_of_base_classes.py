import pytest
import re
from unittest                              import TestCase
from osbot_utils.type_safe.primitives.safe_str.Safe_Str import Safe_Str


# Create custom Safe_Str classes for testing
class Safe_Str__Username(Safe_Str):
    """Allows only alphanumerics and underscores, with a 32 character limit."""
    regex = re.compile(r'[^a-zA-Z0-9_]')
    max_length = 32


class Safe_Str__Email(Safe_Str):
    """Special class for emails with custom validation."""
    regex = re.compile(r'[^a-zA-Z0-9_\-.@]')
    max_length = 256

    def __new__(cls, value=None):
        result = super().__new__(cls, value)
        # Additional validation for email format
        if '@' not in result:
            raise ValueError(f"in {cls.__name__}, email must contain an @ symbol")
        return result


class Safe_Str__Code(Safe_Str):
    """Allows various characters needed for code snippets."""
    regex = re.compile(r'[^a-zA-Z0-9_\-.\s(),;:=+\[\]{}\'"]<>')
    max_length = 1024
    trim_whitespace = False  # Preserve leading whitespace for code indentation


class Safe_Str__Password(Safe_Str):
    """Password with minimum requirements."""
    regex = re.compile(r'[^a-zA-Z0-9_\-.\s!@#$%^&*()]')
    min_length = 8  # Custom attribute

    def __new__(cls, value=None):
        result = super().__new__(cls, value)
        if len(result) < cls.min_length:
            raise ValueError(f"Password must be at least {cls.min_length} characters long")
        return result


class test_Safe_Str___mix_use_of_base_classes(TestCase):

    def test_Safe_Str__Username(self):
        # Valid usernames
        assert str(Safe_Str__Username('john_doe')) == 'john_doe'
        assert str(Safe_Str__Username('admin123')) == 'admin123'
        assert str(Safe_Str__Username('_system_')) == '_system_'

        # Invalid characters get replaced
        assert str(Safe_Str__Username('john.doe')) == 'john_doe'
        assert str(Safe_Str__Username('user-name')) == 'user_name'
        assert str(Safe_Str__Username('email@domain.com')) == 'email_domain_com'

        # Length limitation
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Username('a' * 33)  # Exceeds custom max length
        assert "in Safe_Str__Username, value exceeds maximum length of 32" in str(exc_info.value)

    def test_Safe_Str__Email(self):
        # Valid emails
        assert str(Safe_Str__Email('user@example.com')) == 'user@example.com'
        assert str(Safe_Str__Email('john.doe@gmail.com')) == 'john.doe@gmail.com'
        assert str(Safe_Str__Email('support@company-name.co.uk')) == 'support@company-name.co.uk'

        # Invalid characters get replaced
        assert str(Safe_Str__Email('user name@example.com')) == 'user_name@example.com'
        assert str(Safe_Str__Email('admin#@example.com')) == 'admin_@example.com'

        # Missing @ symbol
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Email('invalid-email')
        assert "in Safe_Str__Email, email must contain an @ symbol" in str(exc_info.value)

    def test_Safe_Str__Code(self):
        # Valid code snippets
        code1 = 'function test() { return true; }'
        assert str(Safe_Str__Code(code1)) == code1

        code2 = 'x = 1; y = 2; print(x + y)'
        assert str(Safe_Str__Code(code2)) == code2

        code3 = 'if (value > 0) { return "positive"; }'
        assert str(Safe_Str__Code(code3)) == code3

        # With indentation (preserved since trim_whitespace=False)
        code4 = '    def example():\n        return True'
        assert str(Safe_Str__Code(code4)) == '    def example():\n        return True'

        # Invalid characters get replaced
        assert str(Safe_Str__Code('function test<T>() {}')) == 'function test<T>() {}'
        assert str(Safe_Str__Code('console.log(`Hello`);')) == 'console.log(`Hello`);'

    def test_Safe_Str__Password(self):
        # Valid passwords
        assert str(Safe_Str__Password('Password123!'            )) == 'Password123!'
        assert str(Safe_Str__Password('Secure_P@ssw0rd'         )) == 'Secure_P@ssw0rd'  # @ is replaced
        assert str(Safe_Str__Password('very-long-password-123'  )) == 'very-long-password-123'

        # Invalid characters get replaced
        assert str(Safe_Str__Password('Pass<>word')) == 'Pass__word'

        # Too short
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Password('Short1')  # Only 6 chars
        assert "Password must be at least 8 characters long" in str(exc_info.value)