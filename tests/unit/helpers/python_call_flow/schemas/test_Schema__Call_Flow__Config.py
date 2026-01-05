# ═══════════════════════════════════════════════════════════════════════════════
# test_Schema__Call_Flow__Config - Tests for config schema
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.utils.Objects                                                       import base_classes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Config          import Schema__Call_Flow__Config
from osbot_utils.helpers.python_call_flow.testing.QA__Call_Flow__Test_Data           import QA__Call_Flow__Test_Data


class test_Schema__Call_Flow__Config(TestCase):                                      # Test config schema

    @classmethod
    def setUpClass(cls):
        cls.qa = QA__Call_Flow__Test_Data()

    def test__init__(self):                                                          # Test initialization
        with Schema__Call_Flow__Config() as _:
            assert type(_)         is Schema__Call_Flow__Config
            assert base_classes(_) == [Type_Safe, object]

    def test__default_values(self):                                                  # Test default config values
        with Schema__Call_Flow__Config() as _:
            assert _.max_depth         == 10
            assert _.include_builtins  == False
            assert _.include_external  == True

    def test__custom_values(self):                                                   # Test custom config values
        with Schema__Call_Flow__Config(max_depth        = 5    ,
                                       include_builtins = True ,
                                       include_external = False) as _:
            assert _.max_depth         == 5
            assert _.include_builtins  == True
            assert _.include_external  == False

    def test__qa_config__default(self):                                              # Test QA default config
        with self.qa as _:
            config = _.create_config__default()

            assert type(config)           is Schema__Call_Flow__Config
            assert config.max_depth       == 10
            assert config.include_builtins == False

    def test__qa_config__shallow(self):                                              # Test QA shallow config
        with self.qa as _:
            config = _.create_config__shallow()

            assert config.max_depth == 1

    def test__qa_config__deep(self):                                                 # Test QA deep config
        with self.qa as _:
            config = _.create_config__deep()

            assert config.max_depth == 20

    def test__qa_config__include_builtins(self):                                     # Test QA builtins config
        with self.qa as _:
            config = _.create_config__include_builtins()

            assert config.include_builtins == True

    def test__qa_config__exclude_external(self):                                     # Test QA exclude external config
        with self.qa as _:
            config = _.create_config__exclude_external()

            assert config.include_external == False

    def test__qa_config__full(self):                                                 # Test QA full options config
        with self.qa as _:
            config = _.create_config__full()

            assert config.max_depth        == 20
            assert config.include_builtins == True
            assert config.include_external == True