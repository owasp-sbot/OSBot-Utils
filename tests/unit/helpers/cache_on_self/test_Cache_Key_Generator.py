from unittest                                                  import TestCase
from osbot_utils.helpers.cache_on_self.Cache_Key_Generator     import Cache_Key_Generator, CACHE_ON_SELF_TYPES, CACHE_ON_SELF_KEY_PREFIX
from osbot_utils.utils.Misc                                    import str_md5


class test_Cache_Key_Generator(TestCase):

    def setUp(self):
        self.key_generator = Cache_Key_Generator()
        self.test_function = lambda self: "test"
        self.test_function.__name__ = 'test_function'

    def test__init__(self):
        assert type(self.key_generator) is Cache_Key_Generator
        assert self.key_generator.supported_types == CACHE_ON_SELF_TYPES

        # Test with custom types
        custom_types = [str, int]
        custom_gen = Cache_Key_Generator(supported_types=custom_types)
        assert custom_gen.supported_types == custom_types

    def test_generate_key__no_args_no_kwargs(self):
        args = ()
        kwargs = {}

        key = self.key_generator.generate_key(self.test_function, args, kwargs)
        assert key == f'{CACHE_ON_SELF_KEY_PREFIX}_test_function__'

    def test_generate_key__with_args(self):
        args = ('self', 42, 'test')
        kwargs = {}

        # With new format: [index]:<type>:value separated by |
        expected_args_str = '[0]:<str>:self|[1]:<int>:42|[2]:<str>:test'
        expected_hash = str_md5(expected_args_str)

        key = self.key_generator.generate_key(self.test_function, args, kwargs)
        assert key == f'{CACHE_ON_SELF_KEY_PREFIX}_test_function_{expected_hash}_'

    def test_generate_key__with_kwargs(self):
        args = ()
        kwargs = {'key1': 'value1', 'key2': 42}

        # With new format: key:<type>:value| for each kwarg
        expected_kwargs_str = 'key1:<str>:value1|key2:<int>:42'
        expected_hash = str_md5(expected_kwargs_str)

        key = self.key_generator.generate_key(self.test_function, args, kwargs)
        assert key == f'{CACHE_ON_SELF_KEY_PREFIX}_test_function__{expected_hash}'

    def test_generate_key__with_args_and_kwargs(self):
        args = ('self', 100)
        kwargs = {'name': 'test'}

        # With new format including type prefixes
        expected_args_str = '[0]:<str>:self|[1]:<int>:100'
        expected_kwargs_str = 'name:<str>:test'
        expected_args_hash = str_md5(expected_args_str)
        expected_kwargs_hash = str_md5(expected_kwargs_str)

        key = self.key_generator.generate_key(self.test_function, args, kwargs)
        assert key == f'{CACHE_ON_SELF_KEY_PREFIX}_test_function_{expected_args_hash}_{expected_kwargs_hash}'

    def test_args_to_str__supported_types(self):
        # Test with all supported types
        args = (42, 3.14, bytearray(b'test'), b'bytes', True, complex(1, 2), 'string')
        result = self.key_generator.args_to_str(args)
        assert result == "[0]:<int>:42|[1]:<float>:3.14|[2]:<bytearray>:bytearray(b'test')|[3]:<bytes>:b'bytes'|[4]:<bool>:True|[5]:<complex>:(1+2j)|[6]:<str>:string"

        # Test with empty args
        assert self.key_generator.args_to_str(()) == ''
        assert self.key_generator.args_to_str(None) == ''  # None args

    def test_args_to_str__unsupported_types(self):
        # Test with unsupported types (should be ignored)
        obj = object()
        args = ('valid', [1, 2, 3], {'key': 'value'}, None, obj, 'another_valid')
        result = self.key_generator.args_to_str(args)
        assert result == ('[0]:<str>:valid|[1]:<list>:[1,2,3]|[2]:<dict>:[["key","value"]]|[3]:<none>|[4]:other:'
                          f'{obj}|[5]:<str>:another_valid')

    def test_args_to_str__potential_collision(self):
        # These different args produce the same string (collision)
        args1 = (1, 23)
        args2 = (12, 3)
        args3 = (123,)

        assert self.key_generator.args_to_str(args1) == '[0]:<int>:1|[1]:<int>:23'
        assert self.key_generator.args_to_str(args2) == '[0]:<int>:12|[1]:<int>:3'
        assert self.key_generator.args_to_str(args3) == '[0]:<int>:123'

    def test_kwargs_to_str__supported_types(self):
        kwargs = {  'int_val'    : 42           ,
                    'float_val'  : 3.14         ,
                    'str_val'    : 'test'       ,
                    'bool_val'   : False        ,
                    'bytes_val'  : b'data'      ,
                    'complex_val': complex(3, 4)}

        result = self.key_generator.kwargs_to_str(kwargs)
        assert result == ("bool_val:<bool>:False|"
                          "bytes_val:<bytes>:b'data'|"
                          "complex_val:<complex>:(3+4j)|"
                          "float_val:<float>:3.14|"
                          "int_val:<int>:42|"
                          "str_val:<str>:test")


        # Test empty kwargs
        assert self.key_generator.kwargs_to_str({}) == ''
        assert self.key_generator.kwargs_to_str(None) == ''

    def test_kwargs_to_str__unsupported_types(self):
        kwargs = {  'valid': 'string',
                    'list': [1, 2, 3],
                    'dict': {'nested': 'value'},
                    'none': None,
                    'also_valid': 42}

        result = self.key_generator.kwargs_to_str(kwargs)
        assert result == ('also_valid:<int>:42|'
                          'dict:<dict>:[["nested","value"]]|'
                          'list:<list>:[1,2,3]|'
                          'none:<none>|'
                          'valid:<str>:string')


    def test_compute_hash(self):
        # Test hash computation
        test_string = 'test_string'
        expected_hash = str_md5(test_string)

        assert self.key_generator.compute_hash(test_string) == expected_hash

        # Test consistency
        assert self.key_generator.compute_hash('abc') == self.key_generator.compute_hash('abc')
        assert self.key_generator.compute_hash('abc') != self.key_generator.compute_hash('def')

    def test_get_args_hash(self):
        # With hashable args
        args = ('test', 123)
        args_str = self.key_generator.args_to_str(args)
        expected_hash = str_md5(args_str)

        assert self.key_generator.get_args_hash(args) == expected_hash

        # With no hashable args
        args = ([1, 2], {'a': 'b'}, None)
        assert self.key_generator.get_args_hash(args) == '2faf49f97e4130a0675885dcb67f9de5'

        # Empty args
        assert self.key_generator.get_args_hash(()) == ''

    def test_get_kwargs_hash(self):
        # With hashable kwargs
        kwargs = {'name': 'test', 'value': 42}
        kwargs_str = self.key_generator.kwargs_to_str(kwargs)
        expected_hash = str_md5(kwargs_str)

        assert self.key_generator.get_kwargs_hash(kwargs) == expected_hash

        # With no hashable kwargs
        kwargs = {'list': [1, 2], 'none': None}
        assert self.key_generator.get_kwargs_hash(kwargs) == '4ad35c3976fb45c49b40a78926d39eaf'

        # Empty kwargs
        assert self.key_generator.get_kwargs_hash({}) == ''

    def test__custom_supported_types(self):
        # Create generator with only string support
        str_only_gen = Cache_Key_Generator(supported_types=[str])

        args = ('string', 42, 3.14, True)
        result = str_only_gen.args_to_str(args)
        assert result == '[0]:<str>:string|[1]:other:42|[2]:other:3.14|[3]:other:True'

        kwargs = {'str_key': 'value', 'int_key': 123}
        result = str_only_gen.kwargs_to_str(kwargs)
        assert result == 'int_key:other:123|str_key:<str>:value'