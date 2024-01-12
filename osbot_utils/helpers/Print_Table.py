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

    def add_data(self, data):
        if type(data) is dict:
            self.add_dict(data)
        elif type(data) is list:
            for item in data:
                self.add_data(item)
        else:
            self.add_row(data)
        return self

    def add_dict(self, data:dict):
        self.fix_table()                                                # makes sure the number of headers and rows are the same

        all_headers = set(self.headers) | set(data.keys())              # get all headers from the table and the data
        for header in sorted(all_headers):                              # sorted to have consistent order of new headers (since without it the order is pseudo random)
            if header not in self.headers:                              # to make sure the table headers and new data keys match
                self.add_header(header)                                 # add any new headers not already present

        row_raw = {header: '' for header in all_headers}                # Create a raw row with empty values for all headers
        row_raw.update(data)                                            # Update the raw row with values from data
        row_by_header = [row_raw[header] for header in self.headers]    # create a new row object, ensuring headers order
        self.add_row(row_by_header)                                     # add the new row to the table
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
        self.headers_size = [len(header) for header in self.headers]                            # initialize the headers size with the size of each header
        for row in self.rows:                                                                   # iterate over each row and update the headers size with the size of the largest cell
            for index, cell in enumerate(row):                                                  # for each row
                self.headers_size[index] = max(self.headers_size[index], len(cell))             # update the header size with the size of the largest cell in the same column

        # fix edge case that happens when the title or footer is longer than the table width
        if len(self.headers_size):
            last_header                 = len(self.headers_size) - 1                            # get the index of the last header
            last_header_size            = self.headers_size[last_header]                        # get the size of the last header
            all_headers_size            = sum(self.headers_size)                                # get the size of all headers
            all_headers_size_minus_last = all_headers_size - last_header_size                   # get the size of all headers minus the last header

            if sum(self.headers_size) < len(self.title):                                        # if the title is longer than the headers, update the last header size
                title_size                     = len(self.title)                                # get the size of the title
                new_last_header_size           = title_size - all_headers_size_minus_last       # calculate the new size of the last header
                self.headers_size[last_header] = new_last_header_size                           # update the last header size
            if sum(self.headers_size) < len(self.footer):                                       # if the footer is longer than the headers, update the last header size
                footer_size                    = len(self.footer)                               # get the size of the footer
                new_last_header_size           = footer_size - all_headers_size_minus_last      # calculate the new size of the last header
                self.headers_size[last_header] = new_last_header_size                           # update the last header size
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

    def reorder_columns(self, new_order: list):
        if set(new_order) != set(self.headers):                                                 # Check if the new_order list has the same headers as the current table
            raise ValueError("New order must contain the same headers as the current table.")

        index_map = {old_header: new_order.index(old_header) for old_header in self.headers}    # Create a mapping from old index to new index
        new_rows = []                                                                           # Reorder each row according to the new header order
        for row in self.rows:
            new_row = [None] * len(row)                                                         # Initialize a new row with placeholders
            for old_index, cell in enumerate(row):
                new_index = index_map[self.headers[old_index]]
                new_row[new_index] = cell
            new_rows.append(new_row)

        self.headers = new_order                                                                # Reorder the headers
        self.rows = new_rows                                                                    # Reorder the rows
        return self


    def set_footer(self, footer):
        self.footer = footer
        return self

    def set_headers(self, headers):
        self.headers = headers
        return self

    def set_title(self, title):
        self.title = title
        return self

    def to_csv(self):
        csv_content = ','.join(self.to_csv__escape_cell(header) for header in self.headers) + '\n'          # Create a CSV string from the headers and rows
        for row in self.rows:
            csv_content += ','.join(self.to_csv__escape_cell(cell) if cell is not None else '' for cell in row) + '\n'
        return csv_content

    def to_csv__escape_cell(self, cell):
        if cell and any(c in cell for c in [',', '"', '\n']):
            cell = cell.replace('"', '""')              # Escape double quotes
            cell = cell.replace('\n', '\\n')            # escape new lines
            return f'"{cell}"'                          # Enclose the cell in double quotes
        return cell

    def to_dict(self):
        table_dict = {header: [] for header in self.headers}                                # Initialize the dictionary with empty lists for each header
        for row in self.rows:                                                               # Iterate over each row and append the cell to the corresponding header's list
            for header, cell in zip(self.headers, row):
                table_dict[header].append(cell)
        return table_dict