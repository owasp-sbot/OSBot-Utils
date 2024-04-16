from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.Lists import unique
from osbot_utils.utils.Misc import timestamp_utc_now

SQLITE__TABLE_NAME__NODES = 'nodes'

class Schema__Table__Nodes(Kwargs_To_Self):
    key       : str
    value     : bytes
    properties: bytes
    timestamp : int

class Sqlite__Table__Nodes(Sqlite__Table):
    allow_duplicate_keys: bool = False
    auto_pickle_blob    : bool = True
    set_timestamp       : bool = True

    def __init__(self, **kwargs):
        self.table_name = SQLITE__TABLE_NAME__NODES
        self.row_schema  = Schema__Table__Nodes
        super().__init__(**kwargs)

    def add_node(self, key, value=None, properties=None):
        if self.allow_duplicate_keys is False:
            if self.contains(key=key):
                return None
        row_data = self.create_node_data(key,value, properties)
        return self.add_row_and_commit(**row_data)

    def create_node_data(self, key, value=None, properties=None):
        node_data =  {'key'        : key                     ,
                      'value'      : value                   ,
                      'properties' : properties              }
        if self.set_timestamp:
            node_data['timestamp'] = timestamp_utc_now()
        return node_data

    @index_by
    def nodes(self):
        return self.rows()

    def keys(self):
        return unique(self.select_field_values('key'))

    def setup(self):
        if self.exists() is False:
            self.create()
            self.index_create('key')
        return self
