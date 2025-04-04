import pytest
from unittest                                                       import TestCase
from osbot_utils.type_safe.shared.Type_Safe__Cache                  import type_safe_cache
from osbot_utils.utils.Env                                          import in_github_action
from osbot_utils.helpers.Random_Guid                                import Random_Guid
from osbot_utils.testing.performance.Performance_Measure__Session   import Performance_Measure__Session
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class test_Performance_Checks__Session(TestCase):

    @classmethod
    def setUpClass(cls):
        if in_github_action():
           pytest.skip("Skipping tests in Github Actions")
        cls.time_0_ns    =      0
        cls.time_100_ns  =    100
        cls.time_200_ns  =    200
        cls.time_600_ns  =    600
        cls.time_700_ns  =    700
        cls.time_800_ns  =    800
        cls.time_1_kns   =  1_000
        cls.time_2_kns   =  2_000
        cls.time_3_kns   =  3_000
        cls.time_4_kns   =  4_000
        cls.time_5_kns   =  5_000
        cls.time_6_kns   =  6_000
        cls.time_7_kns   =  7_000
        cls.time_8_kns   =  8_000
        cls.time_9_kns   =  9_000
        cls.time_10_kns  = 10_000
        cls.time_20_kns =  20_000

    def test_measure(self):
        class An_Class_1:
            pass

        class An_Class_2(Type_Safe):
            pass

        class An_Class_3(Type_Safe):
            an_int : int

        class An_Class_4(Type_Safe):
            an_int : int = 42

        class An_Class_5(Type_Safe):
            an_str: str

        class An_Class_6(Type_Safe):
            an_str: str = '42'

        type_safe_cache.skip_cache = False

        #print()
        with Performance_Measure__Session(assert_enabled=True) as _:
            _.measure(str        ).assert_time(self.time_100_ns , self.time_0_ns                                                          )
            _.measure(Random_Guid).assert_time(self.time_3_kns  , self.time_4_kns, self.time_5_kns, self.time_6_kns , self.time_7_kns ,  self.time_8_kns                      )
            _.measure(An_Class_1 ).assert_time(self.time_100_ns , self.time_200_ns                                                                                            )
            _.measure(An_Class_2 ).assert_time(self.time_600_ns , self.time_700_ns , self.time_800_ns, self.time_1_kns , self.time_2_kns , self.time_3_kns , self.time_4_kns , self.time_5_kns , self.time_6_kns,  self.time_7_kns   )
            _.measure(An_Class_3 ).assert_time(self.time_1_kns  , self.time_2_kns  , self.time_3_kns , self.time_4_kns , self.time_5_kns ,   self.time_8_kns , self.time_9_kns ,self.time_10_kns, self.time_20_kns                     )
            _.measure(An_Class_4 ).assert_time(self.time_2_kns  , self.time_3_kns , self.time_4_kns , self.time_5_kns ,   self.time_8_kns , self.time_9_kns ,self.time_10_kns, self.time_20_kns                     )
            _.measure(An_Class_5 ).assert_time(self.time_1_kns  , self.time_2_kns  , self.time_3_kns , self.time_4_kns , self.time_5_kns ,   self.time_8_kns , self.time_9_kns ,self.time_10_kns, self.time_20_kns                     )
            _.measure(An_Class_6 ).assert_time(self.time_2_kns  , self.time_3_kns , self.time_4_kns , self.time_5_kns ,   self.time_7_kns , self.time_8_kns ,self.time_9_kns , self.time_10_kns, self.time_20_kns                    )

        #type_safe_cache.print_cache_hits()

# with no cache (and other changes) the results were:
#
#      str          | score:     100 ns  | raw:      78 ns
#      Random_Guid  | score:   6,000 ns  | raw:   5,554 ns
#      An_Class_1   | score:     100 ns  | raw:     131 ns
#      An_Class_2   | score:   9,000 ns  | raw:   8,882 ns
#      An_Class_3   | score:  20,000 ns  | raw:  18,633 ns
#      An_Class_4   | score:  20,000 ns  | raw:  18,801 ns
#      An_Class_5   | score:  20,000 ns  | raw:  18,588 ns
#      An_Class_6   | score:  20,000 ns  | raw:  18,965 ns

    # def test_dissaembly_both_paths(self):
    #     from osbot_utils.type_safe.Cache__Class_Kwargs import Cache__Class_Kwargs
    #     cache__class_kwargs = Cache__Class_Kwargs()
    #     import dis
    #     #dis.dis(Type_Safe.__cls_kwargs__)
    #     dis.dis(type_safe_step_class_kwargs.get_cls_kwargs)
