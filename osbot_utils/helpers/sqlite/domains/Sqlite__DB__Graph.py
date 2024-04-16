from osbot_utils.helpers.sqlite.domains.Sqlite__DB__Local import Sqlite__DB__Local


class Sqlite__DB__Graph(Sqlite__DB__Local):


    def setup(self):
        self.table_config()
        return self
