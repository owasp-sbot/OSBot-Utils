from osbot_utils.decorators.methods.cache_on_self import cache_on_self
from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local import Sqlite__DB__Local
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Edges import Sqlite__Table__Edges
from osbot_utils.helpers.sqlite.tables.Sqlite__Table__Nodes import Sqlite__Table__Nodes


class Sqlite__DB__Graph(Sqlite__DB__Local):

    def __init__(self, db_path=None, db_name=None):
        super().__init__(db_path=db_path, db_name=db_name)

    def add_edge(self, source_key, target_key, value=None, properties=None):
        new_edge = self.table_edges().add_edge(source_key, target_key, value, properties)
        self.add_node(source_key)                                   # assuming node_table.allow_duplicate_keys is set to False
        self.add_node(target_key)                                   # make sure there is a node for each part of the edge added
        return new_edge


    def add_node(self, key, value=None, properties=None):
        return self.table_nodes().add_node(key, value, properties)

    def clear(self):
        self.table_edges().clear()
        self.table_nodes().clear()

    def edges(self):
        return self.table_edges().edges()

    def nodes(self):
        return self.table_nodes().nodes()

    def nodes_keys(self):
        return self.table_nodes().keys()

    @cache_on_self
    def table_edges(self):
        return Sqlite__Table__Edges(database=self).setup()

    @cache_on_self
    def table_nodes(self):
        return Sqlite__Table__Nodes(database=self).setup()

    def setup(self):
        #self.table_config()                    # wire this up when I have a use case for it
        self.table_nodes()
        self.table_edges()
        return self
