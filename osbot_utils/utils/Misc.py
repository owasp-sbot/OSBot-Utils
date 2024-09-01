import base64
import hashlib
import importlib
import logging
import os
import random
import string
import sys
import textwrap
import re
import threading
import uuid
import warnings
from datetime       import datetime, timedelta
from secrets        import token_bytes
from time           import sleep
from typing         import Iterable
from urllib.parse   import  quote_plus, unquote_plus


if sys.version_info >= (3, 11):
    from datetime import UTC
else:
    from datetime import timezone                       # For versions before 3.11, we need to use a different method or library to handle UTC
    UTC = timezone.utc

def append_random_string(target, length=6, prefix='-'):
    return f'{target}{random_string(length, prefix)}'

def attr_value_from_module_name(module_name, attr_name, default_value=None):
    module = importlib.import_module(module_name)
    if hasattr(module, attr_name):
        return getattr(module, attr_name)
    return default_value

def bytes_md5(target : bytes):
    return hashlib.md5(target).hexdigest()

def bytes_sha256(target : bytes):
    return hashlib.sha256(target).hexdigest()

def bytes_sha384(target : bytes):
    return hashlib.sha384(target).hexdigest()

def base64_to_bytes(bytes_base64):
    if type(bytes_base64) is str:
        bytes_base64 = bytes_base64.encode()
    return base64.decodebytes(bytes_base64)

def base64_to_str(target, encoding='ascii'):
    return bytes_to_str(base64_to_bytes(target), encoding=encoding)

def bytes_to_base64(target):
    return base64.b64encode(target).decode()

def bytes_to_str(target, encoding='ascii'):
    return target.decode(encoding=encoding)

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

def current_thread_id():
    return threading.current_thread().native_id


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
        value = datetime.now(UTC)
        #value = datetime.utcnow()        # todo: this has been marked for depreciation in python 11
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
    return date_time_less_time_delta(datetime.now(UTC),days=days, hours=hours, minutes=minutes, seconds=seconds,date_time_format=date_time_format, return_str=return_str)

def date_to_str(date, date_format='%Y-%m-%d'):
    return date.strftime(date_format)

def date_today():
    return date_time_now(date_time_format='%Y-%m-%d')

#note: this is here at the moment due to a circular dependency with lists and objects
def list_set(target: object) -> object:
    if hasattr(target, '__iter__'):
        return sorted(list(set(target)))
    return []

def time_str_milliseconds(datetime_str, datetime_format, milliseconds_numbers=0):
    if '.%f' in datetime_format and -1 < milliseconds_numbers < 6:
        chars_to_remove = milliseconds_numbers-6
        if milliseconds_numbers == 0:
            chars_to_remove -= 1
        return datetime_str[:chars_to_remove]
    return datetime_str

def flist(target):
    from osbot_utils.fluent.Fluent_List import Fluent_List
    return Fluent_List(target)

# todo: check if this should still be here
def get_random_color(max=5):
    if max > 5: max = 5                                                             # add support for more than 5 colors
    colors = ['skyblue', 'darkseagreen', 'palevioletred', 'coral', 'darkgray']
    return colors[random_number(0, max-1)]


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

def is_guid(value):
    try:
        uuid_obj = uuid.UUID(value)
        return str(uuid_obj) == value.lower()
    except Exception:
        return False


def ignore_warning__unclosed_ssl():
    warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")


def last_letter(text):
    if text and (type(text) is str) and len(text) > 0:
        return text[-1]


# def log_critical(message): logger().critical(message) # level 50
# def log_debug   (message): logger().debug   (message) # level 10
# def log_error   (message): logger().error   (message) # level 40
# def log_info    (message): logger().info    (message) # level 20
# def log_warning (message): logger().warning (message) # level 30

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


def size(target=None):
    if target and hasattr(target, '__len__'):
        return len(target)
    return 0

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

def print_time_now(use_utc=True):
    print(time_now(use_utc=use_utc))

def str_sha256(text: str):
    if type(text) is str:
        return bytes_sha256(text.encode())
    return None

def str_sha384(text:str):
    if type(text) is str:
        return bytes_sha384(text.encode())
    return

