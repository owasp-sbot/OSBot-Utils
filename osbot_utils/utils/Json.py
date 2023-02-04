import json
import gzip
import logging
import os

from osbot_utils.utils.Misc import str_lines, str_md5

logger_json = logging.getLogger()   # todo: start using this API for capturing error messages from methods bellow

from osbot_utils.utils.Files import file_exists, temp_file, file_create_gz, file_create, load_file_gz, file_contents


class Json:

    @staticmethod
    def dumps(python_object, indent=4, pretty=True,sort_keys=False, default=str):
        if python_object:
            try:
                if pretty:
                    return json.dumps(python_object, indent=indent,sort_keys=sort_keys, default=default)
                return json.dumps(python_object, default=default)
            except Exception as error:
                error_message = f'Error in load_json: {error}'
                logger_json.exception(error_message)

    @staticmethod
    def load_file(path):
        """
        Loads json data from file
        Note: will not throw errors and will return {} as default
        errors are logged to Json.log
        """
        json_data = file_contents(path)
        return json_loads(json_data)

    @staticmethod
    def load_file_and_delete(path):
        data = json_load_file(path)
        if data:
            os.remove(path)
        return data

    @staticmethod
    def load_file_gz(path):
        data = load_file_gz(path)
        return json_loads(data)

    @staticmethod
    def load_file_gz_and_delete(path):
        data = json_load_file_gz(path)
        if data:
            os.remove(path)
        return data

    @staticmethod
    def loads(json_data):
        """
        Loads json data from string
        Note: will not throw errors and will return {} as default
        errors are logged to Json.log
        """
        if json_data:
            try:
                return json.loads(json_data)
            except:
                logger_json.exception('Error in load_json')
        return {}

    @staticmethod
    def loads_json_lines(json_lines):
        json_data = '[' + ','.join(str_lines(json_lines.strip())) + ']'
        return json_loads(json_data)

    @staticmethod
    def md5(data):
        return str_md5(json_dump(data))

    @staticmethod
    def round_trip(data):
        return json.loads(json.dumps(data))

    @staticmethod
    def save_file(python_object, path=None, pretty=False, sort_keys=False):
        json_data = json_dumps(python_object=python_object, indent=2, pretty=pretty, sort_keys=sort_keys)
        return file_create(path=path, contents=json_data)

    @staticmethod
    def save_file_pretty(python_object, path=None):
        return json_save_file(python_object=python_object, path=path, pretty=True)

    @staticmethod
    def save_file_gz(python_object, path=None, pretty=False):
        json_data = json_dumps(python_object,indent=2, pretty=pretty)
        return file_create_gz(path=path, contents=json_data)

    @staticmethod
    def save_file_pretty_gz(python_object, path=None):
        return json_save_file_gz(python_object=python_object, path=path, pretty=True)


    @staticmethod
    def json_save_tmp_file(python_object, pretty=True):
        return Json.save_file(python_object=python_object, pretty=pretty, path=None)

file_create_json             = Json.save_file_pretty

json_dump                    = Json.dumps
json_dumps                   = Json.dumps
json_format                  = Json.dumps
json_file_create             = Json.save_file
json_file_create_gz          = Json.save_file_gz
json_file_contents           = Json.load_file
json_file_contents_gz        = Json.load_file_gz
json_load_file               = Json.load_file
json_load_file_and_delete    = Json.load_file_and_delete
json_load_file_gz            = Json.load_file_gz
json_load_file_gz_and_delete = Json.load_file_gz_and_delete
json_from_string             = Json.loads
json_loads                   = Json.loads
json_md5                     = Json.md5
json_lines_loads             = Json.loads_json_lines
json_parse                   = Json.loads
json_lines_parse             = Json.loads_json_lines
json_to_str                  = Json.dumps
json_round_trip              = Json.round_trip
json_save                    = Json.save_file
json_save_file               = Json.save_file
json_save_file_pretty        = Json.save_file_pretty
json_save_file_gz            = Json.save_file_gz
json_save_file_pretty_gz     = Json.save_file_pretty_gz
json_save_tmp_file           = Json.json_save_tmp_file
str_to_json                  = Json.loads

load_file_json               = json_load_file
load_file_json_gz            = json_load_file_gz