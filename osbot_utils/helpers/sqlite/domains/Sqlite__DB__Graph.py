from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local import Sqlite__DB__Local
from osbot_utils.helpers.sqlite.tables.Sqite__Table__Nodes import Sqlite__Table__Nodes


class Sqlite__DB__Graph(Sqlite__DB__Local):

    def __init__(self, db_path=None, db_name=None):
        super().__init__(db_path=db_path, db_name=db_name)

    def table_nodes(self):
        table_config = Sqlite__Table__Nodes(database=self)
        table_config.setup()
        return table_config

    def setup(self):
        self.table_config()
        self.table_nodes()
        return self
