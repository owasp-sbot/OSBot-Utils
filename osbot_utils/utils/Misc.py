import base64
import hashlib
import importlib
import inspect
import logging
import os
import random
import string
import sys
import textwrap
import re
import types
import uuid
import warnings
from datetime import datetime, timedelta
from secrets    import token_bytes
from time import sleep
from typing import List
from urllib.parse import urlencode, quote_plus, unquote_plus

#from dateutil import parser
from dotenv     import load_dotenv

def append_random_string(target, length=6, prefix='-'):
    return f'{target}{random_string(length, prefix)}'

def attr_value_from_module_name(module_name, attr_name, default_value=None):
    module = importlib.import_module(module_name)
    if hasattr(module, attr_name):
        return getattr(module, attr_name)
    return default_value

def bytes_md5(bytes : bytes):
    return hashlib.md5(bytes).hexdigest()

def bytes_sha256(bytes : bytes):
    return hashlib.sha256(bytes).hexdigest()

def base64_to_bytes(bytes_base64):
    if type(bytes_base64) is str:
        bytes_base64 = bytes_base64.encode()
    return base64.decodebytes(bytes_base64)

def base64_to_str(target, encoding='ascii'):
    return bytes_to_str(base64_to_bytes(target), encoding=encoding)

def bytes_to_base64(bytes):
    return base64.b64encode(bytes).decode()

def bytes_to_str(target, encoding='ascii'):
    return target.decode(encoding=encoding)

def chunks(items:list, split: int):
    if items and split and split > 0:
        for i in range(0, len(items), split):
            yield items[i:i + split]

def class_name(target):
    if target:
        return type(target).__name__

def class_functions(target):
    functions = {}
    for function_name, function_ref in inspect.getmembers(type(target), predicate=inspect.isfunction):
        functions[function_name] = function_ref
    return functions

def class_functions_names(target):
    return list_set(class_functions(target))

def convert_to_number(value):
    if value:
        try:
            if value[0] in ['£','$','€']:
                return float(re.sub(r'[^\d.]', '', value))
            else:
                return float(value)
        except:
          return 0
    else:
        return 0

def date_time_from_to_str(date_time_str, format_from, format_to, print_conversion_error=False):
    try:
        date_time = datetime.strptime(date_time_str, format_from)
        return date_time.strftime(format_to)
    except ValueError as value_error:
        if print_conversion_error:
            print(f"[date_time_from_to_str]: Error: {value_error}")          # todo: use log handler
        return None


def date_time_to_str(date_time, date_time_format='%Y-%m-%d %H:%M:%S.%f', milliseconds_numbers=3):
    if date_time:
        date_time_str = date_time.strftime(date_time_format)
        return time_str_milliseconds(datetime_str=date_time_str, datetime_format=date_time_format, milliseconds_numbers=milliseconds_numbers)
    else:
        return ''

def date_now(use_utc=True, return_str=True):
    value = date_time_now(use_utc=use_utc, return_str=False)
    if return_str:
        return date_to_str(date=value)
    return value

def date_time_now(use_utc=True, return_str=True, milliseconds_numbers=0, date_time_format='%Y-%m-%d %H:%M:%S.%f'):
    if use_utc:
        value = datetime.utcnow()        # todo: this has been marked for depreciation in python 11
        # value = datetime.now(UTC)      #       but this doesn't seem to work in python 10.x : E   ImportError: cannot import name 'UTC' from 'datetime' (/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/datetime.py)

    else:
        value = datetime.now()
    if return_str:
        return date_time_to_str(value, milliseconds_numbers=milliseconds_numbers, date_time_format=date_time_format)
    return value

# def date_time_parse(value):
#     if type(value) is datetime:
#         return value
#     return parser.parse(value)

def date_time_less_time_delta(date_time, days=0, hours=0, minutes=0, seconds=0, date_time_format='%Y-%m-%d %H:%M:%S' , return_str=True):
    new_date_time = date_time - timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    if return_str:
        return date_time_to_str(new_date_time, date_time_format=date_time_format)
    return new_date_time

def date_time_now_less_time_delta(days=0,hours=0, minutes=0, seconds=0, date_time_format='%Y-%m-%d %H:%M:%S', return_str=True):
    return date_time_less_time_delta(datetime.utcnow(),days=days, hours=hours, minutes=minutes, seconds=seconds,date_time_format=date_time_format, return_str=return_str)

def date_to_str(date, date_format='%Y-%m-%d'):
    return date.strftime(date_format)

