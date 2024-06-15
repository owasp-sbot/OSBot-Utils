from unittest import TestCase

from osbot_utils.utils.Str import trim


class test_Str(TestCase):

    def test_trim(self):
        assert trim('  aaa  ') == 'aaa'
        assert trim('\naaa\n') == 'aaa'
        assert trim(''       ) == ''
        assert trim('       ') == ''
        assert trim(' \t \n ') == ''
        assert trim(None     ) == ''
        assert trim({}       ) == ''
