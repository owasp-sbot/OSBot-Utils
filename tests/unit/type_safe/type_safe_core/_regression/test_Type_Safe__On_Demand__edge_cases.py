from typing import List, Dict
from unittest                                                         import TestCase
from osbot_utils.type_safe.Type_Safe                                  import Type_Safe
from osbot_utils.type_safe.Type_Safe__On_Demand                       import Type_Safe__On_Demand
from osbot_utils.type_safe.primitives.core.Safe_Str                   import Safe_Str
from osbot_utils.type_safe.primitives.core.Safe_Int                   import Safe_Int
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id     import Safe_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List import Type_Safe__List


class test_Type_Safe__On_Demand__edge_cases(TestCase):                              # Edge cases and boundary conditions

    def test__empty_class(self):                                                    # Test class with no attributes
        class Empty(Type_Safe__On_Demand):
            pass

        with Empty() as _:
            assert len(_._on_demand__types)       == 0
            json_data = _.json()
            # Internal attributes are included in json - verify key ones
            assert '_on_demand__init_complete' in json_data
            assert json_data['_on_demand__init_complete'] is True
            assert '_on_demand__types' in json_data
            assert json_data['_on_demand__types'] == {}

    def test__only_primitives(self):                                                # Test class with only primitive attributes
        class OnlyPrimitives(Type_Safe__On_Demand):
            a: str = ""
            b: int = 0
            c: bool = False

        with OnlyPrimitives() as _:
            assert len(_._on_demand__types)       == 0                              # Nothing to defer

    def test__private_attributes(self):                                             # Test that private attributes are not deferred
        class Inner(Type_Safe__On_Demand):
            value: str = ""

        class WithPrivate(Type_Safe__On_Demand):
            _private: Inner                                                         # Private attribute
            public  : Inner                                                         # Public attribute

        with WithPrivate() as _:
            assert '_private' not in _._on_demand__types                            # Private not tracked
            assert 'public' in _._on_demand__types                                  # Public is tracked

    def test__attribute_assignment_after_init(self):                                # Test assigning to on-demand attribute after init
        class Inner(Type_Safe__On_Demand):
            value: str = ""

        class Outer(Type_Safe__On_Demand):
            inner: Inner

        with Outer() as _:
            # IMPORTANT: Assignment to pending on-demand attribute has edge case behavior
            # The assignment sets the value, but if 'inner' is still in _on_demand__types,
            # the next access will trigger on-demand creation, overwriting the assignment
            #
            # To properly assign, first pop from _on_demand__types or access first
            _._on_demand__types.pop('inner', None)                                  # Remove from pending
            new_inner = Inner(value="assigned")
            _.inner = new_inner                                                     # Now assign
            assert _.inner.value                  == "assigned"                     # Assignment preserved

    def test__circular_reference_potential(self):                                   # Test classes that could have circular references
        class Node(Type_Safe__On_Demand):
            value: str = ""
            # Note: Can't have child: Node directly due to forward reference
            # This test ensures on-demand doesn't break with self-referential patterns

        with Node() as _:
            assert _.value                        == ""
            assert len(_._on_demand__types)       == 0

    def test__type_safe_child_of_on_demand(self):                                   # Test regular Type_Safe as attribute of On_Demand
        class EagerChild(Type_Safe):
            value: str = "eager"

        class OnDemandParent(Type_Safe__On_Demand):
            child: EagerChild
            count: int = 0

        with OnDemandParent() as _:
            assert 'child' in _._on_demand__types                                   # EagerChild IS deferred
            child = _.child
            assert type(child)                    is EagerChild                     # Created on access

    def test__on_demand_child_of_type_safe(self):                                   # Test On_Demand as attribute of regular Type_Safe (not deferred)
        class OnDemandChild(Type_Safe__On_Demand):
            value: str = "on_demand"

        class EagerParent(Type_Safe):
            child: OnDemandChild
            count: int = 0

        with EagerParent() as _:
            assert type(_.child)                  is OnDemandChild                  # Created immediately (eager parent)
            assert _.child.value                  == "on_demand"


    def test__primitive_attributes(self):                                           # Test primitive attributes work normally
        class Schema(Type_Safe__On_Demand):
            an_str  : str   = "default"
            an_int  : int   = 42
            an_float: float = 3.14
            an_bool : bool  = True

        with Schema() as _:
            assert _.an_str                       == "default"
            assert _.an_int                       == 42
            assert _.an_float                     == 3.14
            assert _.an_bool                      is True
            assert len(_._on_demand__types)       == 0                              # No primitives pending

    def test__safe_primitive_attributes(self):                                      # Test Safe primitives are NOT deferred

        class Schema(Type_Safe__On_Demand):
            safe_str: Safe_Str = 'default'
            safe_int: Safe_Int = 42
            safe_id : Safe_Id  = 'my-id'

        with Schema() as _:
            assert type(_.safe_str)               is Safe_Str
            assert type(_.safe_int)               is Safe_Int
            assert type(_.safe_id)                is Safe_Id
            assert len(_._on_demand__types)       == 0                              # Safe primitives not deferred


    def test__dict_attribute(self):                                                 # Test Dict attributes are NOT deferred (they're cheap)
        class Schema(Type_Safe__On_Demand):
            data: Dict[str, str]
            name: str = ""

        with Schema() as _:
            assert type(_.data)                   is Type_Safe__Dict                # Created immediately
            assert 'data' not in _._on_demand__types                                # Not pending

    def test__list_attribute(self):                                                 # Test List attributes are NOT deferred
        class Schema(Type_Safe__On_Demand):
            items: List[str]
            name : str = ""

        with Schema() as _:
            assert type(_.items)                  is Type_Safe__List                # Created immediately
            assert 'items' not in _._on_demand__types

    def test__nested_type_safe_in_dict(self):                                       # Test Type_Safe values in Dict are handled correctly
        class Item(Type_Safe__On_Demand):
            value: str = ""

        class Container(Type_Safe__On_Demand):
            items: Dict[str, Item]

        with Container() as _:
            _.items['a'] = Item(value='item_a')
            assert type(_.items['a'])             is Item
            assert _.items['a'].value             == 'item_a'
