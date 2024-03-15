from unittest import TestCase

from osbot_utils.helpers.sqlite.sample_data.Sqlite__Sample_Data__Chinook import Sqlite__Sample_Data__Chinook, \
    FOLDER_NAME__SQLITE_DATA_SETS, FOLDER_NAME__CHINOOK_DATA, PATH__DB__TESTS
from osbot_utils.utils.Files import folder_exists, parent_folder, current_temp_folder, folder_name, folder_create
from osbot_utils.utils.Json import json_from_file
from osbot_utils.utils.Misc import list_set


class test_Sqlite__Sample_Data__Chinook(TestCase):

    def setUp(self):
        self.chinook_sqlite = Sqlite__Sample_Data__Chinook()
        folder_create(PATH__DB__TESTS)                          # todo: refactor to handle this better

    def test_chinook_data_as_json(self):
        chinook_data_as_json = self.chinook_sqlite.chinook_data_as_json()
        assert list_set(chinook_data_as_json) == ['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice',
                                                  'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']

    def test_create_tables(self):
        self.chinook_sqlite.create_tables()
        self.chinook_sqlite.save()




    # def test_create_table_from_data(self):
    #     table = self.chinook_sqlite.create_table_from_data()
    #     assert table.fields() == {'id'   : {'cid': 0, 'name': 'id'   , 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1},
    #                               'name' : {'cid': 1, 'name': 'name' , 'type': 'TEXT'   , 'notnull': 0, 'dflt_value': None, 'pk': 0},
    #                               'value': {'cid': 2, 'name': 'value', 'type': 'TEXT'   , 'notnull': 0, 'dflt_value': None, 'pk': 0}}
    #
    #     for row in table.rows():
    #         name = row.get('name')
    #         value = row.get('value')
    #         data = json_loads(value)
    #         print(f'{name:15} {len(value):10} {len(data):10}')


    def test_create_tables_from_schema(self):
        json_db  = self.chinook_sqlite.json_db
        database = json_db.database
        schemas_fields = self.chinook_sqlite.tables_schemas_fields_from_data()

        assert database.tables() == []

        self.chinook_sqlite.create_tables_from_schema()

        database_tables = database.tables()
        assert len(database_tables) == len(schemas_fields)
        for table in database_tables:
            table_schema    = table.schema__by_name_type()
            expected_schema = schemas_fields[table.table_name]
            assert table_schema.get('id') == 'INTEGER'              # confirm default id field has been set
            del table_schema['id']                                  # delete it
            assert table_schema == expected_schema                  # confirm the schema from table matches the schema used to create the table


    def test_load_db_from_disk(self):
        path_to_file         = self.chinook_sqlite.path_chinook_data_as_json()
        data_from__json_file  = json_from_file(path_to_file)
        data_from__db_chinook = self.chinook_sqlite.load_db_from_disk()

        for table in data_from__db_chinook.tables():
            table_name   = table.table_name
            table_fields = table.fields_names__cached(execute_id=True)
            table_data__from_db   = table.rows(table_fields)
            table_data__from_json = data_from__json_file.get(table_name)
            assert len(table_data__from_db) > 0
            assert table_data__from_db == table_data__from_json


    def test_json_loads_file_from_disk(self):
        path_to_file = self.chinook_sqlite.path_chinook_data_as_json()
        all_data = json_from_file(path_to_file)
        assert len(all_data) == 11
        #for name, data in all_data.items():
        #    print(f'{name:15} {len(data):10}')

    def test_path_chinook_data(self):
        path_chinook_data = self.chinook_sqlite.path_chinook_data()
        assert folder_exists(path_chinook_data) is True
        assert parent_folder(path_chinook_data) == self.chinook_sqlite.path_sqlite_sample_data_sets()
        assert folder_name  (path_chinook_data) == FOLDER_NAME__CHINOOK_DATA

    def test_path_sqlite_sample_data_sets(self):
        path_data_sets = self.chinook_sqlite.path_sqlite_sample_data_sets()
        assert folder_exists(path_data_sets) is True
        assert parent_folder(path_data_sets) == current_temp_folder()
        assert folder_name  (path_data_sets) == FOLDER_NAME__SQLITE_DATA_SETS


    def test__check__chinook_data__schema(self):
        expected_schemas = { 'Genre'         : { 'GenreId'        : 'INTEGER' , 'Name'              : 'TEXT'     },
                             'MediaType'     : { 'MediaTypeId'    : 'INTEGER' , 'Name'              : 'TEXT'     },
                             'Artist'        : { 'ArtistId'       : 'INTEGER' , 'Name'              : 'TEXT'     },
                             'Album'         : { 'AlbumId'        : 'INTEGER' , 'ArtistId'          : 'INTEGER'  ,
                                                 'Title'          : 'TEXT'                                       },
                             'Track'         : { 'AlbumId'        : 'INTEGER' , 'Bytes'             : 'INTEGER'  ,
                                                 'Composer'       : 'TEXT'    , 'GenreId'           : 'INTEGER'  ,
                                                 'MediaTypeId'    : 'INTEGER' , 'Milliseconds'      : 'INTEGER'  ,
                                                 'Name'           : 'TEXT'    , 'TrackId'           : 'INTEGER'  ,
                                                 'UnitPrice'      : 'REAL'                                       },
                             'Employee'      : { 'Address'        : 'TEXT'    , 'BirthDate'         : 'TEXT'     ,
                                                 'City'           : 'TEXT'    , 'Country'           : 'TEXT'     ,
                                                 'Email'          : 'TEXT'    , 'EmployeeId'        : 'INTEGER'  ,
                                                 'Fax'            : 'TEXT'    , 'FirstName'         : 'TEXT'     ,
                                                 'HireDate'       : 'TEXT'    , 'LastName'          : 'TEXT'     ,
                                                 'Phone'          : 'TEXT'    , 'PostalCode'        : 'TEXT'     ,
                                                 'ReportsTo'      : 'INTEGER' , 'State'             : 'TEXT'     ,
                                                 'Title'          : 'TEXT'                                       },
                             'Customer'      : { 'Address'        : 'TEXT'     , 'City'             : 'TEXT'     ,
                                                 'Company'        : 'TEXT'     , 'Country'          : 'TEXT'     ,
                                                 'CustomerId'     : 'INTEGER'  , 'Email'            : 'TEXT'     ,
                                                 'Fax'            : 'TEXT'     , 'FirstName'        : 'TEXT'     ,
                                                 'LastName'       : 'TEXT'     , 'Phone'            : 'TEXT'     ,
                                                 'PostalCode'     : 'TEXT'     , 'State'            : 'TEXT'     ,
                                                 'SupportRepId'   : 'INTEGER'                                    },
                             'Invoice'       : { 'BillingAddress' : 'TEXT'     , 'BillingCity'      : 'TEXT'     ,
                                                 'BillingCountry' : 'TEXT'     , 'BillingPostalCode': 'TEXT'     ,
                                                 'BillingState'   : 'TEXT'     , 'CustomerId'       : 'INTEGER'  ,
                                                 'InvoiceDate'    : 'TEXT'     , 'InvoiceId'        : 'INTEGER'  ,
                                                 'Total'          : 'REAL'                                       },
                             'InvoiceLine'   : { 'InvoiceId'      : 'INTEGER'  , 'InvoiceLineId'    : 'INTEGER'  ,
                                                 'Quantity'       : 'INTEGER'  , 'TrackId'          : 'INTEGER'  ,
                                                 'UnitPrice'      : 'REAL'                                       },
                             'Playlist'      : { 'Name'           : 'TEXT'     , 'PlaylistId'       : 'INTEGER'  },
                             'PlaylistTrack' : { 'PlaylistId'     : 'INTEGER'  , 'TrackId'          : 'INTEGER'  }}

        schemas = self.chinook_sqlite.tables_schemas_fields_from_data()
        assert self.chinook_sqlite.tables_schemas_fields_from_data() == expected_schemas # check all schemas in one go

        #test one table
        table_name  = 'Playlist'
        table_schema = schemas.get(table_name)
        table = self.chinook_sqlite.json_db.create_table_from_schema(table_name, table_schema)
        assert table.exists() is True
        assert table.schema__by_name_type() == {'Name': 'TEXT', 'PlaylistId': 'INTEGER', 'id': 'INTEGER'}




    # def test__performance_test__load_db_from_disk__using_sqlite3(self):
    #     def dict_factory(_, row):
    #         fields = [column[0] for column in _.description]
    #         value = {key: value for key, value in zip(fields, row)}
    #         return row
    #
    #     def run_performance_test(use_dict_factory, db_to_load, print_table=True):
    #
    #         if use_dict_factory:
    #             duration_prefix = '\tWith dict_factory   '
    #         else:
    #             duration_prefix = '\tWithout dict_factory'
    #
    #         with Duration(prefix=duration_prefix):
    #             connection     = sqlite3.connect(db_to_load)
    #             if use_dict_factory:
    #                 connection.row_factory = dict_factory
    #             cursor         = connection.cursor()
    #             sql_tables     = 'select name from sqlite_master where type="table"'
    #             sql_table_data = 'select * from {table_name}'
    #             cursor.execute(sql_tables)
    #             tables_names = []
    #             for cell in cursor.fetchall():
    #                 tables_names.append(cell[0])
    #             if print_table:
    #                 print(f"|{'-' * 50}|")
    #                 print(f"| {'Table Name':25} | {'# Rows':5} | {'Duration'} |")
    #                 print(f"|{'-' * 50}|")
    #             for table_name in tables_names:
    #                 with Duration(print_result=False) as duration:
    #                     cursor.execute(f'SELECT COUNT(*) as size FROM {table_name}')
    #                     size = cursor.fetchone()[0]
    #                 print(f'| {table_name:25} | {size:8} | {duration.milliseconds():6.2f} ms |')
    #                 #     sql_query = sql_table_data.format(table_name=table_name)
    #                 #     cursor.execute(sql_query)
    #                 #     table_data = cursor.fetchall()
    #                 # if print_table:
    #                 #     print(f'| {table_name:25} | {len(table_data):6} | {duration.milliseconds():6.2f} ms |')
    #
    #             if print_table:
    #                 print(f"|{'-' * 50}|")
    #             connection.close()
    #
    #
    #     def test_on_file(db_to_load):
    #         print(f"\n******* loading db: {db_to_load} *******\n")
    #         run_performance_test(use_dict_factory=True, db_to_load=db_to_load)
    #         run_performance_test(use_dict_factory=False, db_to_load=db_to_load)
    #
    #
    #     print()
    #     test_on_file(db_to_load=PATH__DB__CHINOOK)
    #     #test_on_file(db_to_load='/Users/diniscruz/Downloads/acs-1-year-2015.sqlite')
    #     #test_on_file(db_to_load='/Users/diniscruz/Downloads/census2000names.sqlite')
    #     #test_on_file(db_to_load='/Users/diniscruz/Downloads/nba.sqlite')
    #     #test_on_file(db_to_load='/Users/diniscruz/Downloads/enwiki-20170820.db')
    #     # test_on_file(db_to_load='/Users/diniscruz/Downloads/enwiki-20170820.db')
    #     #test_on_file(db_to_load='/Users/diniscruz/Downloads/sfpd-incidents.sqlite')




