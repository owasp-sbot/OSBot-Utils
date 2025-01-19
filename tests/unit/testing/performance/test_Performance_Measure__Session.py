from unittest                                                       import TestCase
from osbot_utils.helpers.Random_Guid                                import Random_Guid
from osbot_utils.testing.performance.Performance_Measure__Session   import Performance_Measure__Session
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class test_Performance_Checks__Session(TestCase):

    @classmethod
    def setUpClass(cls):

        cls.time_100_ns  =    100
        cls.time_5_kns   =  5_000
        cls.time_6_kns   =  6_000
        cls.time_10_kns  = 10_000
        cls.time_20_kns =  20_000

    def test_measure(self):
        class An_Class_1():
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


        Performance_Measure__Session().measure(str        ).print().assert_time(self.time_100_ns                    )
        Performance_Measure__Session().measure(Random_Guid).print().assert_time(self.time_5_kns, self.time_6_kns    )
        Performance_Measure__Session().measure(An_Class_1 ).print().assert_time(self.time_100_ns                    )
        Performance_Measure__Session().measure(An_Class_2 ).print().assert_time(self.time_5_kns , self.time_6_kns   )
        Performance_Measure__Session().measure(An_Class_3 ).print().assert_time(self.time_10_kns, self.time_20_kns  )
        Performance_Measure__Session().measure(An_Class_4 ).print().assert_time(self.time_10_kns, self.time_20_kns  )
        Performance_Measure__Session().measure(An_Class_5 ).print().assert_time(self.time_10_kns, self.time_20_kns  )
        Performance_Measure__Session().measure(An_Class_6 ).print().assert_time(self.time_10_kns, self.time_20_kns  )

    # def test_dissaembly_both_paths(self):
    #     from osbot_utils.type_safe.Cache__Class_Kwargs import Cache__Class_Kwargs
    #     cache__class_kwargs = Cache__Class_Kwargs()
    #     import dis
    #     #dis.dis(Type_Safe.__cls_kwargs__)
    #     dis.dis(type_safe_step_class_kwargs.get_cls_kwargs)