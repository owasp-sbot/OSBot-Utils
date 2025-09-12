import pytest
from unittest                                                                           import TestCase
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Code__Snippet   import Safe_Str__Code__Snippet
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Email              import Safe_Str__Email
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Password           import Safe_Str__Password
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Username           import Safe_Str__Username

# todo: refactor these to their own test files and add more edge cases
class test_Safe_Str___mix_web_classes(TestCase):

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

    def test_Safe_Str__Code__Snippet(self):
        # Valid code snippets
        code1 = 'function test() { return true; }'
        assert str(Safe_Str__Code__Snippet(code1)) == code1

        code2 = 'x = 1; y = 2; print(x + y)'
        assert str(Safe_Str__Code__Snippet(code2)) == code2

        code3 = 'if (value > 0) { return "positive"; }'
        assert str(Safe_Str__Code__Snippet(code3)) == code3

        # With indentation (preserved since trim_whitespace=False)
        code4 = '    def example():\n        return True'
        assert str(Safe_Str__Code__Snippet(code4)) == '    def example():\n        return True'

        # Invalid characters get replaced
        assert str(Safe_Str__Code__Snippet('function test<T>() {}')) == 'function test<T>() {}'
        assert str(Safe_Str__Code__Snippet('console.log(`Hello`);')) == 'console.log(`Hello`);'

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