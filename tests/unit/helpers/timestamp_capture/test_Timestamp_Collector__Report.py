import time
from unittest                                                                      import TestCase

from osbot_fast_api_serverless.utils.testing.skip_tests import skip__if_not__in_github_actions

from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                     import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector__Report             import Timestamp_Collector__Report
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.utils.Objects                                                     import base_classes


class test_Timestamp_Collector__Report(TestCase):

    def test__init__(self):                                                        # Test auto-initialization
        collector = Timestamp_Collector()
        with Timestamp_Collector__Report(collector=collector) as _:
            assert type(_)          is Timestamp_Collector__Report
            assert base_classes(_)  == [Type_Safe, object]
            assert _.collector      is collector

    def test_format_report__empty(self):                                           # Test report with no entries
        with Timestamp_Collector(name='empty_test') as collector:
            pass

        report = Timestamp_Collector__Report(collector=collector)
        output = report.format_report()

        assert 'Timestamp Report: empty_test' in output
        assert 'Total Duration'               in output
        assert 'Entry Count'                  in output
        assert 'Methods Traced'               in output

    def test_format_report__with_data(self):                                       # Test report with timing data
        skip__if_not__in_github_actions()
        with Timestamp_Collector(name='data_test') as collector:
            collector.enter('method_a')
            time.sleep(0.01)
            collector.exit('method_a')

            collector.enter('method_b')
            time.sleep(0.005)
            collector.exit('method_b')

        report = Timestamp_Collector__Report(collector=collector)
        output = report.format_report()

        assert 'Timestamp Report: data_test'  in output
        assert 'method_a'                     in output
        assert 'method_b'                     in output
        assert 'Calls'                        in output
        assert 'Total'                        in output
        assert 'Self'                         in output

    def test_format_report__without_self_time(self):                               # Test report without self-time column
        with Timestamp_Collector() as collector:
            collector.enter('test')
            collector.exit('test')

        report = Timestamp_Collector__Report(collector=collector)
        output = report.format_report(show_self_time=False)

        assert 'Self'         not in output
        assert 'Total(ms)'        in output
        assert 'Avg(ms)'          in output

    def test_format_timeline__empty(self):                                         # Test timeline with no entries
        with Timestamp_Collector() as collector:
            pass

        report = Timestamp_Collector__Report(collector=collector)
        output = report.format_timeline()

        assert 'Execution Timeline' in output

    def test_format_timeline__with_data(self):                                     # Test timeline with entries
        with Timestamp_Collector() as collector:
            collector.enter('outer')
            collector.enter('inner')
            collector.exit('inner')
            collector.exit('outer')

        report = Timestamp_Collector__Report(collector=collector)
        output = report.format_timeline()

        assert 'Execution Timeline' in output
        assert '▶ outer'            in output                                      # Enter marker
        assert '▶ inner'            in output
        assert '◀ inner'            in output                                      # Exit marker
        assert '◀ outer'            in output

    def test_format_timeline__max_entries(self):                                   # Test timeline truncation
        with Timestamp_Collector() as collector:
            for i in range(20):
                collector.enter(f'method_{i}')
                collector.exit(f'method_{i}')

        report = Timestamp_Collector__Report(collector=collector)
        output = report.format_timeline(max_entries=10)

        assert 'showing first 10 of 40 entries' in output

    def test_format_hotspots__empty(self):                                         # Test hotspots with no data
        with Timestamp_Collector() as collector:
            pass

        report = Timestamp_Collector__Report(collector=collector)
        output = report.format_hotspots()

        assert 'Hotspots' in output

    def test_format_hotspots__with_data(self):                                     # Test hotspots with timing data
        skip__if_not__in_github_actions()
        with Timestamp_Collector() as collector:
            collector.enter('slow')
            time.sleep(0.015)
            collector.exit('slow')

            collector.enter('fast')
            time.sleep(0.005)
            collector.exit('fast')

        report   = Timestamp_Collector__Report(collector=collector)
        output   = report.format_hotspots(top_n=5)

        assert 'Top 5 Hotspots' in output
        assert 'slow'           in output
        assert 'fast'           in output
        assert 'calls'          in output

    def test_print_report(self):                                      # Test print_report outputs to stdout
        with Timestamp_Collector(name='print_test') as collector:
            collector.enter('test')
            collector.exit('test')

        report = Timestamp_Collector__Report(collector=collector)

        import io
        import sys
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured

        try:
            report.print_report()
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        assert 'Timestamp Report: print_test' in output

    def test_print_timeline(self):                                                 # Test print_timeline outputs to stdout
        with Timestamp_Collector() as collector:
            collector.enter('test')
            collector.exit('test')

        report = Timestamp_Collector__Report(collector=collector)

        import io
        import sys
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured

        try:
            report.print_timeline()
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        assert 'Execution Timeline' in output

    def test_print_hotspots(self):                                                 # Test print_hotspots outputs to stdout
        with Timestamp_Collector() as collector:
            collector.enter('test')
            time.sleep(0.001)
            collector.exit('test')

        report = Timestamp_Collector__Report(collector=collector)

        import io
        import sys
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured

        try:
            report.print_hotspots()
        finally:
            sys.stdout = old_stdout

        output = captured.getvalue()
        assert 'Hotspots' in output