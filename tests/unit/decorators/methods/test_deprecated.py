from unittest import TestCase
from unittest.mock import patch, call
from osbot_utils.decorators.methods.depreciated import deprecated


class test_deprecated(TestCase):

    @patch('warnings.warn')
    def test_deprecated__class__no_reason(self, warnings_warn):

        @deprecated
        class An_Class():
            pass

        An_Class()
        assert warnings_warn.call_count == 1
        warnings_warn.assert_has_calls([call('Call to deprecated class An_Class.', category=DeprecationWarning, stacklevel=2)])

    @patch('warnings.warn')
    def test_deprecated__class__with_reason(self, warnings_warn):

        @deprecated("an message")
        class An_Class():
            pass

        An_Class()
        assert warnings_warn.call_count == 1
        warnings_warn.assert_has_calls([call('Call to deprecated class An_Class (an message).', category=DeprecationWarning, stacklevel=2)])

    @patch('warnings.warn')
    def test_deprecated__function__no_reason(self, warnings_warn):

        @deprecated
        def an_function():
            pass

        an_function()
        assert warnings_warn.call_count == 1
        warnings_warn.assert_has_calls([call('Call to deprecated function an_function.', category=DeprecationWarning, stacklevel=2)])

    @patch('warnings.warn')
    def test_deprecated__function__with_reason(self, warnings_warn):

        @deprecated("an message")
        def an_function():
            pass

        an_function()
        assert warnings_warn.call_count == 1
        warnings_warn.assert_has_calls([call('Call to deprecated function an_function (an message).', category=DeprecationWarning, stacklevel=2)])


    def test_deprecated__function___with_bad_message(self):

        try:
            @deprecated(True)
            def an_function():
                pass

        except Exception as exception:
            assert exception.args[0] == "<class 'bool'>"
