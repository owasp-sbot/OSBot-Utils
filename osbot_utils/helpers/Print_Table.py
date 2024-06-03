from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.utils.Str                   import ansi_text_visible_length

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

MAX_CELL_SIZE = 200

class Print_Table(Kwargs_To_Self):
    title               : str
    headers             : list
    headers_by_index    : dict
    footer              : str
    headers_size        : list
    headers_to_hide     : list
    max_cell_size       : int = MAX_CELL_SIZE
    rows                : list
    rows_texts          : list
    table_width         : int
    text__all           : list
    text__footer        : str
    text__headers       : str
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

    def calculate_max_cell_size(self, cell):
        lines_len = []
        for line in str(cell).split('\n'):                                      # Split the cell into lines and find the maximum length of any line
            line_len_ansi_visible = ansi_text_visible_length(line)              # add support for the use of ansi chars (which impact the len calculations)
            lines_len.append(line_len_ansi_visible)
        max_cell_line_length = max(lines_len)

        if max_cell_line_length > self.max_cell_size:
            max_cell_line_length = self.max_cell_size
        return max_cell_line_length

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
        for index, header in enumerate(self.headers):               # capture the index of the headers
            self.headers_by_index[index] = header

    def hide_headers(self, headers):
        self.headers_to_hide = headers
        return self

    def map_headers_size(self):
        self.headers_size = []                                                                        # initialize the headers size with the size of each header
        for header in self.headers:
            header_len_ansi_visible = ansi_text_visible_length(header)
            self.headers_size.append(header_len_ansi_visible)

        for row in self.rows:                                                                       # iterate over each row and update the headers size with the size of the largest cell
            for index, cell in enumerate(row):                                                      # for each row
                if cell:                                                                            # Check if the cell is not empty or None
                    max_cell_line_length = self.calculate_max_cell_size(cell)
                    self.headers_size[index] = max(self.headers_size[index], max_cell_line_length)  # Update the corresponding header size if this line is longer than the current max

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


    # def map_rows_texts(self):
    #     self.rows_texts = []
    #     if not self.rows:
    #         self.rows_texts = [f"{CHAR_TABLE_VERTICAL}  {CHAR_TABLE_VERTICAL}"]
    #     else:
    #         for row in self.rows:
    #             row_text = CHAR_TABLE_VERTICAL
    #             for index, cell in enumerate(row):
    #                 size = self.headers_size[index]
    #                 row_text += f" {str(cell):{size}} {CHAR_TABLE_VERTICAL}"
    #             self.rows_texts.append(row_text)
    #     return self

    def cell_value(self, cell_value):
        cell_value = str(cell_value)
        if len(cell_value) > self.max_cell_size:
            return cell_value[:self.max_cell_size - 3] + '...'
        return cell_value

    def map_rows_texts(self):
        self.rows_texts = []
        #if not self.rows:
        #    self.rows_texts = [f"{CHAR_TABLE_VERTICAL}aaa{CHAR_TABLE_VERTICAL}"]
        if self.rows:
            for row in self.rows:
                row_text = CHAR_TABLE_VERTICAL
                additional_lines = [[] for _ in row]  # Prepare to hold additional lines from multiline cells
                for index, cell in enumerate(row):
                    if self.should_show_header(index):
                        size          = self.headers_size[index]
                        cell_lines    = str(cell).split('\n')  # Split the cell text by newlines
                        cell_value    = self.cell_value(cell_lines[0])
                        extra_padding = ' ' * (size - ansi_text_visible_length(cell_value))
                        row_text += f" {cell_value}{extra_padding} {CHAR_TABLE_VERTICAL}"  # Add the first line of the cell
                        for i, line in enumerate(cell_lines[1:], start=1):
                            additional_lines[index].append(line)  # Store additional lines

                self.rows_texts.append(row_text)

                # Handle additional lines by creating new row_texts for them
                max_additional_lines = max(len(lines) for lines in additional_lines)

                for depth in range(max_additional_lines):
                    extra_row_text = CHAR_TABLE_VERTICAL
                    for index, column in  enumerate(additional_lines):
                        cell_data     = column[depth] if len(column) > depth else ''
                        size          = self.headers_size[index]
                        cell_value    = self.cell_value(cell_data)
                        extra_padding = ' ' * (size - ansi_text_visible_length(cell_value))
                        extra_row_text += f" {cell_value}{extra_padding} {CHAR_TABLE_VERTICAL}"
                    self.rows_texts.append(extra_row_text)

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
                if self.should_show_header(header):
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


    def print(self, data=None, order=None):
        if data:
            self.add_data(data)
        if order:
            self.reorder_columns(order)
        print()
        self.map_texts()
        for text in self.text__all:
            print(text)
        return self

    def should_show_header(self, header):
        if self.headers_to_hide:
            if type(header) is int:
                header_name = self.headers_by_index[header]
            else:
                header_name = str(header)
            return header_name not in self.headers_to_hide
        return True

    def remove_columns(self,column_names):
        if type (column_names) is str:
            column_names = [column_names]
        if type(column_names) is list:
            for column_name in column_names:
                if column_name in self.headers:
                    column_index = self.headers.index(column_name)
                    del self.headers[column_index]
                    for row in self.rows:
                        del row[column_index]
        return self

    def reorder_columns(self, new_order: list):
        if set(new_order) != set(self.headers):                                                 # Check if the new_order list has the same headers as the current table
            missing = set(self.headers) - set(new_order) or {}
            extra   = set(new_order) - set(self.headers) or {}
            raise ValueError("New order must contain the same headers as the current table.\n"
                             f"  - Missing headers: {missing}\n"
                             f"  - Extra headers: {extra}")

        index_map = {old_header: new_order.index(old_header) for old_header in self.headers}    # Create a mapping from old index to new index
        new_rows = []                                                                           # Reorder each row according to the new header order
        for row in self.rows:
            new_row = [None] * len(row)                                                         # Initialize a new row with placeholders
            for old_index, cell in enumerate(row):
                new_index = index_map[self.headers[old_index]]
                new_row[new_index] = cell
            new_rows.append(new_row)

        self.headers = list(new_order)                                                                # Reorder the headers
        self.rows    = new_rows                                                                    # Reorder the rows
        return self


    def set_footer(self, footer):
        self.footer = footer
        return self

    def set_headers(self, headers):
        self.headers = headers
        return self

    def set_order(self, *new_order):
        return self.reorder_columns(new_order)

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