import pytest
from unittest                                            import TestCase
from osbot_utils.helpers.safe_str.Safe_Str               import TYPE_SAFE__STR__MAX_LENGTH
from osbot_utils.helpers.safe_str.Safe_Str__File__Name   import Safe_Str__File__Name


class test_Safe_Str__File_Name(TestCase):

    def test_Safe_Str__File_Name_class(self):
        # Valid filename characters
        assert str(Safe_Str__File__Name('example.txt')) == 'example.txt'
        assert str(Safe_Str__File__Name('my-file_1.0.js')) == 'my-file_1.0.js'
        assert str(Safe_Str__File__Name('Photo 2023.jpg')) == 'Photo 2023.jpg'
        assert str(Safe_Str__File__Name('index_v2-final.html')) == 'index_v2-final.html'
        assert str(Safe_Str__File__Name('Document Name.pdf')) == 'Document Name.pdf'
        assert str(Safe_Str__File__Name('data_2023-01-01.csv')) == 'data_2023-01-01.csv'
        assert str(Safe_Str__File__Name('config_v1.0.0.json')) == 'config_v1.0.0.json'

        # Spaces in filenames
        assert str(Safe_Str__File__Name('My Document.docx')) == 'My Document.docx'
        assert str(Safe_Str__File__Name('  My Spaced  File  ')) == 'My Spaced  File'  # Trimmed

        # Numeric values
        assert str(Safe_Str__File__Name(12345)) == '12345'
        assert str(Safe_Str__File__Name('version2.0')) == 'version2.0'

        # Invalid characters get replaced
        assert str(Safe_Str__File__Name('file<1>.txt')) == 'file_1_.txt'
        assert str(Safe_Str__File__Name('document?.pdf')) == 'document_.pdf'
        assert str(Safe_Str__File__Name('script:file.js')) == 'script_file.js'
        assert str(Safe_Str__File__Name('file|name.txt')) == 'file_name.txt'
        assert str(Safe_Str__File__Name('c:\\path\\file.txt')) == 'c__path_file.txt'
        assert str(Safe_Str__File__Name('/usr/bin/file')) == '_usr_bin_file'

        # File extensions
        assert str(Safe_Str__File__Name('.gitignore')) == '.gitignore'
        assert str(Safe_Str__File__Name('archive.tar.gz')) == 'archive.tar.gz'

        # Abuse cases
        assert str(Safe_Str__File__Name('a!@£$b.txt')) == 'a____b.txt'
        assert str(Safe_Str__File__Name('../etc/passwd')) == '.._etc_passwd'
        assert str(Safe_Str__File__Name('<script>alert(1)</script>.js')) == '_script_alert_1___script_.js'
        assert str(Safe_Str__File__Name('file\n\t\r.txt')) == 'file___.txt'

        # Security-sensitive examples
        assert str(Safe_Str__File__Name('..\\Windows\\System32\\cmd.exe')) == '.._Windows_System32_cmd.exe'
        assert str(Safe_Str__File__Name('/etc/passwd')) == '_etc_passwd'
        assert str(Safe_Str__File__Name('`rm -rf /`')) == '_rm -rf __'

        # Edge cases: exceptions with specific error message checks
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__File__Name(None)
        assert "in Safe_Str__File__Name, value cannot be None when allow_empty is False" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__File__Name('')
        assert "Value cannot be empty when allow_empty is False" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__File__Name('<?&*^?>')  # All invalid chars
        assert "Sanitized value consists entirely of '_' characters" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:  # spaces only
            Safe_Str__File__Name('  &  ')
        assert "Sanitized value consists entirely of '_' characters" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:  # exceeds max length
            Safe_Str__File__Name('a' * (TYPE_SAFE__STR__MAX_LENGTH + 1))
        assert f"Value exceeds maximum length of {TYPE_SAFE__STR__MAX_LENGTH}" in str(exc_info.value)

    def test_filename_extensions(self):
        """Tests specific to filename extensions."""
        # Common extensions
        assert str(Safe_Str__File__Name('image.png')) == 'image.png'
        assert str(Safe_Str__File__Name('archive.zip')) == 'archive.zip'
        assert str(Safe_Str__File__Name('document.pdf')) == 'document.pdf'
        assert str(Safe_Str__File__Name('script.py')) == 'script.py'

        # Multiple dots
        assert str(Safe_Str__File__Name('backup.tar.gz')) == 'backup.tar.gz'
        assert str(Safe_Str__File__Name('file.name.with.dots')) == 'file.name.with.dots'

        # Starting with dot (hidden files)
        assert str(Safe_Str__File__Name('.hidden')) == '.hidden'
        assert str(Safe_Str__File__Name('.config')) == '.config'