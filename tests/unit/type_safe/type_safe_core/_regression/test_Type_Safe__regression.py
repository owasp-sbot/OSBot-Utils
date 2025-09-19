import re
import sys
import pytest
from enum                                                                               import Enum
from decimal                                                                            import Decimal
from typing                                                                             import Optional, Union, List, Dict, get_origin, Type, ForwardRef, Any, Set
from unittest                                                                           import TestCase
from unittest.mock                                                                      import patch
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Guid                          import Guid
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Hash                   import Random_Hash
from osbot_utils.type_safe.primitives.domains.identifiers.Timestamp_Now                 import Timestamp_Now
from osbot_utils.type_safe.primitives.core.Safe_Str                                     import Safe_Str
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path       import Safe_Str__File__Path
from osbot_utils.helpers.python_compatibility.python_3_8                                import Annotated
from osbot_utils.base_classes.Kwargs_To_Self                                            import Kwargs_To_Self
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.decorators.methods.cache_on_self                                       import cache_on_self
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                   import Random_Guid
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                   import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                   import Type_Safe__List
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Set                    import Type_Safe__Set
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Tuple                  import Type_Safe__Tuple
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Annotations                 import type_safe_annotations
from osbot_utils.type_safe.type_safe_core.shared.Type_Safe__Convert                     import type_safe_convert
from osbot_utils.type_safe.validators.Validator__Min                                    import Min
from osbot_utils.utils.Json                                                             import json_to_str, str_to_json
from osbot_utils.utils.Misc                                                             import list_set, is_guid
from osbot_utils.utils.Objects                                                          import default_value, __, type_full_name


class Node_Value(Type_Safe):
    value: int

