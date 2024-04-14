from osbot_utils.base_classes.Kwargs_To_Self                import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database            import Sqlite__Database
from osbot_utils.helpers.sqlite.Sqlite__Table__Create       import Sqlite__Table__Create
from osbot_utils.helpers.sqlite.models.Sqlite__Field__Type  import Sqlite__Field__Type


class Sqlite__DB__Json(Kwargs_To_Self):
    database     : Sqlite__Database
    table_create : Sqlite__Table__Create
    table_name   : str                    = 'new_db_table'

    def __init__(self):
        super().__init__()
        self.table_create = Sqlite__Table__Create(self.table_name)
        self.table_create.table.database = self.database

    def create_fields_from_json_data(self, json_data):
        for key,value in json_data.items():
            self.table_create.add_field_with_type(key, type(value))

    def create_table_from_schema(self, table_name, schema):
        table_create               = Sqlite__Table__Create(table_name)
        table_create.table.database = self.database
        for field_name,field_type in schema.items():
            table_create.add_field_with_type(field_name, field_type)

        if table_create.create_table():
            return table_create.table

    def create_table_from_json_data(self, json_data):
        self.create_fields_from_json_data(json_data)
        if self.table_create.create_table():
            self.table_create.table.row_add_record(json_data)
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

        overall_schema = {}

        for item in target:
            if not isinstance(item, dict):
                continue  # or raise an exception, depending on your needs

            current_schema = self.get_schema_from_dict(item)

            for key, current_type in current_schema.items():
                if (key                 in overall_schema              and                                   # Check if key exists in the overall schema
                    overall_schema[key] != current_type                and                                   # Check if there's a type mismatch for the key
                    current_type        != Sqlite__Field__Type.UNKNOWN and                                   # Ensure current type is not UNKNOWN
                    overall_schema[key] != Sqlite__Field__Type.UNKNOWN    ):                                 # Ensure overall schema's type for the key is not UNKNOWN
                        message = f"Type conflict for field '{key}': {overall_schema[key]} vs {current_type}"
                        raise ValueError(message)
                else:
                    overall_schema[key] = current_type                                                        # Update or add the key with its type to the overall schema


        return overall_schema

    def get_schema_from_dict(self, target):
        schema = {}
        type_map  = Sqlite__Field__Type.type_map()
        for key, value in target.items():
            value_type = type(value)
            field_type = type_map.get(value_type)
            if field_type is None:
                raise ValueError(f"in get_schema_from_dict, the value_type {value_type} from '{key} = {value}' is not supported by Sqlite__Field__Type")
            schema[key] = field_type
        return schema





