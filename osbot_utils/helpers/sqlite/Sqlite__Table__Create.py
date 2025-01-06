import inspect
from typing                                                 import List
from osbot_utils.base_classes.Kwargs_To_Self                import Kwargs_To_Self
from osbot_utils.decorators.lists.filter_list               import filter_list
from osbot_utils.helpers.sqlite.Sqlite__Field               import Sqlite__Field
from osbot_utils.helpers.sqlite.Sqlite__Table               import Sqlite__Table, DEFAULT_FIELD_NAME__ID
from osbot_utils.helpers.sqlite.models.Sqlite__Field__Type  import Sqlite__Field__Type

class Sqlite__Table__Create(Kwargs_To_Self):
    fields  : List[Sqlite__Field]
    table   : Sqlite__Table

    def __init__(self, table_name):
        super().__init__()
        self.table.table_name = table_name
        self.set_default_fields()

    def add_field(self, field_data: dict):
        if field_data and isinstance(field_data, dict):
            sqlite_field = Sqlite__Field.from_json(field_data)
            self.fields.append(sqlite_field)
            return True
        return False

    def add_fields(self, fields_data:List[dict]):
        results = []
        if fields_data:
            for field_data in fields_data:
                results.append(self.add_field(field_data))
        return results

    def add_fields_from_class(self, table_class):
        if inspect.isclass(table_class):
            for field_name, field_type in table_class.__annotations__.items():
                self.add_field_with_type(field_name, field_type)
        return self

    def add_field_with_type(self, field_name, field_type):
        if inspect.isclass(field_type):
            field_type = Sqlite__Field__Type.type_map().get(field_type)

        return self.add_field(dict(name=field_name, type=field_type))

    def add_field__text(self, field_name):
        return self.add_field_with_type(field_name=field_name, field_type=str)

    def add_fields__text(self, *fields_name):
        for field_name in fields_name:
            self.add_field__text(field_name=field_name)
        return self

    def create_table(self):
        sql_query = self.sql_for__create_table()
        if self.table.not_exists():
            self.table.cursor().execute(sql_query)
            return self.table.exists()
        return False

    def create_table__from_row_schema(self, row_schema):  # todo add check if there is an index field (which is now supported since it clashes with the one that is added by default)
        self.add_fields_from_class(row_schema)
        self.table.row_schema = row_schema
        return self.create_table()

    @filter_list
    def fields_json(self):
        return [field.json() for field in self.fields]

    def fields__by_name_type(self):
        return { item.get('name'): item.get('type') for item in self.fields_json() }

    def fields_reset(self):
        self.fields = []
        return self

    def database(self):
        return self.table.database

    def set_default_fields(self):
        self.add_field(dict(name=DEFAULT_FIELD_NAME__ID, type="INTEGER", pk=True))        # by default every table has an id field
        return self

    def sql_for__create_table(self):
        field_definitions = [field.text_for_create_table() for field in self.fields]
        primary_keys = [field.name for field in self.fields if field.pk]
        foreign_keys_constraints = [field.text_for_create_table() for field in self.fields if field.is_foreign_key]

        # Handling composite primary keys if necessary
        if len(primary_keys) > 1:
            pk_constraint = f"PRIMARY KEY ({', '.join(primary_keys)})"
            field_definitions.append(pk_constraint)

        # Adding foreign key constraints separately if there are any
        if foreign_keys_constraints:
            field_definitions.extend(foreign_keys_constraints)

        table_definition = f"CREATE TABLE {self.table.table_name} ({', '.join(field_definitions)});"
        return table_definition
