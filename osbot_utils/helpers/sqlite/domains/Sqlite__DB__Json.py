from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.helpers.sqlite.Sqlite__Table__Create import Sqlite__Table__Create
from osbot_utils.helpers.sqlite.models.Sqlite__Field__Type import Sqlite__Field__Type


class Sqlite__DB__Json(Kwargs_To_Self):
    database     : Sqlite__Database
    table_create : Sqlite__Table__Create
    table_name   : str                    = 'new_db_table'

    def __init__(self):
        super().__init__()
        self.table_create = Sqlite__Table__Create(self.table_name)

    def create_fields_from_json_data(self, json_data):
        self.table_create.table.database = self.database
        for key,value in json_data.items():
            self.table_create.add_field_with_type(key, type(value))

    def create_table_from_json_data(self, json_data):
        self.create_fields_from_json_data(json_data)
        if self.table_create.create_table():
            self.table_create.table.row_add(json_data)
            return self.table_create.table

    #def add_data_to_data_from_json_data(self, json_data):

    def get_schema_from_json_data(self, json_data):
        if type(json_data) is dict:
            return self.get_schema_from_dict(json_data)
        if type(json_data) is list:
            return self.get_schema_from_list_of_dict(json_data)

    def get_schema_from_list_of_dict(self, target):
        if not isinstance(target, list):
            raise ValueError("in get_schema_from_list_of_dict, the provided target is not a list")
        schemas = []
        for item in target:
            if type(item) is dict:
                schemas.append(self.get_schema_from_dict(item))
        if not schemas:
            return {}

        # Check that all schemas are the same
        base_schema = schemas[0]
        for schema in schemas[1:]:
            if schema != base_schema:
                raise ValueError("In get_schema_from_list_of_dict not all items of the dict in the list had the same schema")
        return base_schema


    def get_schema_from_dict(self, target):
        schema = {}
        for key, value in target.items():
            value_type = type(value)
            field_type = Sqlite__Field__Type.type_map().get(value_type)
            if field_type is None:
                raise ValueError(f"in get_schema_from_dict, the value_type {value_type} from '{key} = {value}' is not supported by Sqlite__Field__Type")
            schema[key] = field_type
        return schema





