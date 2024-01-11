from unittest import TestCase
from unittest.mock import patch, call

from osbot_utils.helpers.Print_Table import Print_Table


class test_Print_Table(TestCase):

    def setUp(self):
        self.print_table = Print_Table()

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
            assert _.call_args_list == [ call('┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐'),
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


