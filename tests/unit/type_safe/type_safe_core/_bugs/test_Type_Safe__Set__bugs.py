import pytest
import re
from typing                                                                              import Set
from unittest                                                                            import TestCase
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe


class test_Type_Safe__Dict__bugs(TestCase):

    def test__bug__set_enums_assignment(self):
        from enum import Enum

        class Enum__Method(str, Enum):
            GET    = "GET"
            POST   = "POST"
            PUT    = "PUT"
            DELETE = "DELETE"

        class An_Class(Type_Safe):
            http_method      : Enum__Method
            allowed_methods  : Set[Enum__Method]

        # Single enum field works with string
        An_Class(http_method = "GET")                          # this works
        An_Class(http_method = Enum__Method.GET)               # this works

        # Set with enum instances works
        An_Class(allowed_methods = {Enum__Method.GET, Enum__Method.POST})  # this works

        # Set with string values should work but doesn't
        error_message_1 = "In Type_Safe__Set: Invalid type for item: Expected 'Enum__Method', but got 'str'"
        with pytest.raises(TypeError, match=re.escape(error_message_1)):
            An_Class(allowed_methods = {"GET", "POST"})        # BUG: but this doesn't
