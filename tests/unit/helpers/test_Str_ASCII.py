from unittest                      import TestCase
from osbot_utils.helpers.Str_ASCII import Str_ASCII


class test_Str_ASCII(TestCase):

    def test_basic_values(self):
        test_cases = [("hello-world"        , "hello-world"      ),
                      ("hello™world"        , "hello_world"      ),
                      ("hello世界"           , "hello__"          ),
                      ("hello@world.com"    , "hello@world.com"  ),
                      ("multiple___spaces"  , "multiple___spaces"),
                      ("_trim_edges_"       , "_trim_edges_"     ),
                      (123                  , "123"              ),
                      (3.14                 , "3.14"             )]
        for input_value, expected in test_cases:
            result = Str_ASCII(input_value)
            assert result == expected

    def test_max_length(self):
        # Valid length
        assert Str_ASCII("test", max_length=10) == "test"
        
        # Invalid length
        with self.assertRaises(ValueError) as context:
            Str_ASCII("too_long_string", max_length=5)
        assert "Value length exceeds maximum" in str(context.exception)

    def test_handle_invalid_inputs(self):
        invalid_cases = [None,                    # None value
                         "",                      # Empty string
                         "™™™",                   # Only special chars
                         "_____"                 # Only underscores
        ]
        for invalid_input in invalid_cases:
            Str_ASCII(invalid_input)

    def test_preserves_allowed_chars(self):
        special_chars = "!@#$%^&*()[]{}-+=:;,.?"
        result = Str_ASCII(f"test{special_chars}123")
        assert result == f"test{special_chars}123"

    def test_replaces_invalid_chars(self):
        invalid_chars = "™£€¥©®℗"
        result = Str_ASCII(f"test{invalid_chars}123")
        assert result == "test_______123"