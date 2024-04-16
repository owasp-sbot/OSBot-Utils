from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.Misc import timestamp_utc_now
from osbot_utils.utils.Objects import pickle_save_to_bytes, obj_to_bytes, bytes_to_obj

SQLITE__TABLE_NAME__NODES = 'nodes'

class Schema__Table__Nodes(Kwargs_To_Self):
    key       : str
    value     : bytes
    properties: bytes
    timestamp : int

class Sqlite__Table__Nodes(Sqlite__Table):
    add_timestamp: bool = True

    def __init__(self, **kwargs):
        self.table_name = SQLITE__TABLE_NAME__NODES
        self.row_schema  = Schema__Table__Nodes
        super().__init__(**kwargs)

    def add_node(self, key, value=None, properties=None):
        row_data = self.create_node_data(key,value, properties)
        return self.add_row(**row_data)

    def create_node_data(self, key, value=None, properties=None):

        node_data =  {'key'        : key,
                      'value'      : obj_to_bytes(value     ),
                      'properties' : obj_to_bytes(properties)}
        if self.add_timestamp:
            node_data['timestamp'] = timestamp_utc_now()
        return node_data

    def deserialize_sqlite_node_data(self, sqlite_node_data:dict):
        if type(sqlite_node_data) is dict:
            node_data = sqlite_node_data.copy()
            node_data['value'     ] = bytes_to_obj(node_data.get('value'     ))
            node_data['properties'] = bytes_to_obj(node_data.get('properties'))
            return node_data

    def setup(self):
        if self.exists() is False:
            self.create()
            self.index_create('key')
        return self
