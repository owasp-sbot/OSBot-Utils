# ═══════════════════════════════════════════════════════════════════════════════
# test_Perf_Report__Storage__Base - Tests for abstract storage base class
# ═══════════════════════════════════════════════════════════════════════════════

import pytest
from unittest                                                                                                    import TestCase
from osbot_utils.helpers.performance.report.schemas.Schema__Perf_Report                                          import Schema__Perf_Report
from osbot_utils.helpers.performance.report.storage.Perf_Report__Storage__Base                                   import Perf_Report__Storage__Base
from osbot_utils.type_safe.Type_Safe                                                                             import Type_Safe


class test_Perf_Report__Storage__Base(TestCase):

    def test__init__(self):                                         # Test initialization
        with Perf_Report__Storage__Base() as _:
            assert type(_)            is Perf_Report__Storage__Base
            assert isinstance(_, Type_Safe)

    # ═══════════════════════════════════════════════════════════════════════════
    # NotImplementedError Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__save__raises_not_implemented(self):                   # Test save raises NotImplementedError
        with pytest.raises(NotImplementedError):
            Perf_Report__Storage__Base().save(Schema__Perf_Report(), 'test_key')

    def test__save_content__raises_not_implemented(self):           # Test save_content raises NotImplementedError
        with pytest.raises(NotImplementedError):
            Perf_Report__Storage__Base().save_content('test_key', 'content', 'txt')

    def test__load__raises_not_implemented(self):                   # Test load raises NotImplementedError
        with pytest.raises(NotImplementedError):
            Perf_Report__Storage__Base().load('test_key')

    def test__list_reports__raises_not_implemented(self):           # Test list_reports raises NotImplementedError
        with pytest.raises(NotImplementedError):
            Perf_Report__Storage__Base().list_reports()

    def test__exists__raises_not_implemented(self):                 # Test exists raises NotImplementedError
        with pytest.raises(NotImplementedError):
            Perf_Report__Storage__Base().exists('test_key')

    def test__delete__raises_not_implemented(self):                 # Test delete raises NotImplementedError
        with pytest.raises(NotImplementedError):
            Perf_Report__Storage__Base().delete('test_key')