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

    def test__bug__reload_next_flag_isolation_between_instances(self):
        """Test that reload_next flag is properly isolated between instances"""
        class Reload_Flag_Class:
            def __init__(self, name):
                self.name = name
                self.call_count = 0

            @cache_on_self
            def method(self):
                self.call_count += 1
                return f"{self.name} call {self.call_count}"

        obj1 = Reload_Flag_Class("obj1")
        obj2 = Reload_Flag_Class("obj2")

        # Initial calls
        assert obj1.method() == "obj1 call 1"
        assert obj2.method() == "obj2 call 1"

        # Set reload_next on obj1's cache manager
        cache1 = obj1.method(__return__='cache_on_self')
        cache2 = obj2.method(__return__='cache_on_self')

        cache1.reload_next = True

        # Verify isolation - obj2 uses cache, obj1 reloads
        assert obj2.method() == "obj2 call 1"   # Cache hit - correct!
        assert obj1.method() != "obj1 call 2"   # Reload triggered          # BUG should be equal
        assert obj1.method() == "obj1 call 1"   # Reload triggered


        # Verify flags
        assert cache1.reload_next is True  # Reset after use            # BUG should be False
        assert cache2.reload_next is False  # Reset after use

