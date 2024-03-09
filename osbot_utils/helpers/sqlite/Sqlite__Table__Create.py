from osbot_utils.helpers.sqlite.Sqlite__Field import Sqlite__Field
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table


class Sqlite__Table__Create:

    def __init__(self):
        self.table = Sqlite__Table()
        self.fields : list[Sqlite__Field]  = []

    def add_field(self, field_data: dict):
        self.fields.append('1')