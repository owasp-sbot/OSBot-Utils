import pytest
from unittest                           import TestCase
from osbot_utils.helpers.Random_Guid    import Random_Guid
from osbot_utils.helpers.Safe_Id        import Safe_Id, SAFE_ID__MAX_LENGTH


class test_Safe_Id(TestCase):
    
    def test_Safe_Id_class(self):
        # Valid cases
        assert str(Safe_Id('aaaabbb'    )) == 'aaaabbb'
        assert str(Safe_Id('aaa_bbb'    )) == 'aaa_bbb'
        assert str(Safe_Id('aaa-bbb'    )) == 'aaa-bbb'
        assert str(Safe_Id('aaa bbb'    )) == 'aaa_bbb'
        assert str(Safe_Id('aa   bb'    )) == 'aa___bb'
        assert str(Safe_Id("aa ' bb"    )) == 'aa___bb'
        assert str(Safe_Id('AAA123_bbb' )) == 'AAA123_bbb'
        assert str(Safe_Id('Abb-123'    )) == 'Abb-123'
        assert str(Safe_Id('A-b-1-3'    )) == 'A-b-1-3'
        assert str(Safe_Id('Abc-'       )) == 'Abc-'
        assert str(Safe_Id('123start'   )) == '123start'
        assert str(Safe_Id('123'        )) == '123'
        assert str(Safe_Id(123          )) == '123'
        assert str(Safe_Id('a'*36       )) == 'a'*36

        # Check random GUIDs
        guid_1 = Random_Guid()
        guid_2 = '13373889-3b23-4ba9-b5f7-fd1b7d2abd94'
        guid_3 = 'c13110ca-8c20-4ead-afe6-81b8eedcfc00'
        assert Safe_Id(guid_1)                 != guid_1                    # should not be equal sice types are the different
        assert type(str(Safe_Id(guid_1)))      is str                       # confirm we get a str if we explicity convert into str
        assert type(Safe_Id(guid_1).__str__()) is str
        assert str(Safe_Id(guid_1)) == str(guid_1)
        assert str(Safe_Id(guid_2)) == str(guid_2)
        assert str(Safe_Id(guid_3)) == str(guid_3)

        # Abuse cases
        assert str(Safe_Id('a!@£$b'     )) == 'a____b'
        assert str(Safe_Id('aaa/../'    )) == 'aaa____'
        assert str(Safe_Id('a\n\t\r'    )) == 'a___'

        assert Safe_Id(None).startswith('safe-id_')                         # if it received a None value it should create a default random value

        # Edge cases: exceptions with specific error message checks
        with pytest.raises(ValueError) as exc_info:
            Safe_Id('')
        assert str(exc_info.value) == "Invalid ID: The ID must not be empty."

        with pytest.raises(ValueError) as exc_info:
            Safe_Id('!@#$%^&*()')
        assert str(exc_info.value) == "Invalid ID: The sanitized ID must not consist entirely of underscores."

        with pytest.raises(ValueError) as exc_info:         # spaces only
            Safe_Id('    ')
        assert str(exc_info.value) == "Invalid ID: The sanitized ID must not consist entirely of underscores."

        with pytest.raises(ValueError) as exc_info:         # underscores only
            Safe_Id('______')
        assert str(exc_info.value) == "Invalid ID: The sanitized ID must not consist entirely of underscores."

        with pytest.raises(ValueError) as exc_info:         # bigger than 36
            Safe_Id('a'* (SAFE_ID__MAX_LENGTH+1))
        assert str(exc_info.value) == f"Invalid ID: The ID must not exceed {SAFE_ID__MAX_LENGTH} characters (was {SAFE_ID__MAX_LENGTH+1})."