class test_Type_Safe__regression(TestCase):

    def test__regression__type_safe_step_init__issue_with_Dict_with_not_types(self):
        class An_Class(Type_Safe):
            an_dict: Dict

        An_Class()
        An_Class(an_dict=None)
        An_Class(an_dict={})
        bug_error_1 = "not enough values to unpack (expected 2, got 0)"
        # with pytest.raises(ValueError, match=re.escape(bug_error_1)):
        #     An_Class(an_dict={'a': 42})                                   # BUG: should have worked
        assert An_Class(an_dict={'a': 42}).json() == {'an_dict': {'a': 42}} # FIXED

    def test__regression__from_json_with_optional(self):
        class An_Enum(Enum):
            value_1  = "abc"
            value_2  = "xyz"

        class An_class(Type_Safe):
            with_optional   : Optional[An_Enum]       = None
            no_optional     : An_Enum                 = None

        An_class(no_optional='abc')                                 # directly works
        An_class(**dict(no_optional='abc'))                         # **kwargs directly work
        An_class.from_json(dict(no_optional  ='abc'))               # and so does from_json
        expected_error_1 = "Value 'ddd' is not a valid member of An_Enum."
        with pytest.raises(ValueError, match=expected_error_1):
            An_class.from_json(dict(no_optional  ='ddd'))           # type validation works here too

        expected_error_2 = "Value '123' is not a valid member of An_Enum."
        with pytest.raises(ValueError, match=expected_error_2):
            An_class.from_json(dict(no_optional  = 123))           # type validation works here too

        bug_error_1 = "On An_class, invalid type for attribute 'with_optional'. Expected 'typing.Optional[test_Type_Safe__bugs.test_Type_Safe__bugs.test__bug__from_json_with_optional.<locals>.An_Enum]' but got '<class 'str'>'"
        # with pytest.raises(ValueError, match=re.escape(bug_error_1)):
        #     An_class.from_json(dict(with_optional='abc'))               # BUG: but with optional the auto conversion of str (which is valid value to convert) didn't work
        An_class.from_json(dict(with_optional='abc'))                     # FIXED

        # with pytest.raises(ValueError, match=re.escape(bug_error_1)):
        #     An_class(with_optional='abc')                               # BUG: but with optional the auto conversion of str (which is valid value to convert) didn't work
        An_class(with_optional='abc')                                     # FIXED

        # with pytest.raises(ValueError, match=re.escape(bug_error_1)):
        #     An_class(**dict(with_optional='abc'))                       # BUG: but with optional the auto conversion of str (which is valid value to convert) didn't work
        An_class(**dict(with_optional='abc'))                             # FIXED


    def test__regression__type_annotation_json_serialization__roundtrip(self):
        from typing import Type

        class Parent_Class(Type_Safe):
            class_type: Type[int]

        class Child_Class(Parent_Class):
            an_type: Type[int]

        Parent_Class.from_json(Parent_Class().json())

        # current working workflows
        assert Parent_Class().json() == {'class_type': 'builtins.int'                           }  # Create instance and serialize to JSON
        assert Child_Class ().json() == {'an_type': 'builtins.int', 'class_type': 'builtins.int'}  # Create instance and serialize to JSON
        assert Parent_Class().json() == Parent_Class.from_json(Parent_Class().json()).json()       # Round trip of Parent_Class works

        # current buggy workflow
        # with pytest.raises(ValueError, match=re.escape("Invalid type for attribute 'class_type'. Expected 'typing.Type[int]' but got '<class 'str'>'")):
        #     assert Child_Class .from_json(Child_Class().json())                                 # BUG should not have raised an exception

        assert Child_Class.from_json(Child_Class().json()).json() == Child_Class().json()        # Fixed : works now :BUG this should work


    def test__regression__roundtrip_tuple_support(self):
        class Inner_Data(Type_Safe):
            tuple_1  : tuple[str, str]
            node_ids: Dict[str, tuple[str, str]]
            edge_ids: Dict[str, set[str]]

        class An_Class(Type_Safe):
            data: Inner_Data

        an_class = An_Class()
        an_class.data = Inner_Data()
        an_class.data.node_ids = {"a": ("id1", "id2")}
        an_class.data.edge_ids = {"b": {"id3"}}
        an_class.data.tuple_1  = ("id1", "id2")

        expected_error = "In tuple at index 0: Expected 'str', but got 'int'"
        with pytest.raises(TypeError, match=expected_error):
            an_class.data.node_ids = {"b": (123, '123')}                            # confirm type safety in tuples

        assert type(an_class.data.tuple_1) is Type_Safe__Tuple                      #  FIXED BUG this should be Type_Safe__Tuple
        expected_error = "In Type_Safe__Tuple: Invalid type for item: Expected 'str', but got 'int'"
        with pytest.raises(TypeError, match=expected_error):
            an_class.data.tuple_1 = (123, '123')                                     #  FIXED BUG should have raised
        assert type(an_class.data.tuple_1) is Type_Safe__Tuple

        assert type(an_class.data.node_ids) is Type_Safe__Dict                      #  FIXED: this should not be a dict
        assert type(an_class.data.edge_ids) is Type_Safe__Dict                      #  FIXED: correct this should be a dict


        assert an_class.json() == {'data': {'edge_ids': {'b': {'id3'}},
                                            'node_ids': {'a': ('id1', 'id2')},
                                            'tuple_1': ['id1', 'id2']}}

        # error_message = "In Type_Safe__Tuple: Invalid type for item: Expected 'str', but got 'int'"
        # with pytest.raises(TypeError, match=error_message):
        roundtrip_obj = An_Class.from_json(an_class.json())         # FIXED

        assert roundtrip_obj.json()             == an_class.json()
        assert roundtrip_obj.data.node_ids      == {"a": ("id1", "id2")}
        assert roundtrip_obj.data.edge_ids      == {"b": {"id3"}}
        assert an_class.data.tuple_1.json()     == ['id1', 'id2']
        assert roundtrip_obj.data.tuple_1       == ('id1', 'id2')
        assert type(roundtrip_obj.data.tuple_1) is Type_Safe__Tuple

    def test__regression__fast_api_routes__no_support_for_slashes_in_path(self):
        class An_Class(Type_Safe):
            tag : Safe_Str             = 'aaaa/bbbb'
            path: Safe_Str__File__Path = 'cccc/dddd'

        #error_message = "Invalid type for attribute 'tag'. Expected '<class 'osbot_utils.type_safe.primitives.safe_str.Safe_Str.Safe_Str'>' but got '<class 'str'>'"
        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     An_Class()                                                            # FIXED: BUG it should be possible to assign values to primitive classes

        assert An_Class().obj()  == __(tag='aaaa_bbbb', path='cccc/dddd')           # FIXED
        assert type(An_Class().tag) is Safe_Str
        assert type(An_Class().path) is Safe_Str__File__Path

        class An_Class_2(Type_Safe):
            tag : Safe_Str             = Safe_Str            ('eeee/ffff')
            path: Safe_Str__File__Path = Safe_Str__File__Path('gggg/hhhh')

        assert An_Class_2().obj()  == __(tag='eeee_ffff', path='gggg/hhhh')           # this works because of the assignment of a Safe_Str value

    def test__regression__error_when_using__dict_with_type_as_key(self):

        class Container(Type_Safe):
            value_nodes: Dict[Type[Node_Value], Obj_Id]

        # Case 1: Using class (should work)
        node_type_1 = Node_Value
        obj_id_1   = Obj_Id()
        #with pytest.raises(TypeError, match=re.escape(expected_error)):                        # BUG should have worked
        container_1  = Container(value_nodes={node_type_1: obj_id_1})

        assert container_1.json() == {'value_nodes': { type_full_name(node_type_1): obj_id_1}}


        # Case 2: roundtrip
        obj_id_2    = Obj_Id()


        expected_error = "Expected subclass of Node_Value, got str"
        with pytest.raises(TypeError, match=re.escape(expected_error)):
            Container(value_nodes={str: obj_id_2})                      # BUG should have raised type safety error


        # confirm round trip
        container = Container(value_nodes={node_type_1: obj_id_1})
        serialized = container.json()
        deserialized = Container.from_json(serialized)
        self.assertEqual(container.value_nodes, deserialized.value_nodes)

    def test__regression__roundtrip_set_support(self):
        class An_Class(Type_Safe):
            an_set_1: set[str]
            an_set_2: Set[str]

        an_class = An_Class()
        an_class.an_set_1.add   ('a')
        an_class.an_set_1.add   ('b')
        an_class.an_set_1.remove('a')
        an_class.an_set_2.add   ('a')
        assert an_class.json() == {'an_set_1': ['b'], 'an_set_2': ['a']}
        assert an_class.obj() == __(an_set_1=['b'], an_set_2=['a'])
        assert type(an_class.an_set_1) is Type_Safe__Set
        assert type(an_class.an_set_2) is Type_Safe__Set

        expected_message = "In Type_Safe__Set: Invalid type for item: Expected 'str', but got 'int'"

        with pytest.raises(TypeError, match=re.escape(expected_message)):
            an_class.an_set_1.add(123)                                              # confirms type safety
        with pytest.raises(TypeError, match=re.escape(expected_message)):
            an_class.an_set_2.add(123)                                              # confirms type safety


        #expected_message = "Invalid type for attribute 'an_set_1'. Expected 'set[str]' but got '<class 'list'>'"
        # with pytest.raises(ValueError, match=re.escape(expected_message)):
        #     An_Class.from_json(an_class.json())                                    # Fixed BUG: should not have raised an exception
        an_class_round_trip = An_Class.from_json(an_class.json())

        assert an_class_round_trip.an_set_1 == {'b'}                                 # Fixed
        assert an_class_round_trip.an_set_2 == {'a'}                                 # Fixed
        assert type(an_class_round_trip.an_set_1) is Type_Safe__Set                  # Fixed: BUG: it should be a set
        assert type(an_class_round_trip.an_set_1) is not list                        # Fixed: BUG: it should not be a list
        assert type(an_class_round_trip.an_set_2) is Type_Safe__Set                  # Fixed: BUG: it should be a set
        assert type(an_class_round_trip.an_set_2) is not list                        # Fixed BUG: it should be a set

        assert an_class_round_trip.json() == an_class.json()                         # Fixed:


    def test__regression__forward_ref_type(self):

        target = Type__With__Forward__Ref()

        json_data     = target.json()                                               # This serializes ref_type as string
        #error_message = "Invalid type for attribute 'ref_type'. Expected 'typing.Type[ForwardRef('Base__Type')]' but got '<class 'str'>'"
        error_message = "Could not reconstruct type from 'test_Type_Safe__regression.Type__With__Forward__Ref': module 'test_Type_Safe__regression' has no attribute 'Type__With__Forward__Ref'"
        #
        assert json_data == {'ref_type': 'test_Type_Safe__regression.Type__With__Forward__Ref'}

        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     Type__With__Forward__Ref.from_json(json_data)                           # Fixed we are now raising the correct exception
        assert Type__With__Forward__Ref.from_json(json_data).json()  == json_data     # now this works
        assert json_data  == {'ref_type': 'test_Type_Safe__regression.Type__With__Forward__Ref'}


    def test__regression__property_descriptor_handling(self):

        class Regular_Class:                                            # First case: Normal Python class without Type_Safe
            @property
            def label(self):
                raise ValueError("Getter should not be called")

            @label.setter
            def label(self, value):
                raise ValueError("Setter should not be called")


        regular_obj = Regular_Class()                                   # Demonstrate normal Python behavior

        assert isinstance(getattr(Regular_Class, 'label'), property)    # Verify it's a property
        with pytest.raises(ValueError, match="Getter should not be called"):
            _ = regular_obj.label

        with pytest.raises(ValueError, match="Setter should not be called"):
            regular_obj.label = "new_label"


        class Base_Class(Type_Safe):                                    # Second case: Type_Safe class with property descriptor
            data: str = "base_data"

        class Test_Class__1(Base_Class):                                # with exception on Getter
            @property
            def label(self):
                raise ValueError("Getter should not be called")

        class Test_Class__2(Base_Class):                                # with exception on Getter
            @property
            def label(self):
                pass

            @label.setter
            def label(self, value):
                raise ValueError("Setter should not be called")

        assert isinstance(getattr(Test_Class__1, 'label'), property)
        assert isinstance(getattr(Test_Class__2, 'label'), property)

        kwargs = Test_Class__1.__cls_kwargs__()
        assert 'label' not in kwargs                                              # Fixed: BUG: label should not exist in __cls_kwargs__

        kwargs = Test_Class__2.__cls_kwargs__()
        assert 'label' not in kwargs                                              # Fixed: BUG: label should not exist in __cls_kwargs__

        # with pytest.raises(ValueError, match="Getter should not be called"):    # Fixed: BUG: This instantiation should not trigger getter or setter
        #     _ = Test_Class__1()                                                 # Fixed:  BUG: But due to the bug, Type_Safe will try to handle the property descriptor incorrectly

        # with pytest.raises(ValueError, match="Setter should not be called"):    # Fixed:  BUG: This instantiation should not trigger getter or setter
        #     _ = Test_Class__2()                                                 # Fixed:  BUG: But due to the bug, Type_Safe will try to handle the property descriptor incorrectly

        Test_Class__1()                                                           # Fixed: no exception raised
        Test_Class__2()                                                           # Fixed: no exception raised
        assert Test_Class__1().data == "base_data"
        assert Test_Class__2().data == "base_data"

        with pytest.raises(ValueError, match="Getter should not be called"):      # Fixed: now the exception should be raised on the getter
            _ = Test_Class__1().label

        with pytest.raises(ValueError, match="Setter should not be called"):     # Fixed: now the exception should be raised on the getter
            Test_Class__2().label = 'abc'

    def test__regression__forward_ref_handling_in_type_matches(self):
        class Base_Node(Type_Safe):
            node_type: Type['Base_Node']  # Forward reference to self
            value: str

        # Test base class
        base_node = Base_Node()
        assert base_node.node_type is Base_Node  # Default value should be the Base_Node

        # Should be able to set it to the class itself
        base_node.node_type = Base_Node
        assert base_node.node_type is Base_Node

        # Subclass should work now too
        class Custom_Node(Base_Node): pass

        custom_node = Custom_Node()                              # This should no longer raise TypeError


        # Should accept either base or subclass
        custom_node.node_type = Custom_Node
        assert custom_node.node_type is Custom_Node

        custom_node.node_type = Custom_Node
        assert custom_node.node_type is Custom_Node

        # Should reject invalid types
        class Other_Class: pass

        with self.assertRaises(ValueError) as context:
            custom_node.node_type = Other_Class

        assert str(context.exception) == "On Custom_Node, invalid type for attribute 'node_type'. Expected 'typing.Type[ForwardRef('Base_Node')]' but got '<class 'test_Type_Safe__regression.test_Type_Safe__regression.test__regression__forward_ref_handling_in_type_matches.<locals>.Other_Class'>'"

        # Test with more complex case (like Schema__MGraph__Node)
        from typing import Dict, Any

        class Node_Config(Type_Safe):
            node_id: Random_Guid

        class Complex_Node(Type_Safe):
            attributes   : Dict[Random_Guid, str]  # Simplified for test
            node_config  : Node_Config
            node_type    : Type['Complex_Node']  # ForwardRef
            value        : Any

        class Custom_Complex(Complex_Node): pass

        # Both should work now
        complex_node = Complex_Node()
        custom_complex = Custom_Complex()  # Should not raise TypeError

        # And type checking should work properly
        with self.assertRaises(ValueError):
            custom_complex.node_type = Complex_Node    # Doesn't Allow base class
        custom_complex.node_type = Custom_Complex  # Allow self

        with self.assertRaises(ValueError):
            custom_complex.node_type = Other_Class  # Reject invalid type

    def test__regression__forward_ref_in_subclass_fails(self):
        class Base_Node(Type_Safe):
            node_type: Type['Base_Node']                # Forward reference to self
            value    : str

        base_node = Base_Node()                         # This works fine
        assert base_node.node_type is Base_Node

        class Custom_Node(Base_Node): pass              # But subclassing causes a TypeError



        # with pytest.raises(TypeError, match="Invalid type for attribute 'node_type'. Expected 'None' but got '<class 'typing.ForwardRef'>'"):
        #     Custom_Node()                               # Fixed; BUG: This fails with TypeError
        assert Custom_Node().node_type == Custom_Node

        class Node_Config(Type_Safe):                   # To demonstrate more complex case (like in Schema__MGraph__Node)
            node_id: Random_Guid

        class Complex_Node(Type_Safe):
            attributes : Dict[Random_Guid, str]         # Simplified for test
            node_config: Node_Config
            node_type  : Type['Complex_Node']           # ForwardRef that causes issues
            value      : Any

        complex_node = Complex_Node()                   # Base class works
        assert complex_node.node_type is Complex_Node

        class Custom_Complex_Node(Complex_Node): pass   # But custom subclass fails
        # with pytest.raises(TypeError, match="Invalid type for attribute 'node_type'. Expected 'None' but got '<class 'typing.ForwardRef'>'"):
        #     Custom_Complex_Node()                       # Fixed; BUG This raises TypeError

        assert Custom_Complex_Node().node_type == Custom_Complex_Node       # node_type is the parent class, in this case Custom_Complex_Node




    def test__regression__type_annotations_with_forward_ref(self):
        class An_Class_1(Type_Safe):
            an_type__forward_ref: Type['An_Class_1']  # Forward reference to self
            an_type__direct: Type[Type_Safe]         # Direct reference for comparison

        # with pytest.raises(TypeError, match=re.escape("Invalid type for attribute 'an_type__forward_ref'. Expected 'typing.Type[ForwardRef('An_Class_1')]' but got '<class 'typing.ForwardRef'>'")):
        #     test_class = An_Class_1()               # Fixed BUG should not have raised
        test_class = An_Class_1()
        assert test_class.an_type__forward_ref is An_Class_1
        assert test_class.an_type__direct      is Type_Safe

        assert test_class.__annotations__['an_type__forward_ref'] == Type[ForwardRef('An_Class_1')] # Confirm forward ref is correct
        assert test_class.__annotations__['an_type__direct'     ] == Type[Type_Safe]                # Confirm direct ref is correct
        #
                                                        # The bug manifests when trying to set default values for these types
        #assert test_class.an_type__forward_ref is None  # Fixed BUG: This fails with TypeError
        assert test_class.an_type__forward_ref  is An_Class_1
        assert test_class.an_type__direct       is Type_Safe  # Direct reference works fine


    def test__regression__type_annotations_default_to_none(self):
        class Schema__Base(Type_Safe): pass                 # Define base class

        class Schema__Default__Types(Type_Safe):
            base_type: Type[Schema__Base]                   # Type annotation that should default to Schema__Base

        defaults = Schema__Default__Types()

        assert defaults.__annotations__     == {'base_type': Type[Schema__Base]}      # Confirm annotation is correct
        #assert defaults.base_type          is None                                    # Fixed BUG: This should be Schema__Base instead of None
        assert defaults.base_type is Schema__Base
        assert type(defaults.__class__.__annotations__['base_type']) == type(Type[Schema__Base])

        # Also test in inheritance scenario to be thorough
        class Schema__Child(Schema__Default__Types):
            child_type: Type[Schema__Base]

        child = Schema__Child()
        assert type_safe_annotations.all_annotations(child)     == {'base_type' : Type[Schema__Base],
                                                                    'child_type': Type[Schema__Base]}      # Confirm both annotations exist
        #assert child.base_type          is None                                      # Fixed BUG: Should be Schema__Base
        #assert child.child_type         is None                                      # Fixed BUG: Should be Schema__Base
        assert child.base_type          is Schema__Base
        assert child.child_type         is Schema__Base

    def test__regression__forward_refs_in_type(self):
        class An_Class_1(Type_Safe):
            an_type__str        : Type[str]
            an_type__forward_ref: Type['An_Class_1']

        an_class = An_Class_1()
        assert an_class.an_type__str          is str
        assert an_class.an_type__forward_ref  is An_Class_1
        assert an_class.json() == { 'an_type__forward_ref': 'test_Type_Safe__regression.An_Class_1' ,
                                    'an_type__str'        : 'builtins.str'                          }
        assert an_class.obj() == __(an_type__str='builtins.str', an_type__forward_ref='test_Type_Safe__regression.An_Class_1')

        an_class.an_type__str = str
        an_class.an_type__str = Random_Guid
        with pytest.raises(ValueError, match=re.escape("On An_Class_1, invalid type for attribute 'an_type__str'. Expected 'typing.Type[str]' but got '<class 'int'>'")) :
            an_class.an_type__str = int

        #with pytest.raises(TypeError, match=re.escape("issubclass() arg 2 must be a class, a tuple of classes, or a union")):
        #    an_class.an_type__forward_ref = An_Class_1           # Fixed; BUG: this should have worked

        an_class.an_type__forward_ref = An_Class_1
        with pytest.raises(ValueError, match=re.escape("On An_Class_1, invalid type for attribute 'an_type__forward_ref'. Expected 'typing.Type[ForwardRef('An_Class_1')]' but got '<class 'str'>'")):
            an_class.an_type__forward_ref = str

        class An_Class_2(An_Class_1):
            pass

        an_class.an_type__forward_ref = An_Class_2

    def test__regression__type__with_type__cannot_be_assigned(self):
        class An_Class(Type_Safe):
            an_guid      : Type[Guid]          =  Guid
            an_time_stamp: Type[Timestamp_Now]

        # with pytest.raises(TypeError, match="Subscripted generics cannot be used with class and instance checks"):
        #     An_Class()                                #  FXIED BUG

        assert An_Class().obj() == __(an_guid       = 'osbot_utils.type_safe.primitives.domains.identifiers.Guid.Guid'                   ,
                                      an_time_stamp = 'osbot_utils.type_safe.primitives.domains.identifiers.Timestamp_Now.Timestamp_Now' )

    def test__regression__type_from_json(self):
        class An_Class(Type_Safe):
            guid_type        : Type[Guid       ] = Guid
            random_guid_type : Type[Random_Guid] = Random_Guid
            str_type         : Type[str        ] = str

        an_class_json = An_Class().json()
        assert an_class_json == { 'guid_type'       : 'osbot_utils.type_safe.primitives.domains.identifiers.Guid.Guid'               ,
                                  'random_guid_type': 'osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid.Random_Guid' ,
                                  'str_type'        : 'builtins.str'                                }
        # with pytest.raises(ValueError, match=re.escape("Invalid type for attribute 'guid_type'. Expected 'typing.Type[from osbot_utils.type_safe.primitives.domains.identifiers.Guid.Guid]' but got '<class 'str'>'")):
        #     An_Class.from_json(an_class_json)       # Fixed BUG

        assert An_Class.from_json(an_class_json).json() == an_class_json
        assert An_Class.from_json(an_class_json).obj () == An_Class().obj()

        # assert obj3.obj () == __(guid_type   = 'from osbot_utils.type_safe.primitives.domains.identifiers.Guid.Guid'    ,
        #                          str_type    = 'builtins.str'                     ,
        #                          str_type_2  = 'from osbot_utils.type_safe.primitives.domains.identifiers.Guid.Guid'    ,)
        #assert An_Class.from_json(An_Class().json()).obj() == An_Class().obj()
    def test__regression__class_level_defaults__mutable_vs_type(self):
        class Problematic(Type_Safe):
            bad_list : list                   # FIXED: BAD: mutable default
            bad_dict : dict                   # FIXED: BAD: mutable default
            bad_set  : set                    # FIXED: BAD: mutable default

        obj1 = Problematic()
        obj2 = Problematic()

        # Demonstrate the shared mutable state problem
        obj1.bad_list.append(42)
        assert obj2.bad_list != [42]              # FIXED: BUG: obj2's list was modified!

        obj1.bad_dict['key'] = 'value'
        assert obj2.bad_dict != {'key': 'value'}  # FIXED:BUG: obj2's dict was modified!

        obj1.bad_set.add('item')
        assert obj2.bad_set != {'item'}           # FIXED: BUG: obj2's set was modified!

        # Now show that Type[T] doesn't have this problem

        class Guid_2(Guid):
            pass

        class Safe(Type_Safe):
            guid_type  : Type[Guid] = Guid
            guid_type_2: Type[Guid] = Guid_2
            str_type   : Type[str ] = str
            str_type_2 : Type[str ] = Guid
            str_type_3 : Type[str ] = Guid_2


        obj3 = Safe()
        obj4 = Safe()

        # Types are immutable, so no shared state problems
        assert obj3.guid_type is obj4.guid_type     # Same type object (singleton)
        assert obj3.str_type  is obj4.str_type      # Same type object (singleton)
        assert obj3.json() == obj4.json()
        assert obj3.obj () == obj4.obj ()

        # Can't modify type objects
        with pytest.raises(ValueError, match=re.escape("On Safe, can't be set to None, to a variable that is already set. Invalid type for attribute 'guid_type'. Expected 'typing.Type[osbot_utils.type_safe.primitives.domains.identifiers.Guid.Guid]' but got '<class 'NoneType'>'")):
            obj3.guid_type = None                 # Can't modify type
        with pytest.raises(ValueError, match=re.escape("On Safe, can't be set to None, to a variable that is already set. Invalid type for attribute 'str_type'. Expected 'typing.Type[str]' but got '<class 'NoneType'>'")):
            obj4.str_type = None                  # Can't modify type

    def test__regression__type__with_type__not_enforced(self):
        class An_Class(Type_Safe):
            an_type_str: Type[str]
            an_type_int: Type[int]

        an_class = An_Class()
        assert an_class.an_type_str is str
        assert an_class.an_type_int is int
        an_class.an_type_str = str
        an_class.an_type_int = int

        with pytest.raises(ValueError, match=re.escape("On An_Class, invalid type for attribute 'an_type_str'. Expected 'typing.Type[str]' but got '<class 'int'>")):
            an_class.an_type_str = int                                                  # Fixed: BUG: should have raised exception

        with pytest.raises(ValueError, match=re.escape("On An_Class, invalid type for attribute 'an_type_int'. Expected 'typing.Type[int]' but got '<class 'str'>")):
            an_class.an_type_int = str                                                  # Fixed: BUG: should have raised exception

        with pytest.raises(ValueError, match=re.escape("On An_Class, invalid type for attribute 'an_type_str'. Expected 'typing.Type[str]' but got '<class 'NoneType'>'")):
            an_class.an_type_str = 'a'


    def test__regression__ctor__does_not_recreate__Dict__objects(self):
        class An_Class_2_B(Type_Safe):
            an_str: str

        class An_Class_2_A(Type_Safe):
            an_dict      : Dict[str,An_Class_2_B]
            an_class_2_b : An_Class_2_B

        json_data_2 = {'an_dict'     : {'key_1': {'an_str': 'value_1'}},
                       'an_class_2_b': {'an_str': 'value_1'}}

        assert An_Class_2_A.from_json(json_data_2).json() == json_data_2
        new_error = "Expected 'An_Class_2_B', but got 'dict'"
        with pytest.raises(TypeError, match=re.escape(new_error)):
            An_Class_2_A(**json_data_2)

        # so the code below started to fail after the fix to the dict object assissment (see above ""Expected 'An_Class_2_B', but got 'dict'"")
        # this feels ok since we should be using from_json to create new nester objects and not **json_data_2
        # an_class = An_Class_2_A(**json_data_2)
        # #assert type(an_class.an_dict)          is dict                                  # Fixed BUG should be Type_Safe__Dict
        # assert type(an_class.an_dict)                             is Type_Safe__Dict
        # assert type(An_Class_2_A(**json_data_2).an_dict['key_1']) is An_Class_2_B
        # #assert type(An_Class_2_A(**json_data_2).an_dict['key_1']) is dict               # BUG: this should be An_Class_2_B
        # assert type(An_Class_2_A(**json_data_2).an_class_2_b    ) is An_Class_2_B       # when not using Dict[str,An_Class_2_B] the object is created correctly

        #assert An_Class_2_A(**json_data_2).json() == json_data_2


    def test__regression__base_types_not_check_over_inheritance(self):
        class Base_Class(Type_Safe):
            an_str: str

        class An_Class(Base_Class):
            an_int: int

        an_class = An_Class()
        assert an_class.json() == {'an_str': '', 'an_int': 0}
        with pytest.raises(ValueError,match="On An_Class, invalid type for attribute 'an_str'. Expected '<class 'str'>' but got '<class 'int'>'"):
            an_class.an_str = 123           # Fixed: BUG

        an_class.an_int = 123           # OK
        an_class.an_str = "a"           # OK
        with pytest.raises(ValueError, match="On An_Class, invalid type for attribute 'an_int'. Expected '<class 'int'>' but got '<class 'str'>'"):
            an_class.an_int = "a"           # OK


    def test__regression__Annotated_inheritance(self):
        if sys.version_info < (3, 9):
            pytest.skip("Skipping tests that doesn't work on 3.8 or lower")

        class Min:
            def __init__(self, value: int):
                self.value = value

        class Max:
            def __init__(self, value: int):
                self.value = value

        class Length:
            def __init__(self, min_len: int):
                self.min_len = min_len

        class BaseClass(Type_Safe):
            age: Annotated[int, Min(0)]

        class ChildClass(BaseClass):
            name: Annotated[str, Length(2)]

        class GrandChildClass(ChildClass):
            score: Annotated[float, Min(0.0), Max(100.0)]

        test = GrandChildClass(age=25, name="John", score=95.5)


        assert test.age   == 25
        assert test.name  == "John"
        assert test.score == 95.5

        #Verify annotations are inherited correctly
        annotations = type_safe_annotations.all_annotations(test)
        assert list_set(annotations) == ['age', 'name', 'score']                        # Fixed: BUG: only the score is in the annotations
        assert get_origin(annotations['age'  ]) is Annotated      # Fixed: BUG missing annotation
        assert get_origin(annotations['name' ]) is Annotated      # Fixed: BUG missing annotation
        assert get_origin(annotations['score']) is Annotated
        expected_exception_str  = "On GrandChildClass, invalid type for attribute 'age'. Expected 'typing.Annotated.*int,.* but got '<class 'str'>"
        with pytest.raises(ValueError, match=expected_exception_str):
            test.age = 'aaaa'                                                               # Fixed: BUG: should have raised exception
        expected_exception_int  = "On GrandChildClass, invalid type for attribute 'name'. Expected 'typing.Annotated.*str,.* but got '<class 'int'>"
        with pytest.raises(ValueError, match=expected_exception_int):
            test.name = 123
        expected_exception_float = "On GrandChildClass, invalid type for attribute 'score'. Expected 'typing.Annotated.*float,.* but got '<class 'str'>"
        with pytest.raises(ValueError, match=expected_exception_float):
            test.score = "123"

    def test__regression__Annotated_doesnt_support_class_assignments(self):
        if sys.version_info < (3, 9):
            pytest.skip("Skipping tests that doesn't work on 3.8 or lower")

        class TestClass(Type_Safe):
            age  : Annotated[int, Min(0)] = 42

        # with pytest.raises(TypeError, match='Subscripted generics cannot be used with class and instance checks'):
        #     TestClass()
        assert TestClass().json() == {'age': 42}

    def test__regression__from_json__does_not_recreate__Dict__objects(self):

        class An_Class_1(Type_Safe):
            an_dict : Dict[str,int]

        json_data_1 = {'an_dict': {'key_1': 42}}
        an_class_1  = An_Class_1.from_json(json_data_1)

        assert type(an_class_1.an_dict) is Type_Safe__Dict                              # Fixed: BUG this should be Type_Safe__Dict
        assert an_class_1.an_dict == {'key_1': 42}

        class An_Class_2_B(Type_Safe):
            an_str: str

        class An_Class_2_A(Type_Safe):
            an_dict      : Dict[str,An_Class_2_B]
            an_class_2_b : An_Class_2_B

        json_data_2 = {'an_dict'     : {'key_1': {'an_str': 'value_1'}},
                       'an_class_2_b': {'an_str': 'value_1'}}
        an_class_2  = An_Class_2_A.from_json(json_data_2)

        assert an_class_2.json() == json_data_2
        assert type(an_class_2.an_dict                          ) is Type_Safe__Dict    # Fixed BUG this should be Type_Safe__Dict
        assert type(an_class_2.an_dict['key_1']                 ) is An_Class_2_B       # Fixed: BUG: this should be An_Class_2_B not an dict


    def test__regression__dict_dont_support_type_checks(self):

        class An_Class_2(Type_Safe):
            an_dict: Dict[str,str]

        an_class_2 = An_Class_2()
        assert type(an_class_2.an_dict) is Type_Safe__Dict                      # Fixed: BUG this should be Type_Safe__Dict
        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            an_class_2.an_dict['key_1'] = 123                                   # Fixed: BUG this should had raise an exception
        #assert an_class_2.an_dict == {'key_1': 123}                            # BUG: this should not have been assigned
        assert an_class_2.an_dict == {}                                         # Fixed

    def test__regression__dicts_dont_support_type_forward(self):
        class An_Class(Type_Safe):
            an_dict: Dict[str, 'An_Class']

        an_class   = An_Class()
        an_class_a = An_Class()
        assert an_class.an_dict == {}
        with pytest.raises(TypeError, match="Expected 'An_Class', but got 'str'"):
            an_class.an_dict['an_str'  ] = 'bb'                                 # Fixed: BUG: exception should have raised
        an_class.an_dict['an_class'] = an_class_a
        assert an_class.an_dict == dict(#an_str='bb'       ,                     # Fixed: BUG: an_str should not have been assigned
                                        an_class=an_class_a)


    def test__regression__nested_dict_serialisations_dont_work(self):
        if sys.version_info < (3, 9):
            pytest.skip("this doesn't work on 3.8 or lower")
        class An_Class_1(Type_Safe):
            dict_5: Dict[Random_Guid, dict[Random_Guid, Random_Guid]]

        json_data_1 = { 'dict_5': {Random_Guid(): { Random_Guid():Random_Guid() ,
                                                    Random_Guid():Random_Guid() ,
                                                    'no-guid-1': 'no-guid-2'    }}}

        json_data_2 = { 'dict_5': {str(Random_Guid()): { Random_Guid():Random_Guid() ,
                                                         Random_Guid():Random_Guid() }}}

        #with pytest.raises(TypeError, match="In dict key 'no-guid-1': Expected 'Random_Guid', but got 'str'"):
        #    assert An_Class_1().from_json(json_data_1).json() == json_data_1  # BUG: should had raised exception on 'no-guid-1': 'no-guid-2'

        with pytest.raises(ValueError, match=re.escape("in Random_Guid: value provided was not a Guid: no-guid-1")):
           assert An_Class_1().from_json(json_data_1).json() == json_data_1  # FIXED: BUG: should had raised exception on 'no-guid-1': 'no-guid-2'


        assert An_Class_1().from_json(json_data_2).json() == json_data_2

    def test__regression__type_safe_is_not_enforced_on_dict_and_Dict(self):
        class An_Class(Type_Safe):
            an_dict : Dict[str,int]

        an_class = An_Class()

        assert An_Class.__annotations__ == {'an_dict': Dict[str, int]}
        assert an_class.__locals__()    == {'an_dict': {}}
        assert type(an_class.an_dict)   is Type_Safe__Dict                      # Fixed: BUG: this should be Type_Safe__Dict
        with pytest.raises(TypeError, match="Expected 'str', but got 'int'"):
            an_class.an_dict[42] = 'an_str'                                     # Fixed: BUG: this should not be allowed
                                                                                #       - using key 42 should have raised exception (it is an int instead of a str)
                                                                                #       - using value 'an_str' should have raised exception (it is a str instead of an int)

    def test__regression__nested_types__not_supported(self):
        class An_Class(Type_Safe):
            an_class : 'An_Class'

        an_class          = An_Class()
        #error_message_1     = "Invalid type for attribute 'an_class'. Expected 'An_Class' but got '<class 'test_Type_Safe__bugs.test_Type_Safe__bugs.test__bug__nested_types__not_supported.<locals>.An_Class'>'"

        an_class.an_class = An_Class()

        # with pytest.raises(ValueError, match=error_message_1):
        #     an_class.an_class = An_Class()            # BUG: should NOT have raised exception here

        assert type(an_class.an_class         ) is An_Class
        assert type(an_class.an_class.an_class) is type(None)
        an_class.an_class = An_Class()                              # FIXED: this now works
        assert type(an_class.an_class) is An_Class
        assert type(an_class.an_class.an_class) is type(None)
        error_message_2 = "On An_Class, invalid type for attribute 'an_class'. Expected 'An_Class' but got '<class 'str'>"
        with pytest.raises(ValueError, match=error_message_2):
            an_class.an_class = 'a'                 # BUG: wrong exception

    def test__regression__list_from_json_not_enforcing_type_safety(self):
        class An_Class__Item(Type_Safe):
            an_str: str

        class An_Class(Type_Safe):
            items : List[An_Class__Item]

        json_data = {'items': [{'an_str': 'abc'}]}

        an_class_1 = An_Class()
        an_class_1.items.append(An_Class__Item(an_str='abc'))
        assert type(an_class_1.items)     == Type_Safe__List
        assert type(an_class_1.items[0])  is An_Class__Item
        assert an_class_1.json()          == json_data
        assert an_class_1.obj ()          == __(items=[__(an_str='abc')])

        an_class_2 = An_Class.from_json(json_data)
        assert an_class_2.json() == an_class_1.json()
        assert an_class_2.obj()  == an_class_1.obj()

        #assert type(an_class_2.items[0]) is dict                    # BUG: should be An_Class__Item

        assert type(an_class_2.items   ) is Type_Safe__List          # FIXED
        assert type(an_class_2.items[0]) is An_Class__Item           # FIXED


        # confirm that the type safety is enforced on the objects created via the ctor
        with pytest.raises(TypeError, match ="Invalid type for item: Expected 'An_Class__Item', but got 'str'"):
            an_class_1.items.append('abc')

        with pytest.raises(TypeError, match ="Invalid type for item: Expected 'An_Class__Item', but got 'int'"):
            an_class_1.items.append(123)

        # BUG, but it is not enforced in the object created using from_json
        #an_class_2.items.append('abc')                                       # BUG, should have raised exception
        #an_class_2.items.append(123)                                         # BUG, should have raised exception

        with pytest.raises(TypeError, match ="Invalid type for item: Expected 'An_Class__Item', but got 'str'"):
            an_class_2.items.append('abc')

        with pytest.raises(TypeError, match ="Invalid type for item: Expected 'An_Class__Item', but got 'int'"):
            an_class_2.items.append(123)

        #assert an_class_2.obj() == __(items=[__(an_str='abc'), 'abc', 123])  # BUG new values should have not been added
        assert an_class_2.obj() == __(items=[__(an_str='abc')])              # correct, values did not change
        assert an_class_2.obj() == __(items=[__(an_str='abc')])              # correct, values did not change


    def test__regression__from_json__pure__Dict__objects_raise_exception(self):
        if sys.version_info < (3, 9):
            pytest.skip("this doesn't work on 3.8 or lower")
        class An_Class(Type_Safe):
            an_dict__lowercase  : dict
            an_dict__uppercase  : Dict
            an_dict__annotations: Dict[str,dict]

        json_data = {'an_dict__lowercase'  : {'key_1': 42},
                     'an_dict__uppercase'  : {'key_2': 42},
                     'an_dict__annotations': {'key_3': {'inner': dict()}}}
        assert An_Class().obj()  == __(an_dict__lowercase   = __(),
                                       an_dict__uppercase   = __(),
                                       an_dict__annotations = __())
        assert An_Class().json() == {'an_dict__annotations': {},
                                     'an_dict__lowercase'  : {},
                                     'an_dict__uppercase'  : {}}

        # with pytest.raises(IndexError, match="tuple index out of range"):
        #     An_Class.from_json(json_data)                                   # FIXED, was: BUG should not raise exception
        assert An_Class.from_json(json_data).json() == json_data
        assert An_Class.from_json(json_data).obj () == __(an_dict__lowercase   = __(key_1=42)            ,
                                                          an_dict__uppercase   = __(key_2=42)            ,
                                                          an_dict__annotations = __(key_3=__(inner=__())))

        # test more variations o dict objects
        class An_Class_2(Type_Safe):
            dict_1: dict[str,int]
            dict_2: Dict[int,str]
            dict_3: dict[Random_Guid, int]
            dict_4: Dict[int, Random_Guid]

        json_data_2 = {'dict_1': {'key_1': 42},
                       'dict_2': {42: 'key_1'},
                       'dict_3': {'not a guid': 42},
                       'dict_4': {42: 'also not a guid'}}

        with pytest.raises(ValueError, match="in Random_Guid: value provided was not a Guid: not a guid"):
            An_Class_2.from_json(json_data_2)

        json_data_2['dict_3'] = {str(Random_Guid()): 42}
        with pytest.raises(ValueError, match="in Random_Guid: value provided was not a Guid: also not a guid"):
            An_Class_2.from_json(json_data_2)

        json_data_2['dict_4'] = {42: Random_Guid()}

        assert An_Class_2.from_json(json_data_2).json() == json_data_2

    def test__regression__from_json__allows_new_fields(self):
        class An_Class(Type_Safe):
            an_str: str

        json_data_1 = {'an_str': 'value_2'}
        assert An_Class.from_json(json_data_1).json() == json_data_1

        json_data_2 = {'an_str': 'value_2', 'new_field': 'new_value'}
        with pytest.raises(ValueError) as exception:
            An_Class.from_json(json_data_2,raise_on_not_found=True).json()        # Fixed:   BUG: should have raised exception because of new_field
        assert exception.value.args[0] == "Attribute 'new_field' not found in 'An_Class'"

        assert An_Class.from_json(json_data_2).json() == json_data_1              # without raise_on_not_found=True it should ignore the new field

    def test__regression__classes_with_str_base_class_dont_round_trip(self):
        class An_Class(Type_Safe):
            an_str      : str = '42'
            random_guid : Random_Guid

        an_class                           = An_Class()
        an_class_obj                       = an_class.obj()
        an_class__via_from_json            = An_Class.from_json(an_class.json())        # works
        an_class__via_ctor                 = An_Class(**an_class.json())                # works
        an_class__via_set_attr             = An_Class()                                 # works
        an_class__via_set_attr.an_str      = an_class.json().get('an_str'     )


        assert an_class__via_from_json.obj() == an_class_obj
        assert an_class               .obj() == an_class_obj
        assert an_class__via_ctor     .obj() == an_class_obj

        class An_Class__using__None(Type_Safe):
            an_str      : str           = None
            random_guid : Random_Guid   = None

        an_class_using_none               = An_Class__using__None.from_json(an_class.json())  # works
        assert an_class_using_none.obj() == an_class_obj


        # these are the exceptions that should happen when we try to assign non GUID value

        bad_guids = ['aaaa'                                 ,  # clearly not a guid :)
                     '1e1a9d4d-cc16-4c59-a593-1f1fcaabebd'  ,  # missing one value at the end
                     'Ge1a9d4d-cc16-4c59-a593-1f1fcaabebdb' ,  # has a G at the start (GUID should only be A-G and 0-9)
                     '1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb1' ,  # has extra char at the end
                     ]
        for bad_guid in bad_guids:
            expected_error = f"in Random_Guid: value provided was not a Guid: {bad_guid}"
            with pytest.raises(ValueError,match=expected_error):
                an_class.random_guid = bad_guid


        # FIXED: these statements now don't throw an exception and assign the correct values

        # use case 1: assign the str representation of an_class.random_guid
        assert is_guid(an_class__via_set_attr.random_guid) is True
        an_class__via_set_attr.random_guid = "1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb"
        assert an_class__via_set_attr .obj() == __(an_str='42', random_guid='1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb')

        # assert an_class_using_none__via_set_attr.obj() == an_class_obj
        # use case 2:  assign the str representation of an_class.random_guid
        assert is_guid(an_class__via_set_attr.random_guid) is True
        an_class__via_set_attr.random_guid = str.__str__((an_class.json().get('random_guid')))
        assert an_class__via_set_attr.obj() == an_class_obj

        # use-case 3: assign the guid when there is a null value
        an_class_using_none__via_set_attr = An_Class__using__None()
        assert an_class_using_none__via_set_attr.random_guid is None
        an_class_using_none__via_set_attr.random_guid = "1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb"
        assert an_class_using_none__via_set_attr.obj() == __(an_str=None, random_guid='1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb')

        # FIXED: below are the tests that were failing when the bug existed
        # #BUG: these three use cases fail the assigment of a valid GUID into the random_guid attribute
        #
        # # use-case 1: assign a valid GUID to the random_guid attribute
        # with pytest.raises(ValueError, match="Invalid type for attribute 'random_guid'. Expected '<class 'osbot_utils.helpers.Random_Guid.Random_Guid'>' but got '<class 'str'>'"):
        #     assert is_guid(an_class__via_set_attr.random_guid) is True
        #     an_class__via_set_attr.random_guid = "1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb"
        #
        # # use-case 2: assign the str representation of an_class.random_guid
        # with pytest.raises(ValueError, match="Invalid type for attribute 'random_guid'. Expected '<class 'osbot_utils.helpers.Random_Guid.Random_Guid'>' but got '<class 'str'>'"):
        #     assert is_guid(an_class__via_set_attr.random_guid) is True
        #     an_class__via_set_attr.random_guid = str.__str__((an_class.json().get('random_guid')))
        #
        # # use-case 3: assign the guid when there is a null value
        # an_class_using_none__via_set_attr = An_Class__using__None()
        # with pytest.raises(ValueError, match="Invalid type for attribute 'random_guid'. Expected '<class 'osbot_utils.helpers.Random_Guid.Random_Guid'>' but got '<class 'str'>'"):
        #     assert an_class_using_none__via_set_attr.random_guid is None
        #     an_class_using_none__via_set_attr.random_guid =  "1e1a9d4d-cc16-4c59-a593-1f1fcaabebdb"

        # assert an_class__via_set_attr .obj() == an_class_obj
        # assert an_class_using_none__via_set_attr.obj() == an_class_obj


        #assert type(str(an_class.json().get('random_guid')))



    def test__regression__base_class_attributes_set_to_null_when_super_is_used(self):

        if sys.version_info < (3, 9):
            pytest.skip("Skipping test that doesn't work on 3.8 or lower")

        class Base_Class(Kwargs_To_Self):
            an_int : int
            an_str : str

            def __init__(self):
                self.an_int = 42
                self.an_str = '42'
                super().__init__()

        class An_Class(Base_Class):
            an_int : int
            an_str : str

            def __init__(self):
                super().__init__()
                self.an_int = 43


        an_class   = An_Class()
        base_class = Base_Class()

        assert an_class.__dict__       == {'an_int': 43, 'an_str': '42' }       # FIXED: BUG lost value assigned in Base_Class
        assert an_class.__locals__()   == {'an_int': 43, 'an_str': '42' }       # FIXED: BUG lost value assigned in Base_Class
        assert base_class.__dict__     == {'an_int': 42, 'an_str': '42' }       # FIXED: BUG lost value assigned in Base_Class
        assert base_class.__locals__() == {'an_int': 42, 'an_str': '42' }       # FIXED: BUG lost value assigned in Base_Class

    def test__regression__default_value_is_not_cached(self):                    # FIXED: this is a test that confirms a BUG the currently exists in the default_value method

        class An_Class(Kwargs_To_Self):
            test_case : TestCase
        with patch('osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Default_Value.default_value') as patched_default_value:

            patched_default_value.side_effect = default_value                   # make sure that the main code uses the original method (i.e. not the patched one)
                                                                                #       since all we need is the ability to count how many times the method was called
            an_class = An_Class()                                               # create instance of class (which will call default_value via __default__kwargs__)
            assert patched_default_value.call_count == 1                        # expected result, since we used the default_value to create an instance of TestCase
            test_case = an_class.__locals__().get('test_case')                  # get a reference of that object (which (BUG) will also call default_value)
            assert test_case                         is not None                # make sure var that is set
            assert type(test_case)                   == TestCase                #       and that is the correct type
            assert patched_default_value.call_count  == 1 # was 2               # FIXED - BUG: we shouldn't see another call to default_value
            assert an_class.__locals__().get('test_case') is test_case          # confirm that although there was a call to default_value, it's value was not used
            assert patched_default_value.call_count  == 1 # was 3               # FIXED -BUG: again we should not see a call to default_value
            assert an_class.__locals__().get('test_case') is test_case          # just to double-check the behaviour/bug we are seeing
            assert patched_default_value.call_count  == 1 # was 4               # FIXED -BUG: this should be 1 (since we should only create the object once via default_value)
            assert default_value(TestCase).__class__ is TestCase                # confirm that a direct call to default_value does create an instance of TestCase
            assert default_value(TestCase)           is not test_case           # confirm that default_value object doesn't match the one we got originally
            assert TestCase()                        is not TestCase()          # double check that TestCase() creates a new object every time
            assert test_case                         is test_case               # confirm that the 'is' operator is the one correct one to check equality
            assert test_case                         == test_case               # confirm that we can't use == (i.e. __eq__) for equality
            assert TestCase()                        == TestCase()              #       since this should be False (i.e. two new instances of TestCase)

    def test__regression__type_safety_race_condition_on_overloaded_vars(self):

        class Base_Class                       :  pass                         # a base class
        class Implements_Base_Class(Base_Class): pass                          # is used as a base class here
        class An_Class(Kwargs_To_Self):                                        # now when a new class
            an_var: Base_Class                                                 # creates a var using the base class
        class Extends_An_Class(An_Class):                                      # and another class uses it has a base class
            an_var: Implements_Base_Class                                      # and changes the type to a compatible type
                                                                               #   we will get an exception, because Kwargs_To_Self creates
                                                                               #   a new object of type Base_Class when it should create
                                                                               #   a new object of type Implements_Base_Class

        Base_Class()                                                           # this works ok
        Implements_Base_Class()                                                # this works ok
        An_Class()                                                             # this works ok (with an_var = Base_Class() )
        Extends_An_Class()                                                     # FIXED: this works now (with an_var = Implements_Base_Class() )

        assert type(An_Class()        .an_var) is Base_Class                  # just confirming an_var is Base_Class
        assert type(Extends_An_Class().an_var) is Implements_Base_Class       # just confirming an_var is now Implements_Base_Class

        # with self.assertRaises(Exception) as context:                       # BUG: this now will fail
        #     Extends_An_Class()                                              # BUG: due to a bug in type safety logic Kwargs_To_Self
        #
        # assert str(context.exception) == ("Invalid type for attribute 'an_var'. Expected '<class 'test_Kwargs_To_Self.Test_Kwargs_To_Self.test__bug__type_safety_race_condition_on_overloaded_vars.<locals>."
        #                                     "Implements_Base_Class'>' "
        #                                  "but got '<class 'test_Kwargs_To_Self.Test_Kwargs_To_Self.test__bug__type_safety_race_condition_on_overloaded_vars.<locals>."
        #                                     "Base_Class'>'")

    def test__regression__type_safety_bug__in___cls_kwargs__(self):
        class Base_Class                           : pass                                  # set of classes that replicate the bug
        class Implements_Base_Class(Base_Class    ): pass                                  # which happens when we have a base class
        class An_Class             (Kwargs_To_Self): an_var: Base_Class                    # and a class that uses it as a var
        class Extends_An_Class     (An_Class      ):an_var: Implements_Base_Class          # and another class that extends it and changes the type

        an_class__cls_kwargs__         = An_Class        .__cls_kwargs__()                 # the bug in __cls_kwargs__() so lets get its output for both
        extends_an_class__cls_kwargs__ = Extends_An_Class.__cls_kwargs__()                 # An_Class and Extends_An_Class
        assert list_set(an_class__cls_kwargs__        )           == ['an_var']            # confirm that the only var created and assigned
        assert list_set(extends_an_class__cls_kwargs__)           == ['an_var']            # the 'an_var' one
        assert type(an_class__cls_kwargs__        .get('an_var')) == Base_Class            # this is ok since the an_var in An_Class should be Base_Class
        assert type(extends_an_class__cls_kwargs__.get('an_var')) == Implements_Base_Class # FIXED: BUG: since an_var in Extends_An_Class should be Implements_Base_Class





    def test__regression__cast_issue_with_base_class_mode_a(self):                   # note although this test is still showing the bug, the test__regression__cast_issue_with_base_class_mode_c shows the fix (which is why it has been changed to regression test)
        class Base_Class(Kwargs_To_Self):
            an_int : int = 42

        class Cast_Mode_A(Base_Class):
            an_str : str = 'abc'

            def cast(self, target):
                self.__dict__ = target.__dict__
                return self

        base_class = Base_Class()                                                    # create an object of Base_Class base class
        assert list_set(base_class.__kwargs__())  == ['an_int']                      # confirm that it has the expected vars
        assert base_class.an_int                  == 42                              # confirm that an_int was correct set via Kwargs_To_Self
        cast_mode_a = Cast_Mode_A()                                                  # create an object of Cast_Mode_A class
        assert list_set(cast_mode_a.__kwargs__()) == ['an_int', 'an_str']            # confirm that it has the vars from Base_Class and Cast_Mode_A
        assert cast_mode_a.an_int                 == 42                              # confirm that an_int was correctly set via Kwargs_To_Self
        assert cast_mode_a.an_str                 == 'abc'                           # confirm that an_str was correctly set via Kwargs_To_Self

        base_class.an_int                          = 123                             # now change the value of base_class.an_int
        assert base_class.an_int                  == 123                             # confirm it has been changed correctly
        cast_mode_a_from_base_class                = Cast_Mode_A().cast(base_class)  # now create a new object of Cast_Mode_A and cast it from base_class
        assert cast_mode_a_from_base_class.an_int == 123                             # confirm that an_int was the new object picked up the new value (via cast)

        cast_mode_a_from_base_class.an_int         = 456                             # now change the an_int on the new class
        assert cast_mode_a_from_base_class.an_int == 456                             # and confirm that the value has been changed correctly in the 'casted' object
        assert base_class.an_int                  == 456                             # and confirm that it also was changed in the original object (i.e. base_class)

        # the example above is the exact behaviour which replicates the 'cast' operation in other languages (i.e. C#), where
        #       cast_mode_a_from_base_class = Cast_Mode_A().cast(base_class)
        # is equivalent to
        #       cast_mode_a_from_base_class = (Cast_Mode_A) base_class
        assert cast_mode_a_from_base_class.an_str  == 'abc'
        cast_mode_a_from_base_class.new_str         = 'new_str'
        assert cast_mode_a_from_base_class.new_str == 'new_str'                      # confirm that the new var is set correctly
        assert base_class.new_str                  == 'new_str'                      # confirm that the new var is set correctly
        assert cast_mode_a_from_base_class.__dict__ == base_class.__dict__

        base_class_2  = Base_Class()                                                 # create a clean instance of Base_Class
        cast_mode_a_2 = Cast_Mode_A()                                                # create a clean instance of Cast_Mode_A
        assert list_set(base_class_2 .__dict__) == ['an_int']                        # confirm that it has the expected vars
        assert list_set(cast_mode_a_2.__dict__) == ['an_int', 'an_str']              # confirm that it has the vars from Base_Class and Cast_Mode_A
        cast_mode_a_2.cast(base_class_2)                                             # cast it from base_class_2
        assert list_set(base_class_2.__dict__ ) == ['an_int']                        # re-config that base_class_2 only has the one var
        assert list_set(cast_mode_a_2.__dict__) == ['an_int']                        # BUG: but now cast_mode_a_2 lost the an_str var
        assert cast_mode_a_2.an_str             == 'abc'                             # works because an_str is defined in the Cast_Mode_A class, it's still accessible by instances of that class, even if it's not in their instance __dict__.

        cast_mode_a_3 = Cast_Mode_A()
        cast_mode_a_3.an_str = 'changed'
        assert cast_mode_a_3.an_str == 'changed'
        cast_mode_a_3.cast(base_class_2)
        assert cast_mode_a_3.an_str == 'abc'

    def test__regression__cast_issue_with_base_class_mode_b(self):                         # note although this test is still showing the bug, the test__regression__cast_issue_with_base_class_mode_c shows the fix (which is why it has been changed to regression test)
        class Base_Class(Kwargs_To_Self):
            an_int : int = 42

        class Cast_Mode_B(Base_Class):
            an_str : str = 'abc'

            def cast(self, target):
                for key, value in target.__dict__.items():
                    setattr(self, key, value)
                return self

        base_class  = Base_Class()                                                  # create a new instance of Base_Class

        base_class.an_int = 222
        cast_mode_b = Cast_Mode_B().cast(base_class)                                # 'cast' that Base_Class object into a Cast_Mode_B object

        assert list_set(base_class.__kwargs__())  == ['an_int']                     # Base_Class correctly still only has one var
        assert list_set(cast_mode_b.__kwargs__()) == ['an_int', 'an_str']           # Cast_Mode_B correctly has both vars
        assert base_class.an_int                  == 222                            # confirm that an_int was correctly set via Kwargs_To_Self
        assert cast_mode_b.an_int                 == 222                            # confirm that the value was correctly set via cast
        cast_mode_b.an_int = 123                                                    # now modify the an_int value in the Cast_Mode_B object
        assert cast_mode_b.an_int                 == 123                            # confirm that the value was correctly set in the Cast_Mode_B object
        assert base_class.an_int                  == 222                            # BUG: but the value in the Base_Class object was not changed!

        base_class.an_int = 456                                                     # now modify the an_int value in the Base_Class object
        assert base_class.an_int                  == 456                            # confirm that the value was correctly set in the Base_Class object
        assert cast_mode_b.an_int                 == 123                            # BUG: but the value in the Cast_Mode_B object was not changed!

        # the current hypothesis is that the current cast code
        #                  for key, value in target.__dict__.items():
        #                     setattr(self, key, value)
        # is actually creating a copy of the an_int object, instead of a reference to it (which is what we want)


    def test__regression__cast_issue_with_base_class_mode_c(self):                  # the cast version below is the one that has the correct behaviour
        class Base_Class(Kwargs_To_Self):
            an_int : int = 42

        class Cast_Mode_C(Base_Class):
            an_str : str = 'abc'

            def cast(self, target):
                original_attrs = {k: v for k, v in self.__dict__.items() if k not in target.__dict__}       # Store the original attributes of self that should be retained.
                self.__dict__ = target.__dict__                                                             # Set the target's __dict__ to self, now self and target share the same __dict__.
                self.__dict__.update(original_attrs)                                                        # Reassign the original attributes back to self.
                return self



        base_class  = Base_Class()                                                  # create a new instance of Base_Class

        base_class.an_int = 222
        cast_mode_c = Cast_Mode_C().cast(base_class)                                # 'cast' that Base_Class object into a Cast_Mode_B object

        assert list_set(base_class.__kwargs__())  == ['an_int']                     # Base_Class correctly still only has one var
        assert list_set(cast_mode_c.__kwargs__()) == ['an_int', 'an_str']           # Cast_Mode_B correctly has both vars
        assert base_class.an_int                  == 222                            # confirm that an_int was correctly set via Kwargs_To_Self
        assert cast_mode_c.an_int                 == 222                            # confirm that the value was correctly set via cast
        cast_mode_c.an_int = 123                                                    # now modify the an_int value in the Cast_Mode_B object
        assert cast_mode_c.an_int                 == 123                            # confirm that the value was correctly set in the Cast_Mode_B object
        assert base_class.an_int                  == 123                            # FIXED :BUG: but the value in the Base_Class object was not changed!

        base_class.an_int = 456                                                     # now modify the an_int value in the Base_Class object
        assert base_class.an_int                  == 456                            # confirm that the value was correctly set in the Base_Class object
        assert cast_mode_c.an_int                 == 456                            # FIXED: BUG: but the value in the Cast_Mode_B object was not changed!

    def test__regression__check_type_safety_assignments__on_obj__union(self):

        if sys.version_info < (3, 9):
            pytest.skip("Skipping test that doesn't work on 3.8 or lower")

        class An_Class(Kwargs_To_Self):
            an_bool    : Optional[bool            ]
            an_int     : Optional[int             ]
            an_str     : Optional[str             ]
            an_bool_int: Optional[Union[bool, int]]
            an_bool_str: Optional[Union[bool, str]]

        an_bytes_value = b'an_bytes_value'
        an_class       = An_Class()

        def asserts_exception(var_name, var_value, expected_type, got_type):
            with self.assertRaises(Exception) as context:
                an_class.__setattr__(var_name, var_value)
            expected_message = f"On An_Class, invalid type for attribute '{var_name}'. Expected '{expected_type}' but got '<class '{got_type}'>'"
            assert context.exception.args[0] == expected_message

        asserts_exception('an_bool'     , an_bytes_value, 'typing.Optional[bool]'            , 'bytes')
        asserts_exception('an_int'      , an_bytes_value, 'typing.Optional[int]'             , 'bytes')
        asserts_exception('an_str'      , an_bytes_value, 'typing.Optional[str]'             , 'bytes')
        asserts_exception('an_bool_int' , an_bytes_value, 'typing.Union[bool, int, NoneType]', 'bytes')
        asserts_exception('an_bool_str' , an_bytes_value, 'typing.Union[bool, str, NoneType]', 'bytes')
        asserts_exception('an_bool_int' , an_bytes_value, 'typing.Union[bool, int, NoneType]', 'bytes')
        asserts_exception('an_bool_str' , an_bytes_value, 'typing.Union[bool, str, NoneType]', 'bytes')

        # below is the code that was passing before the fix
        # an_class.an_bool     = an_bytes_value                                   # FIXED: was BUG: none of these should work
        # an_class.an_int      = an_bytes_value                                   # FIXED: was BUG:   since none the types above have bytes
        # an_class.an_str      = an_bytes_value                                   # FIXED: was BUG:   i.e. we are allowing an incorrect assigment
        # an_class.an_bool_int = an_bytes_value
        # an_class.an_bool_str = an_bytes_value
        # an_class.an_bool_int = an_bytes_value
        # an_class.an_bool_str = an_bytes_value
        #
        # assert an_class.__locals__() == {'an_bool'    : an_bytes_value, 'an_bool_int': an_bytes_value,   # BUG confirm incorrect values assignment
        #                                  'an_bool_str': an_bytes_value, 'an_int'     : an_bytes_value,
        #                                  'an_str'     : an_bytes_value                                }

    def test__regression__check_type_safety_assignments__on_list(self):
        if sys.version_info < (3, 9):
            pytest.skip("Skipping test that needs FIXING on 3.8 or lower")

        class An_Class(Kwargs_To_Self):
            an_str     : str
            an_str_list: list[str]
            an_int_list: list[int]

        an_class = An_Class()

        def asserts_exception(var_name, var_value, expected_type, got_type):
            with self.assertRaises(Exception) as context:
                an_class.__setattr__(var_name, var_value)
            print(context.exception.args[0])
            expected_message = (f"On An_Class, invalid type for attribute '{var_name}'. Expected '<class '{expected_type}'>' "
                                f"but got '<class '{got_type}'>'")
            assert context.exception.args[0] == expected_message

        asserts_exception('an_str', 42, 'str','int')

        an_class.an_str_list.append('should work')
        an_class.an_int_list.append(42            )

        with self.assertRaises(Exception) as context:
            an_class.an_str_list.append(42)                                 # FIXED was: BUG should have not worked
        assert context.exception.args[0] == "In Type_Safe__List: Invalid type for item: Expected 'str', but got 'int'"

        with self.assertRaises(Exception) as context:
            an_class.an_int_list.append('should not work')                  # FIXED was: BUG should have not worked
        assert context.exception.args[0] == "In Type_Safe__List: Invalid type for item: Expected 'int', but got 'str'"

    def test__regression__ctor_doest_allow_none_values(self):
        class An_Class(Kwargs_To_Self):
            an_int  : list
            an_list : list
            an_str  : str
        assert An_Class().__locals__() == {'an_int': [], 'an_list': [], 'an_str': ''}

        class An_Class(Kwargs_To_Self):
            an_int  : int  = None                                       # BUG: will raise exception
            an_str  : str  = None                                       # BUG: will raise exception
            an_list : list = None  # BUG: will raise exception

        an_class = An_Class()
        assert an_class.__locals__() == {'an_int': None, 'an_list': None, 'an_str': None}

        an_class.an_int  = 42                               # confirm that normal assignments are still ok
        an_class.an_str  = '42'
        an_class.an_list = [42, '42']
        assert an_class.__locals__() == {'an_int': 42, 'an_list': [42, '42'], 'an_str': '42'}

        with self.assertRaises(Exception) as context:       # confirm that type safety checks are still in place
            an_class.an_list = 'a'
        assert context.exception.args[0] == ("On An_Class, invalid type for attribute 'an_list'. "
                                             "Expected '<class 'list'>' "
                                             "but got '<class 'str'>'"                )

    def test__regression__cache_on_self__shows_on_locals(self):
        class An_Class(Kwargs_To_Self):
            an_str: str

            def an_method(self):
                return 41

            @cache_on_self
            def an_method__cached(self):
                return 42

        an_class = An_Class()
        assert an_class.__locals__       () == {'an_str': ''}
        assert an_class.an_method        () == 41
        assert an_class.an_method__cached() == 42
        #assert an_class.__locals__       () == {'an_str': '', 'cache_on_self_an_method__cached__': 42}  # FIXED was BUG: cache method should not be here
        assert an_class.__locals__       () == {'an_str': ''}                                            # FIXED, cached value is not returned

    def test__regression__base_attrib_value_not_overwritten(self):
        class Base_Class(Kwargs_To_Self):
            an_str : str  = 'an_str__base'
            an_int : int  = 42
            an_bool: bool = True

        class An_Class(Base_Class):
            an_str : str = 'changed on an_class'                # FIXED: BUG: this is not being changed
            an_int : int = 84                                   # FIXED: BUG: this is not being changed
            an_bool: bool = False                               # FIXED: BUG: this is not being changed

        an_class = An_Class()

        expected_values = {'an_bool': False, 'an_int': 84, 'an_str': 'changed on an_class'}
        assert an_class.__locals__() == expected_values


    def test__regression__callable__not_supported(self):
        class An_Class(Kwargs_To_Self):
            an_callable: callable

        def an_local_function():
            pass

        # checking with a method
        assert An_Class(an_callable=self.test__regression__callable__not_supported).__locals__() == { 'an_callable': self.test__regression__callable__not_supported}
        # checking with a function
        assert An_Class(an_callable=an_local_function).__locals__()                              == { 'an_callable': an_local_function}

        # the assets below where failing before the fix
        # with self.assertRaises(Exception) as context:
        #     An_Class(an_callable=self.test__regression__callable__not_supported)
        # assert context.exception.args[0] == ("Invalid type for attribute 'an_callable'. Expected '<built-in function callable>' but got '<class 'method'>'")

        # with self.assertRaises(Exception) as context:
        #     An_Class(an_callable=an_local_function)
        # assert context.exception.args[0] == ("Invalid type for attribute 'an_callable'. Expected '<built-in function callable>' but got '<class 'function'>'")

    def test__regression__should_create_nested_objects_when_loading_dicts(self):                              # Test method to verify the creation of nested objects from dictionaries.
        class Class_A(Type_Safe):                                                                            # Define a nested class Class_A inheriting from Type_Safe.
            an_int: int                                                                                      # Define an attribute 'an_int' of type int.
            an_str: str                                                                                      # Define an attribute 'an_str' of type str.

        class Class_B(Type_Safe):                                                                            # Define another nested class Class_B inheriting from Type_Safe.
            an_bool: bool                                                                                    # Define an attribute 'an_bool' of type bool.
            an_bytes: bytes                                                                                  # Define an attribute 'an_bytes' of type bytes.

        class Class_C(Type_Safe):                                                                            # Define the main class Class_C inheriting from Type_Safe.
            an_class_a: Class_A                                                                              # Define an attribute 'an_class_a' of type Class_A.
            an_class_b: Class_B                                                                              # Define an attribute 'an_class_b' of type Class_B.

        class_c = Class_C()                                                                                  # Instantiate an object of Class_C.
        class_c_as_dict = { 'an_class_a': {'an_int' : 0    , 'an_str'  : '' },                               # Define a dictionary representing class_c with nested dictionaries.
                            'an_class_b': {'an_bool': False, 'an_bytes': b''}}                               # Define attributes for nested Class_B in the dictionary.

        assert class_c.json() == class_c_as_dict                                                              # Assert that the JSON representation of class_c matches the dictionary.
        assert Class_C(**class_c_as_dict).json() == class_c_as_dict                                           # FIXED: now exception is not raised

        class Class_D(Type_Safe):
            an_class_a: dict
            an_class_b: dict
        assert Class_D(**class_c_as_dict).json() == class_c_as_dict                                           # added use case of when both variables are dict

        class Class_F(Type_Safe):
            an_class_a: dict
            an_class_b: Class_B
        assert Class_F(**class_c_as_dict).json() == class_c_as_dict                                           # added use case of when we have a mix

        # with self.assertRaises(ValueError) as context:                                                      # Assert that ValueError is raised during class instantiation with invalid types.
        #     Class_C(**class_c_as_dict)                                                                      # BUG: Attempt to create a Class_C instance with the dictionary.
        #
        # assert context.exception.args[0] == ("Invalid type for attribute 'an_class_a'. Expected '<class "    # Verify the exception message for invalid type of 'an_class_a'.
        #                                      "'test_Type_Safe__bugs.test_Type_Safe__bugs."
        #                                      "test_bug__should_create_nested_objects_when_loading_dicts."
        #                                      "<locals>.Class_A'>' "
        #                                      "but got '<class 'dict'>'")                                     # Complete the verification of the exception message.

    def test__regression__decimal_and_random_guid_are_not_deserialised_ok(self):
        class An_Class(Type_Safe):
            an_decimal : Decimal
            an_guid    : Random_Guid

        an_class = An_Class(an_decimal= Decimal(1.1))

        an_class_str       = json_to_str(an_class.json())
        an_class_roundtrip = An_Class.from_json(str_to_json(an_class_str))
        assert type(an_class_roundtrip)  is An_Class                            # BUG: FIXED: was failing here
        assert an_class_roundtrip.json() == an_class.json()

        # this was the error before the fix
        # with self.assertRaises(ValueError) as context:
        #     An_Class.from_json(str_to_json(an_class_str))
        # assert context.exception.args[0] == ("Invalid type for attribute 'an_decimal'. Expected '<class "
        #                                      "'decimal.Decimal'>' but got '<class 'str'>'")

    def test__regression__json_is_trying_to_serialise__cache_on_self(self):
        class An_Class(Type_Safe):
            an_str : str
            @cache_on_self
            def cached_value(self):
                self.an_str = '42'
                return 42

        an_class = An_Class()
        assert an_class.json() == {'an_str': ''}
        an_class.cached_value()
        assert an_class.json() == {#'__cache_on_self___cached_value__': 42,  # BUG: FIXED: was this should have not been cached
                                   'an_str': '42'}

    def test__regression__in__convert_dict_to_value_from_obj_annotation(self):
        class An_Class_2_B(Type_Safe):
            an_str: str

        class An_Class_2_A(Type_Safe):
            an_dict      : Dict[str,An_Class_2_B]

        an_class = An_Class_2_A()

        target    = an_class
        attr_name = 'an_dict'
        value    = {'key_1': {'an_str': 'value_1'}}
        converted_value = type_safe_convert.convert_dict_to_value_from_obj_annotation(target, attr_name, value)

        assert converted_value == value
        assert type(converted_value['key_1']) is dict                           # FIXED (not an issue anymore, see comments below) BUG: this should be An_Class_2_B

        an_class_json      = {'an_dict': {'key_1': {'an_str': 'value_1'}}}      # although the above has that behaviour
        an_class_from_json = An_Class_2_A.from_json(an_class_json)              # this sequence shows that the from_json is working ok
        assert an_class_from_json.json()                  == an_class_json
        assert type(an_class_from_json.an_dict['key_1'])  is An_Class_2_B
        assert an_class_from_json.an_dict['key_1'].an_str == 'value_1'

        expected_error_1 = "Expected 'An_Class_2_B', but got 'dict'"
        with pytest.raises(TypeError, match=re.escape(expected_error_1)):                           # this doesn't work
            An_Class_2_A(**an_class_json)                                                           # but that is expected behavior
        #an_class_2b = An_Class_2_B()
        an_class_data   = {'an_dict': {'key_1': An_Class_2_B(**{'an_str': 'value_1'})}}             # since this is how it needs to be done, which works
        an_class_from_kwargs = An_Class_2_A(**an_class_data)                                        #   the idea is if a pure json import is needed,
        assert an_class_from_kwargs.json() == an_class_json                                         #   then .from_json(..) is what should be used


    def test__regression__check_type_safety_assignments__on_ctor__on_bool_to_int_conversion(self):
        an_bool_value = True
        an_int_value  = 42
        an_str_value  = 'an_str_value'

        class An_Class__With_Correct_Values(Kwargs_To_Self):
            an_bool : bool = an_bool_value
            an_int  : int = an_int_value
            an_str  : str = an_str_value

        class An_Class__With_Bad_Values(Kwargs_To_Self):
            an_bool : bool = an_bool_value
            an_int  : int  = an_bool_value                      # FIXED: (exception will now be raised here) BUG: should have thrown exception here
            an_str  : str  = an_bool_value                      # will throw exception here


        an_class =  An_Class__With_Correct_Values()             # should create ok and values should match the type
        assert an_class.__locals__() == {'an_bool': an_bool_value, 'an_int': an_int_value, 'an_str': an_str_value}

        #expected_message = "On An_Class__With_Bad_Values, invalid type for attribute 'an_str'. Expected '<class 'str'>' but got '<class 'bool'>'"
        expected_message = "On An_Class__With_Bad_Values, invalid type for attribute 'an_int'. Expected '<class 'int'>' but got '<class 'bool'>'"
        with self.assertRaises(Exception) as context:
            An_Class__With_Bad_Values()
        assert context.exception.args[0] == expected_message

    def test__regression__check_type_safety_assignments__allows_bool_to_int(self):
        an_bool_value = True                                        # this is a bool

        class Should_Raise_Exception(Type_Safe):                     # a class that uses Kwargs_To_Self as a base class
            an_int: int = an_bool_value                             # BUG : the an_int variable is defined as an int, but it is assigned a bool

        # should_raise_exception = Should_Raise_Exception()                                   # FIXED: BUG an exception should have been raised
        # assert should_raise_exception.__locals__()    == {'an_int': an_bool_value}          # FIXED: BUG confirming that an_int is a bool
        # assert should_raise_exception.an_int          is True                               # FIXED: BUG in this case the value True
        # assert type(an_bool_value                )    is bool                               # FIXED: confirm an_bool_value is a bool
        # assert type(should_raise_exception.an_int)    is bool                               # FIXED: BUG:  confirming that an_int is a bool
        # assert should_raise_exception.__annotations__ == {'an_int': int }                   # FIXED: confirm that the an_int annotation is int

        expected_error_1 = "On Should_Raise_Exception, invalid type for attribute 'an_int'. Expected '<class 'int'>' but got '<class 'bool'>'"
        with pytest.raises(ValueError, match=expected_error_1):
             Should_Raise_Exception()

    def test__regression__type_safety_assignments__on_obj__bool_assigned_to_int(self):
        an_bool_value = True
        an_int_value  = 42
        an_str_value  = 'an_str_value'

        class An_Class(Kwargs_To_Self):
            an_bool : bool
            an_int  : int
            an_str  : str

        an_class = An_Class()
        assert an_class.__locals__() == {'an_bool': False, 'an_int': 0, 'an_str': ''}       # confirm default values assignment

        an_class.an_bool = an_bool_value                                                    # these should all work
        an_class.an_int  = an_int_value                                                     # since we are doing the correct type assigment
        an_class.an_str  = an_str_value

        def asserts_exception(var_name, var_value, expected_type, got_type):
            with self.assertRaises(Exception) as context:
                an_class.__setattr__(var_name, var_value)
            expected_message = f"On An_Class, invalid type for attribute '{var_name}'. Expected '<class '{expected_type}'>' but got '<class '{got_type}'>'"
            assert context.exception.args[0] == expected_message

        asserts_exception('an_bool',an_str_value , 'bool', 'str' )
        asserts_exception('an_bool',an_int_value , 'bool', 'int' )
        asserts_exception('an_str' ,an_bool_value, 'str' , 'bool')
        asserts_exception('an_str' ,an_int_value , 'str' , 'int' )
        asserts_exception('an_int' ,an_str_value , 'int' , 'str' )
        asserts_exception('an_int' ,an_bool_value , 'int' , 'bool' )                     # BUG: should have raised exception
        #an_class.an_int = an_bool_value                                                   # BUG  should have raised exception

    def test_regression__is_kwargs_cacheable__was_caching_random_hash_values(self):
        # note: the reason for the weird behaviour spotted below was that the previous version of
        #       Type_Safe__Step__Class_Kwargs.is_kwargs_cacheable was only checking if there was an instance of
        #       Random_Guid in the kwargs, and if there wasn't, it wouldn't cache the values
        #       The fix, now makes it so that of any the values is Type_Save_Primitive, we also dont' cache

        class Cache_Entry_A(Type_Safe):
            entry_id    : Random_Hash                                           # when we only have this fields

        assert Cache_Entry_A().entry_id != Cache_Entry_A().entry_id             # FIXED: BUG: the values are the same!! (and should be different)
        assert Cache_Entry_A().entry_id != 'b006648417679b59'                   # this confirms we are getting new hash everytime

        class Cache_Entry_B(Type_Safe):
            entry_id    : Random_Hash
            random_guid : Random_Guid                                           # but when we add this class

        assert Cache_Entry_B().entry_id    != Cache_Entry_B().entry_id          # now it works
        assert Cache_Entry_B().random_guid != Cache_Entry_B().random_guid       # these are also difference

        class Cache_Entry_C(Type_Safe):
            random_guid : Random_Guid                                           # changing the order
            entry_id    : Random_Hash                                           # where Random_Hash is here

        assert Cache_Entry_C().entry_id    != Cache_Entry_C().entry_id          # still works as expected
        assert Cache_Entry_C().random_guid != Cache_Entry_C().random_guid       #

        class Cache_Entry_D(Type_Safe):
            random_guid : Random_Guid                                           # just random class

        assert Cache_Entry_D().random_guid != Cache_Entry_D().random_guid       # is all good

        class Cache_Entry_E(Type_Safe):
            entry_id    : Random_Hash
            an_str      : str                                                   # with another Type_Safe class

        assert Cache_Entry_E().entry_id != Cache_Entry_E().entry_id             # FIXED: BUG: we have the same problem

        class Cache_Entry_F(Type_Safe):
            entry_id    : Random_Hash
            an_safe_str : Safe_Str                                              # with another Type_Safe class

        assert Cache_Entry_F().entry_id != Cache_Entry_F().entry_id             # FIXED: BUG: we have the same problem

        class Cache_Entry_G(Type_Safe):
            entry_id    : Random_Hash
            entry_id_2  : Random_Hash                                           # with two entries

        assert Cache_Entry_G().entry_id   != Cache_Entry_G().entry_id           # FIXED: BUG: we have the same problem
        assert Cache_Entry_G().entry_id_2 != Cache_Entry_G().entry_id_2         # FIXED: BUG: we have the same problem
        assert Cache_Entry_G().entry_id   != Cache_Entry_G().entry_id_2         # but we do get two different hashes

        class Cache_Entry_H(Type_Safe):
            entry_id    : Random_Hash
            entry_id_2  : Random_Hash                                           # with two entries
            an_guid     : Random_Guid                                           # as soon as we add the Random_Guid

        assert Cache_Entry_H().entry_id   != Cache_Entry_H().entry_id           # it works again

class Base__Type(Type_Safe):
    ref_type: Type['Base__Type']

class Type__With__Forward__Ref(Base__Type):
    pass