def dict_insert_field(target_dict, new_key, insert_at, new_value=None):
    if type(target_dict) is dict:
        new_dict = {}
        for i, (key, value) in enumerate(target_dict.items()):
            if i == insert_at:
                new_dict[new_key] = new_value
            new_dict[key] = value
        return new_dict

def dict_remove(data, target):
    if type(data) is dict:
        if type(target) is list:
            for key in list(data.keys()):
                if key in target:
                    del data[key]
        else:
            if target in data:
                del data[target]
    return data


def time_str_milliseconds(datetime_str, datetime_format, milliseconds_numbers=0):
    if '.%f' in datetime_format and -1 < milliseconds_numbers < 6:
        chars_to_remove = milliseconds_numbers-6
        if milliseconds_numbers == 0:
            chars_to_remove -= 1
        return datetime_str[:chars_to_remove]
    return datetime_str

def env_value(var_name):
    return env_vars().get(var_name, None)

def env_vars(reload_vars=False):
    """
    if reload_vars reload data from .env file
    then return dictionary with current environment variables
    """
    if reload_vars:
        load_dotenv()
    vars = os.environ
    data = {}
    for key in vars:
        data[key] = vars[key]
    return data

def env_vars_list():
    return list_set(env_vars())

def flist(target):
    from osbot_utils.fluent.Fluent_List import Fluent_List
    return Fluent_List(target)

def get_field(target, field, default=None):
    if target is not None:
        try:
            value = getattr(target, field)
            if value is not None:
                return value
        except:
            pass
    return default

def get_value(target, key, default=None):
    if target is not None:
        value = target.get(key)
        if value is not None:
            return value
    return default

# todo: check if this should still be here
def get_random_color(max=5):
    if max > 5: max = 5                                                             # add support for more than 5 colors
    colors = ['skyblue', 'darkseagreen', 'palevioletred', 'coral', 'darkgray']
    return colors[random_number(0, max-1)]

def get_missing_fields(target,field):
    missing_fields = []
    for field in field:
        if get_field(target, field) is None:
            missing_fields.append(field)
    return missing_fields

def is_debugging():
    return sys.gettrace() is not None

def is_number(value):
    try:
        if type(value) is int or type(value) is float :
            int(value)
            return True
    except:
        pass
    return False

def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def ignore_warning__unclosed_ssl():
    warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")


def last_letter(text):
    if text and (type(text) is str) and len(text) > 0:
        return text[-1]

def len_list(target):
    return len(list(target))

def list_add(array : list, value):
    if value is not None:
        array.append(value)
    return value

def list_contains_list(array : list, values):
    if array is not None:
        if type(values) is list:
            for item in values:
                if (item in array) is False:
                    return False
            return True
    return False

def list_remove_list(source: list, target: list):
    if type(source) is list and type(target) is list:
        for item in target:
            if item in source:
                source.remove(item)

def list_find(array:list, item):
    if item in array:
        return array.index(item)
    return -1

def list_get_field(values, field):
    return [item.get(field) for item in values]

def list_index_by(values, index_by):
    from osbot_utils.fluent.Fluent_Dict import Fluent_Dict
    results = {}
    if values and index_by:
        for item in values:
            results[item.get(index_by)] = item
    return Fluent_Dict(results)

def list_group_by(values, group_by):
    results = {}
    for item in values:
        value = str(item.get(group_by))
        if results.get(value) is None: results[value] = []
        results[value].append(item)
    return results

def list_get(array, position=None, default=None):
    if type(array) is list:
        if type(position) is int and position >=0 :
            if  len(array) > position:
                return array[position]
    return default

def list_order_by(urls: List[dict], key: str, reverse: bool=False) -> List[dict]:
    """
    Sorts a list of dictionaries containing URLs by a specified key.

    Args:
        urls (List[dict]): A list of dictionaries containing URLs.
        key (str): The key to sort the URLs by.
        reverse (bool): Whether to sort the URLs in reverse order.

    Returns:
        List[dict]: The sorted list of URLs.
    """
    return sorted(urls, key=lambda x: x[key], reverse=reverse)

def list_pop(array:list, position=None, default=None):
    if array:
        if len(array) >0:
            if type(position) is int:
                if len(array) > position:
                    return array.pop(position)
            else:
                return array.pop()
    return default

def list_pop_and_trim(array, position=None):
    value = array_pop(array,position)
    if type(value) is str:
        return trim(value)
    return value

