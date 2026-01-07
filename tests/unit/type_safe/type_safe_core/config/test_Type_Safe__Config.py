# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Config Class Tests
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                         import TestCase
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                    import Type_Safe__Config
#from osbot_utils.type_safe.type_safe_core.config.static_methods.find_type_safe_config import TYPE_SAFE__CONFIG__VAR_NAME, TYPE_SAFE__CONFIG__CHECKED_VAR, TYPE_SAFE__CONFIG__MAX_DEPTH


class test_Type_Safe__Config(TestCase):

    @classmethod
    def setUpClass(cls):                                                            # Shared test fixtures
        cls.config_default   = Type_Safe__Config()
        cls.config_fast      = Type_Safe__Config.fast_mode()
        cls.config_on_demand = Type_Safe__Config.on_demand_mode()
        cls.config_bulk      = Type_Safe__Config.bulk_load_mode()

    # ═══════════════════════════════════════════════════════════════════════════
    # __init__ Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                         # Test default initialization
        with Type_Safe__Config() as _:
            assert type(_)               is Type_Safe__Config
            assert _.skip_setattr        is False
            assert _.skip_validation     is False
            assert _.skip_conversion     is False
            assert _.skip_mro_walk       is False
            assert _.on_demand_nested    is False
            assert _.fast_collections    is False

    def test__init____with_single_flag(self):                                       # Test initialization with one flag
        with Type_Safe__Config(skip_setattr=True) as _:
            assert _.skip_setattr        is True
            assert _.skip_validation     is False
            assert _.skip_conversion     is False

    def test__init____with_multiple_flags(self):                                    # Test initialization with multiple flags
        with Type_Safe__Config(skip_setattr    = True,
                               skip_validation = True) as _:
            assert _.skip_setattr        is True
            assert _.skip_validation     is True
            assert _.skip_conversion     is False
            assert _.skip_mro_walk       is False

    def test__init____with_all_flags(self):                                         # Test all flags enabled
        with Type_Safe__Config(skip_setattr     = True,
                               skip_validation  = True,
                               skip_conversion  = True,
                               skip_mro_walk    = True,
                               on_demand_nested = True,
                               fast_collections = True) as _:
            assert _.skip_setattr        is True
            assert _.skip_validation     is True
            assert _.skip_conversion     is True
            assert _.skip_mro_walk       is True
            assert _.on_demand_nested    is True
            assert _.fast_collections    is True

    # ═══════════════════════════════════════════════════════════════════════════
    # Context Manager Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__enter__(self):                                                        # Test __enter__ returns self
        config = Type_Safe__Config()
        result = config.__enter__()
        assert result is config

    def test__exit__(self):                                                         # Test __exit__ returns False (no exception suppression)
        config = Type_Safe__Config()
        result = config.__exit__(None, None, None)
        assert result is False

    def test__exit____with_exception(self):                                         # Test exceptions propagate through context
        class TestException(Exception):
            pass

        def raise_in_context():
            _type_safe_config_ = Type_Safe__Config()
            with _type_safe_config_:
                raise TestException("test")

        with self.assertRaises(TestException):
            raise_in_context()

    # ═══════════════════════════════════════════════════════════════════════════
    # __repr__ Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__repr__(self):                                                         # Test repr with no flags
        with Type_Safe__Config() as _:
            assert repr(_) == "Type_Safe__Config(default)"

    def test__repr____with_single_flag(self):                                       # Test repr with one flag
        with Type_Safe__Config(skip_setattr=True) as _:
            assert repr(_) == "Type_Safe__Config(skip_setattr)"

    def test__repr____with_multiple_flags(self):                                    # Test repr with multiple flags
        with Type_Safe__Config(skip_setattr=True, skip_validation=True) as _:
            assert "skip_setattr"    in repr(_)
            assert "skip_validation" in repr(_)
            assert "skip_conversion" not in repr(_)

    def test__repr____with_all_flags(self):                                         # Test repr shows all enabled flags
        with Type_Safe__Config.fast_mode() as _:
            repr_str = repr(_)
            assert "skip_setattr"     in repr_str
            assert "skip_validation"  in repr_str
            assert "skip_conversion"  in repr_str
            assert "skip_mro_walk"    in repr_str
            assert "fast_collections" in repr_str

    # ═══════════════════════════════════════════════════════════════════════════
    # __eq__ Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__eq__(self):                                                           # Test equality with same flags
        config1 = Type_Safe__Config(skip_setattr=True)
        config2 = Type_Safe__Config(skip_setattr=True)
        assert config1 == config2

    def test__eq____different_flags(self):                                          # Test inequality with different flags
        config1 = Type_Safe__Config(skip_setattr=True)
        config2 = Type_Safe__Config(skip_validation=True)
        assert config1 != config2

    def test__eq____with_non_config(self):                                          # Test inequality with non-config types
        with Type_Safe__Config() as _:
            assert _ != "not a config"
            assert _ != None
            assert _ != 42
            assert _ != {'skip_validation': True}

    # ═══════════════════════════════════════════════════════════════════════════
    # __slots__ Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__slots__(self):                                                        # Test __slots__ prevents arbitrary attributes
        with Type_Safe__Config() as _:
            with self.assertRaises(AttributeError):
                _.arbitrary_attribute = True

    # ═══════════════════════════════════════════════════════════════════════════
    # Factory Method Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test_fast_mode(self):                                                       # Test fast_mode factory
        with Type_Safe__Config.fast_mode() as _:
            assert _.skip_setattr      is True
            assert _.skip_validation   is True
            assert _.skip_conversion   is True
            assert _.skip_mro_walk     is True
            assert _.fast_collections  is True
            assert _.on_demand_nested  is False                                     # Not part of fast_mode

    def test_on_demand_mode(self):                                                  # Test on_demand_mode factory
        with Type_Safe__Config.on_demand_mode() as _:
            assert _.on_demand_nested  is True
            assert _.skip_setattr      is False                                     # Only on_demand enabled
            assert _.skip_validation   is False
            assert _.skip_conversion   is False

    def test_bulk_load_mode(self):                                                  # Test bulk_load_mode factory
        with Type_Safe__Config.bulk_load_mode() as _:
            assert _.skip_setattr      is True
            assert _.skip_validation   is True
            assert _.skip_conversion   is True
            assert _.skip_mro_walk     is False                                     # Not part of bulk_load
            assert _.on_demand_nested  is False






    # todo: refactor these tests to respective test file

    # ═══════════════════════════════════════════════════════════════════════════════
    # Constants Tests
    # ═══════════════════════════════════════════════════════════════════════════════


    # def test_TYPE_SAFE__CONFIG__VAR_NAME(self):                                     # Test variable name constant
    #     assert TYPE_SAFE__CONFIG__VAR_NAME == '_type_safe_config_'
    #
    # def test_TYPE_SAFE__CONFIG__CHECKED_VAR(self):                                  # Test checked marker constant
    #     assert TYPE_SAFE__CONFIG__CHECKED_VAR == '_type_safe_config__checked_'
    #
    # def test_TYPE_SAFE__CONFIG__MAX_DEPTH(self):                                    # Test max depth constant
    #     assert TYPE_SAFE__CONFIG__MAX_DEPTH == 15
    #     assert TYPE_SAFE__CONFIG__MAX_DEPTH > 0