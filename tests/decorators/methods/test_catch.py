from unittest import TestCase
from osbot_utils.decorators.methods.catch import catch


class test_catch(TestCase):

    def test_catch(self):

        @catch
        def raise_exception():
            raise Exception('exception raised')

        assert str(raise_exception()) == ("{'status': 'error', 'error': 'exception raised', 'exception': "
                                            "Exception('exception raised')}")