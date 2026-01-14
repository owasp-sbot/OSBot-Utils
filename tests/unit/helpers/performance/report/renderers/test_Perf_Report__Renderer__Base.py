# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Report__Renderer__Base - Tests for abstract renderer base class
# ═══════════════════════════════════════════════════════════════════════════════

import pytest
from unittest                                                                                                    import TestCase
from osbot_utils.helpers.performance.report.renderers.Perf_Report__Renderer__Base                                import Perf_Report__Renderer__Base
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report                                          import Schema__Perf_Report
from osbot_utils.type_safe.Type_Safe                                                                             import Type_Safe


class test_Perf_Report__Renderer__Base(TestCase):

    def test__init__(self):                                         # Test initialization
        with Perf_Report__Renderer__Base() as _:
            assert type(_)            is Perf_Report__Renderer__Base
            assert isinstance(_, Type_Safe)

    # ═══════════════════════════════════════════════════════════════════════════
    # NotImplementedError Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__render__raises_not_implemented(self):                 # Test render raises NotImplementedError
        with pytest.raises(NotImplementedError):
            Perf_Report__Renderer__Base().render(Schema__Perf_Report())

    # ═══════════════════════════════════════════════════════════════════════════
    # Helper Method Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__format_ns(self):                                      # Test nanosecond formatting
        with Perf_Report__Renderer__Base() as _:
            assert _.format_ns(500)           == '500ns'
            assert _.format_ns(1_500)         == '1.50µs'
            assert _.format_ns(1_500_000)     == '1.50ms'
            assert _.format_ns(1_500_000_000) == '1.50s'

    def test__format_ns__boundaries(self):                          # Test boundary values
        with Perf_Report__Renderer__Base() as _:
            assert _.format_ns(999)           == '999ns'
            assert _.format_ns(1_000)         == '1.00µs'
            assert _.format_ns(999_999)       == '1000.00µs'
            assert _.format_ns(1_000_000)     == '1.00ms'
            assert _.format_ns(999_999_999)   == '1000.00ms'
            assert _.format_ns(1_000_000_000) == '1.00s'

    def test__format_pct(self):                                     # Test percentage formatting
        with Perf_Report__Renderer__Base() as _:
            assert _.format_pct(50.0)   == ' 50.0%'
            assert _.format_pct(5.5)    == '  5.5%'
            assert _.format_pct(100.0)  == '100.0%'
            assert _.format_pct(0.1)    == '  0.1%'

    def test__format_pct__custom_width(self):                       # Test custom width
        with Perf_Report__Renderer__Base() as _:
            assert _.format_pct(50.0, width=3) == '50.0%'
            assert _.format_pct(5.5, width=7)  == '    5.5%'

    def test__format_timestamp(self):                               # Test timestamp formatting
        with Perf_Report__Renderer__Base() as _:
            result = _.format_timestamp(1704067200000)              # 2024-01-01 00:00:00 UTC
            assert '2024' in result
            assert '01' in result
            assert ':' in result

    def test__escape_markdown(self):                                # Test markdown escaping
        with Perf_Report__Renderer__Base() as _:
            assert _.escape_markdown('test|pipe')   == 'test\\|pipe'
            assert _.escape_markdown('test`code`')  == 'test\\`code\\`'
            assert _.escape_markdown('*bold*')      == '\\*bold\\*'
            assert _.escape_markdown('_italic_')    == '\\_italic\\_'
            assert _.escape_markdown('[link]')      == '\\[link\\]'
            assert _.escape_markdown('<tag>')       == '\\<tag\\>'

    def test__escape_markdown__no_special_chars(self):              # Test no escaping needed
        with Perf_Report__Renderer__Base() as _:
            assert _.escape_markdown('plain text')  == 'plain text'
            assert _.escape_markdown('123')         == '123'