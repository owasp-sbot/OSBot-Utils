from unittest                                           import TestCase
from osbot_utils.base_classes.Kwargs_To_Self            import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Table           import Sqlite__Table
from osbot_utils.helpers.sqlite.sql_builder.SQL_Builder import SQL_Builder
from osbot_utils.utils.Objects                          import default_value

TEST_TABLE_NAME       = 'an_table'

class An_Table_Class(Kwargs_To_Self):
    an_str: str
    an_int: int
    an_bytes: bytes


class test_SQL_Builder(TestCase):
    #db_chinook: Sqlite__Database
    table     : Sqlite__Table

    @classmethod
    def setUpClass(cls) -> None:
        #cls.db_chinook = Sqlite__Sample_Data__Chinook().load_db_from_disk()
        #cls.table      = cls.db_chinook.table('Genre')
        cls.table      = Sqlite__Table(table_name=TEST_TABLE_NAME, row_schema=An_Table_Class)
        assert cls.table.create() is True

    @classmethod
    def tearDownClass(cls):
        cls.table.delete()


    def setUp(self):
        self.sql_builder = SQL_Builder(table=self.table)

    def test_validate_query_data(self):
        self.sql_builder.validate_query_data()
        # with self.assertRaises(ValueError) as context:
        #
        # assert context.exception.args[0] == 'in SQL_Builder, there was no row_schema defined in the mapped table'

    def test_create_temp_schema(self):
        field_types= self.table.fields_types__cached()

        Schema = type('Schema', (Kwargs_To_Self,), {k: default_value(v) for k, v in field_types.items()})
        Schema.__annotations__ = field_types
        assert type(Schema) == type
        schema_obj = Schema(an_str='abc')
        schema_obj.an_int = 123
        assert schema_obj.__locals__() == {'an_bytes': b'', 'an_int': 123, 'an_str': 'abc', 'id': 0}

    def test_command_delete_table(self):
        assert self.sql_builder.command__delete_table() == 'DELETE FROM an_table'

    def test_command__delete_where(self):
        query_conditions = dict(an_int=4)
        sql_query, params = self.sql_builder.command__delete_where(query_conditions)
        assert sql_query == 'DELETE FROM an_table WHERE an_int=?'
        assert params    == [4]

        with self.assertRaises(Exception) as context:
            self.sql_builder.command__delete_where(dict(an_int_2=42))
        assert context.exception.args[0] == 'in validate_query_fields, invalid, invalid return_field: "an_int_2"'

    def test_sql_command_for_insert(self):
        valid_field_names = self.table.fields_names__cached()
        assert valid_field_names == ['an_bytes', 'an_int', 'an_str', 'id']
        assert self.sql_builder.command_for_insert({'id': 42}            ) == ('INSERT INTO an_table (id) VALUES (?)'           , [42  ])
        assert self.sql_builder.command_for_insert({'id': 1, 'an_int':2 }) == ('INSERT INTO an_table (id, an_int) VALUES (?, ?)', [1, 2])
        assert self.sql_builder.command_for_insert({'id': None          }) == ('INSERT INTO an_table (id) VALUES (?)'           , [None])
        assert self.sql_builder.command_for_insert({}                    ) is None
        assert self.sql_builder.command_for_insert(None                  ) is None
        assert self.sql_builder.command_for_insert(''                    ) is None
        assert self.sql_builder.command_for_insert('aaa'                 ) is None
        with self.assertRaises(Exception) as context:
            self.sql_builder.command_for_insert({None: 42})
        assert context.exception.args[0] == 'in sql_command_for_insert, there was a field_name "None" that did exist in the current table'
        with self.assertRaises(Exception) as context:
            self.sql_builder.command_for_insert({'a': 42})
        assert context.exception.args[0] == 'in sql_command_for_insert, there was a field_name "a" that did exist in the current table'

    def test_sql_query_for_fields(self):
        assert self.sql_builder.query_for_fields() == 'SELECT an_bytes, an_int, an_str, id FROM an_table;'
        assert self.sql_builder.query_for_fields(['id']) == 'SELECT id FROM an_table;'
        assert self.sql_builder.query_for_fields(['an_int']) == 'SELECT an_int FROM an_table;'
        assert self.sql_builder.query_for_fields(['an_str']) == 'SELECT an_str FROM an_table;'
        assert self.sql_builder.query_for_fields(['an_str', 'id']) == 'SELECT an_str, id FROM an_table;'

    def test_sql_query_for_size(self):
        assert self.sql_builder.query_for_size() == 'SELECT COUNT(*) as size FROM an_table'

    def test_sql_query_select_fields_from_table_with_conditions(self):
        _ = self.sql_builder.query_select_fields_with_conditions
        #assert _(None, None) is None
        #assert _(None, None) is None
        #assert _('bb', None) is None
        #assert _('bb', {}  ) is None
        assert _(['an_int'], {'an_int': 12  }) == ('SELECT an_int FROM an_table WHERE an_int=?', [12  ])
        assert _(['an_int'], {'an_int': None}) == ('SELECT an_int FROM an_table WHERE an_int=?', [None])


    def test_sql_query_update_with_conditions(self):
        update_fields    = {'an_int': 12}
        query_conditions = {'an_str': '42'}
        _ = self.sql_builder.sql_query_update_with_conditions
        assert _(update_fields, query_conditions) == ('UPDATE an_table SET an_int=? WHERE an_str=?', [12, '42'])

        update_fields = {}
        assert _(update_fields, query_conditions) is None
        update_fields = {'an_int': 12}
        query_conditions = {}
        assert _(update_fields, query_conditions) is None

        update_fields = {'aaaaaa': 12}
        with self.assertRaises(ValueError) as context:
            _(update_fields, query_conditions)
        assert context.exception.args[0] == 'in validate_query_fields, invalid, invalid return_field: "aaaaaa"'
        update_fields    = {'an_int': 12}
        query_conditions = {'bbbb': '42'}
        with self.assertRaises(ValueError) as context:
            _(update_fields, query_conditions)
        assert context.exception.args[0] == 'in validate_query_fields, invalid, invalid return_field: "bbbb"'

    def test__regression__vulnerability__multiple_sqli_in__query_select_fields_from_table_with_conditions(self):

        current_table_name = self.table.table_name
        self.table.table_name = 'aa'
        with self.assertRaises(ValueError) as context:                                                                              # FIXED: exception is now raised
           vulnerable_function         = self.sql_builder.query_select_fields_with_conditions
           var_name                    = 'an_name'
           query_conditions            = {var_name: None}
           return_fields               = ['bb']
           sql_query__no_payloads      = 'SELECT bb FROM aa WHERE an_name=?'
           assert vulnerable_function(return_fields,query_conditions) == (sql_query__no_payloads, [None])
        assert context.exception.args[0] == 'in validate_query_fields, invalid target_table name: "aa"' != ''
        self.table.table_name = current_table_name

        self.table.fields__cached(reload_cache=True) # need to reset this value because "self.table.table_name= 'aa'" above corrupted this value

        # case 1: SQLi payload on table_name
        with self.assertRaises(ValueError) as context:                                                                              # FIXED: exception is now raised
            table_name_with_sqli                  = 'another_table --'
            self.table.table_name                 = table_name_with_sqli
            sql_query__sqli_on_table_name         = f'SELECT bb FROM {table_name_with_sqli} WHERE an_name=?'
            assert sql_query__sqli_on_table_name == 'SELECT bb FROM another_table -- WHERE an_name=?'
            assert vulnerable_function(return_fields, query_conditions) == (sql_query__sqli_on_table_name, [None])
        #assert context.exception.args[0] == 'in validate_query_fields, invalid target_table name: "another_table --"'
        assert context.exception.args[0] == 'Invalid table name. Table names can only contain alphanumeric characters, numbers, underscores, and hyphens.'      # to take into account that now the validation occurs on the setter for table.table_name

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
            vunerable_function =self.sql_builder.query_select_fields_with_conditions
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
        validator = self.sql_builder.validator()
        def assert_validation_error(kwargs, expected_error):
            with self.assertRaises(ValueError) as context:
                validator.validate_query_fields(**kwargs)
            error = context.exception.args[0]
            assert error == expected_error, f"Expected: {expected_error}, Got: {error}"

        # use case 1: no exception when default values are used
        payload = dict(table=self.table, return_fields=[], query_conditions={})
        assert validator.validate_query_fields(**payload) == validator


        # use case 2: return_fields not a list
        payload['table'        ] = self.table
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
        validator.validate_query_fields(**payload)         # no exception raised


