from unittest import TestCase
from osbot_utils.decorators.methods.capture_status import capture_status, apply_capture_status


class test_capture_status(TestCase):

    def test__capture_status(self):


        @capture_status
        def an_method():
            return 42

        assert an_method() == {'status': 'ok', 'data': 42}

    def test__capture_status__with_exception(self):

        @capture_status
        def an_method():
            raise Exception('test exception')

        assert an_method() == {'status': 'error', 'error': 'test exception'}

    def test__apply_capture_status(self):

        class MyClass:
            def an_method(self):
                return 42

            def another_method(self):
                raise Exception('test exception')

        MyClass = apply_capture_status(MyClass)

        assert MyClass().an_method()      == {'status': 'ok', 'data': 42}
        assert MyClass().another_method() == {'status': 'error', 'error': 'test exception'}