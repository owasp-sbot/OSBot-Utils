from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Field import Sqlite__Field
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table

class Sqlite__Table__Create(Kwargs_To_Self):
    fields : list[Sqlite__Field]
    table  : Sqlite__Table

    def __init__(self,table_name):
        super().__init__()
        self.table.table_name = table_name

    def add_field(self, field_data: dict):
        sqlite_field = Sqlite__Field.from_json(field_data)
        if sqlite_field:
            self.fields.append(sqlite_field)
            return True
        return False

    def create_table(self):
        sql_query = self.sql_for__create_table()
        if self.table.not_exists():
            self.table.cursor().execute(sql_query)
            return self.table.exists()
        return False

    def database(self):
        return self.table.database

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
