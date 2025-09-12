import re
import pytest
from unittest                                                                     import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Str                               import TYPE_SAFE__STR__MAX_LENGTH, Safe_Str
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Name import Safe_Str__File__Name
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path import Safe_Str__File__Path


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
        #with pytest.raises(ValueError) as exc_info:
        assert Safe_Str__File__Name(None) == ''
        #assert "in Safe_Str__File__Name, value cannot be None when allow_empty is False" in str(exc_info.value)

        #with pytest.raises(ValueError) as exc_info:
        assert Safe_Str__File__Name('') == ''
        #assert "in Safe_Str__File__Name, value cannot be empty when allow_empty is False" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__File__Name('<?&*^?>')  # All invalid chars
        assert "in Safe_Str__File__Name, sanitized value consists entirely of '_' characters" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:  # spaces only
            Safe_Str__File__Name('  &  ')
        assert "in Safe_Str__File__Name, sanitized value consists entirely of '_' characters" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:  # exceeds max length
            Safe_Str__File__Name('a' * (TYPE_SAFE__STR__MAX_LENGTH + 1))
        assert f"in Safe_Str__File__Name, value exceeds maximum length of {TYPE_SAFE__STR__MAX_LENGTH}" in str(exc_info.value)

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

    def test__str_concat_returns_safe_str_class(self):
        value_1 = Safe_Str__File__Name('aaa')
        value_2 = Safe_Str__File__Name('bbb')
        value_3 = Safe_Str            ('ccc')

        assert type(value_1) is Safe_Str__File__Name
        assert type(value_2) is Safe_Str__File__Name

        assert type(value_1 + 'xyz'  ) is Safe_Str__File__Name           # confirms we keep the Safe_Str__File__Name
        assert type(value_1 + value_2) is Safe_Str__File__Name           # confirms we keep the Safe_Str__File__Name
        assert type(value_1 + value_3) is Safe_Str__File__Name  # confirms we keep the Safe_Str__File__Name


        with pytest.raises(TypeError, match=re.escape('can only concatenate str (not "int") to str')):
            type(value_1 + 123    )                     # OK: since we don't want to prevent non string concats

    def test__safe_str__mixed_types(self):
        # Different Safe_Str subclasses
        file_name = Safe_Str__File__Name('document')
        file_path = Safe_Str__File__Path('/path/to/')

        result = file_path + file_name
        assert type(result) is Safe_Str__File__Path  # Left operand type wins

        # Reverse order
        result = file_name + file_path
        assert type(result) is Safe_Str__File__Name  # Left operand type wins

    def test__safe_str_file_name__string_representation(self):
        # Valid filename
        filename = Safe_Str__File__Name("document.pdf")
        assert str(filename)        == "document.pdf"
        assert f"File: {filename}"  == "File: document.pdf"
        assert repr(filename)       == "Safe_Str__File__Name('document.pdf')"

        # Filename with invalid chars (should be sanitized)
        filename_sanitized = Safe_Str__File__Name("doc/file?.pdf")
        assert "/" not in str(filename_sanitized)  # Path separator removed
        assert "?" not in str(filename_sanitized)  # Invalid char removed