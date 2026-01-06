# ═══════════════════════════════════════════════════════════════════════════════
# find_type_safe_config Tests
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                      import TestCase
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config import Type_Safe__Config
from osbot_utils.type_safe.type_safe_core.config.static_methods.find_type_safe_config import find_type_safe_config


class test_find_type_safe_config(TestCase):

    # ═══════════════════════════════════════════════════════════════════════════
    # Basic Discovery Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_find_type_safe_config(self):                                           # Test finding config in same frame
        _type_safe_config_ = Type_Safe__Config(skip_validation=True)
        with _type_safe_config_:
            result = find_type_safe_config()
            assert result is _type_safe_config_

    def test_find_type_safe_config__no_config(self):                                # Test when no config exists
        result = find_type_safe_config()
        assert result is None

    def test_find_type_safe_config__parent_frame(self):                             # Test config one level up
        def inner():
            return find_type_safe_config()

        _type_safe_config_ = Type_Safe__Config(skip_setattr=True)
        with _type_safe_config_:
            result = inner()
            assert result                 is _type_safe_config_
            assert result.skip_setattr    is True

    def test_find_type_safe_config__grandparent_frame(self):                        # Test config two levels up
        def level2():
            return find_type_safe_config()
        def level1():
            return level2()

        _type_safe_config_ = Type_Safe__Config(skip_conversion=True)
        with _type_safe_config_:
            result = level1()
            assert result                  is _type_safe_config_
            assert result.skip_conversion  is True

    def test_find_type_safe_config__deeply_nested(self):                            # Test config many levels up
        def level5():
            return find_type_safe_config()
        def level4():
            return level5()
        def level3():
            return level4()
        def level2():
            return level3()
        def level1():
            return level2()

        _type_safe_config_ = Type_Safe__Config.fast_mode()
        with _type_safe_config_:
            result = level1()
            assert result is _type_safe_config_

    # ═══════════════════════════════════════════════════════════════════════════
    # Scope Boundary Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_find_type_safe_config__outside_context(self):                          # Test config gone after context exits
        def check_config():
            return find_type_safe_config()

        def with_context():
            _type_safe_config_ = Type_Safe__Config()
            with _type_safe_config_:
                return check_config()

        inside_result  = with_context()
        outside_result = check_config()

        assert inside_result  is not None
        assert outside_result is None

    def test_find_type_safe_config__nested_contexts(self):                          # Test nested configs - finds innermost
        def check_config():
            return find_type_safe_config()

        _type_safe_config_ = Type_Safe__Config(skip_setattr=True)
        with _type_safe_config_:
            outer_result = check_config()
            assert outer_result.skip_setattr    is True
            assert outer_result.skip_validation is False

            _type_safe_config_ = Type_Safe__Config(skip_validation=True)
            with _type_safe_config_:
                inner_result = check_config()
                assert inner_result.skip_validation is True
                assert inner_result.skip_setattr    is False                        # Different config

    # ═══════════════════════════════════════════════════════════════════════════
    # Variable Name Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_find_type_safe_config__wrong_variable_name(self):                      # Test that wrong name not found
        my_config = Type_Safe__Config()                                             # Wrong name!
        result    = find_type_safe_config()
        assert result is None

    def test_find_type_safe_config__correct_variable_name(self):                    # Test exact variable name required
        type_safe_config = Type_Safe__Config()                                      # Missing underscores
        result1          = find_type_safe_config()
        assert result1 is None

        _type_safe_config_ = Type_Safe__Config()                                    # Correct name
        with _type_safe_config_:
            result2 = find_type_safe_config()
            assert result2 is _type_safe_config_

    # ═══════════════════════════════════════════════════════════════════════════
    # Type Checking Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_find_type_safe_config__none_value(self):                               # Test None value not treated as config
        _type_safe_config_ = None
        result             = find_type_safe_config()
        assert result is None

    def test_find_type_safe_config__wrong_type(self):                               # Test wrong type not found
        _type_safe_config_ = "not a config"
        result             = find_type_safe_config()
        assert result is None

    def test_find_type_safe_config__dict_not_found(self):                           # Test dict with same keys not found
        _type_safe_config_ = {'skip_validation': True}
        result             = find_type_safe_config()
        assert result is None

    # ═══════════════════════════════════════════════════════════════════════════
    # max_depth Parameter Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_find_type_safe_config__respects_max_depth(self):                       # Test max_depth parameter
        def create_deep_stack(depth, func):
            if depth == 0:
                return func()
            return create_deep_stack(depth - 1, func)

        _type_safe_config_ = Type_Safe__Config()
        with _type_safe_config_:
            result = create_deep_stack(5, find_type_safe_config)
            assert result is _type_safe_config_



