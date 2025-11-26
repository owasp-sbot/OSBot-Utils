import re
import pytest
from typing                                                                         import Dict, List, Any
from unittest                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Hash  import Safe_Str__Hash
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict


class test_Type_Safe__Dict__bugs(TestCase):


    def test__bug__type_safe_list_with_dict_any_type__and__error_message_is_confusing(self):   # Document bug where Dict[str, any] fails in List ,and the error message doesn't mention that Any works

        class Schema__Order__Bug(Type_Safe):
            items: List[Dict[str, any]]                                                    # BUG: lowercase 'any' is a function, not a type

        class Schema__Order__Fixed(Type_Safe):
            items: List[Dict[str, Any]]                                                    # FIXED: uppercase 'Any' from typing

        # Document the bug - lowercase 'any' causes TypeError
        with Schema__Order__Bug() as buggy_order:
            error_message = "In Type_Safe__List: Invalid type for item: In dict value for key 'product': isinstance() arg 2 must be a type, a tuple of types, or a union"
            with pytest.raises(TypeError, match=re.escape(error_message)):
                buggy_order.items = [{'product': 'laptop', 'qty': 1}]                     # BUG: fails with isinstance error

        # Document what SHOULD work (using Any from typing)
        with Schema__Order__Fixed() as fixed_order:
            fixed_order.items = [{'product': 'laptop', 'qty': 1, 'price': 999.99}]       # Works with Any
            assert fixed_order.items == [{'product': 'laptop', 'qty': 1, 'price': 999.99}]

        # Alternative that also works - using dict without type params
        class Schema__Order__Alternative(Type_Safe):
            items: List[dict]                                                             # Plain dict also works

        with Schema__Order__Alternative() as alt_order:
            alt_order.items = [{'product': 'laptop', 'qty': 1}]                          # Works
            assert alt_order.items == [{'product': 'laptop', 'qty': 1}]

    def test__bug__list_of_dict_subclasses_from_plain_dicts(self):
        from typing import List

        class Hash_Mapping(Type_Safe__Dict):
            expected_key_type = Safe_Str__Hash
            expected_value_type = str

        class Container(Type_Safe):
            mappings: List[Hash_Mapping]

        error_message = "Invalid type for item: Expected 'Hash_Mapping', but got 'dict'"
        with pytest.raises(TypeError, match=re.escape(error_message)):
            container = Container(mappings=[{'abc1234567': 'first'},
                                            {'def4567890': 'second'}])                      # BUG: Lists are currently not supported
