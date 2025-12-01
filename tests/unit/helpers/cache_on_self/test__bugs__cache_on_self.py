from unittest                                      import TestCase
from osbot_utils.decorators.methods.cache_on_self  import cache_on_self

class test__bugs__cache_on_self(TestCase):

    def test__bug__weak_reference_cleanup(self):                     # Test that cache is properly cleaned up when instances are garbage collected

        class Temp_Class:
            @cache_on_self
            def method(self, value):
                return value + 1

        # Create instance and cache some values
        temp_obj = Temp_Class()
        cache_manager = temp_obj.method(__return__='cache_on_self')

        # Cache some values
        assert temp_obj.method(1) == 2
        assert temp_obj.method(2) == 3

        # Verify cache exists
        assert len(cache_manager.cache_storage.cache_data          ) == 1
        assert len(cache_manager.cache_storage.cache_data[temp_obj]) == 2

        # Delete instance
        del temp_obj

        import gc
        gc.collect()
        assert len(cache_manager.cache_storage.cache_data) == 1             # BUG: reference is still there


