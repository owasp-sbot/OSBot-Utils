from unittest import TestCase

from osbot_utils.helpers.pubsub.PubSub__Sqlite import PubSub__Sqlite, TABLE_SCHEMA__PUB_SUB__CLIENTS, \
    TABLE_NAME__PUB_SUB__CLIENTS
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table


class test_PubSub__Sqlite(TestCase):
    pubsub_sqlite : PubSub__Sqlite

    @classmethod
    def setUpClass(cls):
        cls.pubsub_sqlite = PubSub__Sqlite().setup()

    def test_setup(self):
        with self.pubsub_sqlite as _:
            assert _.exists()  is True
            assert _.in_memory is True
            assert _.tables_names() == ['pubsub_clients']

        with self.pubsub_sqlite.table_clients() as _:
            assert type(_)       is Sqlite__Table
            assert _.exists()    is True
            assert _.row_schema  is TABLE_SCHEMA__PUB_SUB__CLIENTS
            assert _.table_name  == TABLE_NAME__PUB_SUB__CLIENTS
