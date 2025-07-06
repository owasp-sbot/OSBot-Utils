from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.pubsub.schemas.Schema__PubSub__Client import Schema__PubSub__Clients
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database

TABLE_NAME__PUB_SUB__CLIENTS   = 'pubsub_clients'
TABLE_SCHEMA__PUB_SUB__CLIENTS = Schema__PubSub__Clients

class PubSub__Sqlite(Sqlite__Database):

    @cache_on_self
    def table_clients(self):
        return self.table(TABLE_NAME__PUB_SUB__CLIENTS)

    def table_clients__create(self):
        with self.table_clients() as _:
            _.row_schema = TABLE_SCHEMA__PUB_SUB__CLIENTS
            if _.exists() is False:
                _.create()  # create if it doesn't exist
                return True
        return False

    def setup(self):
        self.table_clients__create()
        return self