from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.helpers.sqlite.Sqlite__Table__Create import Sqlite__Table__Create
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Json import Sqlite__DB__Json
from osbot_utils.testing.Duration import duration, Duration
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Files import current_temp_folder, path_combine, folder_create, file_exists, file_not_exists, \
    file_contents
from osbot_utils.utils.Http import GET, GET_to_file
from osbot_utils.utils.Json import json_loads, json_from_file, json_dump, json_file_create, json_file_load
from osbot_utils.utils.Objects import obj_info

URL__CHINOOK_JSON                = 'https://github.com/lerocha/chinook-database/releases/download/v1.4.5/ChinookData.json'
FILE_NAME__CHINOOK_DATA_JSON     = 'ChinookData.json'
FILE_NAME__TABLES_SCHEMAS_FIELDS = 'chinook__tables_schemas_fields.json'
FOLDER_NAME__CHINOOK_DATA        = 'chinook_data'
FOLDER_NAME__SQLITE_DATA_SETS    = '_sqlite_data_sets'
PATH__DB__TESTS                  = '/tmp/db-tests'
PATH__DB__CHINOOK                = '/tmp/db-tests/test-chinook.db'
TABLE_NAME__CHINOOK              = 'chinook_data'

class Sqlite__Sample_Data__Chinook(Kwargs_To_Self):
    url_chinook_database_json : str                 = URL__CHINOOK_JSON
    path_local_db             : str                 = PATH__DB__CHINOOK
    table_name                : str                 = TABLE_NAME__CHINOOK
    json_db                   : Sqlite__DB__Json



    def chinook_data_as_json(self):
        path_chinook_data_as_json = self.path_chinook_data_as_json()
        if file_not_exists(path_chinook_data_as_json):
            GET_to_file(self.url_chinook_database_json, path_chinook_data_as_json)
        return json_from_file(path_chinook_data_as_json)

    # def create_table_from_data(self):
    #     chinook_data = self.chinook_data_as_json()
    #     table_creator = Sqlite__Table__Create(table_name=self.table_name)
    #     table         = table_creator.table
    #     table_creator.add_fields__text("name", "value").create_table()
    #
    #     cursor = table.cursor()
    #     assert len(chinook_data) == 11
    #     for key, items in chinook_data.items():
    #         name = key
    #         value = json_dump(items)
    #         table.row_add(dict(name=name, value=value))
    #
    #     cursor.commit()
    #     return table

    def create_tables(self):
        self.create_tables_from_schema()
        chinook_data = self.chinook_data_as_json()
        for table_name, rows in chinook_data.items():
            table = self.json_db.database.table(table_name)
            table.rows_add(rows)



    def create_tables_from_schema(self):
        schemas  = self.tables_schemas_fields_from_data()
        for table_name, table_schema in schemas.items():
            self.json_db.create_table_from_schema(table_name, table_schema)
        return self

    def database(self):                         # todo: need to refactor this code based from the creation of the database to the use of it
        return self.json_db.database

    @cache_on_self
    def load_db_from_disk(self):
        db_chinook = Sqlite__Database(db_path=PATH__DB__CHINOOK, auto_schema_row=True)          # set the auto_schema_row so that we have a row_schema defined for all tables
        return db_chinook
        # db_chinook.connect()
        # return db_chinook.table(self.table_name)

    def path_chinook_data_as_json(self):
        return path_combine(self.path_chinook_data(), FILE_NAME__CHINOOK_DATA_JSON)

    def path_chinook_data(self):
        path_chinook_data = path_combine(self.path_sqlite_sample_data_sets(), FOLDER_NAME__CHINOOK_DATA)
        return folder_create(path_chinook_data)

    def path_sqlite_sample_data_sets(self):                     # todo: refactor to sqlite_sample_data_sets helper class
        path_data_sets = path_combine(current_temp_folder(), FOLDER_NAME__SQLITE_DATA_SETS)
        return folder_create(path_data_sets)

    def path_tables_schemas_fields(self):
        return path_combine(self.path_chinook_data(), FILE_NAME__TABLES_SCHEMAS_FIELDS)

    def table__genre(self):
        return self.load_db_from_disk().table('Genre')          # todo: refactor to sqlite_sample_data_sets helper class

    def table__track(self):
        return self.load_db_from_disk().table('Track')          # todo: refactor to sqlite_sample_data_sets helper class

    # def tables(self):
    #     return self.load_db_from_disk().tables()

    def tables_schemas_fields_from_data(self):
        path_tables_schemas_fields = self.path_tables_schemas_fields()
        if file_not_exists(path_tables_schemas_fields):
            tables_schemas = {}
            for name, data  in self.chinook_data_as_json().items():
                table_schema = self.json_db.get_schema_from_json_data(data)
                tables_schemas[name] = table_schema
            json_file_create(tables_schemas, path=path_tables_schemas_fields)

        return json_file_load(path_tables_schemas_fields)

    def save(self, path=PATH__DB__CHINOOK):
        database = self.database()
        database.save_to(path)
        return True