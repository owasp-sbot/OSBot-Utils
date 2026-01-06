# ═══════════════════════════════════════════════════════════════════════════════
# Frame Injection Caching Tests
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                         import TestCase
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                    import Type_Safe__Config
from osbot_utils.type_safe.type_safe_core.config.static_methods.find_type_safe_config import find_type_safe_config


class test_find_type_safe_config__caching(TestCase):

    def test_find_type_safe_config__repeated_lookups(self):                         # Test repeated lookups work correctly
        call_count = [0]

        def inner():
            call_count[0] += 1
            return find_type_safe_config()

        _type_safe_config_ = Type_Safe__Config()
        with _type_safe_config_:
            result1 = inner()
            result2 = inner()
            result3 = inner()

            assert result1       is _type_safe_config_
            assert result2       is _type_safe_config_
            assert result3       is _type_safe_config_
            assert call_count[0] == 3

    def test_find_type_safe_config__different_paths(self):                          # Test caching across call paths
        def path_a():
            return find_type_safe_config()
        def path_b():
            return find_type_safe_config()

        _type_safe_config_ = Type_Safe__Config()
        with _type_safe_config_:
            result_a = path_a()
            result_b = path_b()

            assert result_a is _type_safe_config_
            assert result_b is _type_safe_config_

    def test_find_type_safe_config__negative_cache(self):                           # Test "not found" is cached
        def inner():
            return find_type_safe_config()

        result1 = inner()
        result2 = inner()

        assert result1 is None
        assert result2 is None