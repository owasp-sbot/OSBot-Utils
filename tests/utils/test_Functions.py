# currently at 34% code coverage
import types
from inspect import FullArgSpec
from unittest import TestCase

import pytest

from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Env import platform_darwin, env__terminal_xterm, env__not_terminal_xterm
from osbot_utils.utils.Objects import obj_info

from osbot_utils.utils.Files import parent_folder, file_name
from osbot_utils.utils.Functions import function_file, function_folder, function_name, function_module, function_args, \
    function_source_code, get_line_number, is_callable, method_params, module_file, module_folder, module_full_name, \
    module_name, signature, python_file, type_file, function_line_number, method_line_number


class test_Functions(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if env__terminal_xterm():
            pytest.skip('Skipping tests that require terminal_xterm')  # todo: figure out why multiple of these were failing inside docker

    def test_function_args(self):
        assert function_args(test_Functions.test_function_file) == FullArgSpec(args=['self'], varargs=None, varkw=None,
                                                                               defaults=None, kwonlyargs=[],
                                                                               kwonlydefaults=None, annotations={})
        assert function_args(self.test_function_file) is None
        assert function_args("self.test_function_file") is None


    def test_function_file(self):
        assert function_file(test_Functions.test_function_file) == __file__
        assert function_file(self.test_function_file          ) is None
        assert function_file("self.test_function_file"        ) is None

    def test_function_folder(self):
        assert function_folder(test_Functions.test_function_file) == parent_folder(__file__)
        assert function_folder(self.test_function_file          ) is None
        assert function_folder("self.test_function_file"        ) is None

    def test_function_name(self):
        assert function_name(test_Functions.test_function_file) == "test_function_file"
        assert function_name(self.test_function_file          ) is None
        assert function_name("self.test_function_file"        ) is None

    def test_function_module(self):
        module = function_module(test_Functions.test_function_file)
        assert module.__name__                                  == test_Functions.__module__
        assert type(module)                                     is types.ModuleType
        assert function_module(self.test_function_file        ) is None
        assert function_module("self.test_function_file"      ) is None


    def test_function_source_code(self):
        def an_function(): pass
        assert function_source_code(an_function) == "def an_function(): pass"
        assert function_source_code(test_Functions.test_function_file).startswith('def test_function_file(self):\n') is True
        assert function_source_code("aaa") == "aaa"        # this function assumes that if a sting is passed in, it's already source code
        assert function_source_code(42   ) is None
        assert function_source_code(None ) is None

    def test_get_line_number(self):
        assert get_line_number(TestCase) == 345  # these number shouldn't change very ofter
        assert get_line_number(42      ) is None

    def test_is_callable(self):
        assert is_callable(test_Functions.test_function_file) is True
        assert is_callable(self.test_function_file          ) is True
        assert is_callable("self.test_function_file"        ) is False
        assert is_callable(None                             ) is False
        assert is_callable(TestCase                         ) is True

    def test_method_params(self):
        def test_method(a, b: int, c=1, d=2): pass

        assert method_params(self.test_method_params) == {'args': [], 'kwargs': {}}
        assert method_params(test_method            ) == {'args': ['a', 'b'], 'kwargs': {'c': 1, 'd': 2}}

    def test_module_file(self):
        module = function_module(test_Functions.test_function_file)
        assert module_file(module                    ) == __file__
        assert module_file(self.test_function_file   ) is None
        assert module_file("self.test_function_file" ) is None

    def test_module_folder(self):
        module = function_module(test_Functions.test_function_file)
        assert module_folder(module)                    == parent_folder   (__file__)
        assert module_folder(self.test_function_file  ) is None
        assert module_folder("self.test_function_file") is None

    def test_module_full_name(self):
        module = function_module(parent_folder)
        assert module_full_name(module                   ) == "osbot_utils.utils.Files"
        assert module_full_name(self.test_function_file  ) is None
        assert module_full_name("self.test_function_file") is None

    def test_module_name(self):
        module = function_module(parent_folder)
        assert module_name(module                   ) == "Files"
        assert module_name(self.test_function_file  ) is None
        assert module_name("self.test_function_file") is None

    def test_signature(self):
        def test_method(a,b:int,c=1,d=2): pass
        assert signature(test_method)               == {'name'      : 'test_method',
                                                        'parameters': {'a': {'kind': 'POSITIONAL_OR_KEYWORD'},
                                                                       'b': {'annotation': "<class 'int'>",'kind': 'POSITIONAL_OR_KEYWORD'},
                                                                       'c': {'default': 1, 'kind': 'POSITIONAL_OR_KEYWORD'},
                                                                       'd': {'default': 2, 'kind': 'POSITIONAL_OR_KEYWORD'}}}
        assert signature(self.test_function_file  ) == {'name': 'test_function_file', 'parameters': {}}
        assert signature("self.test_function_file") == {}

    def test_python_file(self):
        assert python_file(test_Functions.test_function_file ) == __file__
        assert python_file(test_Functions                    ) == __file__
        assert python_file(self.test_function_file           ) == __file__
        assert python_file("self.test_function_file"         ) is None

    def test_type_file(self):
        assert type_file(test_Functions.test_function_file   ) is None
        assert type_file(test_Functions                      ) == __file__
        assert type_file(self.test_function_file             ) is None
        assert type_file("self.test_function_file"           ) is None

    def test__extra_function_alias(self):
        assert function_line_number == get_line_number
        assert method_line_number   == get_line_number
