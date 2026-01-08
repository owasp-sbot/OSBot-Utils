# ═══════════════════════════════════════════════════════════════════════════════
# Type_Safe__Config Class Tests
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                         import TestCase
from osbot_utils.type_safe.type_safe_core.config.Type_Safe__Config                    import Type_Safe__Config

class test_Type_Safe__Config(TestCase):

    @classmethod
    def setUpClass(cls):                                                            # Shared test fixtures
        cls.config_default   = Type_Safe__Config()
        cls.config_fast      = Type_Safe__Config.fast_mode()

    # ═══════════════════════════════════════════════════════════════════════════
    # __init__ Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__init__(self):                                                         # Test default initialization
        with Type_Safe__Config() as _:
            assert type(_)               is Type_Safe__Config
            assert _.skip_validation     is False
            assert _.fast_create         is False

    def test__init____with_single_flag(self):                                       # Test initialization with one flag
        with Type_Safe__Config(fast_create=True) as _:
            assert _.fast_create        is True
            assert _.skip_validation     is False

    def test__init____with_multiple_flags(self):                                    # Test initialization with multiple flags
        with Type_Safe__Config(fast_create     = True,
                               skip_validation = True) as _:
            assert _.fast_create        is True
            assert _.skip_validation    is True

    def test__init____with_all_flags(self):                                         # Test all flags enabled
        with Type_Safe__Config(fast_create      = True,
                               skip_validation  = True) as _:
            assert _.fast_create         is True
            assert _.skip_validation     is True

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
        with Type_Safe__Config(fast_create=True) as _:
            assert repr(_) == "Type_Safe__Config(fast_create)"

    def test__repr____with_multiple_flags(self):                                    # Test repr with multiple flags
        with Type_Safe__Config(fast_create=True, skip_validation=True) as _:
            assert "fast_create"    in repr(_)
            assert "skip_validation" in repr(_)

    def test__repr____with_all_flags(self):                                         # Test repr shows all enabled flags
        with Type_Safe__Config.fast_mode() as _:
            repr_str = repr(_)
            assert "fast_create"     in repr_str
            assert "skip_validation"  in repr_str

    # ═══════════════════════════════════════════════════════════════════════════
    # __eq__ Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__eq__(self):                                                           # Test equality with same flags
        config1 = Type_Safe__Config(fast_create=True)
        config2 = Type_Safe__Config(fast_create=True)
        assert config1 == config2

    def test__eq____different_flags(self):                                          # Test inequality with different flags
        config1 = Type_Safe__Config(fast_create=True)
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
            assert _.fast_create       is True
            assert _.skip_validation   is True