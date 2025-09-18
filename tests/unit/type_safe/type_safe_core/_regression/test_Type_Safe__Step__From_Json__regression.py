import re
import pytest
from typing                                                                 import Optional, List, Dict, ForwardRef, Any
from unittest                                                               import TestCase
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id import Safe_Id
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__From_Json  import Type_Safe__Step__From_Json


class test_Type_Safe__Step__From_Json__bugs(TestCase):          # Document bugs with Type_Safe__Step__From_Json

    @classmethod
    def setUpClass(cls):
        cls.step_from_json = Type_Safe__Step__From_Json()

    def test__regression__forward_ref_to_same_class(self):                                  # Basic self-reference bug
        """Bug: Forward reference to same class doesn't deserialize from dict"""

        class Tree_Node(Type_Safe):
            value : str
            left  : 'Tree_Node'
            right : 'Tree_Node'

        # Create a simple tree
        root       = Tree_Node(value='root')
        root.left  = Tree_Node(value='left')
        root.right = Tree_Node(value='right')

        json_data = root.json()

        # WHAT SHOULD HAPPEN (but currently doesn't):   # FIXED
        restored = Tree_Node.from_json(json_data)
        assert type(restored.left)  is Tree_Node
        assert restored.left.value  == 'left'
        assert restored.json()      == json_data

        # WHAT ACTUALLY HAPPENS (the bug):              # BUG
        # error_message = "On Tree_Node, invalid type for attribute 'left'. Expected 'Tree_Node' but got '<class 'dict'>'"
        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     Tree_Node.from_json(json_data)

    def test__regression__nested_self_references(self):                                     # Deep nesting with self-refs
        """Bug: Deeply nested self-references fail"""

        class Linked_Node(Type_Safe):
            data : int
            next : 'Linked_Node'

        # Create a linked list
        node1 = Linked_Node(data=1)
        node2 = Linked_Node(data=2)
        node3 = Linked_Node(data=3)
        node1.next = node2
        node2.next = node3

        json_data = node1.json()

        # The deserialization fails at the first level
        # error_message = "On Linked_Node, invalid type for attribute 'next'. Expected 'Linked_Node' but got '<class 'dict'>'"
        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     Linked_Node.from_json(json_data)                          # BUG
        assert Linked_Node.from_json(json_data).json() == json_data     # FIXED

    def test__regression__forward_ref__circular(self):                                       # Optional self-reference
        """Bug: Optional forward references also fail"""

        class Person(Type_Safe):
            name   : str
            spouse : 'Person'
            parent : 'Person'


        person1 = Person(name='Alice')
        person2 = Person(name='Bob'  )
        person3 = Person(name='Eve'  )

        error_message = 'maximum recursion depth exceeded'
        person1.spouse = person2
        person2.spouse = person1  # Circular reference
        with pytest.raises(RecursionError, match=re.escape(error_message)):
            json_data = person1.json()                                                  # todo: check if this is indeed a bug with Type_Safe

        person2.spouse = person3
        json_data = person1.json()

        # error_message_2 = "On Person, invalid type for attribute 'spouse'. Expected 'Person' but got '<class 'dict'>'"
        # with pytest.raises(ValueError, match=re.escape(error_message_2)):
        #     Person.from_json(json_data)                                       # BUG
        assert Person.from_json(json_data).json() == json_data                  # FIXED


    def test__regression__mixed_forward_refs(self):                                         # Mix of working and broken
        """Bug: Direct forward ref fails even when List forward ref works"""

        class Graph_Node(Type_Safe):
            id        : str
            neighbors : List['Graph_Node']  # This will work
            parent    : 'Graph_Node'        # This will fail

        node1 = Graph_Node(id='node1')
        node2 = Graph_Node(id='node2')
        node1.neighbors = [node2]
        node1.parent = node2

        json_data = node1.json()

        # The List part would work, but the direct ref fails first
        # error_message = "On Graph_Node, invalid type for attribute 'parent'. Expected 'Graph_Node' but got '<class 'dict'>'"
        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     Graph_Node.from_json(json_data)
        assert Graph_Node.from_json(json_data).json() == json_data


    def test__regression__dict__issue__in__deserialize_from_dict(self):
        class An_Class_1(Type_Safe):
            items: List[Dict[str, Any]]                             # BUG happens with Dict

        class An_Class_2(Type_Safe):
            items: List[dict[str, Any]]                             # and works with dict


        data = {'items': [{'id': 0, 'value': f'item_0'}]}

        obj = An_Class_1()
        # error_message = "Type Dict cannot be instantiated; use dict() instead"
        # with pytest.raises(TypeError, match=re.escape(error_message)):
        #     self.step_from_json.deserialize_from_dict(obj, data)               # BUG
        assert self.step_from_json.deserialize_from_dict(obj         , data).json() == data      # Fixed

        assert self.step_from_json.deserialize_from_dict(An_Class_2(), data).json() == data


    def test__regression__round_trip_serialization(self):                                         # Test complete round-trip
        class Complex_Class(Type_Safe):
            id       : Safe_Id
            name     : str
            items    : List[str]
            metadata : Dict[str, Any]
            nested   : 'Complex_Class'

        original = Complex_Class()
        original.id       = Safe_Id('test-123')
        original.name     = 'Test Object'
        original.items    = ['item1', 'item2']
        original.metadata = {'key': 'value', 'number': 42}
        original.nested   = Complex_Class(name='Nested Object')

        # Serialize
        json_data = original.json()

        # This is what we get
        assert json_data == {
            'id'      : 'test-123',
            'name'    : 'Test Object',
            'items'   : ['item1', 'item2'],
            'metadata': {'key': 'value', 'number': 42},
            'nested'  : {
                'id'      : original.nested.id,  # Some auto-generated ID
                'name'    : 'Nested Object',
                'items'   : [],
                'metadata': {},
                'nested'  : None
            }
        }

        # The bug: forward reference to same class doesn't deserialize
        # error_message = "On Complex_Class, invalid type for attribute 'nested'. Expected 'Complex_Class' but got '<class 'dict'>'"
        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     restored = Complex_Class.from_json(json_data)
        assert Complex_Class.from_json(json_data).json() == json_data