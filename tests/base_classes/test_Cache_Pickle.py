import types
from unittest import TestCase

from osbot_utils.base_classes.Cache_Pickle import Cache_Pickle
from osbot_utils.decorators.methods.context import context
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, current_temp_folder, pickle_load_from_file
from osbot_utils.utils.Misc import date_time_now, date_now, str_md5


class test_Cache_Pickle(TestCase):

    def setUp(self) -> None:
        self.cache_pickle = Cache_Pickle()

    def test_aaaa(self):
        pass

    def test__init__(self):
        with self.cache_pickle as _:
            assert _._cache_enabled is True
            assert _._cache_files() == []

        assert Cache_Pickle._cache__FOLDER_CACHE_ROOT_FOLDER ==  '_cache_pickle'
        assert Cache_Pickle._cache__SUPPORTED_PARAMS_TYPES   == [int, float, bytearray, bytes, bool, complex, str]


    def test__cache_data(self):
        class An_Class(Cache_Pickle):
            def return_42(self):
                return 42



        an_class = An_Class()
        assert isinstance(an_class , An_Class    )
        assert isinstance(an_class , Cache_Pickle)
        assert an_class._cache_path().endswith('_cache_pickle/test_Cache_Pickle/An_Class')
        assert an_class._cache_clear()   is an_class
        assert an_class._cache_files()  == []
        assert An_Class().return_42() == 42
        cache_files = an_class._cache_files()
        cache_file  = cache_files[0]
        assert cache_file.endswith('_cache_pickle/test_Cache_Pickle/An_Class/return_42.pickle')
        assert len(cache_files) == 1
        assert pickle_load_from_file(cache_file)



    def test__cache_disable(self):
        with self.cache_pickle as _:
            assert _._cache_disable() == _
            self._cache_enabled = False
        return self

    def test__cache_path(self):
        cache_path = self.cache_pickle._cache_path()
        assert folder_exists(cache_path)
        assert cache_path.endswith  ("_cache_pickle/osbot_utils/base_classes/Cache_Pickle")
        assert cache_path.startswith(current_temp_folder())

    def test__cache_kwargs_to_str(self):
        with context(self.cache_pickle._cache_kwargs_to_str) as _:
            assert _({}                   ) == ''
            assert _({'a':1}              ) == 'a:1|'
            assert _({'a':1,'b':2}        ) == 'a:1|b:2|'
            assert _({'a':1,'b':2,'c':3  }) == 'a:1|b:2|c:3|'
            assert _({'aaaaa':'bbbb'     }) == 'aaaaa:bbbb|'
            assert _({'tttt':Cache_Pickle}) == 'tttt:(...)|'            # for the values not in _cache__SUPPORTED_PARAMS_TYPES
            assert _({'nnnn': None       }) == 'nnnn:None|'
            assert _({None: None         }) == 'None:None|'
            assert _({None}               ) == '{None}'
            assert _(''                   ) == ''
            assert _(None                 ) == ''
            assert _(0                    ) == ''
            assert _(1                    ) == '1'
            assert _(str                  ) == "<class 'str'>"

    def test__cache_args_to_str(self):
        with context(self.cache_pickle._cache_args_to_str) as _:
            assert _([]               ) == ''
            assert _([1]              ) == '1|'
            assert _([1,'2']          ) == '1|2|'
            assert _([None]           ) == 'None|'
            assert _([1, None]        ) == '1|None|'
            assert _([1, Cache_Pickle]) == '1|(...)|'                   # for the values not in _cache__SUPPORTED_PARAMS_TYPES
            assert _(None             ) == ''
            assert _(0                ) == ''
            assert _(''               ) == ''
            assert _(1                ) == '1'
            assert _(str              ) == "<class 'str'>"

    def test___cache_resolve_file_name(self):
        def an_function(): pass

        with context(self.cache_pickle._cache_resolve_file_name) as _:
            assert _(an_function              ) == 'an_function.pickle'
            assert _(an_function, None, None  ) == 'an_function.pickle'
            assert _(an_function, []  , None  ) == 'an_function.pickle'
            assert _(an_function, []  , {}    ) == 'an_function.pickle'
            assert _(an_function, [0]         ) == 'an_function_8b879ac2fa.pickle'
            assert _(an_function, [1]         ) == 'an_function_77529b68d1.pickle'
            assert _(an_function, [] , {'a':1}) == 'an_function_e280cf8acd.pickle'
            assert _(an_function, [1], {'a':1}) == 'an_function_77529b68d1_e280cf8acd.pickle'
