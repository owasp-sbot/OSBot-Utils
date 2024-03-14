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
        json_db          = Sqlite__DB__Json()
        chinook_data     = self.chinook_sqlite.chinook_data_as_json()
        expected_schemas = { 'Genre'         : { 'GenreId'        : Sqlite__Field__Type.INTEGER , 'Name'              : Sqlite__Field__Type.TEXT     },
                             'MediaType'     : { 'MediaTypeId'    : Sqlite__Field__Type.INTEGER , 'Name'              : Sqlite__Field__Type.TEXT     },
                             'Artist'        : { 'ArtistId'       : Sqlite__Field__Type.INTEGER , 'Name'              : Sqlite__Field__Type.TEXT     },
                             'Album'         : { 'AlbumId'        : Sqlite__Field__Type.INTEGER , 'ArtistId'          : Sqlite__Field__Type.INTEGER  ,
                                                 'Title'          : Sqlite__Field__Type.TEXT                                                         },
                             'Track'         : { 'AlbumId'        : Sqlite__Field__Type.INTEGER , 'Bytes'             : Sqlite__Field__Type.INTEGER  ,
                                                 'Composer'       : Sqlite__Field__Type.TEXT    , 'GenreId'           : Sqlite__Field__Type.INTEGER  ,
                                                 'MediaTypeId'    : Sqlite__Field__Type.INTEGER , 'Milliseconds'      : Sqlite__Field__Type.INTEGER  ,
                                                 'Name'           : Sqlite__Field__Type.TEXT    , 'TrackId'           : Sqlite__Field__Type.INTEGER  ,
                                                 'UnitPrice'      : Sqlite__Field__Type.REAL                                                         },
                             'Employee'      : { 'Address'        : Sqlite__Field__Type.TEXT    , 'BirthDate'         : Sqlite__Field__Type.TEXT     ,
                                                 'City'           : Sqlite__Field__Type.TEXT    , 'Country'           : Sqlite__Field__Type.TEXT     ,
                                                 'Email'          : Sqlite__Field__Type.TEXT    , 'EmployeeId'        : Sqlite__Field__Type.INTEGER  ,
                                                 'Fax'            : Sqlite__Field__Type.TEXT    , 'FirstName'         : Sqlite__Field__Type.TEXT     ,
                                                 'HireDate'       : Sqlite__Field__Type.TEXT    , 'LastName'          : Sqlite__Field__Type.TEXT     ,
                                                 'Phone'          : Sqlite__Field__Type.TEXT    , 'PostalCode'        : Sqlite__Field__Type.TEXT     ,
                                                 'ReportsTo'      : Sqlite__Field__Type.INTEGER , 'State'             : Sqlite__Field__Type.TEXT     ,
                                                 'Title'          : Sqlite__Field__Type.TEXT                                                         },
                             'Customer'      : { 'Address'        : Sqlite__Field__Type.TEXT     , 'City'             : Sqlite__Field__Type.TEXT     ,
                                                 'Company'        : Sqlite__Field__Type.TEXT     , 'Country'          : Sqlite__Field__Type.TEXT     ,
                                                 'CustomerId'     : Sqlite__Field__Type.INTEGER  , 'Email'            : Sqlite__Field__Type.TEXT     ,
                                                 'Fax'            : Sqlite__Field__Type.TEXT     , 'FirstName'        : Sqlite__Field__Type.TEXT     ,
                                                 'LastName'       : Sqlite__Field__Type.TEXT     , 'Phone'            : Sqlite__Field__Type.TEXT     ,
                                                 'PostalCode'     : Sqlite__Field__Type.TEXT     , 'State'            : Sqlite__Field__Type.TEXT     ,
                                                 'SupportRepId'   : Sqlite__Field__Type.INTEGER                                                      },
                             'Invoice'       : { 'BillingAddress' : Sqlite__Field__Type.TEXT     , 'BillingCity'      : Sqlite__Field__Type.TEXT     ,
                                                 'BillingCountry' : Sqlite__Field__Type.TEXT     , 'BillingPostalCode': Sqlite__Field__Type.TEXT     ,
                                                 'BillingState'   : Sqlite__Field__Type.TEXT     , 'CustomerId'       : Sqlite__Field__Type.INTEGER  ,
                                                 'InvoiceDate'    : Sqlite__Field__Type.TEXT     , 'InvoiceId'        : Sqlite__Field__Type.INTEGER  ,
                                                 'Total'          : Sqlite__Field__Type.REAL                                                         },
                             'InvoiceLine'   : { 'InvoiceId'      : Sqlite__Field__Type.INTEGER  , 'InvoiceLineId'    : Sqlite__Field__Type.INTEGER  ,
                                                 'Quantity'       : Sqlite__Field__Type.INTEGER  , 'TrackId'          : Sqlite__Field__Type.INTEGER  ,
                                                 'UnitPrice'      : Sqlite__Field__Type.REAL                                                         },
                             'Playlist'      : { 'Name'           : Sqlite__Field__Type.TEXT     , 'PlaylistId'       : Sqlite__Field__Type.INTEGER  },
                             'PlaylistTrack' : { 'PlaylistId'     : Sqlite__Field__Type.INTEGER  , 'TrackId'          : Sqlite__Field__Type.INTEGER  }}

        print()
        for name, data  in chinook_data.items():
            expected_schema = expected_schemas.get(name)
            with Duration(prefix =name):
                assert json_db.get_schema_from_json_data(data) == expected_schema


