from unittest import TestCase
from osbot_utils.decorators.methods.function_type_check import function_type_check, is_instance_method


#@class_type_check
class An_Class:

    @function_type_check
    def method_1(self, an_int: int, an_string: str, an_bool : bool = False ) -> int:
        #print('---- in method 1')
        return 12

    @function_type_check
    def method_2(self):
        #print('---- in method 2')
        pass

    @function_type_check
    def method_3(self,return_me) -> str:
        return return_me

    @staticmethod
    @function_type_check
    def method_4(an_int : int, an_string:str) -> int:
        return an_int

class test_function_type_check(TestCase):

    def setUp(self) -> None:
        pass

    def test_is_instance_method(self):
        def an_method():
            pass

        an_class = An_Class()
        self.assertFalse(is_instance_method(an_method,[]))
        self.assertTrue (is_instance_method(an_class.method_1, [an_class]))
        self.assertTrue (is_instance_method(an_class.method_2, [an_class]))
        self.assertFalse(is_instance_method(an_class.method_4, []))

    def test_function_type_checker(self):

        def an_method(an_string: str, an_int:int=0, an_bool:bool=False):
            pass

        wrapped_function = function_type_check(an_method)

        wrapped_function('abca')
        wrapped_function('abca', 42)
        wrapped_function('abca', an_bool=False)

        self.assertRaises(Exception, wrapped_function, 12         )
        self.assertRaises(Exception, wrapped_function, 'a','a'    )
        self.assertRaises(Exception, wrapped_function, 'a', False )
        self.assertRaises(Exception, wrapped_function, 'a', 12,'a')

        an_class = An_Class()
        an_class.method_1(12,'b')
        an_class.method_1(12,'b',False)
        an_class.method_2()
        an_class.method_3('a')
        an_class.method_4(12, 'a')

        self.assertRaises(Exception, an_class.method_1, 12         )
        self.assertRaises(Exception, an_class.method_1, 12, 12     )
        self.assertRaises(Exception, an_class.method_1, 12, False  )
        self.assertRaises(Exception, an_class.method_1, 12, 'a','a')
        self.assertRaises(Exception, an_class.method_2, 'a'        )
        self.assertRaises(Exception, an_class.method_3, 12         )
        self.assertRaises(Exception, an_class.method_3, False      )
        self.assertRaises(Exception, an_class.method_3, None       )

    # trying to do this at class level was causing too many side effects
    # def test_class_decorator(self):
    #     an_class = An_Class()
    #     an_class.method_1(12,'b')
    #     an_class.method_1(12,'b')
    #     an_class.method_1(12,'b',False)
    #     an_class.method_2()
    #     an_class.method_3('a')
    #
    #     self.assertRaises(Exception, an_class.method_1, 12         )
    #     self.assertRaises(Exception, an_class.method_1, 12, 12     )
    #     self.assertRaises(Exception, an_class.method_1, 12, False  )
    #     self.assertRaises(Exception, an_class.method_1, 12, 'a','a')
    #     self.assertRaises(Exception, an_class.method_2, 'a'        )
    #     self.assertRaises(Exception, an_class.method_3, 12         )
    #     self.assertRaises(Exception, an_class.method_3, False      )
    #     self.assertRaises(Exception, an_class.method_3, None       )