def str_sha384_as_base64(text:str, include_prefix=True):
    if type(text) is str:
        hash_object = hashlib.sha384(text.encode())
        digest      = hash_object.digest()                                  # Getting the digest of the hash
        digest_base64 = base64.b64encode(digest).decode()                   # Converting the digest to Base64 encoding
        if include_prefix:
            return "sha384-" + digest_base64
        return digest_base64
    return

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
        datetime_now = datetime.now(UTC)
    else:
        datetime_now = datetime.now()
    return time_to_str(datetime_value=datetime_now,milliseconds_numbers=milliseconds_numbers)

def time_to_str(datetime_value, time_format='%H:%M:%S.%f', milliseconds_numbers=3):
    time_str = datetime_value.strftime(time_format)
    return time_str_milliseconds(datetime_str=time_str, datetime_format=time_format, milliseconds_numbers=milliseconds_numbers)

def timestamp_utc_now():
    return int(datetime.now(UTC).timestamp() * 1000)

def timestamp_utc_now_less_delta(days=0,hours=0, minutes=0, seconds=0):
    date_time = date_time_now_less_time_delta(days=days,hours=hours, minutes=minutes, seconds=seconds, return_str=False)
    return datetime_to_timestamp(date_time)

def datetime_to_timestamp(datetime):
    return int(datetime.timestamp() * 1000)

def timestamp_to_datetime(timestamp):
    timestamp = float(timestamp)                            # handle cases when timestamp is a Decimal
    return datetime.fromtimestamp(timestamp/1000)

def timestamp_to_str(timestamp, date_time_format='%Y-%m-%d %H:%M:%S.%f'):
    date_time = timestamp_to_datetime(timestamp)
    return datetime_to_str(date_time, date_time_format=date_time_format)

def timestamp_to_str_date(timestamp, date_format='%Y-%m-%d'):
    return timestamp_to_str(timestamp, date_format)

def timestamp_to_str_time(timestamp, time_format='%H:%M:%S'):
    return timestamp_to_str(timestamp, time_format)

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

def random_text(prefix:str=None,length:int=12, lowercase=False):
    if prefix is None: prefix = 'text_'
    if last_letter(prefix) not in ['_','/']:
        prefix += '_'
    value = random_string_and_numbers(length=length, prefix=prefix)
    if lowercase:
        return lower(value)
    return value

def random_uuid():
    return str(uuid.uuid4())

def random_uuid_short():
    return str(uuid.uuid4())[0:6]

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

def sorted_set(target : Iterable):
    if target:
        return sorted(set(target))
    return []

def str_to_base64(target):
    return bytes_to_base64(str_to_bytes(target))

def str_to_bytes(target):
    return target.encode()

def str_to_bool(value):
    if type(value) is str:
        return value.lower() in ('true', '1', 'yes')
    return False

def str_to_date(str_date, format='%Y-%m-%d %H:%M:%S.%f'):
    return datetime.strptime(str_date,format)

def str_to_date_time(str_date, format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(str_date,format)

def str_to_int(str_data):
    return int(float(str_data))


def to_int(value, default=0):
    try:
        return int(value)
    except:
        return default

def under_debugger():
    return 'pydevd' in sys.modules


def url_encode(data):
    if type(data) is str:
        return quote_plus(data)

def url_decode(data):
    if type(data) is str:
        return unquote_plus(data)

def utc_now():
    return datetime.now(UTC)

def upper(target : str):
    if target:
        return target.upper()
    return ""

def wait(seconds):
    if seconds and seconds > 0:
        sleep(seconds)

def word_wrap(text,length = 40):
    if text:
        wrapped_text = ""
        for line in text.splitlines():                                  # handle case when there are newlines inside the text value
            wrapped_text += '\n'.join(textwrap.wrap(line, length))
            wrapped_text += '\n'
        return wrapped_text
    return ''

def word_wrap_escaped(text,length = 40):
    if text:
        return '\\n'.join(textwrap.wrap(text, length))

bytes_to_string     = bytes_to_str

convert_to_float    = convert_to_number

datetime_now               = date_time_now
datetime_to_str            = date_time_to_str
datetime_from_timestamp    = timestamp_to_datetime
datetime_utc_now           = utc_now
date_time_to_timestamp     = datetime_to_timestamp
date_time_from_timestamp   = timestamp_to_datetime
date_time_from_time_stamp  = timestamp_to_datetime
date_time_utc_now          = utc_now

hash_sha256         = str_sha256

new_guid            = random_uuid

sha_256             = str_sha256
str_lines           = split_lines
str_remove          = remove

random_id           = random_string
random_int          = random_number
random_guid         = random_uuid
random_value        = random_string

time_utc            = time_now
wait_for            = wait

