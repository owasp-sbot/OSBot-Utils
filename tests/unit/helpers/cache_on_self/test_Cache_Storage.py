from unittest                                          import TestCase
from osbot_utils.helpers.cache_on_self.Cache_Storage   import Cache_Storage
from osbot_utils.helpers.cache_on_self.Cache_On_Self   import Cache_On_Self


class test_Cache_Storage(TestCase):

    def setUp(self):
        self.cache_on_self = Cache_On_Self()
        self.storage = Cache_Storage(self.cache_on_self)

        class TestClass:
            pass

        self.test_instance = TestClass()

    def test__init__(self):
        assert type(self.storage)            is Cache_Storage
        assert self.storage.cache_on_self    == self.cache_on_self

    def test_has_cached_value(self):
        cache_key = '__cache_on_self___test_method__'

        # Initially no cache
        assert self.storage.has_cached_value(self.test_instance, cache_key) is False

        # Add cache entry
        setattr(self.test_instance, cache_key, 'cached_value')
        assert self.storage.has_cached_value(self.test_instance, cache_key) is True

        # Non-existent key
        assert self.storage.has_cached_value(self.test_instance, 'non_existent') is False

    def test_get_cached_value(self):
        cache_key = '__cache_on_self___test_method__'
        expected_value = 'test_cached_value'

        # Set cache value
        setattr(self.test_instance, cache_key, expected_value)

        # Get cached value
        result = self.storage.get_cached_value(self.test_instance, cache_key)
        assert result == expected_value

        # Test with different types
        setattr(self.test_instance, 'int_cache', 42)
        assert self.storage.get_cached_value(self.test_instance, 'int_cache') == 42

        setattr(self.test_instance, 'list_cache', [1, 2, 3])
        assert self.storage.get_cached_value(self.test_instance, 'list_cache') == [1, 2, 3]

    def test_set_cached_value(self):
        cache_key = '__cache_on_self___test_method__'
        value = 'new_cached_value'

        # Initially no attribute
        assert not hasattr(self.test_instance, cache_key)

        # Set cache value
        self.storage.set_cached_value(self.test_instance, cache_key, value)

        # Verify it was set
        assert hasattr(self.test_instance, cache_key)
        assert getattr(self.test_instance, cache_key) == value

        # Overwrite existing value
        new_value = 'updated_value'
        self.storage.set_cached_value(self.test_instance, cache_key, new_value)
        assert getattr(self.test_instance, cache_key) == new_value

    def test_get_all_cache_keys(self):
        # Initially no cache keys
        assert self.storage.get_all_cache_keys(self.test_instance) == []

        # Add some cache entries
        self.test_instance.__cache_on_self___method1__      = 'value1'
        self.test_instance.__cache_on_self___method2_hash__ = 'value2'
        self.test_instance.regular_attribute                = 'not_cache'

        # Get all cache keys
        keys = self.storage.get_all_cache_keys(self.test_instance)

        assert len(keys) == 2
        assert '__cache_on_self___method1__'      in keys
        assert '__cache_on_self___method2_hash__' in keys
        assert 'regular_attribute' not in keys

        # Order doesn't matter, so sort for comparison
        assert sorted(keys) == ['__cache_on_self___method1__', '__cache_on_self___method2_hash__']

    def test_clear_key(self):
        cache_key = '__cache_on_self___test_method__'

        # Set a cached value
        setattr(self.test_instance, cache_key, 'cached_value')
        assert hasattr(self.test_instance, cache_key)

        # Clear specific key
        self.storage.clear_key(self.test_instance, cache_key)
        assert not hasattr(self.test_instance, cache_key)

        # Clear non-existent key (should not raise error)
        self.storage.clear_key(self.test_instance, 'non_existent_key')

    def test_clear_all(self):
        # Set multiple cache entries and regular attributes
        self.test_instance.__cache_on_self___method1__ = 'value1'
        self.test_instance.__cache_on_self___method2_hash_ = 'value2'
        self.test_instance.__cache_on_self___method3_abc123_ = 'value3'
        self.test_instance.regular_attribute = 'keep_this'
        self.test_instance._private_attr = 'keep_this_too'

        # Clear all cache
        self.storage.clear_all(self.test_instance)

        # Verify only cache entries were cleared
        assert not hasattr(self.test_instance, '__cache_on_self___method1__')
        assert not hasattr(self.test_instance, '__cache_on_self___method2_hash_')
        assert not hasattr(self.test_instance, '__cache_on_self___method3_abc123_')
        assert hasattr(self.test_instance, 'regular_attribute')
        assert hasattr(self.test_instance, '_private_attr')

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