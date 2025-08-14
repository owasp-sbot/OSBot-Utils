import pytest
from unittest                        import TestCase
from osbot_utils.type_safe.primitives.safe_str.identifiers.Random_Guid import Random_Guid
from osbot_utils.utils.Str           import trim, safe_id


class test_Str(TestCase):

    def test_safe_id(self):
        # Valid cases
        assert safe_id('aaaabbb'    ) == 'aaaabbb'
        assert safe_id('aaa_bbb'    ) == 'aaa_bbb'
        assert safe_id('aaa-bbb'    ) == 'aaa-bbb'
        assert safe_id('aaa bbb'    ) == 'aaa_bbb'
        assert safe_id('aa   bb'    ) == 'aa___bb'
        assert safe_id("aa ' bb"    ) == 'aa___bb'
        assert safe_id('AAA123_bbb' ) == 'AAA123_bbb'
        assert safe_id('Abb-123'    ) == 'Abb-123'
        assert safe_id('A-b-1-3'    ) == 'A-b-1-3'
        assert safe_id('Abc-'       ) == 'Abc-'
        assert safe_id('123start'   ) == '123start'
        assert safe_id('123'        ) == '123'
        assert safe_id(123          ) == '123'
        assert safe_id('a'*36       ) == 'a'*36

        #check random guid
        guid_1 = Random_Guid()
        guid_2 = '13373889-3b23-4ba9-b5f7-fd1b7d2abd94'
        guid_3 = 'c13110ca-8c20-4ead-afe6-81b8eedcfc00'
        assert safe_id(guid_1) == guid_1
        assert safe_id(guid_2) == guid_2
        assert safe_id(guid_3) == guid_3

        # Abuse cases
        assert safe_id('a!@£$b'     ) == 'a____b'
        assert safe_id('aaa/../'    ) == 'aaa____'
        assert safe_id('a\n\t\r'    ) == 'a___'

        # Edge cases: exceptions with specific error message checks
        with pytest.raises(ValueError) as exc_info:
            safe_id(None)
        assert str(exc_info.value) == "Invalid ID: The ID must not be empty."

        with pytest.raises(ValueError) as exc_info:
            safe_id('')
        assert str(exc_info.value) == "Invalid ID: The ID must not be empty."

        with pytest.raises(ValueError) as exc_info:
            safe_id('!@#$%^&*()')
        assert str(exc_info.value) == "Invalid ID: The sanitized ID must not consist entirely of underscores."

        with pytest.raises(ValueError) as exc_info:         # spaces only
            safe_id('    ')
        assert str(exc_info.value) == "Invalid ID: The sanitized ID must not consist entirely of underscores."

        with pytest.raises(ValueError) as exc_info:         # underscores only
            safe_id('______')
        assert str(exc_info.value) == "Invalid ID: The sanitized ID must not consist entirely of underscores."

        with pytest.raises(ValueError) as exc_info:         # bigger than 36
            safe_id('a'*37)
        assert str(exc_info.value) == 'Invalid ID: The ID must not exceed 36 characters (was 37).'


    def test_trim(self):
        assert trim('  aaa  ') == 'aaa'
        assert trim('\naaa\n') == 'aaa'
        assert trim(''       ) == ''
        assert trim('       ') == ''
        assert trim(' \t \n ') == ''
        assert trim(None     ) == ''
        assert trim({}       ) == ''
