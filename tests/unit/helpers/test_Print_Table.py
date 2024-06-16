import sys
from unittest import TestCase
from unittest.mock import patch, call

import pytest

from osbot_utils.helpers.Print_Table import Print_Table


class test_Print_Table(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        if sys.version_info < (3, 10):
            pytest.skip("Skipping tests that don't work on 3.10 or lower")

    def setUp(self):
        self.print_table = Print_Table()

    def test___init__(self):
        assert self.print_table.__locals__() == { 'footer'              : '' ,
                                                  'headers'             : [] ,
                                                  'headers_by_index'    : {} ,
                                                  'headers_size'        : [] ,
                                                  'headers_to_hide'     : [] ,
                                                  'max_cell_size'       : 200,
                                                  'rows'                : [] ,
                                                  'rows_texts'          : [] ,
                                                  'table_width'         : 0  ,
                                                  'text__all'           : [] ,
                                                  'text__footer'        : '' ,
                                                  'text__headers'       : '' ,
                                                  'text__table_bottom'  : '' ,
                                                  'text__table_middle'  : '' ,
                                                  'text__table_top'     : '' ,
                                                  'text__title'         : '' ,
                                                  'text__width'         : 0  ,
                                                  'title'               : '' }

    def test_add_column(self):
        with self.print_table as _:
            _.add_column(header='header_1', cells=['cell_1', 'cell_2', 'cell_3'])
            _.map_texts()
            assert _.to_dict() == {'header_1': ['cell_1', 'cell_2', 'cell_3']}

            _.add_header('header_2')
            _.map_texts()
            assert _.to_dict() == {'header_1': ['cell_1', 'cell_2', 'cell_3'],
                                   'header_2': ['', '', '']}

            _.add_column(header='header_3',cells= ['cell_4', 'cell_5', 'cell_6'])
            _.map_texts()
            assert _.to_dict() == {'header_1': ['cell_1', 'cell_2', 'cell_3'],
                                  'header_2': ['', '', ''],
                                  'header_3': ['cell_4', 'cell_5', 'cell_6']} != {'header_1': ['cell_1', 'cell_2', 'cell_3'], 'header_2': ['', '', '']}
            _.add_row(['cell_7', 'cell_8', 'cell_9'])
            _.add_row('cell_10')
            _.add_column(header='header_4', cells= ['cell_11', 'cell_12', 'cell_13'])
            assert _.to_dict() == {'header_1': ['cell_1', 'cell_2', 'cell_3', 'cell_7', 'cell_10'],
                                   'header_2': ['', '', '', 'cell_8', ''],
                                   'header_3': ['cell_4', 'cell_5', 'cell_6', 'cell_9', ''],
                                   'header_4': ['cell_11', 'cell_12', 'cell_13']}

            _.add_column(header='header_5', cells=['cell_14', 'cell_15', 'cell_16', 'cell_17', 'cell_18', 'cell_19'])
            assert _.to_dict() == {'header_1': ['cell_1', 'cell_2', 'cell_3', 'cell_7', 'cell_10', ''],
                                   'header_2': ['', '', '', 'cell_8', '', ''],
                                   'header_3': ['cell_4', 'cell_5', 'cell_6', 'cell_9', '', ''],
                                   'header_4': ['cell_11', 'cell_12', 'cell_13', '', '', ''],
                                   'header_5': ['cell_14', 'cell_15', 'cell_16', 'cell_17', 'cell_18', 'cell_19']}
            _.map_texts()
            assert _.text__all == ['┌──────────────────────────────────────────────────────┐',
                                   '│ header_1 │ header_2 │ header_3 │ header_4 │ header_5 │',
                                   '├──────────────────────────────────────────────────────┤',
                                   '│ cell_1   │          │ cell_4   │ cell_11  │ cell_14  │',
                                   '│ cell_2   │          │ cell_5   │ cell_12  │ cell_15  │',
                                   '│ cell_3   │          │ cell_6   │ cell_13  │ cell_16  │',
                                   '│ cell_7   │ cell_8   │ cell_9   │          │ cell_17  │',
                                   '│ cell_10  │          │          │          │ cell_18  │',
                                   '│          │          │          │          │ cell_19  │',
                                   '└──────────────────────────────────────────────────────┘']

            _.add_row([' a\'c ', '  c"d ' , ' e\nf ' ] )
            assert _.to_csv() == ('header_1,header_2,header_3,header_4,header_5\n'
                                  'cell_1,,cell_4,cell_11,cell_14\n'
                                  'cell_2,,cell_5,cell_12,cell_15\n'
                                  'cell_3,,cell_6,cell_13,cell_16\n'
                                  'cell_7,cell_8,cell_9,,cell_17\n'
                                  'cell_10,,,,cell_18\n'
                                  ',,,,cell_19\n'
                                  ' a\'c ,"  c""d "," e\\nf "\n')

    def test_add_data(self):
        data = {'header_1': 'cell_1a',
                'header_2': 'cell_2a',
                'header_4': 'cell_4a'}
        with self.print_table as _:
            _.add_data("will add as row")
            _.map_texts()
            assert _.to_dict() == {'Header #1': ['will add as row']}
        with self.print_table as _:
            _.reset()
            _.add_header('header_3')
            _.add_row('cell_3a')
            _.add_data(data)
            _.add_data({'header_1': 'cell_1b'})
            _.add_data({'header_3': 'cell_3b'})
            _.add_data({'header_2': 'cell_2b'})

            assert _.to_dict() == {'header_1': [''       , 'cell_1a', 'cell_1b' , ''        , ''        ],
                                   'header_2': [''       , 'cell_2a', ''        , ''        , 'cell_2b' ],
                                   'header_3': ['cell_3a', ''       , ''        , 'cell_3b' , ''        ],
                                   'header_4': [''       , 'cell_4a', ''        , ''        , ''        ]}

            _.map_texts()
            assert _.text__all == ['┌───────────────────────────────────────────┐',
                                   '│ header_3 │ header_1 │ header_2 │ header_4 │',
                                   '├───────────────────────────────────────────┤',
                                   '│ cell_3a  │          │          │          │',
                                   '│          │ cell_1a  │ cell_2a  │ cell_4a  │',
                                   '│          │ cell_1b  │          │          │',
                                   '│ cell_3b  │          │          │          │',
                                   '│          │          │ cell_2b  │          │',
                                   '└───────────────────────────────────────────┘']
            _.reorder_columns(sorted(_.headers))
            _.map_texts()
            assert _.text__all == ['┌───────────────────────────────────────────┐',
                                   '│ header_1 │ header_2 │ header_3 │ header_4 │',
                                   '├───────────────────────────────────────────┤',
                                   '│          │          │ cell_3a  │          │',
                                   '│ cell_1a  │ cell_2a  │          │ cell_4a  │',
                                   '│ cell_1b  │          │          │          │',
                                   '│          │          │ cell_3b  │          │',
                                   '│          │ cell_2b  │          │          │',
                                   '└───────────────────────────────────────────┘']

        with self.print_table as _:
            _.reset()
            _.add_data([{'header_1': 'cell_1a'                      },
                        {'header_2': 'cell_2a'                      },
                        {'header_1': 'cell_1b','header_2': 'cell_2b'}])
            _.map_texts()
            assert _.text__all == ['┌─────────────────────┐',
                                   '│ header_1 │ header_2 │',
                                   '├─────────────────────┤',
                                   '│ cell_1a  │          │',
                                   '│          │ cell_2a  │',
                                   '│ cell_1b  │ cell_2b  │',
                                   '└─────────────────────┘']


    def test_add_headers(self):
        headers = ['header_1', 'header_2', 'header_3']
        with self.print_table as _:
            _.add_headers(*headers)
            _.map_texts()
            assert _.text__all == ['┌────────────────────────────────┐',
                                   '│ header_1 │ header_2 │ header_3 │',
                                   '├────────────────────────────────┤',
                                   '└────────────────────────────────┘']
    def test_add_row(self):
        headers = ['header_1', 'header_2', 'header_3']
        row   = ['cell_1', 'cell_2']
        with self.print_table as _:
            _.add_headers(*headers)
            _.add_row(row)
            _.map_texts()
            assert _.text__all == ['┌────────────────────────────────┐',
                                   '│ header_1 │ header_2 │ header_3 │',
                                   '├────────────────────────────────┤',
                                   '│ cell_1   │ cell_2   │          │',
                                   '└────────────────────────────────┘']

    def test_add_rows(self):
        row_1 = ['cell_1'                    ]
        row_2 = ['cell_2', 'cell_3'          ]
        row_3 = ['cell_4', 'cell_5', 'cell_6']
        row_4 = ['cell_7', 'cell_8'          ]
        rows  = [row_1, row_2, row_3, row_4]
        with self.print_table as _:
            _.add_rows(rows)
            _.map_texts()
            assert _.to_dict() == {'Header #1': ['cell_1', 'cell_2', 'cell_4', 'cell_7'],
                                   'Header #2': ['', 'cell_3', 'cell_5', 'cell_8'],
                                   'Header #3': ['', '', 'cell_6', '']}

            assert _.text__all == ['┌───────────────────────────────────┐',
                                   '│ Header #1 │ Header #2 │ Header #3 │',
                                   '├───────────────────────────────────┤',
                                   '│ cell_1    │           │           │',
                                   '│ cell_2    │ cell_3    │           │',
                                   '│ cell_4    │ cell_5    │ cell_6    │',
                                   '│ cell_7    │ cell_8    │           │',
                                   '└───────────────────────────────────┘']

    def test_fix_table(self):
        with self.print_table as _:
            _.add_row('cell_1')
            _.map_texts()
            assert _.to_dict() == {'Header #1': ['cell_1']}
            _.add_row(['cell_2', 'cell_3'])
            _.map_texts()
            assert _.to_dict() == {'Header #1': ['cell_1', 'cell_2'], 'Header #2': ['', 'cell_3']}
            assert _.text__all == ['┌───────────────────────┐',
                                   '│ Header #1 │ Header #2 │',
                                   '├───────────────────────┤',
                                   '│ cell_1    │           │',
                                   '│ cell_2    │ cell_3    │',
                                   '└───────────────────────┘']
            _.add_header('Header #3')
            assert _.to_dict() == {'Header #1': ['cell_1', 'cell_2'],
                                   'Header #2': ['', 'cell_3'],
                                   'Header #3': []}
            _.map_texts()
            assert _.text__all == ['┌───────────────────────────────────┐',
                                   '│ Header #1 │ Header #2 │ Header #3 │',
                                   '├───────────────────────────────────┤',
                                   '│ cell_1    │           │           │',
                                   '│ cell_2    │ cell_3    │           │',
                                   '└───────────────────────────────────┘']
            _.add_header('some name')
            _.add_row(['cell_4', 'cell_5', 'cell_6', 'cell_7', 'cell_8'])

            _.map_texts()
            assert _.to_dict() == {'Header #1': ['cell_1', 'cell_2', 'cell_4'],
                                   'Header #2': ['', 'cell_3', 'cell_5'],
                                   'Header #3': ['', '', 'cell_6'],
                                   'Header #5': ['', '', 'cell_8'],                     # note that this dict is not ordered
                                   'some name': ['', '', 'cell_7']}

            assert _.text__all == ['┌───────────────────────────────────────────────────────────┐',
                                   '│ Header #1 │ Header #2 │ Header #3 │ some name │ Header #5 │',
                                   '├───────────────────────────────────────────────────────────┤',
                                   '│ cell_1    │           │           │           │           │',
                                   '│ cell_2    │ cell_3    │           │           │           │',
                                   '│ cell_4    │ cell_5    │ cell_6    │ cell_7    │ cell_8    │',
                                   '└───────────────────────────────────────────────────────────┘']


    def test_map_texts(self):
        with  self.print_table as _:
            assert _.text__all == []
            _.map_texts()
            assert _.text__all == ['┌──┐', '└──┘']
            with patch("builtins.print") as _:
                self.print_table.print()
                assert _.call_args_list == [call(), call('┌──┐'), call('└──┘')]


    def test_map_text__footer(self):
        with  self.print_table as _:
            _.footer = 'an footer value'
            _.map_texts()
            assert _.text__all == ['┌─────────────────┐',
                                   '├─────────────────┤',
                                   '│ an footer value │',
                                   '└─────────────────┘']

            with patch("builtins.print") as _:
                self.print_table.print()
                assert _.call_args_list == [ call(),
                                             call('┌─────────────────┐'),
                                             call('├─────────────────┤'),
                                             call('│ an footer value │'),
                                             call('└─────────────────┘')]

    def test_map_text__title(self):
        with  self.print_table as _:
            _.title = 'an title value'
            _.map_texts()
            assert _.text__all == ['┌────────────────┐',
                                   '│ an title value │',
                                   '├────────────────┤',
                                   '└────────────────┘']
    def test_print(self):
        with self.print_table as _:
            _.title        =  "BOTO3 REST calls (via BaseClient._make_api_call)"
            _.footer       = "Total Duration:   0.73 secs | Total calls: 3"
            _.headers      = [ '#', 'Method', 'Duration', 'Params', 'Return Value']
            _.rows         = [ ["0", "GetCallerIdentity", "412 ms", " ('GetCallerIdentity', {}) ", " {'UserId': 'AIDAW3', 'Account': '47', 'Arn': 'arn:aws:iam:...'}"],
                               ["1", "GetCallerIdentity", " 97 ms", " ('GetCallerIdentity', {}) ", " {'UserId': 'AIDAW3', 'Account': '47', 'Arn': 'arn:aws:iam:...'}"],
                               ["2", "GetCallerIdentity", " 96 ms", " ('GetCallerIdentity', {}) ", " {'UserId': 'AIDAW3', 'Account': '47', 'Arn': 'arn:aws:iam:...'}"]]
            #_.print()


        with patch("builtins.print") as _:
            self.print_table.print()
            #assert len(_.call_args_list) == 12
            assert _.call_args_list == [ call(),
                                         call('┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐'),
                                         call('│ BOTO3 REST calls (via BaseClient._make_api_call)                                                                                  │'),
                                         call('├───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤'),
                                         call('│ # │ Method            │ Duration │ Params                      │ Return Value                                                     │'),
                                         call('├───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤'),
                                         call("│ 0 │ GetCallerIdentity │ 412 ms   │  ('GetCallerIdentity', {})  │  {'UserId': 'AIDAW3', 'Account': '47', 'Arn': 'arn:aws:iam:...'} │"),
                                         call("│ 1 │ GetCallerIdentity │  97 ms   │  ('GetCallerIdentity', {})  │  {'UserId': 'AIDAW3', 'Account': '47', 'Arn': 'arn:aws:iam:...'} │"),
                                         call("│ 2 │ GetCallerIdentity │  96 ms   │  ('GetCallerIdentity', {})  │  {'UserId': 'AIDAW3', 'Account': '47', 'Arn': 'arn:aws:iam:...'} │"),
                                         call('├───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤'),
                                         call('│ Total Duration:   0.73 secs | Total calls: 3                                                                                      │'),
                                         call('└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘')]

    def test_map_text__width(self):
        with self.print_table as _:
            assert _.text__width   == 0                 # check conner case of that used to happen when: self.table_width < 4
            assert _.table_width   == 0
            _.map_texts()
            assert _.table_width   == 4
            assert _.text__width   == 0
            assert _.text__headers == '│  │'

    def test_reorder_columns(self):
        with self.print_table as _:
            _.add_headers('header_1', 'header_2', 'header_3')
            with self.assertRaises(ValueError) as context:
                _.reorder_columns(['header_1'])
            self.assertTrue("New order must contain the same headers as the current table." in str(context.exception))

    def test__regression__headers_with_no_rows_and_title(self):
        with self.print_table as _:
            _.set_title('title longer than header')
            _.set_headers(['header_1','h2'])
            _.map_texts()
            assert _.text__all == ['┌─────────────────────────────┐',
                                   '│ title longer than header    │',
                                   '├─────────────────────────────┤',
                                   '│ header_1 │ h2               │',
                                   '├─────────────────────────────┤',
                                   '└─────────────────────────────┘']

        with self.print_table as _:
            _.reset()
            _.set_title('title longer than header and cell')
            _.add_row(['cell bigger than header'])
            _.map_texts()
            assert _.text__all == ['┌───────────────────────────────────┐',
                                   '│ title longer than header and cell │',
                                   '├───────────────────────────────────┤',
                                   '│ Header #1                         │',
                                   '├───────────────────────────────────┤',
                                   '│ cell bigger than header           │',
                                   '└───────────────────────────────────┘']

        with self.print_table as _:
            _.reset()
            _.set_footer('footer longer than header')
            _.headers = ['header_1']
            _.map_texts()
            assert _.text__all == ['┌───────────────────────────┐',
                                   '│ header_1                  │',
                                   '├───────────────────────────┤',
                                   '├───────────────────────────┤',
                                   '│ footer longer than header │',
                                   '└───────────────────────────┘']

        with self.print_table as _:
            _.reset()
            _.set_footer('footer longer than header and cell')
            _.add_row(['cell bigger than header'])
            _.map_texts()
            assert _.text__all == ['┌────────────────────────────────────┐',
                                   '│ Header #1                          │',
                                   '├────────────────────────────────────┤',
                                   '│ cell bigger than header            │',
                                   '├────────────────────────────────────┤',
                                   '│ footer longer than header and cell │',
                                   '└────────────────────────────────────┘']

    def test__regression__call_with_new_line(self):
        with self.print_table as _:
            _.add_row(['cell_1', ''                   ,'cell_3'])
            _.add_row(['cell\n_4', 'cell_5\n--\n--\n-','cell_6'])
            _.add_row(['cell_7', 'cell_8'             ,'cell_9'])
            _.map_texts()
            #_.print()
            assert _.text__all == ['┌───────────────────────────────────┐',
                                   '│ Header #1 │ Header #2 │ Header #3 │',
                                   '├───────────────────────────────────┤',
                                   '│ cell_1    │           │ cell_3    │',
                                   '│ cell      │ cell_5    │ cell_6    │',
                                   '│ _4        │ --        │           │',
                                   '│           │ --        │           │',
                                   '│           │ -         │           │',
                                   '│ cell_7    │ cell_8    │ cell_9    │',
                                   '└───────────────────────────────────┘']

    def test__regression__print_empty_table(self):
        with self.print_table as _:
            _.map_texts()
            assert _.text__all == ['┌──┐',
                                   '└──┘']
