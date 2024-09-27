from unittest                                       import TestCase
from osbot_utils.helpers.sqlite.Sqlite__Database    import Sqlite__Database
from osbot_utils.helpers.sqlite.domains.Sqlite__DB  import Sqlite__DB


class test_Sqlite__DB(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.sqlite_db = Sqlite__DB().setup()

    def test__init__(self):
        with self.sqlite_db as _:
            default_vars  = Sqlite__Database().__attr_names__()
            expected_vars = default_vars

            assert _.__attr_names__() == sorted(expected_vars)
            assert _.tables_names(include_indexes=False) == ['config']

    def test_table_config(self):
        with self.sqlite_db.table_config() as _:
            assert _.exists()   is True
            assert _.table_name == 'config'
            assert _.data()     == {}

    def test_setup(self):
        with self.sqlite_db as _:
            assert _.exists()  is True
            assert _.in_memory is True
            assert _.db_path   is None
            assert _.tables_names() == ['config']
