import re
import pytest
from typing                                                                 import Optional, List, Dict, ForwardRef, Any
from unittest                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__From_Json  import Type_Safe__Step__From_Json


class test_Type_Safe__Step__From_Json__bugs(TestCase):          # Document bugs with Type_Safe__Step__From_Json

    @classmethod
    def setUpClass(cls):
        cls.step_from_json = Type_Safe__Step__From_Json()

    def test__bug__optional_forward_ref__assignment(self):                              # Assignment bug
        """Bug: Optional forward references fail during assignment"""

        class Person(Type_Safe):
            name   : str
            spouse : Optional['Person']

        person1 = Person(name='Alice')
        person2 = Person(name='Bob')

        # BUG: Assignment should work but doesn't
        error_message = "On Person, invalid type for attribute 'spouse'. Expected 'typing.Optional[ForwardRef('Person')]' but got '<class 'test_Type_Safe__Step__From_Json__bugs.test_Type_Safe__Step__From_Json__bugs.test__bug__optional_forward_ref__assignment.<locals>.Person'>'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            person1.spouse = person2  # This SHOULD work

        # BUG: also fails like this
        with pytest.raises(ValueError, match=re.escape(error_message)):
            person1 = Person(name='Alice', spouse=person2)  # This might work

    def test__known_limitation__forward_ref_to_different_class(self):                   # Not a bug
        """Known limitation: Forward references to other classes cannot be resolved"""

        class ClassB(Type_Safe):
            value: str

        class ClassA(Type_Safe):
            ref: 'ClassB'  # Can't resolve without ClassB in scope

        obj_a = ClassA()
        obj_a.ref = ClassB(value='test')  # Assignment works (ClassB is available)

        json_data = obj_a.json()

        # Known limitation: Can't deserialize forward ref to different class
        # Would need to pass class registry or use eval (security risk)
        with pytest.raises(ValueError):
            ClassA.from_json(json_data)
