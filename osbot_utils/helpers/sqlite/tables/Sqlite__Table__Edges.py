from osbot_utils.decorators.lists.index_by import index_by
from osbot_utils.helpers.sqlite.Sqlite__Table   import Sqlite__Table
from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.utils.Misc import timestamp_utc_now

SQLITE__TABLE_NAME__EDGES = 'edges'

class Schema__Table__Edges(Kwargs_To_Self):
    source_key : str
    target_key : str
    value      : bytes
    properties : bytes
    timestamp  : int

class Sqlite__Table__Edges(Sqlite__Table):
    auto_pickle_blob    : bool = True
    set_timestamp       : bool = True

    def __init__(self, **kwargs):
        self.table_name = SQLITE__TABLE_NAME__EDGES
        self.row_schema  = Schema__Table__Edges
        super().__init__(**kwargs)


    def add_edge(self, source_key, target_key, value=None, properties=None):
        row_data = self.create_node_data(source_key, target_key,value, properties)
        return self.add_row_and_commit(**row_data)

    def create_node_data(self, source_key, target_key, value=None, properties=None):
        node_data =  {'source_key' : source_key              ,
                      'target_key' : target_key              ,
                      'value'      : value                   ,
                      'properties' : properties              }
        if self.set_timestamp:
            node_data['timestamp'] = timestamp_utc_now()
        return node_data

    def edges(self):
        return self.rows()

    def setup(self):
        if self.exists() is False:
            self.create()
            self.index_create('source_key')
            self.index_create('target_key')
        return self