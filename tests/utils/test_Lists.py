from unittest import TestCase

from osbot_utils.utils.Lists import list_empty, list_first, list_not_empty, array_add, array_find, array_get, array_pop, \
    array_pop_and_trim, chunks


class test_Lists(TestCase):

    def test_array_add(self):
        array = ['aaa']
        self.assertEqual  (array_add(array,'abc'), 'abc'       )
        self.assertIsNone (array_add(array, None)              )
        self.assertEqual  (array                      ,['aaa','abc'])

    def test_array_find(self):
        array = ['1',2,'3']
        self.assertEqual  (array_find(array, '1' ),  0)
        self.assertEqual  (array_find(array,  2  ),  1)
        self.assertEqual  (array_find(array, '3' ),  2)
        self.assertEqual  (array_find(array, 'a' ), -1)
        self.assertEqual  (array_find(array, None), -1)
        self.assertRaises (Exception, array_find, None, None)
        self.assertRaises (Exception, array_find, 'a', None)

    def test_array_get(self):
        array = ['1',2,'3']
        assert array_get(array,  0  ) == '1'
        assert array_get(array,  1  ) ==  2
        assert array_get(array,  2  ) == '3'
        assert array_get(array, -1  ) is None
        assert array_get(array,  3  ) is None
        assert array_get(array, None) is None
        assert array_get(None , None) is None

    def test_array_pop(self):
        array = ['1',2,'3']
        assert array_pop(array) == '3'
        assert array_pop(array) ==  2
        assert array_pop(array) == '1'
        assert array_pop(array) is None
        assert array_pop(None)  is None
        array = ['1', 2, '3']
        assert array_pop(array, 1) ==  2
        assert array_pop(array, 1) == '3'
        assert array_pop(array, 1) is None
        assert array_pop(array, 0) == '1'
        assert array_pop(array, 0) is None

    def test_array_pop_and_trim(self):
        array = [' 1 ',2,'3']
        assert array_pop_and_trim(array,  1  ) ==  2
        assert array_pop_and_trim(array,   1 ) == '3'
        assert array_pop_and_trim(array,   0 ) == '1'
        assert array_pop_and_trim(array, None) is None

    def test_chunks(self):
        array = ['1',2,'3',4 ,'5']
        assert list(chunks(array,  2  )) == [['1', 2    ], ['3', 4], ['5']]
        assert list(chunks(array,  3  )) == [['1', 2,'3'], [ 4 , '5'     ]]
        assert list(chunks(array,  0  )) == []
        assert list(chunks(array, None)) == []
        assert type(chunks(None , 0)).__name__ == 'generator'
        assert list(chunks(None , 0)) == []

    def test_list_empty(self):
        assert list_empty([]   ) is True
        assert list_empty(['a']) is False

    def test_list_first(self):
        assert list_first(['a ','b']             ) is 'a '
        assert list_first(['a', 'b'], strip=True) is 'a'
        assert list_first([]) is None

    def test_list_not_empty(self):
        assert list_not_empty([]   ) is False
        assert list_not_empty(['a']) is True