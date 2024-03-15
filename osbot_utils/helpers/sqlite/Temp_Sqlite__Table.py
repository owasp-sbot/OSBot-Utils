from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.helpers.sqlite.Sqlite__Database import Sqlite__Database
from osbot_utils.helpers.sqlite.Sqlite__Table import Sqlite__Table
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Misc import random_text


class Temp_Sqlite__Table(Kwargs_To_Self):
    table_name   : str           = random_text(prefix='random_table')
    table_fields : list
    table        : Sqlite__Table


    def __init__(self):
        super().__init__()
        self.table.table_name   = self.table_name

    def __enter__(self):
        self.table.create()
        return self.table

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.table.delete()
