import sys
from unittest import TestCase

import pytest

from osbot_utils.utils.Toml import dict_to_toml, toml_to_dict


class test_Toml(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if sys.version_info < (3, 11):
            pytest.skip("TOML parsing is not supported in Python versions earlier than 3.11")

    def test_dict_to_toml(self):
        data = {
            "title": "TOML Example",
            "owner": {
                "name": "Aaaaa Baaaa",
                "dob": "1111-05-12"
            },
            "database": {
                "server": "192.168.1.1",
                "ports": [8001, 8001, 8002],
                "connection_max": 5000,
                "enabled": True
            }
        }

        expected_output = """title = 'TOML Example'
[owner]
    name = 'Aaaaa Baaaa'
    dob = '1111-05-12'
[database]
    server = '192.168.1.1'
    ports = [
        8001,
        8001,
        8002,
    ]
    connection_max = 5000
    enabled = true
"""

        toml_string = dict_to_toml(data)

        assert toml_string == expected_output
        assert data        == toml_to_dict(toml_string)

    def test_toml_to_dict(self):
        toml_string = """title = 'TOML Example'
[owner]
    name = 'Aaaaa Baaaa'
    dob = '1111-05-12'
[database]
    server = '192.168.1.1'
    ports = [
        8001,
        8001,
        8002,
    ]
    connection_max = 5000
    enabled = true
"""

        expected_dict = {
            "title": "TOML Example",
            "owner": {
                "name": "Aaaaa Baaaa",
                "dob": "1111-05-12"
            },
            "database": {
                "server": "192.168.1.1",
                "ports": [8001, 8001, 8002],
                "connection_max": 5000,
                "enabled": True
            }
        }

        result_dict = toml_to_dict(toml_string)

        assert result_dict == expected_dict, f"Expected:\n{expected_dict}\n\nGot:\n{result_dict}"
        assert toml_string == dict_to_toml(result_dict)