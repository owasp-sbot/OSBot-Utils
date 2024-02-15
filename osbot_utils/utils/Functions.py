import builtins
import inspect
import textwrap
import types

from osbot_utils.utils.Files import parent_folder

def function_args(function):
    if isinstance(function, types.FunctionType):
        return inspect.getfullargspec(function)

def function_file(function):
    if isinstance(function, types.FunctionType):
        return inspect.getfile(function)

def function_folder(function):
    if isinstance(function, types.FunctionType):
        return parent_folder(inspect.getfile(function))

def function_module(function):
    if isinstance(function, types.FunctionType):
        return inspect.getmodule(function)

def function_name(function):
    if isinstance(function, types.FunctionType):
        return function.__name__

def function_source_code(function):
    if isinstance(function, types.FunctionType):
        source_code = inspect.getsource(function)
        source_code = textwrap.dedent(source_code).strip()
        return source_code
    elif isinstance(function, str):
        return function
    return None

def get_line_number(function):
    try:
        code, line  = inspect.getsourcelines(function)
        return line
    except Exception:
        return None

def is_callable(target):
    return callable(target)

def method_params(target):
    params = {}
    method_signature = signature(target)
    if method_signature:
        parameters = method_signature.get('parameters')
        args = []
        kwargs = {}
        for name, data in parameters.items():
            if 'default' in set(data):
                kwargs[name] = data['default']
            else:
                args.append(name)
        params['args'  ] = args
        params['kwargs'] = kwargs
    return params


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

# todo Improve this method to return more usefull set of data (like an signature str,better view of the param.kind, annotations )
def signature(callable_obj):
    if not isinstance(callable_obj, (types.FunctionType, types.MethodType)):
        return {}

    signature = inspect.signature(callable_obj)
    parameters = {}
    sig_dict = { 'name'      : callable_obj.__name__,
                 'parameters': parameters           }

    for name, param in signature.parameters.items():
        value = {'kind'      : str(param.kind)}
        if param.default is not inspect.Parameter.empty:
            value['default'] = param.default

        if param.annotation is not inspect.Parameter.empty:
            value['annotation'] = str(param.annotation)

        sig_dict['parameters'][name] = value
    return sig_dict

def python_file(target):
    if isinstance(target, type) or type(target) in [types.ModuleType , types.MethodType,
                                                    types.FunctionType, types.TracebackType,
                                                    types.FrameType, types.CodeType]:
        return inspect.getfile(target)

def type_file(target):
    if isinstance(target, type):
        return python_file(target)


function_line_number = get_line_number
method_line_number   = get_line_number