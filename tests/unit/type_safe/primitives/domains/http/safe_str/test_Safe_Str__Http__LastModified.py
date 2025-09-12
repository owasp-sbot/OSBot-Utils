import pytest
from unittest                                                                             import TestCase
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Last_Modified import Safe_Str__Http__Last_Modified


class test_Safe_Str__Http__Last_Modified(TestCase):

    def test_Safe_Str__Http__LastModified_class(self):
        # Standard RFC formats
        assert Safe_Str__Http__Last_Modified('Wed, 21 Oct 2023 07:28:00 GMT') == 'Wed, 21 Oct 2023 07:28:00 GMT'
        assert Safe_Str__Http__Last_Modified('Mon, 15 May 2024 12:30:45 GMT') == 'Mon, 15 May 2024 12:30:45 GMT'
        assert Safe_Str__Http__Last_Modified('Sat, 01 Jan 2022 00:00:00 GMT') == 'Sat, 01 Jan 2022 00:00:00 GMT'

        # Different date formats that might be used
        assert Safe_Str__Http__Last_Modified('2023-10-21T07:28:00Z') == '2023-10-21T07:28:00Z'
        assert Safe_Str__Http__Last_Modified('21 Oct 2023 07:28:00 GMT') == '21 Oct 2023 07:28:00 GMT'

        # Whitespace handling (trim_whitespace = True)
        assert Safe_Str__Http__Last_Modified('  Wed, 21 Oct 2023 07:28:00 GMT  ') == 'Wed, 21 Oct 2023 07:28:00 GMT'

        # Invalid characters get replaced
        assert Safe_Str__Http__Last_Modified('Wed, 21 Oct 2023<script>') == 'Wed, 21 Oct 2023_script_'
        assert Safe_Str__Http__Last_Modified('Wed; 21 Oct 2023') == 'Wed_ 21 Oct 2023'
        assert Safe_Str__Http__Last_Modified('Wed, 21/Oct/2023') == 'Wed, 21_Oct_2023'

        assert Safe_Str__Http__Last_Modified('<?&*^?>')  == '_______'
        # allow empty values
        assert Safe_Str__Http__Last_Modified(None)  == ''
        assert Safe_Str__Http__Last_Modified('')    == ''
        assert Safe_Str__Http__Last_Modified('   ') == '' # Spaces only (will be trimmed)

        # Numeric conversion
        assert Safe_Str__Http__Last_Modified(20231021) == '20231021'

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__Last_Modified('a' * 65)  # Exceeds max length
        assert "in Safe_Str__Http__Last_Modified, value exceeds maximum length of 64" in str(exc_info.value)