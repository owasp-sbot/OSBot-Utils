from unittest import TestCase

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.helpers.sqlite.sample_data.Sqlite__Sample_Data__Chinook import Sqlite__Sample_Data__Chinook
from osbot_utils.helpers.sqlite.sql_builder.SQL_Builder import SQL_Builder
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import default_value


class test_SQL_Builder(TestCase):
    db_chinook: Sqlite__Database
    table     : Sqlite__Table

    @classmethod
    def setUpClass(cls) -> None:
        cls.db_chinook = Sqlite__Sample_Data__Chinook().load_db_from_disk()
        cls.table      = cls.db_chinook.table('Genre')

    def setUp(self):
        self.sql_builder = SQL_Builder(table=self.table)

    def test_validate_query_data(self):
        with self.assertRaises(ValueError) as context:
            self.sql_builder.validate_query_data()
        assert context.exception.args[0] == 'in SQL_Builder, there was no row_schema defined in the mapped table'

    def test_create_temp_schema(self):
        field_types= self.table.fields_types__cached()


        Schema = type('Schema', (Kwargs_To_Self,), {k: default_value(v) for k, v in field_types.items()})
        Schema.__annotations__ = field_types

        assert type(Schema) == type
        schema_obj = Schema(Name='asd')
        schema_obj.id = 123
        pprint(schema_obj.__locals__())



