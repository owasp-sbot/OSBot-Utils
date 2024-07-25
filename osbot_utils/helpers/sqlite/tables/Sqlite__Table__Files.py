from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.utils.Misc import timestamp_utc_now, bytes_sha256, str_sha256
from osbot_utils.utils.Status import status_warning, status_ok

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
        if self.contains(path=path):                                                    # don't allow multiple entries for the same file path (until we add versioning support)
            return status_warning(f"File not added, since file with path '{path}' already exists in the database")
        if metadata is None:
            metadata = {}
        metadata.update(self.create_contents_metadata(contents))
        row_data    = self.create_node_data(path, contents, metadata)
        new_row_obj = self.add_row_and_commit(**row_data)
        return status_ok(message='file added', data= new_row_obj)

    def create_contents_metadata(self, contents):
        file_size       = len(contents)
        file_is_binary = type(contents) is bytes
        if file_is_binary:
            file_hash  = bytes_sha256(contents)
        else:
            file_hash = str_sha256(str(contents))
        return dict(file_contents=dict(hash      = file_hash      ,
                                       is_binary = file_is_binary ,
                                       size      = file_size      ))

    def delete_file(self, path):
        if self.not_contains(path=path):                                                    # don't allow multiple entries for the same file path (until we add versioning support)
            return status_warning(f"File not deleted, since file with path '{path}' did not exist in the database")

        self.rows_delete_where(path=path)
        return status_ok(message='file deleted')

    def create_node_data(self, path, contents=None, metadata= None):
        node_data = {'path'    : path     ,
                     'contents': contents ,
                     'metadata': metadata }
        if self.set_timestamp:
            node_data['timestamp'] = timestamp_utc_now()
        return node_data

    def field_names_without_content(self):                      # todo: refactor to get this directly from the schema
        return ['id', 'path', 'metadata', 'timestamp']          #       and so that these values are not hard-coded here

    def file(self, path, include_contents=True):
        if include_contents:
            fields = ['*']
        else:
            fields = self.field_names_without_content()
        return self.row(where=dict(path=path), fields = fields)

    def file_contents(self, path):
        fields = ['contents']
        row    = self.row(where=dict(path=path), fields = fields)
        if row:
            return row.get('contents')

    def file_without_contents(self, path):
        return self.file(path, include_contents=False)

    def file_exists(self, path):
        return self.contains(path=path)

    def files(self, include_contents=False):
        if include_contents:
            return self.rows()
        fields_names = self.field_names_without_content()
        return self.rows(fields_names)

    def setup(self):
        if self.exists() is False:
            self.create()
            self.index_create('path')
        return self