from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.Call_Flow__Call__Filter                   import Call_Flow__Call__Filter
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config        import Schema__Call_Graph__Config


class test_Call_Flow__Call__Filter(TestCase):                                        # Test call filter

    def test__init__(self):                                                          # Test initialization
        with Call_Flow__Call__Filter() as _:
            assert type(_.config) is Schema__Call_Graph__Config

    def test__is_dunder(self):                                                       # Test dunder detection
        with Call_Flow__Call__Filter() as _:
            assert _.is_dunder('__init__')  is True
            assert _.is_dunder('__str__')   is True
            assert _.is_dunder('_private')  is False
            assert _.is_dunder('public')    is False

    def test__is_private(self):                                                      # Test private detection
        with Call_Flow__Call__Filter() as _:
            assert _.is_private('_private')  is True
            assert _.is_private('_helper')   is True
            assert _.is_private('__init__')  is False                                # Dunder is not private
            assert _.is_private('public')    is False

    def test__is_stdlib(self):                                                       # Test stdlib detection
        with Call_Flow__Call__Filter() as _:
            assert _.is_stdlib('print')   is True
            assert _.is_stdlib('len')     is True
            assert _.is_stdlib('dict')    is True
            assert _.is_stdlib('append')  is True
            assert _.is_stdlib('my_func') is False

    def test__should_skip__dunder(self):                                             # Test dunder filtering
        with Call_Flow__Call__Filter(config=Schema__Call_Graph__Config(include_dunder=False)) as _:
            assert _.should_skip('__init__') is True
            assert _.should_skip('__str__')  is True

        with Call_Flow__Call__Filter(config=Schema__Call_Graph__Config(include_dunder=True)) as _:
            assert _.should_skip('__init__') is False

    def test__should_skip__private(self):                                            # Test private filtering
        with Call_Flow__Call__Filter(config=Schema__Call_Graph__Config(include_private=False)) as _:
            assert _.should_skip('_private') is True

        with Call_Flow__Call__Filter(config=Schema__Call_Graph__Config(include_private=True)) as _:
            assert _.should_skip('_private') is False

    def test__should_skip__stdlib(self):                                             # Test stdlib filtering
        with Call_Flow__Call__Filter(config=Schema__Call_Graph__Config(include_stdlib=False)) as _:
            assert _.should_skip('print') is True
            assert _.should_skip('len')   is True

        with Call_Flow__Call__Filter(config=Schema__Call_Graph__Config(include_stdlib=True)) as _:
            assert _.should_skip('print') is False

    def test__should_include_method(self):                                           # Test method inclusion check
        with Call_Flow__Call__Filter(config=Schema__Call_Graph__Config(include_dunder=False, include_private=True)) as _:
            assert _.should_include_method('public')    is True
            assert _.should_include_method('_private')  is True
            assert _.should_include_method('__init__')  is False

    def test__is_blocked(self):                                                      # Test blocklist
        with Call_Flow__Call__Filter() as _:
            _.config.module_blocklist.append('blocked_module')
            assert _.is_blocked('blocked_module.func') is True
            assert _.is_blocked('allowed.func')        is False

    def test__is_allowed(self):                                                      # Test allowlist
        with Call_Flow__Call__Filter() as _:
            assert _.is_allowed('any_func') is True                                  # No allowlist = allow all

            _.config.module_allowlist.append('allowed_module')
            assert _.is_allowed('allowed_module.func') is True
            assert _.is_allowed('other.func')          is False
