import inspect
import textwrap
import types

from osbot_utils.utils.Files import parent_folder


def function_file(function):
    if isinstance(function, types.FunctionType):
        return inspect.getfile(function)

def function_folder(function):
    if isinstance(function, types.FunctionType):
        return parent_folder(inspect.getfile(function))

def function_name(function):
    if isinstance(function, types.FunctionType):
        return function.__name__


def function_module(function):
    if isinstance(function, types.FunctionType):
        return inspect.getmodule(function)

def function_args(function):
    return inspect.getfullargspec(function)

def function_source_code(function):
    if isinstance(function, types.FunctionType):
        source_code = inspect.getsource(function)
        source_code = textwrap.dedent(source_code).strip()
        return source_code
    elif isinstance(function, str):
        return function
    return None

def module_file(module):
    if isinstance(module, types.ModuleType):
        return inspect.getfile(module)

def module_folder(module):
    if isinstance(module, types.ModuleType):
        return parent_folder(inspect.getfile(module))

def module_full_name(module):
    if isinstance(module, types.ModuleType):
        return module.__name__

def module_name(module):
    if isinstance(module, types.ModuleType):
        return module.__name__.split('.')[-1]
