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
    text__all           : list
    text__footer        : str
    text__headers       : list
    text__table_bottom  : str
    text__table_middle  : str
    text__table_top     : str
    text__title         : str
    text__width         : int

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_column(self, header, cells:list):
        self.fix_table()
        columns_count = len(self.headers)
        self.add_header(header)
        for index, cell in enumerate(cells):
            if len(self.rows) <= index:
                new_row = ['' for _ in range(columns_count)] + [cell]
                self.rows.append(new_row)
            else:
                self.rows[index].append(cell)
        return self

    def add_header(self, header:str):
        self.headers.append(header)
        return self

    def add_headers(self, *headers:list):
        for header in headers:
            self.add_header(header)
        return self

    def add_row(self, row:list):
        if type(row) is not list:
            self.rows.append([row])
        else:
            self.rows.append(row)
        return self

    def add_rows(self, rows:list):
        for row in rows:
            self.add_row(row)
        return self

    def fix_table(self):
        if self.rows:
            max_cells = max(len(row) for row in self.rows)          # get max number of cells in any row
        else:
            max_cells = 0

        extra_header_count = len(self.headers) + 1                  # Start counting extra headers from the current number of headers
        while len(self.headers) < max_cells:                        # Extend headers if necessary
            self.headers.append(f"Header #{extra_header_count}")    # headers cannot have empty values
            extra_header_count += 1
        for row in self.rows:                                       # Ensure each row has the same number of cells as there are headers
            while len(row) < len(self.headers):
                row.append("")

    def map_headers_size(self):
        self.headers_size = [len(header) for header in self.headers]
        for row in self.rows:                                                       # Update max width based on row data
            for index, cell in enumerate(row):
                self.headers_size[index] = max(self.headers_size[index], len(cell))
        return self

    def map_table_width(self):
        self.table_width = len(self.text__headers)
        if len(self.footer) > self.table_width:
            self.table_width = len(self.footer) + 4
        if len(self.title) > self.table_width:
            self.table_width = len(self.title) + 4


    def map_rows_texts(self):
        self.rows_texts = []
        if not self.rows:
            self.rows_texts = [f"{CHAR_TABLE_VERTICAL}  {CHAR_TABLE_VERTICAL}"]
        else:
            for row in self.rows:
                row_text = CHAR_TABLE_VERTICAL
                for index, cell in enumerate(row):
                    size = self.headers_size[index]
                    row_text += f" {cell:{size}} {CHAR_TABLE_VERTICAL}"
                self.rows_texts.append(row_text)
        return self

    def map_text__all(self):
        self.text__all                      = [  self.text__table_top                              ]
        if self.title   :   self.text__all += [  self.text__title        , self.text__table_middle ]
        if self.headers :   self.text__all += [  self.text__headers      , self.text__table_middle ]
        if self.rows    :   self.text__all += [ *self.rows_texts                                   ]
        if self.footer  :   self.text__all += [  self.text__table_middle , self.text__footer       ]
        self.text__all                     += [  self.text__table_bottom                           ]

    def map_text__footer(self):
        self.text__footer = f"{CHAR_TABLE_VERTICAL} {self.footer:{self.text__width}} {CHAR_TABLE_VERTICAL}"

    def map_text__headers(self):
        self.text__headers = CHAR_TABLE_VERTICAL
        if not self.headers:
            self.text__headers += f"  {CHAR_TABLE_VERTICAL}"
        else:
            for header, size in zip(self.headers, self.headers_size):
                self.text__headers += f" {header:{size}} {CHAR_TABLE_VERTICAL}"
            return self

    def map_text__table_bottom(self):   self.text__table_bottom = f"{CHAR_TABLE_BOTTOM_LEFT}" + CHAR_TABLE_HORIZONTAL * (self.text__width + 2) + f"{CHAR_TABLE_BOTTOM_RIGHT }"
    def map_text__table_middle(self):   self.text__table_middle = f"{CHAR_TABLE_MIDDLE_LEFT}" + CHAR_TABLE_HORIZONTAL * (self.text__width + 2) + f"{CHAR_TABLE_MIDDLE_RIGHT }"
    def map_text__table_top   (self):   self.text__table_top    = f"{CHAR_TABLE_TOP_LEFT   }" + CHAR_TABLE_HORIZONTAL * (self.text__width + 2) + f"{CHAR_TABLE_TOP_RIGHT    }"

    def map_text__title(self):
        self.text__title = f"{CHAR_TABLE_VERTICAL} {self.title:{self.text__width}} {CHAR_TABLE_VERTICAL}"

    def map_text__width(self):
        self.text__width = self.table_width - 4
        # if self.table_width > 3:                                      # there is no use case that that needs this check
        #     self.text__width = self.table_width - 4
        # else:
        #     self.text__width = 0

    def map_texts(self):
        self.fix_table              ()
        self.map_headers_size       ()
        self.map_text__headers      ()
        self.map_rows_texts         ()
        self.map_table_width        ()
        self.map_text__width        ()
        self.map_text__footer       ()
        self.map_text__title        ()
        self.map_text__table_bottom ()
        self.map_text__table_middle ()
        self.map_text__table_top    ()
        self.map_text__all          ()


    def print(self):
        print()
        self.map_texts()
        for text in self.text__all:
            print(text)

    def escape_csv_cell(self, cell):
        if cell and any(c in cell for c in [',', '"', '\n']):
            cell = cell.replace('"', '""')              # Escape double quotes
            cell = cell.replace('\n', '\\n')            # escape new lines
            return f'"{cell}"'                          # Enclose the cell in double quotes
        return cell

    def to_csv(self):
        csv_content = ','.join(self.escape_csv_cell(header) for header in self.headers) + '\n'          # Create a CSV string from the headers and rows
        for row in self.rows:
            csv_content += ','.join(self.escape_csv_cell(cell) if cell is not None else '' for cell in row) + '\n'
        return csv_content

    def to_dict(self):
        table_dict = {header: [] for header in self.headers}                                # Initialize the dictionary with empty lists for each header
        for row in self.rows:                                                               # Iterate over each row and append the cell to the corresponding header's list
            for header, cell in zip(self.headers, row):
                table_dict[header].append(cell)
        return table_dict
