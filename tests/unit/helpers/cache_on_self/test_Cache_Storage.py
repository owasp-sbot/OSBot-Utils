from unittest                                          import TestCase
from weakref                                           import WeakKeyDictionary
from osbot_utils.helpers.cache_on_self.Cache_Storage   import Cache_Storage


class test_Cache_Storage(TestCase):

    def setUp(self):
        self.storage = Cache_Storage()

        class TestClass:
            pass

        self.test_instance = TestClass()

    def test__init__(self):
        assert type(self.storage) is Cache_Storage
        assert type(self.storage.cache_data) is WeakKeyDictionary
        assert len(self.storage.cache_data) == 0

    def test_has_cached_value(self):
        cache_key = '__cache_on_self___test_method__'

        # Initially no cache
        assert self.storage.has_cached_value(self.test_instance, cache_key) is False

        # Add cache entry internally
        self.storage.set_cached_value(self.test_instance, cache_key, 'cached_value')
        assert self.storage.has_cached_value(self.test_instance, cache_key) is True

        # Non-existent key
        assert self.storage.has_cached_value(self.test_instance, 'non_existent') is False

    def test_get_cached_value(self):
        cache_key = '__cache_on_self___test_method__'
        expected_value = 'test_cached_value'

        # Set cache value internally
        self.storage.set_cached_value(self.test_instance, cache_key, expected_value)

        # Get cached value
        result = self.storage.get_cached_value(self.test_instance, cache_key)
        assert result == expected_value

        # Test with different types
        self.storage.set_cached_value(self.test_instance, 'int_cache', 42)
        assert self.storage.get_cached_value(self.test_instance, 'int_cache') == 42

        self.storage.set_cached_value(self.test_instance, 'list_cache', [1, 2, 3])
        assert self.storage.get_cached_value(self.test_instance, 'list_cache') == [1, 2, 3]

    def test_set_cached_value(self):
        cache_key = '__cache_on_self___test_method__'
        value = 'new_cached_value'

        # Initially no cache entry
        assert not self.storage.has_cached_value(self.test_instance, cache_key)

        # Set cache value
        self.storage.set_cached_value(self.test_instance, cache_key, value)

        # Verify it was set
        assert self.storage.has_cached_value(self.test_instance, cache_key)
        assert self.storage.get_cached_value(self.test_instance, cache_key) == value

        # Overwrite existing value
        new_value = 'updated_value'
        self.storage.set_cached_value(self.test_instance, cache_key, new_value)
        assert self.storage.get_cached_value(self.test_instance, cache_key) == new_value

    def test_get_all_cache_keys(self):
        # Initially no cache keys
        assert self.storage.get_all_cache_keys(self.test_instance) == []

        # Add some cache entries
        self.storage.set_cached_value(self.test_instance, '__cache_on_self___method1__', 'value1')
        self.storage.set_cached_value(self.test_instance, '__cache_on_self___method2_hash__', 'value2')

        # Get all cache keys
        keys = self.storage.get_all_cache_keys(self.test_instance)

        assert len(keys) == 2
        assert '__cache_on_self___method1__' in keys
        assert '__cache_on_self___method2_hash__' in keys

        # Order doesn't matter, so sort for comparison
        assert sorted(keys) == ['__cache_on_self___method1__', '__cache_on_self___method2_hash__']

    def test_clear_key(self):
        cache_key = '__cache_on_self___test_method__'

        # Set a cached value
        self.storage.set_cached_value(self.test_instance, cache_key, 'cached_value')
        assert self.storage.has_cached_value(self.test_instance, cache_key)

        # Clear specific key
        self.storage.clear_key(self.test_instance, cache_key)
        assert not self.storage.has_cached_value(self.test_instance, cache_key)

        # Clear non-existent key (should not raise error)
        self.storage.clear_key(self.test_instance, 'non_existent_key')

    def test_clear_all(self):
        # Set multiple cache entries
        self.storage.set_cached_value(self.test_instance, '__cache_on_self___method1__', 'value1')
        self.storage.set_cached_value(self.test_instance, '__cache_on_self___method2_hash_', 'value2')
        self.storage.set_cached_value(self.test_instance, '__cache_on_self___method3_abc123_', 'value3')

        # Clear all cache
        self.storage.clear_all(self.test_instance)

        # Verify all cache entries were cleared
        assert not self.storage.has_cached_value(self.test_instance, '__cache_on_self___method1__')
        assert not self.storage.has_cached_value(self.test_instance, '__cache_on_self___method2_hash_')
        assert not self.storage.has_cached_value(self.test_instance, '__cache_on_self___method3_abc123_')

        # Verify get_all_cache_keys returns empty
        assert self.storage.get_all_cache_keys(self.test_instance) == []

    def test__edge_cases(self):
        # Test with None values
        self.storage.set_cached_value(self.test_instance, 'none_cache', None)
        assert self.storage.get_cached_value(self.test_instance, 'none_cache') is None
        assert self.storage.has_cached_value(self.test_instance, 'none_cache') is True

        # Test with complex objects
        complex_obj = {'key': [1, 2, 3], 'nested': {'data': 'value'}}
        self.storage.set_cached_value(self.test_instance, 'complex_cache', complex_obj)
        retrieved = self.storage.get_cached_value(self.test_instance, 'complex_cache')
        assert retrieved == complex_obj
        assert retrieved is complex_obj  # Same object reference

    def test__weak_reference_behavior(self):
        """Test that WeakKeyDictionary properly cleans up when instances are deleted"""
        class TempClass:
            pass

        # Create instance and cache some data
        temp_instance = TempClass()
        self.storage.set_cached_value(temp_instance, 'key1', 'value1')
        self.storage.set_cached_value(temp_instance, 'key2', 'value2')

        # Verify data exists
        assert self.storage.has_cached_value(temp_instance, 'key1')
        assert len(self.storage.cache_data[temp_instance]) == 2  # test_instance and temp_instance

        # Delete the instance
        #instance_id = id(temp_instance)
        del temp_instance

        # Force garbage collection (in real scenarios this happens automatically)
        #import gc              # looks like we don't need this in the test
        #gc.collect()

        # Cache data for deleted instance should be gone
        assert len(self.storage.cache_data) == 0 # and there should be nothing left in the weak dict

    def test__multiple_instances_isolation(self):
        """Test that cache is properly isolated between instances"""
        class TestClass:
            pass

        instance1 = TestClass()
        instance2 = TestClass()

        # Set different values for same key on different instances
        self.storage.set_cached_value(instance1, 'shared_key', 'value_from_instance1')
        self.storage.set_cached_value(instance2, 'shared_key', 'value_from_instance2')

        # Verify isolation
        assert self.storage.get_cached_value(instance1, 'shared_key') == 'value_from_instance1'
        assert self.storage.get_cached_value(instance2, 'shared_key') == 'value_from_instance2'

        # Clear instance1's cache
        self.storage.clear_all(instance1)

        # instance2's cache should be unaffected
        assert not self.storage.has_cached_value(instance1, 'shared_key')
        assert self.storage.has_cached_value(instance2, 'shared_key')
        assert self.storage.get_cached_value(instance2, 'shared_key') == 'value_from_instance2'

    def test__no_instance_pollution(self):
        """Verify that cache storage doesn't modify the instance's __dict__"""
        class CleanClass:
            def __init__(self):
                self.my_attr = 'original'

        clean_instance = CleanClass()
        original_dict = dict(clean_instance.__dict__)

        # Add multiple cache entries
        self.storage.set_cached_value(clean_instance, 'cache_key_1', 'value1')
        self.storage.set_cached_value(clean_instance, 'cache_key_2', 'value2')
        self.storage.set_cached_value(clean_instance, '__cache_on_self___method__', 'value3')

        # Instance __dict__ should be unchanged
        assert clean_instance.__dict__ == original_dict
        assert clean_instance.__dict__ == {'my_attr': 'original'}

        # But cache should exist in storage
        assert len(self.storage.get_all_cache_keys(clean_instance)) == 3