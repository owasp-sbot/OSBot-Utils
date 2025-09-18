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

    def test__bug__optional_forward_ref(self):                                       # Optional self-reference
        """Bug: Optional forward references also fail"""

        class Person(Type_Safe):
            name   : str
            spouse : Optional['Person']
            parent : Optional['Person']


        person1 = Person(name='Alice')
        person2 = Person(name='Bob')

        error_message_1 = "On Person, invalid type for attribute 'spouse'. Expected 'typing.Optional[ForwardRef('Person')]' but got '<class 'test_Type_Safe__Step__From_Json__bugs.test_Type_Safe__Step__From_Json__bugs.test__bug__optional_forward_ref.<locals>.Person'>'"
        with pytest.raises(ValueError, match=re.escape(error_message_1)):
            person1.spouse = person2
        error_message_1 = "On Person, invalid type for attribute 'spouse'. Expected 'typing.Optional[ForwardRef('Person')]' but got '<class 'test_Type_Safe__Step__From_Json__bugs.test_Type_Safe__Step__From_Json__bugs.test__bug__optional_forward_ref.<locals>.Person'>'"
        with pytest.raises(ValueError, match=re.escape(error_message_1)):
            person2.spouse = person1  # Circular reference

        json_data = person1.json()

        # Even Optional forward refs fail
        #error_message_2 = "On Person, invalid type for attribute 'spouse'. Expected 'typing.Union[Person, NoneType]' but got '<class 'dict'>'"
        #with pytest.raises(ValueError, match=re.escape(error_message_2)):
        #   Person.from_json(json_data)                                         # BUG

        assert Person.from_json(json_data).obj () == person1.obj()
        assert Person.from_json(json_data).json() == json_data


    def test__bug__forward_ref_to_different_class(self):                            # Forward ref to other class
        """Bug: Forward references to other Type_Safe classes also fail"""

        # This is a different issue - forward refs to OTHER classes
        # Python doesn't resolve these at runtime without eval

        class ClassB(Type_Safe):
            value: str

        class ClassA(Type_Safe):
            ref: 'ClassB'  # Forward ref to different class

        obj_a = ClassA()
        obj_a.ref = ClassB(value='test')

        json_data = obj_a.json()

        # This also fails but for different reasons - can't resolve 'ClassB' string
        with pytest.raises(ValueError):
            ClassA.from_json(json_data)                                             # todo: isn't this a know limitation? (since with the current implementation we can't use ForwardRefs from different classes

    def test__bug__dict_with_forward_ref_values(self):                              # Dict values with forward refs
        """Bug: Dict values that are forward refs also fail"""

        class Registry(Type_Safe):
            name  : str
            items : Dict[str, 'Registry']

        reg = Registry(name='root')
        reg.items['child'] = Registry(name='child')

        json_data = reg.json()

        # Dict values with forward refs also have issues
        #error_message_1 = "'ForwardRef' object is not callable"
        error_message_2 = "isinstance() arg 2 must be a type, a tuple of types, or a union"
        with pytest.raises(TypeError, match=re.escape(error_message_2)):
            restored = Registry.from_json(json_data)

        # Check if Dict properly handles the forward ref in values
        # if type(restored.items['child']) is not Registry:
        #     assert False, "Dict didn't properly deserialize forward ref values"
