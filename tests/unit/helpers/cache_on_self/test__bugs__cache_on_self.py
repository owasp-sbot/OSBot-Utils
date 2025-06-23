from unittest                                      import TestCase
from osbot_utils.decorators.methods.cache_on_self  import cache_on_self


# todo: we need to fix these bugs
class test__bugs__cache_on_self(TestCase):

    # todo: double check this test with the one in test__weak_reference_behavior , since on that one the object is being cleaned up
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

    def test__bug__clear_all_affects_other_instances(self):
        """Test that clear_all can affect other instances"""
        class Clear_All_Class:
            def __init__(self, name):
                self.name = name

            @cache_on_self
            def method(self, value):
                return f"{self.name}: {value}"

        obj1 = Clear_All_Class("obj1")
        obj2 = Clear_All_Class("obj2")

        # Cache some data
        assert obj1.method("a") == "obj1: a"
        assert obj1.method("b") == "obj1: b"
        assert obj2.method("x") == "obj2: x"
        assert obj2.method("y") == "obj2: y"

        # Get cache manager and clear obj1's cache
        cache_mgr = obj1.method(__return__='cache_on_self')
        cache_mgr.target_self = obj1
        cache_mgr.clear_all()

        # obj1's cache is cleared
        assert obj1.method("a") == "obj1: a"  # Recomputed

        # obj2's cache is NOT affected (this part works correctly due to WeakKeyDictionary)
        # But the shared cache manager state is problematic

    def test__bug__disabled_flag_affects_all_instances(self):
        """Test that disabled flag would affect all instances"""
        class Disabled_Flag_Class:
            def __init__(self, name):
                self.name = name
                self.compute_count = 0

            @cache_on_self
            def expensive_computation(self):
                self.compute_count += 1
                return f"{self.name} computed {self.compute_count} times"

        obj1 = Disabled_Flag_Class("obj1")
        obj2 = Disabled_Flag_Class("obj2")

        # Initial calls - both cached
        assert obj1.expensive_computation() == "obj1 computed 1 times"
        assert obj1.expensive_computation() == "obj1 computed 1 times"  # Cached
        assert obj2.expensive_computation() == "obj2 computed 1 times"
        assert obj2.expensive_computation() == "obj2 computed 1 times"  # Cached

        # Disable cache via obj1
        cache_mgr = obj1.expensive_computation(__return__='cache_on_self')
        cache_mgr.disabled = True

        # This would affect BOTH instances if the disabled flag was checked!
        # (Currently the disabled flag isn't implemented in handle_call)

    def test__bug__multiple_methods_share_storage(self):
        """Test that different methods on the same class share cache storage"""
        class Multi_Method_Class:
            @cache_on_self
            def method_a(self, value):
                return f"A: {value}"

            @cache_on_self
            def method_b(self, value):
                return f"B: {value}"

        obj = Multi_Method_Class()

        # Call both methods
        assert obj.method_a(1) == "A: 1"
        assert obj.method_b(1) == "B: 1"

        # Get cache managers
        cache_a = obj.method_a(__return__='cache_on_self')
        cache_b = obj.method_b(__return__='cache_on_self')

        # They have different cache managers (good)
        assert cache_a is not cache_b

        # But they could still interfere with each other if not careful
        print(f"\nCache A storage id: {id(cache_a.cache_storage)}")
        print(f"Cache B storage id: {id(cache_b.cache_storage)}")

        # Each method has its own storage (good)
        assert id(cache_a.cache_storage) != id(cache_b.cache_storage)

    def test__bug__security_implications(self):
        """Demonstrate security implications of shared cache manager"""
        class Secure_Service:
            def __init__(self, user_token):
                self.user_token = user_token

            @cache_on_self
            def get_sensitive_data(self, resource_id):
                # Simulate authorization check
                if self.user_token == "admin_token":
                    return f"SECRET: {resource_id}"
                else:
                    return f"Access denied for {resource_id}"

        # Create services for different users
        admin_service = Secure_Service("admin_token")
        user_service = Secure_Service("user_token")

        # Admin accesses secret
        assert admin_service.get_sensitive_data("secret_file") == "SECRET: secret_file"

        # Regular user should be denied
        assert user_service.get_sensitive_data("secret_file") == "Access denied for secret_file"

        # But because they share a cache manager, a malicious user could:
        # 1. Get the cache manager
        cache_mgr = user_service.get_sensitive_data(__return__='cache_on_self')

        # 2. Access the shared cache storage that contains admin's cached data
        print("\nShared cache storage contains:")
        for instance, cache_dict in cache_mgr.cache_storage.cache_data.items():
            print(f"  Token '{instance.user_token}': {list(cache_dict.values())}")

        # The cache storage contains both admin and user data!
        # While they can't directly access each other's cache due to instance keys,
        # the shared state is still a security concern
