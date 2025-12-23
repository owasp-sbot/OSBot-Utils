import time as time_module
from unittest                                                                         import TestCase
from osbot_aws.testing.skip_tests                                                     import skip__if_not__in_github_actions
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector                        import Timestamp_Collector
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector__Analysis              import Timestamp_Collector__Analysis
from osbot_utils.helpers.timestamp_capture.Timestamp_Collector__Report                import Timestamp_Collector__Report
from osbot_utils.helpers.timestamp_capture.context_managers.timestamp_block           import timestamp_block
from osbot_utils.helpers.timestamp_capture.decorators.timestamp                       import timestamp
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe


class test_Timestamp_Collector__integration(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        skip__if_not__in_github_actions()

    def test_full_workflow__decorator_and_block(self):                                # Test decorators and blocks together
        _timestamp_collector_ = Timestamp_Collector(name='integration_test')

        with _timestamp_collector_:
            converter = Demo_Converter()

            with timestamp_block('iteration_0'):
                result = converter.convert('data_0')

        assert result                                == "{'transformed': {'raw': 'data_0'}}"
        assert _timestamp_collector_.entry_count()   > 0
        assert _timestamp_collector_.method_count()  > 1

        analysis = Timestamp_Collector__Analysis(collector=_timestamp_collector_)
        timings  = analysis.get_method_timings()

        assert 'iteration_0'                         in timings
        assert 'Demo_Converter.convert'              in timings
        assert 'Demo_Converter._parse'               in timings
        assert 'Demo_Converter._transform'           in timings
        assert 'Demo_Converter._transform_step'      in timings
        assert 'Demo_Converter._serialize'           in timings

    def test_full_workflow__multiple_iterations(self):                                # Test multiple iterations with aggregation
        _timestamp_collector_ = Timestamp_Collector(name='multi_iteration')

        with _timestamp_collector_:
            converter = Demo_Converter()
            for i in range(3):
                with timestamp_block(f'iteration_{i}'):
                    converter.convert(f'data_{i}')

        analysis = Timestamp_Collector__Analysis(collector=_timestamp_collector_)
        timings  = analysis.get_method_timings()

        assert timings['Demo_Converter.convert'].call_count      == 3
        assert timings['Demo_Converter._parse'].call_count       == 3
        assert timings['Demo_Converter._transform'].call_count   == 3
        assert timings['Demo_Converter._transform_step'].call_count == 9             # 3 calls per convert * 3 iterations
        assert timings['Demo_Converter._serialize'].call_count   == 3

    def test_full_workflow__report_generation(self):                                  # Test report generation
        _timestamp_collector_ = Timestamp_Collector(name='report_test')

        with _timestamp_collector_:
            converter = Demo_Converter()
            converter.convert('test_data')

        report = Timestamp_Collector__Report(collector=_timestamp_collector_)

        report_text = report.format_report()
        assert 'Timestamp Report: report_test' in report_text
        assert 'Demo_Converter.convert'        in report_text

        timeline_text = report.format_timeline()
        assert 'Execution Timeline'            in timeline_text
        assert '▶'                             in timeline_text                       # Enter markers

        hotspot_text = report.format_hotspots()
        assert 'Hotspots'                      in hotspot_text

        report.print_all()


    def test_full_workflow__hotspot_analysis(self):                                   # Test hotspot correctly identifies slow methods
        _timestamp_collector_ = Timestamp_Collector(name='hotspot_test')

        with _timestamp_collector_:
            converter = Demo_Converter()
            converter.convert('data')

        analysis = Timestamp_Collector__Analysis(collector=_timestamp_collector_)
        hotspots = analysis.get_hotspots(top_n=3)

        hotspot_names = [h.name for h in hotspots]

        assert 'Demo_Converter._transform_step' in hotspot_names                      # 3 calls * 5ms = 15ms
        assert 'Demo_Converter._parse'          in hotspot_names                      # 1 call * 15ms

    def test_full_workflow__no_collector_overhead(self):                              # Test decorated code runs without collector
        converter = Demo_Converter()

        start = time_module.perf_counter_ns()
        result = converter.convert('no_collector_data')
        end = time_module.perf_counter_ns()

        assert result == "{'transformed': {'raw': 'no_collector_data'}}"
        duration_ms = (end - start) / 1_000_000
        assert duration_ms < 100                                                      # Should complete in reasonable time

    def test_full_workflow__self_time_calculation(self):                              # Test self-time is correctly calculated
        _timestamp_collector_ = Timestamp_Collector(name='self_time_test')

        with _timestamp_collector_:
            converter = Demo_Converter()
            converter.convert('data')

        analysis = Timestamp_Collector__Analysis(collector=_timestamp_collector_)
        timings  = analysis.get_method_timings()

        convert_timing   = timings['Demo_Converter.convert']
        transform_timing = timings['Demo_Converter._transform']
        step_timing      = timings['Demo_Converter._transform_step']

        assert convert_timing.total_ns   > convert_timing.self_ns                     # Total > Self (has children)
        assert transform_timing.total_ns > transform_timing.self_ns                   # Total > Self (calls _transform_step)
        assert step_timing.total_ns      == step_timing.self_ns                       # Total == Self (leaf method)


class Demo_Converter(Type_Safe):                                                      # Demo class for testing

    @timestamp
    def convert(self, data: str) -> str:
        parsed      = self._parse(data)
        transformed = self._transform(parsed)
        return self._serialize(transformed)

    @timestamp
    def _parse(self, data: str) -> dict:
        time_module.sleep(0.015)                                                      # 15ms
        return {"raw": data}

    @timestamp
    def _transform(self, data: dict) -> dict:
        for i in range(3):
            self._transform_step(i)
        return {"transformed": data}

    @timestamp
    def _transform_step(self, step: int):
        time_module.sleep(0.005)                                                      # 5ms

    @timestamp
    def _serialize(self, data: dict) -> str:
        time_module.sleep(0.008)                                                      # 8ms
        return str(data)