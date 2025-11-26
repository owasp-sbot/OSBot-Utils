import re
import pytest
from typing                                                                              import List
from unittest                                                                            import TestCase
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash import Safe_Str__Cache_Hash
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                    import Type_Safe__List


class test_Type_Safe__List__bugs(TestCase):

    def test__bug__type_safe_list_with_callable(self):
        from typing import Callable

        class An_Class(Type_Safe):
            an_list__callable: List[Callable[[int], str]]

        an_class = An_Class()

        def invalid_func(x: str) -> int:                    # Invalid callable (wrong signature)
            return len(x)

        an_class.an_list__callable.append(invalid_func)     # BUG doesn't raise  (i.e. at the moment we are not detecting the callable signature and return type)