def list_remove(array, item):
    if type(item) is list:
        result = []
        for element in array:
            if element not in item:
                result.append(element)
        return result

    return [element for element in array if element != item]


def list_remove_empty(array):
    return [element for element in array if element]

def list_set(target):
    if hasattr(target, '__iter__'):
        return sorted(list(set(target)))
    return []

def list_zip(*args):
    return list(zip(*args))


def list_set_dict(target):
    return sorted(list(set(obj_dict(target))))

def list_filter(target_list, filter_function):
    return list(filter(filter_function, target_list))

def list_sorted(target_list, key, descending=False):
    return list(sorted(target_list, key= lambda x:x.get(key,None) ,reverse=descending))

def list_filter_starts_with(target_list, prefix):
    return list_filter(target_list, lambda x: x.startswith(prefix))

def list_filter_contains(target_list, value):
    return list_filter(target_list, lambda x: x.find(value) > -1)

def log_critical(message): logger().critical(message) # level 50
def log_debug   (message): logger().debug   (message) # level 10
def log_error   (message): logger().error   (message) # level 40
def log_info    (message): logger().info    (message) # level 20
def log_warning (message): logger().warning (message) # level 30

def log_to_console(level="INFO"):
    logger_set_level(level)
    logger_add_handler__console()
    print()                             # add extra print so that in pytest the first line is not hidden

def log_to_file(level="INFO"):
    logger_set_level(level)
    return logger_add_handler__file()

def logger():
    return logging.getLogger()

def logger_add_handler(handler):
    logger().addHandler(handler)

def logger_add_handler__console():
    logger_add_handler(logging.StreamHandler())

def logger_add_handler__file(log_file=None):
    from osbot_utils.utils.Files import temp_file
    log_file = log_file or temp_file(extension=".log")
    logger_add_handler(logging.FileHandler(filename=log_file))
    return log_file
    #logging.basicConfig(level=logging.DEBUG, filename='myapp.log', format='%(asctime)s %(levelname)s:%(message)s')

def logger_set_level(level):
    logger().setLevel(level)

def logger_set_level_critical(): logger_set_level('CRITICAL') # level 50
def logger_set_level_debug   (): logger_set_level('DEBUG'   ) # level 10
def logger_set_level_error   (): logger_set_level('ERROR'   ) # level 40
def logger_set_level_info    (): logger_set_level('INFO'    ) # level 20
def logger_set_level_warning (): logger_set_level('WARNING' ) # level 30

def lower(target : str):
    if target:
        return target.lower()
    return ""

def obj_data(target=None):
    data = {}
    for key,value in obj_items(target):
        data[key] = value
    return data

def obj_dict(target=None):
    if target and hasattr(target,'__dict__'):
        return target.__dict__
    return {}

def obj_items(target=None):
    return sorted(list(obj_dict(target).items()))

def obj_keys(target=None):
    return sorted(list(obj_dict(target).keys()))

def obj_full_name(target):
    module = target.__class__.__module__
    name   = target.__class__.__qualname__
    return f"{module}.{name}"

def obj_get_value(target=None, key=None, default=None):
    return get_field(target=target, field=key, default=default)

def obj_values(target=None):
    return list(obj_dict(target).values())




def size(target=None):
    if target and hasattr(target, '__len__'):
        return len(target)
    return 0

def str_index(target:str, source:str):
    try:
        return target.index(source)
    except:
        return -1

def str_max_width(target, value):
    return str(target)[:value]

def sys_path_python(python_folder='lib/python'):
    return list_contains(sys.path, python_folder)

def str_md5(text : str):
    if text:
        return bytes_md5(text.encode())
    return ''

def none_or_empty(target,field):
    if target and field:
        value = target.get(field)
        return (value is None) or value == ''
    return True

def print_date_now(use_utc=True):
    print(date_time_now(use_utc=use_utc))

def print_object_methods(target, name_width=30, value_width=100, show_private=False, show_internals=False):
    print_object_members(target, name_width=name_width, value_width=value_width,show_private=show_private,show_internals=show_internals, only_show_methods=True)

def print_obj_data_as_dict(target, **kwargs):
    data = obj_data(target, **kwargs)
    max_key_length = max(len(k) for k in data.keys())                                 # Find the maximum key length
    items          = [f"{k:<{max_key_length}} = {v!r:6}," for k, v in data.items()]   # Format each key-value pair
    items[-1]      = items[-1][:-2]                                                   # Remove comma from the last item
    indented_items = '\n     '.join(items)                                            # Join the items with newline and four-space indentation
    print("dict(" + indented_items + " )")
    return data

