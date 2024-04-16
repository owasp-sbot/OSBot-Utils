from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.utils.Misc import timestamp_utc_now

SQLITE__TABLE_NAME__FILES = 'files'

class Schema__Table__Files(Kwargs_To_Self):
    path     : str
    contents : bytes
    metadata : bytes
    timestamp: int


class Sqlite__Table__Files(Sqlite__Table):
    auto_pickle_blob    : bool = True
    set_timestamp       : bool = True

    def __init__(self, **kwargs):
        self.table_name = SQLITE__TABLE_NAME__FILES
        self.row_schema  = Schema__Table__Files
        super().__init__(**kwargs)

    def add_file(self, path, contents=None, metadata= None):
        if self.contains(path=path):                                     # don't allow multiple entries for the same file path (until we add versioning support)
            return None
        row_data = self.create_node_data(path, contents, metadata)
        return self.add_row_and_commit(**row_data)

    def create_node_data(self, path, contents=None, metadata= None):
        node_data = {'path'    : path     ,
                     'contents': contents ,
                     'metadata': metadata }
        if self.set_timestamp:
            node_data['timestamp'] = timestamp_utc_now()
        return node_data


    def files(self):
        return self.rows()

    def setup(self):
        if self.exists() is False:
            self.create()
            self.index_create('path')
        return self