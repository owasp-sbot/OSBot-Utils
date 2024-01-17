from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Lists import list_empty, list_first, list_not_empty, array_add, array_find, array_get, array_pop, \
    array_pop_and_trim, chunks, list_chunks, list_delete, list_lower, tuple_to_list, list_add, list_find, list_get, \
    list_pop, list_pop_and_trim, list_contains_list, list_filter, list_filter_starts_with, list_filter_contains, \
    list_get_field, list_group_by, list_index_by, len_list, list_order_by, list_remove, list_remove_list, \
    list_remove_empty, list_set_dict, list_sorted, list_stats, list_to_tuple, list_zip, tuple_replace_position, unique, \
    sys_path_python


class test_Lists(TestCase):

    def test_len_list(self):
        assert len_list(None) == 0
        assert len_list([]  ) == 0
        assert len_list([1] ) == 1
        assert len_list([1,2]) == 2
        assert len_list([1,2,3]) == 3

    def test_list_add(self):
        array = ['aaa']
        self.assertEqual  (list_add(array,'abc'), 'abc'       )
        self.assertIsNone (list_add(array, None)              )
        self.assertEqual  (array                      ,['aaa','abc'])

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

    def test_list_contains_list(self):
        assert list_contains_list(['a','b','c'], ['a','b']) is True
        assert list_contains_list(['a','b','c'], ['a','d']) is False
        assert list_contains_list(['a','b','c'], ['a'    ]) is True
        assert list_contains_list(None , ['a']) is False
        assert list_contains_list(['a'], None ) is False
        assert list_contains_list(None , None ) is False

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

    def test_list_filter(self):
        assert list_filter(['a','b','c'], lambda x: x.startswith('a')) == ['a']
        assert list_filter(['a','b','c'], lambda x: x.startswith('b')) == ['b']

    def test_list_filter_starts_with(self):
        assert list_filter_starts_with(['a' , 'b', 'c' ], 'a') == ['a']
        assert list_filter_starts_with(['a' , 'b', 'c' ], 'b') == ['b']
        assert list_filter_starts_with(['a' , 'b', 'c' ], 'c') == ['c']
        assert list_filter_starts_with(['a1', 'b', 'a2'], 'a') == ['a1','a2']

    def test_list_filter_contains(self):
        assert list_filter_contains(['a' , 'b', 'c' ], 'a') == ['a']
        assert list_filter_contains(['a' , 'b', 'c' ], 'b') == ['b']
        assert list_filter_contains(['a' , 'b', 'c' ], 'c') == ['c']
        assert list_filter_contains(['ca', 'b', 'da'], 'a') == ['ca','da']

    def test_list_find(self):
        array = ['1',2,'3']
        self.assertEqual  (list_find(array, '1' ),  0)
        self.assertEqual  (list_find(array,  2  ),  1)
        self.assertEqual  (list_find(array, '3' ),  2)
        self.assertEqual  (list_find(array, 'a' ), -1)
        self.assertEqual  (list_find(array, None), -1)
        self.assertRaises (Exception, list_find, None, None)
        self.assertRaises (Exception, list_find, 'a', None)

    def test_list_first(self):
        assert list_first(['a ','b']             ) is 'a '
        assert list_first(['a', 'b'], strip=True) is 'a'
        assert list_first([]) is None

    def test_list_get(self):
        array = ['1',2,'3']
        assert list_get(array,  0  ) == '1'
        assert list_get(array,  1  ) ==  2
        assert list_get(array,  2  ) == '3'
        assert list_get(array, -1  ) is None
        assert list_get(array,  3  ) is None
        assert list_get(array, None) is None
        assert list_get(None , None) is None

    def test_list_get_field(self):
        values = [{'a': 1}, {'a': 2}, {'a': 3}]
        assert list_get_field(values=values, field='a' ) == [1, 2, 3]
        assert list_get_field(values=values, field='b' ) == [None, None, None]
        assert list_get_field(values=None  , field='a' ) == []
        assert list_get_field(values=values, field=None) == [None, None, None]

    def test_list_group_by(self):
        assert list_group_by([{'a': 1}, {'a': 2}, {'a': 3}], 'a') == {'1': [{'a': 1}], '2': [{'a': 2}], '3': [{'a': 3}]}
        assert list_group_by([{'a': 1}, {'a': 2}, {'a': 3}], 'b') == {'None': [{'a': 1}, {'a': 2}, {'a': 3}]}
        assert list_group_by(None, 'a') == {}
        assert list_group_by([{'a': 1}, {'a': 2}, {'a': 3}], None) == {'None': [{'a': 1}, {'a': 2}, {'a': 3}]}

    def test_list_index_by(self):
        assert list_index_by([{'a': 1}, {'a': 2}, {'a': 3}], 'a') == {1: {'a': 1}, 2: {'a': 2}, 3: {'a': 3}}
        assert list_index_by([{'a': 1}, {'a': 2}, {'a': 3}], 'b') == {None: {'a': 3}}
        assert list_index_by(None, 'a') == {}
        assert list_index_by([{'a': 1}, {'a': 2}, {'a': 3}], None) == {}

    def test_list_lower(self):
        assert list_lower(['A','B']) == ['a','b']

    def test_list_not_empty(self):
        assert list_not_empty([]   ) is False
        assert list_not_empty(['a']) is True

    def test_list_order_by(self):
        target = [{'a':1, 'b':6}, {'a':2, 'b':5}, {'a':3, 'b':4}, {'a':4, 'b':3}, {'a':5, 'b':2}, {'a':6, 'b':1}]
        assert list_order_by(target, 'a') == [{'a': 1, 'b': 6}, {'a': 2, 'b': 5}, {'a': 3, 'b': 4}, {'a': 4, 'b': 3}, {'a': 5, 'b': 2}, {'a': 6, 'b': 1}]
        assert list_order_by(target, 'b') == [{'a': 6, 'b': 1}, {'a': 5, 'b': 2}, {'a': 4, 'b': 3}, {'a': 3, 'b': 4}, {'a': 2, 'b': 5}, {'a': 1, 'b': 6}]
        assert list_order_by(target, 'a', reverse=True) == [{'a': 6, 'b': 1}, {'a': 5, 'b': 2}, {'a': 4, 'b': 3}, {'a': 3, 'b': 4}, {'a': 2, 'b': 5}, {'a': 1, 'b': 6}]
        assert list_order_by(target, 'b', reverse=True) == [{'a': 1, 'b': 6}, {'a': 2, 'b': 5}, {'a': 3, 'b': 4}, {'a': 4, 'b': 3}, {'a': 5, 'b': 2}, {'a': 6, 'b': 1}]
        assert list_order_by(None, 'a') == []
        assert list_order_by(target, None) == []


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

    def test_list_remove(self):
        assert list_remove(['a', 'b', 'c'], 'a' ) == [ 'b', 'c']
        assert list_remove(['a', 'b', 'c'],  1  ) == ['a', 'b', 'c']
        assert list_remove(['a', 'b', 'c'], 'b' ) == [ 'a', 'c']
        assert list_remove(['a', 'b', 'c'], None) == ['a', 'b', 'c']
        assert list_remove(None, 'a' ) is None
        assert list_remove('a' , 'a' ) == 'a'
        assert list_remove(None, None) is None
        assert list_remove(['a', 'b', 'c'], ['a'    ]) == [ 'b', 'c']
        assert list_remove(['a', 'b', 'c'], ['a','b']) == [ 'c'     ]
        assert list_remove(['a', 'b', 'c'], ['a','c']) == [ 'b'     ]
        assert list_remove(['a', 'b', 'c'], ['b','c']) == [ 'a'     ]

    def test_list_remove_list(self):
        assert list_remove_list(['a', 'b', 'c'], ['a'    ]) == [ 'b', 'c']
        assert list_remove_list(['a', 'b', 'c'], ['a','b']) == [ 'c'     ]
        assert list_remove_list(['a', 'b', 'c'], ['a','c']) == [ 'b'     ]
        assert list_remove_list(['a', 'b', 'c'], ['b','c']) == [ 'a'     ]
        assert list_remove_list(['a', 'b', 'c'], ['a','b','c']) == [        ]
        assert list_remove_list(['a', 'b', 'c'], ['d'    ]) == [ 'a', 'b', 'c']
        assert list_remove_list(['a', 'b', 'c'], ['a','d']) == [ 'b', 'c']
        assert list_remove_list(['a', 'b', 'c'], ['a','b','d']) == [ 'c'     ]
        assert list_remove_list(['a', 'b', 'c'], ['a','b','c','d']) == [        ]
        assert list_remove_list(['a', 'b', 'c'], None) == [ 'a', 'b', 'c']
        assert list_remove_list(None, ['a'    ]) is None
        assert list_remove_list(None, None     ) is None
        
    def test_list_remove_empty(self):
        assert list_remove_empty(['a', '', 'c']) == [ 'a', 'c']
        assert list_remove_empty(['a', 'b', 'c']) == [ 'a', 'b', 'c']
        assert list_remove_empty(['', '', '']) == [        ]
        assert list_remove_empty(None) is None

    def test_list_set_dict(self):
        assert 'tearDownClass' in list_set_dict(TestCase)
        assert list_set_dict(None) == []

    def test_list_sorted(self):
        assert list_sorted([{'a': 1}, {'a': 2}, {'a': 3}], 'a') == [{'a': 1}, {'a': 2}, {'a': 3}]
        assert list_sorted([{'a': 1}, {'a': 2}, {'a': 3}], 'a', descending=True) == [{'a': 3}, {'a': 2}, {'a': 1}]


    def test_list_stats(self):
        assert list_stats(['a','b','c']) == {'a': 1, 'b': 1, 'c': 1}
        assert list_stats(['a','b','a']) == {'a': 2, 'b': 1}
        assert list_stats(None) == {}
        assert list_stats([]) == {}
        assert list_stats(['a','b','c',None]) == {'a': 1, 'b': 1, 'c': 1, None: 1}

    def test_list_to_tuple(self):
        assert list_to_tuple(['a','b']) == ('a','b')
        assert list_to_tuple('a'      ) is None
        assert list_to_tuple(None     ) is None

    def test_list_zip(self):
        assert list_zip([1,2,3],['a','b','c']) == [(1, 'a'), (2, 'b'), (3, 'c')]
        assert list_zip([1,2,3],['a','b'    ]) == [(1, 'a'), (2, 'b')]
        assert list_zip([1,2  ],['a','b','c']) == [(1, 'a'), (2, 'b')]
        assert list_zip([1,2,3],['a'        ]) == [(1, 'a')]
        assert list_zip([1    ],['a','b','c']) == [(1, 'a')]
        assert list_zip([     ],['a','b','c']) == []
        #assert list_zip(None  ,['a','b','c']) == []                    # todo: add support for these scenarios
        #assert list_zip([1,2,3],None        ) == []
        #assert list_zip(None  ,None         ) == []

    def test_sys_path_python(self):
        assert len(sys_path_python('lib/python'   )) > 0
        assert len(sys_path_python('lib/python_2x')) == 0
        assert len(sys_path_python('lib/abc_12345')) == 0

    def test_tuple_to_list(self):
        assert tuple_to_list(('a','b')) == ['a','b']
        assert tuple_to_list('a'      ) is None
        assert tuple_to_list(None     ) is None

    def test_tuple_replace_position(self):
        assert tuple_replace_position(('a','b','c'), 0, 'x') == ('x','b','c')
        assert tuple_replace_position(('a','b','c'), 1, 'x') == ('a','x','c')
        assert tuple_replace_position(('a','b','c'), 2, 'x') == ('a','b','x')
        assert tuple_replace_position(('a','b','c'), 3, 'x') == ('a','b','c')
        assert tuple_replace_position(('a','b','c'), 0, None) == (None,'b','c')
        assert tuple_replace_position(('a','b','c'), 1, None) == ('a',None,'c')
        assert tuple_replace_position(('a','b','c'), 2, None) == ('a','b',None)
        assert tuple_replace_position(('a','b','c'), 3, None) == ('a','b','c')
        assert tuple_replace_position(('a','b','c'), 0, '') == ('','b','c')
        assert tuple_replace_position(('a','b','c'), 1, '') == ('a','','c')
        assert tuple_replace_position(('a','b','c'), 2, '') == ('a','b','')
        assert tuple_replace_position(('a','b','c'), 3, '') == ('a','b','c')
        assert tuple_replace_position(('a','b','c'), 0, 0) == (0,'b','c')
        assert tuple_replace_position(('a','b','c'), 1, 0) == ('a',0,'c')
        assert tuple_replace_position(('a','b','c'), 2, 0) == ('a','b',0)
        assert tuple_replace_position(('a','b','c'), 3, 0) == ('a','b','c')
        assert tuple_replace_position(('a','b','c'), 0, 1) == (1,'b','c')

def test_unique():
    assert unique([1,2,3,4,5,6,7,8,9,0]) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert unique([1,2,3,4,5,6,7,8,9,0,0,0,0,0]) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert unique([1,2,3,4,5,6,7,8,9,0,0,0,0,0,1,2,3,4,5,6,7,8,9]) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


