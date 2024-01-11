from osbot_utils.utils.Dev import pprint

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self


raw_data = """|-------------------------------------------------------------------------------------|
| BOTO3 REST calls (via BaseClient._make_api_call)                                    |
|-------------------------------------------------------------------------------------|
| #  | Method                 | Duration | Params                                     | Return Value                               |
|-------------------------------------------------------------------------------------|
|  0 | GetCallerIdentity      |   412 ms | ('GetCallerIdentity', {}) | {'UserId': 'AIDAW3B45JBMJ7OKHCQZL', 'Account': '470426667096', 'Arn': 'arn:aws:iam::470426667096:user/OSBot-AWS-Dev__Only-IAM'}     |
|  1 | GetCallerIdentity      |    97 ms | ('GetCallerIdentity', {}) | {'UserId': 'AIDAW3B45JBMJ7OKHCQZL', 'Account': '470426667096', 'Arn': 'arn:aws:iam::470426667096:user/OSBot-AWS-Dev__Only-IAM'}     |
|  2 | GetCallerIdentity      |    96 ms | ('GetCallerIdentity', {}) | {'UserId': 'AIDAW3B45JBMJ7OKHCQZL', 'Account': '470426667096', 'Arn': 'arn:aws:iam::470426667096:user/OSBot-AWS-Dev__Only-IAM'}     |
|-------------------------------------------------------------------------------------|
| Total Duration:   0.73 secs | Total calls: 3          |
|-------------------------------------------------------------------------------------|
"""

CHAR_TABLE_HORIZONTAL = "─"

CHAR_TABLE_BOTTOM_LEFT  = "└"
CHAR_TABLE_BOTTOM_RIGHT = "┘"
CHAR_TABLE_MIDDLE_LEFT  = "├"
CHAR_TABLE_MIDDLE_RIGHT = "┤"
CHAR_TABLE_MIDDLE       = "┼"
CHAR_TABLE_VERTICAL     = "│"
CHAR_TABLE_TOP_LEFT     = "┌"
CHAR_TABLE_TOP_RIGHT    = "┐"

class Print_Table(Kwargs_To_Self):
    title               : str
    headers             : list
    footer              : str
    headers_size        : list
    rows                : list
    rows_texts          : list
    table_width         : int
    #top_separator      : str
    text__footer        : str
    text__headers       : list
    text__table_bottom  : str
    text__table_middle  : str
    text__table_top     : str
    text__title         : str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def print(self):
        self.map_headers_size       ()
        self.map_text__headers      ()
        self.map_rows_texts         ()
        self.map_table_width        ()
        self.map_text__footer       ()
        self.map_text__title        ()
        self.map_text__table_bottom ()
        self.map_text__table_middle ()
        self.map_text__table_top    ()


        #text_separator = f"{CHAR_TABLE_VERTICAL}" + CHAR_TABLE_HORIZONTAL * (self.table_width  -3) + f"-{CHAR_TABLE_VERTICAL}"


        text_separator = self.text__table_middle

        print(self.text__table_top)
        print(self.text__title)
        print(text_separator)
        print(self.text__headers)
        print(text_separator)
        for row_text in self.rows_texts:
            print(row_text)
        print(text_separator)
        print(self.text__footer)
        print(self.text__table_bottom)

    def map_text__headers(self):
        self.text__headers = CHAR_TABLE_VERTICAL
        for header, size in zip(self.headers, self.headers_size):
            self.text__headers += f" {header:{size}} {CHAR_TABLE_VERTICAL}"
        return self

    def map_headers_size(self):
        self.headers_size = [len(header) for header in self.headers]
        for row in self.rows:                               # Update max width based on row data
            for index, cell in enumerate(row):
                self.headers_size[index] = max(self.headers_size[index], len(cell))
        return self

    def map_text__footer(self):
        self.text__footer = f"{CHAR_TABLE_VERTICAL} {self.footer:{self.table_width - 4}} {CHAR_TABLE_VERTICAL}"

    def map_text__table_bottom(self):
        self.text__table_bottom = f"{CHAR_TABLE_BOTTOM_LEFT}" + CHAR_TABLE_HORIZONTAL * (self.table_width - 2) + f"{CHAR_TABLE_BOTTOM_RIGHT}"

    def map_text__table_middle(self):
        self.text__table_middle = f"{CHAR_TABLE_MIDDLE_LEFT}" + CHAR_TABLE_HORIZONTAL * (self.table_width - 2) + f"{CHAR_TABLE_MIDDLE_RIGHT}"

    def map_text__table_top(self):
        self.text__table_top = f"{CHAR_TABLE_TOP_LEFT}" + CHAR_TABLE_HORIZONTAL * (self.table_width - 2) + f"{CHAR_TABLE_TOP_RIGHT}"

    def map_text__title(self):
        self.text__title = f"{CHAR_TABLE_VERTICAL} {self.title:{self.table_width - 4}} {CHAR_TABLE_VERTICAL}"

    def map_rows_texts(self):
        self.rows_texts = []
        for row in self.rows:
            row_text = CHAR_TABLE_VERTICAL
            for index, cell in enumerate(row):
                size = self.headers_size[index]
                row_text += f" {cell:{size}} {CHAR_TABLE_VERTICAL}"
            self.rows_texts.append(row_text)
        return self

    def map_table_width(self):
        self.table_width = len(self.text__headers)