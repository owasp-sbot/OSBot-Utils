import base64
import datetime
import os
import sys
import time
import warnings
from unittest import TestCase
from unittest.mock import patch
from dotenv import load_dotenv
from osbot_utils.fluent import Fluent_List
from osbot_utils.utils import Misc
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import Files, file_extension, file_contents, current_folder, folder_exists
from osbot_utils.utils.Misc import bytes_to_base64, base64_to_bytes, date_time_now, class_name, str_to_date, get_value, \
    get_random_color, is_number, none_or_empty, random_filename, random_port, random_number, random_string, \
    random_string_and_numbers, str_md5, random_uuid, trim, to_int, wait, word_wrap, word_wrap_escaped, \
    convert_to_number, remove_html_tags, get_field, last_letter, random_text, random_password, split_lines, \
    under_debugger, base64_to_str, \
    str_sha256, str_to_base64, env_vars_list, env_vars, env_value, flist, ignore_warning__unclosed_ssl, list_set, \
    lower, remove_multiple_spaces, split_spaces, sorted_set, upper, log_to_file, log_debug, log_error, \
    log_info, time_now, str_index, time_str_milliseconds, url_encode, url_decode, obj_dict, obj_items, obj_keys, \
    obj_values, obj_get_value, size


class test_Misc(TestCase):

    def setUp(self):
        load_dotenv()

    def test_array_add(self):
        array = ['aaa']
        self.assertEqual  (Misc.array_add(array,'abc'), 'abc'       )
        self.assertIsNone (Misc.array_add(array, None)              )
        self.assertEqual  (array                      ,['aaa','abc'])

    def test_array_find(self):
        array = ['1',2,'3']
        self.assertEqual  (Misc.array_find(array, '1' ),  0)
        self.assertEqual  (Misc.array_find(array,  2  ),  1)
        self.assertEqual  (Misc.array_find(array, '3' ),  2)
        self.assertEqual  (Misc.array_find(array, 'a' ), -1)
        self.assertEqual  (Misc.array_find(array, None), -1)
        self.assertRaises (Exception, Misc.array_find, None, None)
        self.assertRaises (Exception, Misc.array_find, 'a', None)

    def test_array_get(self):
        array = ['1',2,'3']
        assert Misc.array_get(array,  0  ) == '1'
        assert Misc.array_get(array,  1  ) ==  2
        assert Misc.array_get(array,  2  ) == '3'
        assert Misc.array_get(array, -1  ) is None
        assert Misc.array_get(array,  3  ) is None
        assert Misc.array_get(array, None) is None
        assert Misc.array_get(None , None) is None

    def test_array_pop(self):
        array = ['1',2,'3']
        assert Misc.array_pop(array) == '3'
        assert Misc.array_pop(array) ==  2
        assert Misc.array_pop(array) == '1'
        assert Misc.array_pop(array) is None
        assert Misc.array_pop(None)  is None
        array = ['1', 2, '3']
        assert Misc.array_pop(array, 1) ==  2
        assert Misc.array_pop(array, 1) == '3'
        assert Misc.array_pop(array, 1) is None
        assert Misc.array_pop(array, 0) == '1'
        assert Misc.array_pop(array, 0) is None

    def test_array_pop_and_trim(self):
        array = [' 1 ',2,'3']
        assert Misc.array_pop_and_trim(array,  1  ) ==  2
        assert Misc.array_pop_and_trim(array,   1 ) == '3'
        assert Misc.array_pop_and_trim(array,   0 ) == '1'
        assert Misc.array_pop_and_trim(array, None) is None

    def test_base64_to_bytes__bytes_to_base64(self):
        bytes        = b"\x89PNG__"
        bytes_base64 = "iVBOR19f"
        assert bytes_to_base64(bytes                ) == bytes_base64
        assert base64_to_bytes(bytes_base64         ) == bytes
        assert base64_to_bytes(bytes_base64.encode()) == bytes

    def test_chunks(self):
        array = ['1',2,'3',4 ,'5']
        assert list(Misc.chunks(array,  2  )) == [['1', 2    ], ['3', 4], ['5']]
        assert list(Misc.chunks(array,  3  )) == [['1', 2,'3'], [ 4 , '5'     ]]
        assert list(Misc.chunks(array,  0  )) == []
        assert list(Misc.chunks(array, None)) == []
        assert type(Misc.chunks(None , 0)).__name__ == 'generator'
        assert list(Misc.chunks(None , 0)) == []

    def test_class_name(self):
        assert class_name(TestCase)   == "type"
        assert class_name(TestCase()) == "TestCase"

    def test_date_now(self):
        now = date_time_now(milliseconds_numbers=6)
        assert type(str_to_date(now)) == datetime.datetime

    def test_get_field(self):
        print()
        print(self.__module__)
        assert str(get_field(self, '__module__')) == "test_Misc"
        assert get_field({}, None               ) == None
        assert get_field({}, None, default=42   ) == 42

    def test_get_value(self):
        assert get_value({}, 'a'           ) is None
        assert get_value({}, 'a', 'default') == 'default'
        assert get_value({}, None , 'd'    ) == 'd'
        assert get_value({}, None          ) is None
        assert get_value({'a': 42}, 'a'    ) == 42
        assert get_value(None, 'a'         ) == None

    def test_get_random_color(self):
        assert get_random_color() in ['skyblue', 'darkseagreen', 'palevioletred', 'coral', 'darkgray']

    def test_is_number(self):
        assert is_number      ( 42   ) is True
        assert is_number      ( 4.2  ) is True
        assert is_number      ( -1   ) is True

        assert is_number      ( True ) is False
        assert is_number      ( '42' ) is False
        assert is_number      ( None ) is False

        assert Misc.is_number ( 123  ) is True

        assert Misc.is_number ( '123') is False
        assert Misc.is_number ( 'abc') is False
        assert Misc.is_number ( None ) is False
        assert Misc.is_number ( []) is False

    def test_last_letter(self):
        assert last_letter("abc") == "c"
        assert last_letter(""   ) == None
        assert last_letter(None ) == None

    def test_logger_add_handler__file(self):
        log_file = log_to_file()
        log_debug('debug')
        log_error('error')
        log_info ('info')
        assert file_contents(log_file) == 'error\ninfo\n'

    def test_obj_dict(self):
        class Target:
            def __init__(self):
                self.var_1 = 'the answer'
                self.var_2 = 'is'
                self.var_3 = 42
        assert obj_dict  (Target()) == {'var_1': 'the answer', 'var_2': 'is', 'var_3': 42}
        assert obj_items (Target()) == [('var_1', 'the answer'), ('var_2', 'is'), ('var_3', 42)]
        assert obj_keys  (Target()) == ['var_1', 'var_2', 'var_3']
        assert obj_values(Target()) == ['the answer', 'is', 42]
        target = Target()
        for key,value in obj_items(target):
            assert obj_get_value(target, key          ) == value
            assert obj_get_value(target, key    , 'aa') == value
            assert obj_get_value(target, key+'a', 'aa') == 'aa'

        # check cases when bad data is submitted
        assert obj_dict  ()   == {}
        assert obj_items ()   == []
        assert obj_keys  ()   == []
        assert obj_values()   == []
        assert obj_dict  (42) == {}
        assert obj_items (42) == []
        assert obj_keys  (42) == []
        assert obj_values({}) == []
        assert obj_dict  ({}) == {}
        assert obj_items ({}) == []
        assert obj_keys  ({}) == []
        assert obj_values({}) == []

    def test_none_or_empty(self):
        assert none_or_empty(None, None) is True
        assert none_or_empty(None, 'aa') is True
        assert none_or_empty('aa', None) is True
        assert none_or_empty({}  , 'aa') is True
        assert none_or_empty({'a': 42}, 'b') is True
        assert none_or_empty({'a': 42}, 'a') is False

    def test_size(self):
        assert size(    ) == 0
        assert size(0   ) == 0
        assert size(''  ) == 0
        assert size(None) == 0
        assert size('1' ) == 1
        assert size(1   ) == 0
        assert size('2' ) == 1
        assert size(2   ) == 0
        assert size('22') == 2

        assert size([]   ) == 0
        assert size([0]  ) == 1
        assert size([0,1]) == 2

        assert size({}     ) == 0
        assert size({'a':0}) == 1

    def test_random_filename(self):
        result = random_filename()
        assert len(result) == 14
        assert ".tmp" in result

    def test_random_password(self):
        result = random_password()                 # todo: improve test to also check for the password complexity
        assert len(result) == 24

    def test_random_text(self):
        result = random_text()
        assert len(result) == 17
        assert result[:5] == "text_"

        assert len(random_text(length=37)) == 42
        assert random_text(prefix='abc_')[:4] == "abc_"
        assert random_text(prefix='abc' )[:4] == "abc_"

    def test_split_lines(self):
        text="aaa\nbbbbb\r\ncccc"
        assert split_lines(text) == ['aaa', 'bbbbb','cccc']

    def test_random_filename(self):
        assert len(random_filename())==14
        assert len(random_filename(length=20)) == 24
        assert file_extension(random_filename()) == '.tmp'
        assert file_extension(random_filename(extension='txt' )) == '.txt'
        assert file_extension(random_filename(extension='.txt')) == '.txt'

    def test_def_random_port(self):
        assert 19999 < random_port() < 65001
        assert 19 < random_port(20,22) < 23
        assert 20 < random_port(21, 22) < 23
        assert random_port(20, 20) == 20

    def test_def_random_number(self):
        assert 0 < random_number() < 65001

    def test_def_random_string(self):
        assert len(random_string()) == 8
        assert len(random_string(length=12)) == 12
        assert len(random_string(prefix="prefix_")) == 15
        assert random_string(prefix="prefix_")[:7]  == "prefix_"

    def test_random_string_and_numbers(self):
        assert len(random_string_and_numbers()) == 6

    def test_md5(self):
        assert str_md5('admin') == '21232f297a57a5a743894a0e4a801fc3'
        assert str_md5(None   ) is ''

    def test_sha256(self):
        assert str_sha256('admin') == '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'
        assert str_sha256(None   ) is  None

    def test_random_uuid(self):
        assert len(random_uuid()) == 36
        assert len(random_uuid().split('-')) == 5

    def test_time_now(self):
        assert time_now() in date_time_now(milliseconds_numbers=2)
        assert time_now(milliseconds_numbers=0) in date_time_now(milliseconds_numbers=0)
        assert time_now(milliseconds_numbers=2) in date_time_now(milliseconds_numbers=2)
        assert str_index(time_now(milliseconds_numbers=0), ':') ==  2
        assert str_index(time_now(milliseconds_numbers=3), '.') ==  8
        assert str_index(time_now(milliseconds_numbers=0), '.') == -1

    def test_time_str_milliseconds(self):
        def size_of_milliseconds(target):
            return len(time_str.split('.').pop())
        time_str = time_now(milliseconds_numbers=6)
        assert size_of_milliseconds(time_str                            )== 6
        assert size_of_milliseconds(time_str_milliseconds(time_str,"%f")) == 6

    def test_trim(self):
        assert trim('  aaa  ') == 'aaa'
        assert trim('\naaa\n') == 'aaa'
        assert trim(''       ) == ''
        assert trim('       ') == ''
        assert trim(' \t \n ') == ''
        assert trim(None     ) == ''
        assert trim({}       ) == ''

    def test_to_int(self):
        assert to_int('12'   ) == 12
        assert to_int('aaa'  ) == 0
        assert to_int('aaa',1) == 1

    def test_wait(self):
        delay = 0.001               # time to wait (in seconds)
        start = time.time()
        wait(delay)
        end = time.time()
        assert end - start > delay

    def test_word_wrap(self):
        text = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        assert word_wrap(text) == """AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAALorem ipsum dolor
sit amet, consectetur adipiscing elit,
sed do eiusmod tempor incididunt ut
labore et dolore magna aliqua."""

        assert word_wrap(text, length=60) == """AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed
do eiusmod tempor incididunt ut labore et dolore magna
aliqua."""


    def test_word_wrap_escaped(self):
        text = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
        assert word_wrap_escaped(text) == "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\\nAAAAAAAAAAAAAAAAAAAALorem ipsum dolor\\nsit amet, consectetur adipiscing elit,\\nsed do eiusmod tempor incididunt ut\\nlabore et dolore magna aliqua."

    def test_convert_to_number(self):
        assert convert_to_number("123"   ) == 123
        assert convert_to_number("123.45") == 123.45
        assert convert_to_number("1234.5") == 1234.5
        assert convert_to_number("£123.4") == 123.4
        assert convert_to_number("€123.4") == 123.4
        assert convert_to_number("$123.4") == 123.4

        assert convert_to_number("#123.4") == 0
        assert convert_to_number("1,235" ) == 0
        assert convert_to_number("abc"   ) == 0
        assert convert_to_number(None    ) == 0

    def test_remove_html_tags(self):
        assert remove_html_tags("<b>42</b>"           ) == "42"
        assert remove_html_tags("<a href='abc'>42</a>") == "42"
        assert remove_html_tags("<a href='abc'>42</b>") == "42"

    def test_under_debugger(self):
        if 'pydevd' in sys.modules:
            assert under_debugger() is True
        else:
            assert under_debugger() is False

    def test_base64_to_str_and_str_to_base64(self):
        text = "Lorem Ipsum AAAAAA"
        base64_encoded_string = base64.b64encode(text.encode()).decode()
        assert base64_to_str(base64_encoded_string) == text
        assert str_to_base64(text                 ) == base64_encoded_string

    def test_env_value(self):
        assert env_value("ENV_VAR_1") == "ENV_VAR_1_VALUE"

    def test_env_vars(self):
        os.environ.__setitem__("ENV_VAR_FROM_CODE", "ENV_VAR_FROM_CODE_VALUE")
        loaded_env_vars = env_vars()
        assert loaded_env_vars.get("ENV_VAR_1"        ) == 'ENV_VAR_1_VALUE'
        assert loaded_env_vars.get("ENV_VAR_2"        ) == 'ENV_VAR_2_VALUE'
        assert loaded_env_vars.get("ENV_VAR_FROM_CODE") == 'ENV_VAR_FROM_CODE_VALUE'

    def test_env_vars_list(self):
        assert env_vars_list().__contains__("ENV_VAR_1")
        assert env_vars_list().__contains__("ENV_VAR_2")
        assert env_vars_list() == sorted(set(env_vars()))

    def test_flist(self):
        fluent_list = flist(["element1", "element2"])
        self.assertIsNotNone(fluent_list)
        assert fluent_list.type() == Fluent_List.Fluent_List

    def test_ignore_warning_unclosed_ssl(self):
        with warnings.catch_warnings(record=True) as raisedWarning:
            warnings.simplefilter("always")
            warnings.warn("unclosed.test<ssl.SSLSocket.test>", ResourceWarning)
            assert len(raisedWarning) == 1
        with warnings.catch_warnings(record=True) as ignoredWarning:
            ignore_warning__unclosed_ssl()
            warnings.warn("unclosed.test<ssl.SSLSocket.test>", ResourceWarning)
            assert ignoredWarning == []

    def test_list_set(self):
        test_set = {3, 2, 1}
        sorted_list = list_set(test_set)
        assert sorted_list == sorted(list(test_set))

    def test_lower(self):
        assert lower("ABC#$4abc") == "abc#$4abc"
        assert lower("")          == ""
        assert lower(" ")         == " "

    def test_remove_multiple_spaces(self):
        assert remove_multiple_spaces("")           == ""
        assert remove_multiple_spaces(" ")          == " "
        assert remove_multiple_spaces("a  a  a") == "a a a"

    def test_split_spaces(self):
        assert split_spaces("a b") == ["a", "b"]
        assert split_spaces("")    == [""]

    def test_sorted_set(self):
        assert sorted_set({})              == []
        assert sorted_set({"b", "a", "c"}) == ["a", "b", "c"]

    def test_url_encode(self):
        data = "https://aaa.com?aaaa=bbb&cccc=ddd+eee fff ;/n!@£$%"
        assert url_encode(data) == 'https%3A%2F%2Faaa.com%3Faaaa%3Dbbb%26cccc%3Dddd%2Beee+fff+%3B%2Fn%21%40%C2%A3%24%25'
        assert url_decode(url_encode(data)) == data             # confirm round trip

    def test_upper(self):
        assert upper("abc$#4ABC") == "ABC$#4ABC"
        assert upper("")          == ""
        assert upper(" ")         == " "