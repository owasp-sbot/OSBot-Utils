from unittest import TestCase

from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Json import Sqlite__DB__Json
from osbot_utils.helpers.sqlite.models.Sqlite__Field__Type import Sqlite__Field__Type
from osbot_utils.helpers.sqlite.sample_data.Sqlite__Sample_Data__Chinook import Sqlite__Sample_Data__Chinook, \
    FOLDER_NAME__SQLITE_DATA_SETS, FOLDER_NAME__CHINOOK_DATA, PATH__DB__TESTS
from osbot_utils.testing.Duration import Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import folder_exists, parent_folder, current_temp_folder, folder_name, file_exists, \
    folder_create
from osbot_utils.utils.Json import json_loads, json_from_file
from osbot_utils.utils.Misc import list_set


class test_Sqlite__Sample_Data__Chinook(TestCase):

    def setUp(self):
        self.chinook_sqlite = Sqlite__Sample_Data__Chinook()
        folder_create(PATH__DB__TESTS)                          # todo: refactor to handle this better

    def test_chinook_data_as_json(self):
        chinook_data_as_json = self.chinook_sqlite.chinook_data_as_json()
        assert list_set(chinook_data_as_json) == ['Album', 'Artist', 'Customer', 'Employee', 'Genre', 'Invoice',
                                                  'InvoiceLine', 'MediaType', 'Playlist', 'PlaylistTrack', 'Track']

    def test_create_table_from_data(self):
        table = self.chinook_sqlite.create_table_from_data()
        assert table.fields() == {'id'   : {'cid': 0, 'name': 'id'   , 'type': 'INTEGER', 'notnull': 0, 'dflt_value': None, 'pk': 1},
                                  'name' : {'cid': 1, 'name': 'name' , 'type': 'TEXT'   , 'notnull': 0, 'dflt_value': None, 'pk': 0},
                                  'value': {'cid': 2, 'name': 'value', 'type': 'TEXT'   , 'notnull': 0, 'dflt_value': None, 'pk': 0}}

        for row in table.rows():
            name = row.get('name')
            value = row.get('value')
            data = json_loads(value)
            print(f'{name:15} {len(value):10} {len(data):10}')


    def test_load_db_from_disk(self):
        table = self.chinook_sqlite.load_db_from_disk()
        for row in table.rows():
            name = row.get('name')
            value = row.get('value')
            data = json_loads(value)
            print(f'{name:15} {len(value):10} {len(data):10}' )

    def test_json_loads_file_from_disk(self):
        path_to_file = self.chinook_sqlite.path_chinook_data_as_json()
        all_data = json_from_file(path_to_file)
        for name, data in all_data.items():
            print(f'{name:15} {len(data):10}')

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
        #json_db          = Sqlite__DB__Json()
        #chinook_data     = self.chinook_sqlite.chinook_data_as_json()
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

        # test one table
        # table_name  = 'Playlist'
        # table_schema = schemas.get(table_name)
        # table = self.chinook_sqlite.json_db.create_table_from_schema(table_name, table_schema)
        # assert table.exists() is True
        # assert table.schema__by_name_type() == {'Name': 'TEXT', 'PlaylistId': 'INTEGER', 'id': 'INTEGER'}

        # test all tables
        json_db  = self.chinook_sqlite.json_db
        database = json_db.database
        assert database.tables() == []
        for table_name, table_schema in schemas.items():
            table = json_db.create_table_from_schema(table_name, table_schema)
            assert table.exists() is True
        database_tables = database.tables()
        assert len(database_tables) == len(schemas)
        for table in database_tables:
            table_schema    = table.schema__by_name_type()
            expected_schema = schemas[table.table_name]
            assert table_schema.get('id') == 'INTEGER'              # confirm default id field has been set
            del table_schema['id']                                  # delete it
            assert table_schema == expected_schema                  # confirm the schema from table matches the schema used to create the table