def obj_data(target, name_width=30, value_width=100, show_private=False, show_internals=False, show_value_class=False, show_methods=False, only_show_methods=False):
    result = {}
    for name, value in inspect.getmembers(target):
        if show_methods is False and type(value) is types.MethodType:
            continue
        if only_show_methods and type(value) is not types.MethodType:
            continue
        if not show_private and name.startswith("_"):
            continue
        if not show_internals and name.startswith("__"):
            continue
        if only_show_methods:
            value = inspect.signature(value)
        if value !=None and type(value) not in [bool, int, float]:
            value       = str(value).encode('unicode_escape').decode("utf-8")
            value       = str_unicode_escape(value)
            value       = str_max_width(value, value_width)
            name        = str_max_width(name, name_width)
        result[name] = value
    return result


# todo: add option to not show class methods that are not bultin types
def print_object_members(target, name_width=30, value_width=100, show_private=False, show_internals=False, show_value_class=False, show_methods=False, only_show_methods=False):
    max_width = name_width + value_width
    print()
    print(f"Members for object:\n\t {target} of type:{type(target)}")
    print(f"Settings:\n\t name_width: {name_width} | value_width: {value_width} | show_private: {show_private} | show_internals: {show_internals}")
    print()
    if only_show_methods:
        print(f"{'method':<{name_width}} (params)")
    else:
        if show_value_class:
            print(f"{'field':<{name_width}} | {'type':<{name_width}} |value")
        else:
            print(f"{'field':<{name_width}} | value")

    print(f"{'-' * max_width}")
    for name, value in obj_data(target, name_width=name_width, value_width=value_width, show_private=show_private, show_internals=show_internals, show_value_class=show_value_class, show_methods=show_methods, only_show_methods=only_show_methods).items():
        if only_show_methods:
            print(f"{name:<{name_width}} {value}"[:max_width])
        else:
            if show_value_class:
                value_class = obj_full_name(value)
                print(f"{name:<{name_width}} | {value_class:{name_width}} | {value}"[:max_width])
            else:
                print(f"{name:<{name_width}} | {value}"[:max_width])

def print_time_now(use_utc=True):
    print(time_now(use_utc=use_utc))

def str_sha256(text: str):
    if text:
        return bytes_sha256(text.encode())
        #return hashlib.sha256('{0}'.format(text).encode()).hexdigest()
    return None

def time_delta_to_str(time_delta):
    microseconds  = time_delta.microseconds
    milliseconds  = int(microseconds / 1000)
    total_seconds = int(time_delta.total_seconds())
    return f'{total_seconds}s {milliseconds}ms'

def time_delta_in_days_hours_or_minutes(time_delta):
    total_seconds = int(time_delta.total_seconds())
    days   , seconds = divmod(total_seconds, 86400)
    hours  , seconds = divmod(seconds      , 3600 )
    minutes, seconds = divmod(seconds      , 60   )
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours:4}h {minutes}m"
    elif minutes >0:
        return f"{minutes}m"
    elif seconds >0:
        return f"{seconds}s"


def time_now(use_utc=True, milliseconds_numbers=1):
    if use_utc:
        datetime_now = datetime.utcnow()
    else:
        datetime_now = datetime.now()
    return time_to_str(datetime_value=datetime_now,milliseconds_numbers=milliseconds_numbers)

def time_to_str(datetime_value, time_format='%H:%M:%S.%f', milliseconds_numbers=3):
    time_str = datetime_value.strftime(time_format)
    return time_str_milliseconds(datetime_str=time_str, datetime_format=time_format, milliseconds_numbers=milliseconds_numbers)

def timestamp_utc_now():
    return int(datetime.utcnow().timestamp() * 1000)
    #return int(datetime.utcnow().strftime('%s')) * 1000

def timestamp_utc_now_less_delta(days=0,hours=0, minutes=0, seconds=0):
    date_time = date_time_now_less_time_delta(days=days,hours=hours, minutes=minutes, seconds=seconds, return_str=False)
    return datetime_to_timestamp(date_time)

def datetime_to_timestamp(datetime):
    return int(datetime.timestamp() * 1000)

def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp/1000)

def timestamp_to_str(timestamp):
    date_time = timestamp_to_datetime(timestamp)
    return datetime_to_str(date_time)

def to_string(target):
    if target:
        return str(target)
    return ''

def random_bytes(length=24):
    return token_bytes(length)

