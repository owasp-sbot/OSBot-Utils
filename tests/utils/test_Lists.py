from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Lists import list_empty, list_first, list_not_empty, array_add, array_find, array_get, array_pop, \
    array_pop_and_trim, chunks, list_chunks, list_delete, list_lower, tuple_to_list, list_add, list_find, list_get, \
    list_pop, list_pop_and_trim


class test_Lists(TestCase):

    def test_list_add(self):
        array = ['aaa']
        self.assertEqual  (list_add(array,'abc'), 'abc'       )
        self.assertIsNone (list_add(array, None)              )
        self.assertEqual  (array                      ,['aaa','abc'])

    def test_list_find(self):
        array = ['1',2,'3']
        self.assertEqual  (list_find(array, '1' ),  0)
        self.assertEqual  (list_find(array,  2  ),  1)
        self.assertEqual  (list_find(array, '3' ),  2)
        self.assertEqual  (list_find(array, 'a' ), -1)
        self.assertEqual  (list_find(array, None), -1)
        self.assertRaises (Exception, list_find, None, None)
        self.assertRaises (Exception, list_find, 'a', None)

    def test_list_get(self):
        array = ['1',2,'3']
        assert list_get(array,  0  ) == '1'
        assert list_get(array,  1  ) ==  2
        assert list_get(array,  2  ) == '3'
        assert list_get(array, -1  ) is None
        assert list_get(array,  3  ) is None
        assert list_get(array, None) is None
        assert list_get(None , None) is None

    def test_list_pop(self):
        array = ['1',2,'3']
        assert list_pop(array) == '3'
        assert list_pop(array) ==  2
        assert list_pop(array) == '1'
        assert list_pop(array) is None
        assert list_pop(None)  is None
        array = ['1', 2, '3']
        assert list_pop(array, 1) ==  2
        assert list_pop(array, 1) == '3'
        assert list_pop(array, 1) is None
        assert list_pop(array, 0) == '1'
        assert list_pop(array, 0) is None

    def test_list_pop_and_trim(self):
        array = [' 1 ',2,'3']
        assert list_pop_and_trim(array,  1  ) ==  2
        assert list_pop_and_trim(array,   1 ) == '3'
        assert list_pop_and_trim(array,   0 ) == '1'
        assert list_pop_and_trim(array, None) is None

    def test_list_chunks(self):
        array = ['1',2,'3',4 ,'5']
        assert list(list_chunks(array,  0     )) == []
        assert list(list_chunks(array,  1     )) == [['1'], [2], ['3'], [4], ['5']]
        assert list(list_chunks(array,  2     )) == [['1', 2    ], ['3', 4], ['5']]
        assert list(list_chunks(array,  3     )) == [['1', 2,'3'], [ 4 , '5'     ]]

        assert list(list_chunks(array, None   )) == []
        assert type(list_chunks(None , 0)).__name__ == 'generator'
        assert list(list_chunks(None , 0)) == []
        assert list(list_chunks(array, 2)) == list(list_chunks(array, 2))  # test alias
        assert list(list_chunks(array, 3)) == list(list_chunks(array, 3))

    def test_list_delete(self):
        target = ['a', 'b', 'c']
        assert list_delete(target, 'a' ) == [ 'b', 'c']
        assert list_delete(target, 1   ) == [ 'b', 'c']
        assert list_delete(target, 'b' ) == [ 'c'     ]
        assert list_delete(target, None) == ['c'      ]
        assert list_delete(target, 'c' ) == [         ]

    def test_list_empty(self):
        assert list_empty([]   ) is True
        assert list_empty(['a']) is False

    def test_list_first(self):
        assert list_first(['a ','b']             ) is 'a '
        assert list_first(['a', 'b'], strip=True) is 'a'
        assert list_first([]) is None

    def test_list_lower(self):
        assert list_lower(['A','B']) == ['a','b']

    def test_list_not_empty(self):
        assert list_not_empty([]   ) is False
        assert list_not_empty(['a']) is True

    def test_tuple_to_list(self):
        assert tuple_to_list(('a','b')) == ['a','b']
        assert tuple_to_list('a'      ) is None
        assert tuple_to_list(None     ) is None