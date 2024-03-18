from unittest import TestCase

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.Print_Table import Print_Table
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.utils.Dev import pprint

TEST_TABLE_NAME       = 'an_table'
EXPECTED_TABLE_SCHEMA = [{'cid': 0, 'name': 'id'      , 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1},
                         {'cid': 1, 'name': 'an_str'  , 'type': 'TEXT'   , 'notnull': 0, 'dflt_value': None, 'pk': 0},
                         {'cid': 2, 'name': 'an_int'  , 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 0},
                         {'cid': 3, 'name': 'an_bytes', 'type': 'BLOB'   , 'notnull': 0, 'dflt_value': None, 'pk': 0}]

class An_Table_Class(Kwargs_To_Self):
    an_str: str
    an_int: int
    an_bytes: bytes

class test_Sqlite__Table(TestCase):
    table        : Sqlite__Table
    #table_fields : list
    #table_name   : str

    @classmethod
    def setUpClass(cls):
        cls.table        = Sqlite__Table(table_name=TEST_TABLE_NAME, row_schema=An_Table_Class)
        assert cls.table.create() is True
        #assert cls.table.create() == True

    @classmethod
    def tearDownClass(cls):
        cls.table.delete()
        #assert cls.table.delete() is True

    def create_test_data(self, size=10):
        return [{'an_str': f'an_str_{i}', 'an_int': i} for i in range(size)]

    def test__init__(self):
        expected_vars = dict(database=self.table.database, table_name=TEST_TABLE_NAME, row_schema=self.table.row_schema)
        assert self.table.__locals__() == expected_vars

    def test_add_row(self):
        expected_rows = [{'an_bytes': b'a', 'an_int': 42, 'an_str': '', 'id': 1},
                         {'an_bytes': b'a', 'an_int': 12, 'an_str': '', 'id': 2}]
        with self.table as _:
            _.add_row(an_bytes=b'a', an_int=42      )
            _.add_row(an_bytes=b'a', an_int=12, id=2)
            assert _.rows() == expected_rows

            with self.assertRaises(Exception) as context:
                _.add_row(an_bytes=b'a', an_int='an-str')
            assert context.exception.args[0] == ("Invalid type for attribute 'an_int'. Expected '<class 'int'>' but got "
                                                 "'<class 'str'>'")
            with self.assertRaises(Exception) as context:
                _.add_row(an_bytes=b'a', bad_var='an-str')
            assert context.exception.args[0] == ('in row_add the provided row_obj is not valid: provided row_obj has a field '
                                                  'that is not part of the current table: bad_var') != ''

            assert _.rows() == expected_rows

    def test_create(self):
        assert self.table.delete() is True                  # confirm table exists
        assert self.table.delete() is False                 # confirm that deleting table when it doesn't exist returns False
        assert self.table.create() is True                  # created ok
        assert self.table.create() is False                 # can't create if already exists
        assert self.table.exists() is True                  # confirm table exists

        tables_raw = self.table.database.tables_raw()
        tables     = self.table.database.tables()
        table      = tables[0]

        assert len(tables) == 1
        assert type(table) is Sqlite__Table
        assert tables_raw  == [{ 'name'       : 'an_table'   ,
                                 'rootpage'  : 2             ,
                                 'sql'       : 'CREATE TABLE an_table (id INTEGER PRIMARY KEY, '
                                                                       'an_str TEXT, '
                                                                       'an_int INTEGER, '
                                                                       'an_bytes BLOB)',
                                 'tbl_name'  : 'an_table'    ,
                                 'type'      : 'table'       }]
        assert table.schema() == EXPECTED_TABLE_SCHEMA

        assert table.schema__by_name_type() == {'an_bytes': 'BLOB', 'an_int': 'INTEGER', 'an_str': 'TEXT', 'id': 'INTEGER'}

    def test_exists(self):
        assert self.table.exists() is True

    def test_fields__cached(self):
        fields = self.table.fields__cached()
        assert fields == self.table.fields()
        assert list(fields.values()) == EXPECTED_TABLE_SCHEMA
        assert list(fields.keys  ()) == ['an_bytes', 'an_int', 'an_str', 'id']
        assert list(fields.keys  ()) == self.table.fields_names__cached()

    def test_fields_types__cached(self):
        assert self.table.fields_types__cached() == { 'an_bytes': bytes,
                                                      'an_int'  : int  ,
                                                      'an_str'  : str  ,
                                                      'id'      : int  }

    def test_indexes(self):
        index_field = 'an_int'
        index_name  = f'idx__{self.table.table_name}__{index_field}'
        assert self.table.indexes() == []
        self.table.index_create(index_field)
        assert self.table.indexes() == [index_name]
        assert self.table.index_exists(index_field) is True
        self.table.index_delete(index_name)
        assert self.table.index_exists(index_field) is False
        assert self.table.indexes() == []


    def test_schema(self):
        table_schema = self.table.schema()
        assert table_schema == EXPECTED_TABLE_SCHEMA


    def test_row_add(self):
        with self.table as _:
            row_obj_1 = self.table.new_row_obj()
            row_obj_2 = self.table.new_row_obj(dict(an_str='A', an_int=42))
            assert self.table.row_add(row_obj_1) == {'data': None, 'error': None, 'message': '', 'status': 'ok'}
            assert self.table.row_add(row_obj_2) == {'data': None, 'error': None, 'message': '', 'status': 'ok'}
            assert self.table.rows() == [{'an_bytes': b'', 'an_int': 0 , 'an_str': '' , 'id': 1},
                                         {'an_bytes': b'', 'an_int': 42, 'an_str': 'A', 'id': 2}]
            assert self.table.size() == 2
            assert self.table.clear() == {'data': None, 'error': None, 'message': '', 'status': 'ok'}
            assert self.table.size() == 0
            assert self.table.rows() == []



    def test_rows(self):
        size = 10
        test_data = self.create_test_data(size)
        self.table.rows_add(test_data)
        assert len(self.table.rows()) == len(test_data)
        self.table.clear()

    def test_select_rows_where(self):
        with self.table as _:
            _.add_row(an_bytes=b'a', an_int=42      )
            _.add_row(an_bytes=b'a', an_int=12, id=2)
            assert _.select_rows_where(an_int=42) == [{'an_bytes': b'a', 'an_int': 42, 'an_str': '', 'id': 1}]
            assert _.select_rows_where(an_bytes=b'a') == [{'an_bytes': b'a', 'an_int': 42, 'an_str': '', 'id': 1},
                                                          {'an_bytes': b'a', 'an_int': 12, 'an_str': '', 'id': 2}]


            with self.assertRaises(Exception) as context:
                _.select_rows_where(bad_var=123)
            assert context.exception.args[0] == 'in select_rows_where, the provided field is not valid: bad_var'
            _.clear()

    def test_select_field_values(self):
        with self.table as _:
            _.add_row(an_str='str_in_1', an_int=42)
            _.add_row(an_str='str_in_2', an_int=12)
            assert _.select_field_values('an_str') == ['str_in_1', 'str_in_2']
            with self.assertRaises(Exception) as context:
                _.select_field_values('an_str_2')
            assert context.exception.args[0] == ('in select_all_vales_from_field, the provide field_name "an_str_2" does not '
                                                 'exist in the current table "an_table"')
            _.clear()

    def test_sql_query_for_fields(self):
        assert self.table.sql_query_for_fields(                ) == 'SELECT an_bytes, an_int, an_str, id FROM an_table;'
        assert self.table.sql_query_for_fields(['id'          ]) == 'SELECT id FROM an_table;'
        assert self.table.sql_query_for_fields(['an_int'      ]) == 'SELECT an_int FROM an_table;'
        assert self.table.sql_query_for_fields(['an_str'      ]) == 'SELECT an_str FROM an_table;'
        assert self.table.sql_query_for_fields(['an_str', 'id']) == 'SELECT an_str, id FROM an_table;'

    def test_validate_row_obj(self):
        def assert_validation_error(table, obj, expected_error):
            error = table.validate_row_obj(obj)
            assert error == expected_error, f"Expected: {expected_error}, Got: {error}"

        # Test case where table_class is not defined
        table_with_no_row_schema = Sqlite__Table(table_name='no-row-schema')
        assert table_with_no_row_schema.row_schema is None
        assert_validation_error(table_with_no_row_schema,None,  f"there is no row_schema defined for this table no-row-schema")  # at column 100


        # Test case where row_obj is None
        assert_validation_error(self.table, None, "provided row_obj was None")  # at column 100

        # Test case where row_obj does not subclass Kwargs_To_Self
        class NonSubclassRow:
            pass
        non_subclass_instance            = NonSubclassRow()
        non_subclass_instance__type_name = str(type(non_subclass_instance))
        assert_validation_error(self.table, non_subclass_instance, f"provided row_obj ({non_subclass_instance__type_name}) is not a subclass of Kwargs_To_Self")  # at column 100

        # Test case where row_obj has an extra field not in the table
        class SubclassRowWithExtra(Kwargs_To_Self):
            extra_field: int
        sub_class_with_extra_row = SubclassRowWithExtra()
        assert_validation_error(self.table, sub_class_with_extra_row, 'provided row_obj has a field that is not part of the current table: ''extra_field')

        # Test case where row_obj has an extra field that doesn't match the correct field type
        class An_Table_Class__With_Bad_Field(Kwargs_To_Self):
            an_str: int
        new_obj_bad_field = An_Table_Class__With_Bad_Field()
        assert_validation_error(self.table, new_obj_bad_field, "provided row_obj has a field an_str that has a field type <class 'int'> that "
                                                                             "does not match the current tables type of that field: <class 'str'>")

        # Test case where row_obj has an extra field with data that doesn't match the correct field type
        new_obj_bad_data        = An_Table_Class(disable_type_safety=True) # we need to disable type safety, or we will not be able to make the assignment in the next line
        new_obj_bad_data.an_str = 123
        expected_reason         = ('provided row_obj has a field an_str that has a field value 123 value that '
                                   "has a type <class 'int'> that does not match the current tables type of that "
                                   "field: <class 'str'>")
        assert_validation_error(self.table, new_obj_bad_data, expected_reason)  # BUG