def random_filename(extension='.tmp', length=10):
    from osbot_utils.utils.Files import file_extension_fix
    extension = file_extension_fix(extension)
    return '{0}{1}'.format(''.join(random.choices(string.ascii_lowercase + string.digits, k=length)) ,  extension)

def random_port(min=20000,max=65000):
    return random_number(min, max)

def random_number(min=1,max=65000):
    return random.randint(min, max)

def random_password(length=24, prefix=''):
    password = prefix + ''.join(random.choices(string.ascii_lowercase  +
                                               string.ascii_uppercase +
                                               string.punctuation     +
                                               string.digits          ,
                                               k=length))
    # replace these chars with _  (to make prevent errors in command prompts and urls)
    items = ['"', '\'', '`','\\','/','}','?','#',';',':']
    for item in items:
        password = password.replace(item, '_')
    return password

def random_string(length:int=8, prefix:str='', postfix:str=''):
    if is_int(length):
        length -= 1                                                 # so that we get the exact length when the value is provided
    else:
        length = 7                                                  # default length
    value   = '_' + ''.join(random.choices(string.ascii_uppercase, k=length)).lower()
    return f"{prefix}{value}{postfix}"

def random_string_and_numbers(length:int=6,prefix:str=''):
    return prefix + ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def random_text(prefix:str=None,length:int=12):
    if prefix is None: prefix = 'text_'
    if last_letter(prefix) not in ['_','/']:
        prefix += '_'
    return random_string_and_numbers(length=length, prefix=prefix)

def random_uuid():
    return str(uuid.uuid4())

def remove(target_string, string_to_remove):                        # todo: refactor to str_*
    return replace(target_string, string_to_remove, '')

def remove_multiple_spaces(target):                                 # todo: refactor to str_*
    return re.sub(' +', ' ', target)

def replace(target_string, string_to_find, string_to_replace):      # todo: refactor to str_*
    return target_string.replace(string_to_find, string_to_replace)

def remove_html_tags(html):
    if html:
        TAG_RE = re.compile(r'<[^>]+>')
        return TAG_RE.sub('', html).replace('&nbsp;', ' ')

def split_lines(text):
    return text.replace('\r\n','\n').split('\n')

def split_spaces(target):
    return remove_multiple_spaces(target).split(' ')

def sorted_set(target : object):
    if target:
        return sorted(set(target))
    return []

def str_to_base64(target):
    return bytes_to_base64(str_to_bytes(target))

def str_to_bytes(target):
    return target.encode()

def str_to_date(str_date, format='%Y-%m-%d %H:%M:%S.%f'):
    return datetime.strptime(str_date,format)

def str_to_date_time(str_date, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(str_date,format)

def str_to_int(str_data):
    return int(float(str_data))

def str_unicode_escape(target):
    return str(target).encode('unicode_escape').decode("utf-8")

def to_int(value, default=0):
    try:
        return int(value)
    except:
        return default

def trim(target):
    if type(target) is str:
        return target.strip()
    return ""

def under_debugger():
    return 'pydevd' in sys.modules

def unique(target):
    return list_set(target)

def url_encode(data):
    if type(data) is str:
        return quote_plus(data)

def url_decode(data):
    if type(data) is str:
        return unquote_plus(data)

def utc_now():
    return datetime.utcnow()

def upper(target : str):
    if target:
        return target.upper()
    return ""

def wait(seconds):
    if seconds and seconds > 0:
        sleep(seconds)

def word_wrap(text,length = 40):
    if text:
        return '\n'.join(textwrap.wrap(text, length))
    return ''

def word_wrap_escaped(text,length = 40):
    if text:
        return '\\n'.join(textwrap.wrap(text, length))


array_find          = list_find
array_get           = list_get
array_pop           = list_pop
array_pop_and_trim  = list_pop_and_trim
array_add           = list_add

bytes_to_string     = bytes_to_str

convert_to_float    = convert_to_number

datetime_now               = date_time_now
datetime_to_str            = date_time_to_str
datetime_from_timestamp    = timestamp_to_datetime
date_time_to_timestamp     = datetime_to_timestamp
date_time_from_timestamp   = timestamp_to_datetime
date_time_from_time_stamp  = timestamp_to_datetime

list_contains           = list_filter_contains
list_sort_by            = list_sorted

new_guid            = random_uuid

obj_list_set        = obj_keys
obj_info            = print_object_members
obj_methods         = print_object_methods

str_lines           = split_lines
str_remove          = remove

random_id           = random_string
random_guid         = random_uuid

wait_for            = wait

