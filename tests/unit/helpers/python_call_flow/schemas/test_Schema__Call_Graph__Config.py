from unittest                                                                import TestCase
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config import Schema__Call_Graph__Config
from osbot_utils.testing.__                                                  import __
from osbot_utils.type_safe.primitives.core.Safe_UInt                         import Safe_UInt


class test_Schema__Call_Graph__Config(TestCase):                                     # Test config schema

    def test__init__(self):                                                          # Test defaults
        with Schema__Call_Graph__Config() as _:
            assert int(_.max_depth)          == 5
            assert _.include_stdlib          is False
            assert _.include_external        is False
            assert _.include_private         is True
            assert _.include_dunder          is False
            assert _.resolve_self_calls      is True
            assert _.capture_source          is False
            assert _.create_external_nodes   is True
            assert len(_.module_allowlist)   == 0
            assert len(_.module_blocklist)   == 0
            assert len(_.class_allowlist)    == 0
            assert len(_.class_blocklist)    == 0

    def test__obj(self):                                                             # Test full object comparison
        with Schema__Call_Graph__Config() as _:
            assert _.obj() == __(max_depth             = 5     ,
                                 include_private       = True  ,
                                 include_dunder        = False ,
                                 include_stdlib        = False ,
                                 include_external      = False ,
                                 include_inherited     = False ,
                                 module_allowlist      = []    ,
                                 module_blocklist      = []    ,
                                 class_allowlist       = []    ,
                                 class_blocklist       = []    ,
                                 resolve_self_calls    = True  ,
                                 capture_source        = False ,
                                 create_external_nodes = True  )

    def test__with_custom_depth(self):                                               # Test custom max_depth
        with Schema__Call_Graph__Config(max_depth=Safe_UInt(10)) as _:
            assert int(_.max_depth) == 10

    def test__with_include_flags(self):                                              # Test visibility flags
        with Schema__Call_Graph__Config(include_private  = False ,
                                        include_dunder   = True  ,
                                        include_stdlib   = True  ,
                                        include_external = True  ) as _:
            assert _.include_private  is False
            assert _.include_dunder   is True
            assert _.include_stdlib   is True
            assert _.include_external is True

    def test__with_analysis_options(self):                                           # Test analysis option flags
        with Schema__Call_Graph__Config(resolve_self_calls    = False ,
                                        capture_source        = True  ,
                                        create_external_nodes = False ) as _:
            assert _.resolve_self_calls    is False
            assert _.capture_source        is True
            assert _.create_external_nodes is False
