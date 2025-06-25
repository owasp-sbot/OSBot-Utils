from unittest                                      import TestCase
from osbot_utils.decorators.methods.cache_on_self  import cache_on_self


class test__security__cache_on_self(TestCase):

    def test__security__cache_key_collision_exploit(self):
        """Test how cache key collisions could be exploited"""
        class Auth_Class:
            @cache_on_self
            def check_permission(self, user_id, resource_id):
                # Simulate permission check
                if user_id == "admin" and resource_id == "secret":
                    return "granted"
                return "denied"

        obj = Auth_Class()

        # Admin checks permission (gets cached)
        assert obj.check_permission("admin", "secret") == "granted"

        # Due to collision bug, attacker could craft args that produce same cache key
        # For example, if they know the concatenated string is "adminsecret"
        assert obj.check_permission("admins", "ecret") == "denied"  # FIXED: BUG: Security issue!
        assert obj.check_permission("ad", "minsecret") == "denied"  # FIXED: BUG: Security issue!

    def test__security__no_direct_cache_access(self):
        """Verify that external code cannot directly access or modify the cache"""
        class Protected_Class:
            @cache_on_self
            def sensitive_method(self, token):
                return f"authenticated with {token}"

        obj = Protected_Class()

        # Use the method normally
        result = obj.sensitive_method("secret123")
        assert result == "authenticated with secret123"

        # Instance should have no cache-related attributes
        cache_attrs = [attr for attr in obj.__dict__ if 'cache' in attr.lower()]
        assert cache_attrs == []

        # Cannot access cache directly through instance
        assert not hasattr(obj, '__cache_on_self___sensitive_method__')

    def test__security__cache_manager_access_control(self):
        """Test that cache manager access requires explicit request"""
        class Controlled_Class:
            @cache_on_self
            def method(self, value):
                return value * 2

        obj = Controlled_Class()

        # Normal call doesn't expose cache manager
        result = obj.method(5)
        assert result == 10
        assert type(result) is int

        # Cache manager only available with special parameter
        cache_manager = obj.method(__return__='cache_on_self')
        assert cache_manager.__class__.__name__ == 'Cache_On_Self'

        # But this doesn't affect normal operation
        assert obj.method(5) == 10

    def test__security__cache_isolation_between_instances(self):
        """Ensure one instance cannot access another's cache"""
        class User_Class:
            def __init__(self, user_id):
                self.user_id = user_id

            @cache_on_self
            def get_private_data(self):
                return f"private data for {self.user_id}"

        user1 = User_Class("alice")
        user2 = User_Class("bob"  )

        # Each user gets their own data
        assert user1.get_private_data() == "private data for alice"
        assert user2.get_private_data() == "private data for bob"

        # Get cache managers
        cache1 = user1.get_private_data(__return__='cache_on_self')
        cache2 = user2.get_private_data(__return__='cache_on_self')

        # Different cache managers
        assert cache1 != cache2                                 # these should be different
        assert cache1 is not cache2                             # these should be different

        # But even if we had access to cache1, we can't access user2's data
        assert user1 not in cache2.cache_storage.cache_data
        assert user2 not in cache1.cache_storage.cache_data