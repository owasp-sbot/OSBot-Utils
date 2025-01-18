from unittest                                                       import TestCase
from osbot_utils.helpers.Random_Guid                                import Random_Guid
from osbot_utils.testing.performance.Performance_Measure__Session   import Performance_Measure__Session
from osbot_utils.type_safe.Type_Safe                                import Type_Safe


class test_Performance_Checks__Session(TestCase):

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

        print()
        Performance_Measure__Session().measure(str        ).print()#.assert_time(  100)
        Performance_Measure__Session().measure(Random_Guid).print()#.assert_time( 6000)
        Performance_Measure__Session().measure(An_Class_1 ).print()#.assert_time(  100)
        Performance_Measure__Session().measure(An_Class_2 ).print()#.assert_time( 6000)
        Performance_Measure__Session().measure(An_Class_3 ).print()#.assert_time(20000)
        Performance_Measure__Session().measure(An_Class_4 ).print()#.assert_time(20000)
        Performance_Measure__Session().measure(An_Class_5 ).print()#.assert_time(20000)
        Performance_Measure__Session().measure(An_Class_6 ).print()#.assert_time(20000)