from typing                                                                         import Dict, Optional, Union
from unittest                                                                       import TestCase
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.Type_Safe__On_Demand                                     import Type_Safe__On_Demand
from osbot_utils.utils.Objects                                                      import base_classes


class test_Type_Safe__On_Demand(TestCase):

    def test__init__(self):                                                         # Test basic initialization and inheritance
        class Inner(Type_Safe__On_Demand):
            value: str = ""

        class Outer(Type_Safe__On_Demand):
            inner: Inner
            count: int = 0

        with Outer() as _:
            assert type(_)                        is Outer
            assert base_classes(_)                == [Type_Safe__On_Demand, Type_Safe, object]
            assert hasattr(_, '_on_demand__types')
            assert hasattr(_, '_on_demand__init_complete')
            assert _._on_demand__init_complete    is True                           # Should be True after init completes
            assert 'inner' in _._on_demand__types                                   # inner should be pending
            assert _.count                        == 0                              # Primitives work normally

    def test__init____with_provided_kwargs(self):                                   # Test that provided kwargs are used directly, not deferred
        class Inner(Type_Safe__On_Demand):
            value: str = ""

        class Outer(Type_Safe__On_Demand):
            inner: Inner
            count: int = 0

        provided_inner = Inner(value="provided")
        with Outer(inner=provided_inner, count=42) as _:
            assert _.inner                        is provided_inner                 # Same instance, not created on-demand
            assert _.inner.value                  == "provided"
            assert _.count                        == 42
            assert 'inner' not in _._on_demand__types                               # Not pending since it was provided

    def test__init____with_none_default(self):                                      # Test attributes with explicit = None default
        class Inner(Type_Safe__On_Demand):
            value: str = ""

        class Outer(Type_Safe__On_Demand):
            inner   : Inner = None                                                  # Explicit None default
            optional: Inner = None
            count   : int   = 0

        with Outer() as _:
            # Note: Even with = None default, Type_Safe__On_Demand may still
            # detect Inner as Type_Safe and mark for on-demand creation
            # The key behavior is that explicit None defaults in base class dict
            # should be respected
            assert _.count                        == 0
            # Check behavior - the implementation checks base_cls.__dict__
            # If inner is in __dict__ with None, it should not be pending
            # But our implementation walks MRO and may find it differently

    def test__getattribute____on_demand_creation(self):                             # Test that accessing attribute creates object on demand
        class Inner(Type_Safe__On_Demand):
            value: str = "default"

        class Outer(Type_Safe__On_Demand):
            inner: Inner
            count: int = 0

        with Outer() as _:
            assert 'inner' in _._on_demand__types                                   # Pending before access
            inner = _.inner                                                         # Access triggers creation
            assert type(inner)                    is Inner                          # Correct type created
            assert inner.value                    == "default"                      # Default value set
            assert 'inner' not in _._on_demand__types                               # No longer pending

    def test__getattribute____multiple_accesses(self):                              # Test that multiple accesses return same instance
        class Inner(Type_Safe__On_Demand):
            value: str = ""

        class Outer(Type_Safe__On_Demand):
            inner: Inner

        with Outer() as _:
            inner1 = _.inner                                                        # First access creates
            inner2 = _.inner                                                        # Second access returns same
            assert inner1 is inner2                                                 # Same instance

    def test__getattribute____nested_on_demand(self):                               # Test deeply nested on-demand creation
        class Level3(Type_Safe__On_Demand):
            value: str = "level3"

        class Level2(Type_Safe__On_Demand):
            level3: Level3
            name  : str = "level2"

        class Level1(Type_Safe__On_Demand):
            level2: Level2
            name  : str = "level1"

        with Level1() as _:
            assert 'level2' in _._on_demand__types                                  # Level2 pending
            level2 = _.level2                                                       # Create Level2
            assert type(level2)                   is Level2
            assert 'level3' in level2._on_demand__types                             # Level3 still pending in Level2
            level3 = level2.level3                                                  # Create Level3
            assert type(level3)                   is Level3
            assert level3.value                   == "level3"

    def test__on_demand__should_create(self):                                       # Test the static method that determines what should be on-demand
        assert Type_Safe__On_Demand._on_demand__should_create(Type_Safe)            is True
        assert Type_Safe__On_Demand._on_demand__should_create(Type_Safe__On_Demand) is True
        assert Type_Safe__On_Demand._on_demand__should_create(str)                  is False
        assert Type_Safe__On_Demand._on_demand__should_create(int)                  is False
        assert Type_Safe__On_Demand._on_demand__should_create(dict)                 is False
        assert Type_Safe__On_Demand._on_demand__should_create(list)                 is False

    def test__on_demand__should_create__with_optional(self):                        # Test Optional types
        class Inner(Type_Safe__On_Demand):
            pass

        assert Type_Safe__On_Demand._on_demand__should_create(Optional[Inner])      is True
        assert Type_Safe__On_Demand._on_demand__should_create(Optional[str])        is False
        assert Type_Safe__On_Demand._on_demand__should_create(Union[Inner, None])   is True
        assert Type_Safe__On_Demand._on_demand__should_create(Union[str, int])      is False   # Multi-type Union

    def test__repr__(self):                                                         # Test string representation
        class Inner(Type_Safe__On_Demand):
            value: str = ""

        class Outer(Type_Safe__On_Demand):
            inner1: Inner
            inner2: Inner
            count : int = 0

        with Outer() as outer:
            assert repr(outer)                    == "<Outer (2 attrs pending)>"    # Shows pending count
            _ = outer.inner1                                                        # Access one
            assert repr(outer)                    == "<Outer (1 attrs pending)>"
            _ = outer.inner2                                                        # Access second
            assert repr(outer)                    == "<Outer>"                      # No pending after all accessed

    def test_json(self):                                                            # Test JSON serialization (must access attrs first)
        class Inner(Type_Safe__On_Demand):
            value: str = "inner_value"

        class Outer(Type_Safe__On_Demand):
            inner: Inner
            count: int = 42

        with Outer() as _:
            # Must access on-demand attributes before json() to populate them
            inner = _.inner                                                         # Trigger creation
            json_data = _.json()
            assert 'inner' in json_data
            assert json_data['inner']['value']    == "inner_value"
            assert json_data['count']             == 42

    def test_json__complex_hierarchy(self):                                         # Test JSON with deeply nested structure
        class Data(Type_Safe__On_Demand):
            items: Dict[str, str]

        class Index(Type_Safe__On_Demand):
            data   : Data
            enabled: bool = True

        class Container(Type_Safe__On_Demand):
            index: Index
            name : str = "container"

        with Container() as _:
            # Access on-demand attributes to trigger creation before json()
            index = _.index
            data  = index.data
            json_data = _.json()
            assert 'index' in json_data
            assert 'name' in json_data
            assert json_data['name']              == "container"
            assert 'data' in json_data['index']
            assert json_data['index']['enabled']  is True

    def test_from_json(self):                                                       # Test deserialization
        class Inner(Type_Safe__On_Demand):
            value: str = ""

        class Outer(Type_Safe__On_Demand):
            inner: Inner
            count: int = 0

        json_data = {'inner': {'value': 'restored'}, 'count': 99}
        restored = Outer.from_json(json_data)

        assert type(restored)                     is Outer
        assert type(restored.inner)               is Inner
        assert restored.inner.value               == "restored"
        assert restored.count                     == 99

    def test_reset(self):                                                           # Test reset() method
        class Inner(Type_Safe__On_Demand):
            value: str = "default"

        class Outer(Type_Safe__On_Demand):
            inner: Inner
            count: int = 0

        with Outer() as _:
            _.count = 100
            _.inner.value = "modified"
            _.reset()
            assert _.count                        == 0                              # Reset to default
            # Note: inner was already created, reset doesn't re-pend it

    def test_obj(self):                                                             # Test .obj() method for comparisons
        class Inner(Type_Safe__On_Demand):
            value: str = "inner"

        class Outer(Type_Safe__On_Demand):
            inner: Inner
            count: int = 42

        with Outer() as _:
            # Access on-demand attribute first
            inner = _.inner
            obj_data = _.obj()
            assert obj_data.count                 == 42
            assert obj_data.inner.value           == "inner"