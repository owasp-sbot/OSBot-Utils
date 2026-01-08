# ═══════════════════════════════════════════════════════════════════════════════
# Test: Type_Safe__Hypothesis_E_v2 - Simplified On-Demand
# Verify the simplified approach works correctly
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                                   import Dict
from unittest                                                                                 import TestCase
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                            import Type_Safe__Config
from osbot_utils.utils.Env                                                                    import not_in_github_action

from Type_Safe__Hypothesis_E_v2                                                               import Type_Safe__Hypothesis_E_v2


# ═══════════════════════════════════════════════════════════════════════════════
# Test Classes
# ═══════════════════════════════════════════════════════════════════════════════

class TS__Inner(Type_Safe__Hypothesis_E_v2):
    value : str = ''
    count : int = 0

class TS__With_One_Nested(Type_Safe__Hypothesis_E_v2):
    inner : TS__Inner
    name  : str = ''

class TS__With_Three_Nested(Type_Safe__Hypothesis_E_v2):
    child1 : TS__Inner
    child2 : TS__Inner
    child3 : TS__Inner
    name   : str = ''

class TS__Level3(Type_Safe__Hypothesis_E_v2):
    data : str = ''

class TS__Level2(Type_Safe__Hypothesis_E_v2):
    level3 : TS__Level3
    value  : int = 0

class TS__Level1(Type_Safe__Hypothesis_E_v2):
    level2 : TS__Level2
    name   : str = ''

class TS__Deep_Nested(Type_Safe__Hypothesis_E_v2):
    level1 : TS__Level1
    count  : int = 0


class test_Type_Safe__Hypothesis_E_v2(TestCase):

    def test__on_demand__attrs_are_none_initially(self):
        """Test that nested attrs are None initially when on_demand_nested=True"""
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_Three_Nested()

            # Use object.__getattribute__ to get raw value (bypass auto-creation)
            raw_child1 = object.__getattribute__(obj, 'child1')
            raw_child2 = object.__getattribute__(obj, 'child2')
            raw_child3 = object.__getattribute__(obj, 'child3')

            assert raw_child1 is None, "child1 should be None initially"
            assert raw_child2 is None, "child2 should be None initially"
            assert raw_child3 is None, "child3 should be None initially"

            # Primitives should still be set
            assert obj.name == '', "name should be set"

    def test__on_demand__access_creates_object(self):       # Test that accessing a None attr creates the object
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_One_Nested()
            # Initially None
            raw_inner = object.__getattribute__(obj, 'inner')
            assert raw_inner is None, "inner should be None initially"

            # Access triggers creation
            inner = obj.inner
            assert inner is not None, "inner should be created on access"
            assert isinstance(inner, TS__Inner), f"inner should be TS__Inner, got {type(inner)}"

            # Now it's set
            raw_inner = object.__getattribute__(obj, 'inner')
            assert raw_inner is not None, "inner should now be set"

    def test__on_demand__deep_nesting_works(self):
        """Test that deep nesting auto-creates at each level"""
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__Deep_Nested()

            # Access deep path - each level should be created
            data = obj.level1.level2.level3.data
            assert data == '', "Deep access should work"

            # Verify all levels were created
            assert obj.level1 is not None
            assert obj.level1.level2 is not None
            assert obj.level1.level2.level3 is not None

    def test__normal_mode__creates_all_upfront(self):
        """Test that normal mode (on_demand_nested=False) creates everything"""
        with Type_Safe__Config(on_demand_nested=False):
            obj = TS__With_Three_Nested()

            # All children should exist immediately
            raw_child1 = object.__getattribute__(obj, 'child1')
            raw_child2 = object.__getattribute__(obj, 'child2')
            raw_child3 = object.__getattribute__(obj, 'child3')

            assert raw_child1 is not None, "child1 should exist"
            assert raw_child2 is not None, "child2 should exist"
            assert raw_child3 is not None, "child3 should exist"

    def test__on_demand__user_provided_kwargs_used(self):
        """Test that user-provided kwargs are used, not replaced with None"""
        with Type_Safe__Config(on_demand_nested=True):
            custom_inner = TS__Inner(value='custom')
            obj = TS__With_One_Nested(inner=custom_inner)

            # Should use the provided value
            assert obj.inner.value == 'custom', "provided inner should be used"

            # Verify it wasn't set to None and then created
            raw_inner = object.__getattribute__(obj, 'inner')
            assert raw_inner is custom_inner, "should be the exact object we provided"

    def test__on_demand__no_tracking_dict_needed(self):
        """Test that v2 doesn't have _on_demand__types dict"""
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_Three_Nested()

            # Should NOT have the tracking dict from v1
            assert not hasattr(obj, '_on_demand__types'), "v2 should not have _on_demand__types"
            assert not hasattr(obj, '_on_demand__init_complete'), "v2 should not have _on_demand__init_complete"

    def test__on_demand__second_access_returns_same_object(self):
        """Test that accessing twice returns the same object"""
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_One_Nested()

            inner1 = obj.inner
            inner2 = obj.inner

            assert inner1 is inner2, "Should return the same object on second access"

    def test__on_demand__json_works(self):
        """Test that JSON serialization works (triggers creation)"""
        with Type_Safe__Config(on_demand_nested=True):
            obj = TS__With_One_Nested(name='test')

            # json() should work and include the nested object
            json_data = obj.json()

            assert 'name' in json_data, "name should be in json"
            assert json_data['name'] == 'test'
            assert 'inner' in json_data, "inner should be in json"