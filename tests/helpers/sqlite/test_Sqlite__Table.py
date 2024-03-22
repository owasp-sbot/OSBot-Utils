import inspect
from unittest import TestCase

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.obj_as_context import obj_as_context
from osbot_utils.helpers.Print_Table import Print_Table
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table, SQL_TABLE__MODULE_NAME__ROW_SCHEMA, ROW_BASE_CLASS
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Objects import type_full_name

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

    def test_row_schema__create_from_current_field_types(self):
        with self.table as _:
            expected_schema          = {'an_bytes': bytes, 'an_int': int, 'an_str': str}
            expected_values          = {'an_bytes': b'', 'an_int': 0, 'an_str': ''}
            field_types              = _.fields_types__cached(exclude_id=True)
            Current_Row_Schema_Class = _.row_schema
            Dynamic_Row_Schema_Class = _.row_schema__create_from_current_field_types()

            assert _.row_schema                                         == An_Table_Class
            assert field_types                                          == expected_schema
            assert inspect.isclass(Current_Row_Schema_Class           ) is True
            assert inspect.isclass(Dynamic_Row_Schema_Class           ) is True
            assert issubclass(Current_Row_Schema_Class, Kwargs_To_Self) is True
            assert issubclass(Dynamic_Row_Schema_Class, Kwargs_To_Self) is True
            assert Current_Row_Schema_Class.__cls_kwargs__()            == expected_values
            assert Dynamic_Row_Schema_Class.__cls_kwargs__()            == expected_values
            assert Current_Row_Schema_Class.__schema__()                == expected_schema
            assert Dynamic_Row_Schema_Class.__schema__()                == expected_schema
            assert Current_Row_Schema_Class.__name__                    == 'An_Table_Class'
            assert Dynamic_Row_Schema_Class.__name__                    == 'Row_Schema__An_Table'
            assert Current_Row_Schema_Class.__module__                  == 'test_Sqlite__Table'
            assert Dynamic_Row_Schema_Class.__module__                  == SQL_TABLE__MODULE_NAME__ROW_SCHEMA

            current_obj = Current_Row_Schema_Class()
            dynamic_obj = Dynamic_Row_Schema_Class()
            assert current_obj.__locals__()    == expected_values
            assert dynamic_obj.__locals__()    == expected_values
            assert type_full_name(current_obj) == 'test_Sqlite__Table.An_Table_Class'
            assert type_full_name(dynamic_obj) == f'{SQL_TABLE__MODULE_NAME__ROW_SCHEMA}.Row_Schema__An_Table'

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

    def test_size(self):
        assert self.table.size() == 0

    def test_sql_command_delete_table(self):
        assert self.table.sql_command_delete_table() == 'DELETE FROM an_table'

    def test_sql_command_for_insert(self):
        valid_field_names = self.table.fields_names__cached()
        assert valid_field_names == ['an_bytes', 'an_int', 'an_str', 'id']
        assert self.table.sql_command_for_insert({'id': 42            }) == ('INSERT INTO an_table (id) VALUES (?)'           , [42])
        assert self.table.sql_command_for_insert({'id': 1, 'an_int':2 }) == ('INSERT INTO an_table (id, an_int) VALUES (?, ?)', [1, 2])
        assert self.table.sql_command_for_insert({'id': None          })  == ('INSERT INTO an_table (id) VALUES (?)'          , [None])
        assert self.table.sql_command_for_insert({}                    ) is None
        assert self.table.sql_command_for_insert(None                  ) is None
        assert self.table.sql_command_for_insert(''                    ) is None
        assert self.table.sql_command_for_insert('aaa'                 ) is None
        with self.assertRaises(Exception) as context:
            self.table.sql_command_for_insert({None: 42})
        assert context.exception.args[0] == 'in sql_command_for_insert, there was a field_name "None" that did exist in the current table'
        with self.assertRaises(Exception) as context:
            self.table.sql_command_for_insert({'a': 42})
        assert context.exception.args[0] == 'in sql_command_for_insert, there was a field_name "a" that did exist in the current table'

    def test_sql_query_for_fields(self):
        assert self.table.sql_query_for_fields(                ) == 'SELECT an_bytes, an_int, an_str, id FROM an_table;'
        assert self.table.sql_query_for_fields(['id'          ]) == 'SELECT id FROM an_table;'
        assert self.table.sql_query_for_fields(['an_int'      ]) == 'SELECT an_int FROM an_table;'
        assert self.table.sql_query_for_fields(['an_str'      ]) == 'SELECT an_str FROM an_table;'
        assert self.table.sql_query_for_fields(['an_str', 'id']) == 'SELECT an_str, id FROM an_table;'

    def test_sql_query_for_select_field_name(self):
        assert self.table.sql_query_for_select_field_name('a' ) == 'SELECT a FROM an_table;'
        assert self.table.sql_query_for_select_field_name(''  ) is None
        assert self.table.sql_query_for_select_field_name(None) is None

    def test_sql_query_for_size(self):
        assert self.table.sql_query_for_size('a' ) == 'SELECT COUNT(*) as a FROM an_table'
        assert self.table.sql_query_for_size(''  ) is None
        assert self.table.sql_query_for_size(None) is None

    def test_sql_query_select_fields_from_table_with_conditions(self):
        _ = self.table.sql_query_select_fields_with_conditions
        #assert _(None, None) is None
        #assert _(None, None) is None
        #assert _('bb', None) is None
        #assert _('bb', {}  ) is None
        assert _(['an_int'], {'an_int': 12  }) == ('SELECT an_int FROM an_table WHERE an_int=?', [12  ])
        assert _(['an_int'], {'an_int': None}) == ('SELECT an_int FROM an_table WHERE an_int=?', [None])


    def test__regression__vulnerability__multiple_sqli_in__query_select_fields_from_table_with_conditions(self):

        current_table_name = self.table.table_name
        self.table.table_name = 'aa'
        with self.assertRaises(ValueError) as context:                                                                              # FIXED: exception is now raised
           vulnerable_function         = self.table.sql_query_select_fields_with_conditions
           var_name                    = 'an_name'
           query_conditions            = {var_name: None}
           return_fields               = ['bb']
           sql_query__no_payloads      = 'SELECT bb FROM aa WHERE an_name=?'
           assert vulnerable_function(return_fields,query_conditions) == (sql_query__no_payloads, [None])
        #assert context.exception.args[0] == 'in validate_query_fields, invalid target_table name: "aa"' != ''
        self.table.table_name = current_table_name

        self.table.fields__cached(reload_cache=True) # need to reset this value because "self.table.table_name= 'aa'" above corrupted this value

        # case 1: SQLi payload on table_name
        with self.assertRaises(ValueError) as context:                                                                              # FIXED: exception is now raised
            table_name_with_sqli                  = 'another_table --'
            self.table.table_name                 = table_name_with_sqli
            sql_query__sqli_on_table_name         = f'SELECT bb FROM {table_name_with_sqli} WHERE an_name=?'
            assert sql_query__sqli_on_table_name == 'SELECT bb FROM another_table -- WHERE an_name=?'
            assert vulnerable_function(return_fields, query_conditions) == (sql_query__sqli_on_table_name, [None])
        assert context.exception.args[0] == 'in validate_query_fields, invalid target_table name: "another_table --"'

        # case 2: SQLi payload on return_fields
        with self.assertRaises(ValueError) as context:                                                                              # FIXED: exception is now raised
            self.table.table_name                 = 'an_table'
            return_fields_with_sqli               = ['* from another_table --']
            sql_query__sqli_on_table_name         = f'SELECT {return_fields_with_sqli[0]} FROM {self.table.table_name} WHERE an_name=?'
            assert sql_query__sqli_on_table_name == f'SELECT * from another_table -- FROM an_table WHERE an_name=?'
            assert vulnerable_function(return_fields_with_sqli, query_conditions) == (sql_query__sqli_on_table_name, [None])
        assert context.exception.args[0] == 'in validate_query_fields, invalid, invalid return_field: "* from another_table --"'

        # case 3: SQLi payload on field_name
        with self.assertRaises(ValueError) as context:                                                                              # FIXED: exception is now raised
            field_name__with_sqli                 = "a=? or 1=1 or b="
            param_value                           = "doesn't matter what goes here"
            return_fields                         = ['bb']
            query_conditions                      = { field_name__with_sqli : param_value}
            query_with_sqli                       = 'SELECT bb FROM aa WHERE a=? or 1=1 or b==?'
            assert vulnerable_function(return_fields, query_conditions) == (query_with_sqli, [param_value])
        assert context.exception.args[0] == 'in validate_query_fields, invalid, invalid return_field: "bb"'

    def test__regression__vulnerability__sqli_in__query_select_fields_from_table_with_conditions(self):
        def get_sql_query(field_name,param_value):
            vunerable_function =self.table.sql_query_select_fields_with_conditions
            return_fields      = ['*']
            query_conditions   = { field_name : param_value}
            sql_query,params   = vunerable_function(return_fields, query_conditions)
            return sql_query,params

        assert self.table.schema__by_name_type() == {'an_bytes': 'BLOB'     ,
                                                     'an_int'  : 'INTEGER'  ,
                                                     'an_str'  : 'TEXT'     ,
                                                     'id'      : 'INTEGER'  }
        self.table.add_row(an_int=1 , an_str='uno value')
        self.table.add_row(an_int=42, an_str='the answer')
        assert self.table.rows() == [{'an_bytes': b'', 'an_int': 1 , 'an_str': 'uno value' , 'id': 1},
                                     {'an_bytes': b'', 'an_int': 42, 'an_str': 'the answer', 'id': 2}]

        payload_1__no_exploit = 'an_int'
        sql_query_1, params   = get_sql_query(payload_1__no_exploit, 42)
        result_1              = self.table.cursor().execute(sql_query_1, params)
        data_1                = self.table.cursor().fetch_all()
        status_1              = result_1.get('status')
        assert status_1      == 'ok'
        assert sql_query_1   == 'SELECT * FROM an_table WHERE an_int=?'
        assert data_1        == [{'an_bytes': b'', 'an_int': 42, 'an_str': 'the answer', 'id': 2}]


        with self.assertRaises(ValueError) as context:                                                                     # FIXED: need to catch exception
            payload_2__bad_sql    = 'an_int AAAAAA'
            sql_query_2, params   = get_sql_query(payload_2__bad_sql, 42)                                       # FIXED: was # VULN
            # result_2              = self.table.cursor().execute(sql_query_2, params)
            # status_2              = result_2.get('status')
            # error_2               = result_2.get('error')
            # assert sql_query_2   == 'SELECT * FROM an_table WHERE an_int AAAAAA=?'
            # assert status_2      == 'exception'
            # assert error_2       ==  'near "AAAAAA": syntax error'
        assert context.exception.args[0] == 'in validate_query_fields, invalid, invalid return_field: "an_int AAAAAA"'      # FIXED: correct exception was raised

        with self.assertRaises(ValueError) as context:                                                                      # FIXED: need to catch exception
            payload_3__sqli_1    = 'an_int=? or 1=1 --'
            sql_query_3, params  = get_sql_query(payload_3__sqli_1, 42)                                          # FIXED:  was # VULN
            # result_3             = self.table.cursor().execute(sql_query_3, params)
            # data_3               = self.table.cursor().fetch_all()
            # status_3             = result_3.get('status')
            # assert sql_query_3 == 'SELECT * FROM an_table WHERE an_int=? or 1=1 --=?'
            # assert status_3     == 'ok'
            # assert data_3       == [{'an_bytes': b'', 'an_int': 1, 'an_str': 'uno value', 'id': 1},
            #                         {'an_bytes': b'', 'an_int': 42, 'an_str': 'the answer', 'id': 2}]
        assert context.exception.args[0] == 'in validate_query_fields, invalid, invalid return_field: "an_int=? or 1=1 --"' # FIXED: correct exception was raised
        self.table.clear()

    def test_validate_query_fields(self):
        def assert_validation_error(kwargs, expected_error):
            with self.assertRaises(ValueError) as context:
                self.table.validate_query_fields(**kwargs)
            error = context.exception.args[0]
            assert error == expected_error, f"Expected: {expected_error}, Got: {error}"

        # use case 1: bad table
        payload = dict(target_table='a', return_fields=[], query_conditions={})
        assert_validation_error(payload, 'in validate_query_fields, invalid target_table name: "a"')

        # use case 2: return_fields not a list
        payload['target_table' ] = self.table.table_name
        payload['return_fields'] = 'not a list'
        expected_error           = "in validate_query_fields, return_fields value must be a list, and it was \"<class 'str'>\""
        assert_validation_error(payload, expected_error)

        # use case 3: return_fields bad value
        payload['return_fields'] = ['not a field']
        expected_error           = 'in validate_query_fields, invalid, invalid return_field: "not a field"'
        assert_validation_error(payload, expected_error)

        # use case 4: query_conditions not a dict
        payload['return_fields'   ] = ['an_str']
        payload['query_conditions'] = 'not a dict'
        expected_error              = 'in validate_query_fields, query_conditions value must be a dict, and it was "<class \'str\'>"'
        assert_validation_error(payload, expected_error)

        # use case 5: query_conditions bad value
        payload['query_conditions'] = {'bad field': 42}
        expected_error              = 'in validate_query_fields, invalid, invalid return_field: "bad field"'
        assert_validation_error(payload, expected_error)

        # use case 5: valid data
        payload['query_conditions'] = {'an_int': 42}
        self.table.validate_query_fields(**payload)         # no exception raised

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
        assert_validation_error(self.table, non_subclass_instance, f"provided row_obj ({non_subclass_instance__type_name}) is not a subclass of {ROW_BASE_CLASS}")  # at column 100

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

