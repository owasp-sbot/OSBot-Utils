# ═══════════════════════════════════════════════════════════════════════════════
# test_Call_Flow__Exporter__Mermaid - Tests for Mermaid diagram export
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.helpers.python_call_flow.export.Call_Flow__Exporter__Mermaid        import Call_Flow__Exporter__Mermaid
from osbot_utils.utils.Objects                                                       import base_classes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.helpers.python_call_flow.testing.QA__Call_Flow__Test_Data           import QA__Call_Flow__Test_Data


class test_Call_Flow__Exporter__Mermaid(TestCase):                                   # Test Mermaid exporter

    @classmethod
    def setUpClass(cls):                                                             # Shared setup
        cls.qa     = QA__Call_Flow__Test_Data()
        cls.result = cls.qa.create_result__self_calls()                              # Cached result

    def test__init__(self):                                                          # Test initialization
        with Call_Flow__Exporter__Mermaid() as _:
            assert type(_)          is Call_Flow__Exporter__Mermaid
            assert base_classes(_)  == [Type_Safe, object]
            assert _.direction      == 'TD'
            assert _.show_contains  == True
            assert _.show_calls     == True

    def test__init__with_result(self):                                               # Test init with result
        with Call_Flow__Exporter__Mermaid(result=self.result) as _:
            assert _.result is self.result
            assert _.graph  is self.result.graph

    def test__init__with_direction(self):                                            # Test init with direction
        with Call_Flow__Exporter__Mermaid(direction='LR') as _:
            assert _.direction == 'LR'

    def test__export__basic(self):                                                   # Test basic export
        with self.qa as _:
            exporter = _.create_exporter__default(self.result)
            mermaid  = exporter.export()

            assert type(mermaid)     is str
            assert 'flowchart TD'    in mermaid

    def test__export__contains_node_names(self):                                     # Test nodes in output
        with self.qa as _:
            exporter = _.create_exporter__default(self.result)
            mermaid  = exporter.export()

            assert _.assert_mermaid_has_node(mermaid, 'Sample__Self_Calls')

    def test__export__self_call_styling(self):                                       # Test self-call arrows
        with self.qa as _:
            exporter = _.create_exporter__default(self.result)
            mermaid  = exporter.export()

            assert _.assert_mermaid_has_self_call(mermaid)                           # Has -.-> and |self|

    def test__export__direction_td(self):                                            # Test TD direction
        with self.qa as _:
            exporter = _.create_exporter__default(self.result)
            mermaid  = exporter.export()

            assert _.assert_mermaid_has_header(mermaid, 'TD')

    def test__export__direction_lr(self):                                            # Test LR direction
        with self.qa as _:
            exporter = _.create_exporter__left_right(self.result)
            mermaid  = exporter.export()

            assert _.assert_mermaid_has_header(mermaid, 'LR')

    def test__export__no_contains_edges(self):                                       # Test hiding contains
        with self.qa as _:
            exporter = _.create_exporter__no_contains(self.result)
            mermaid  = exporter.export()

            assert 'flowchart' in mermaid                                            # Still valid

    def test__export__empty_graph(self):                                             # Test empty graph handling
        with Call_Flow__Exporter__Mermaid() as exporter:
            mermaid = exporter.export()

            assert 'No graph data' in mermaid

    def test__to_html(self):                                                         # Test HTML generation
        with self.qa as _:
            exporter = _.create_exporter__default(self.result)
            html     = exporter.to_html()

            assert '<!DOCTYPE html>' in html
            assert 'mermaid'         in html

    def test__to_html__with_title(self):                                             # Test HTML with title
        with self.qa as _:
            exporter = _.create_exporter__default(self.result)
            html     = exporter.to_html(title='Test Diagram')

            assert 'Test Diagram' in html

    def test__expected_mermaid__arrow_styles(self):                                  # Test arrow style constants
        with self.qa as _:
            assert _.get_expected_mermaid__self_call_arrow()  == '-.->'
            assert _.get_expected_mermaid__chain_call_arrow() == '==>'
            assert _.get_expected_mermaid__contains_arrow()   == '-->'

    def test__expected_mermaid__labels(self):                                        # Test label constants
        with self.qa as _:
            assert _.get_expected_mermaid__self_call_label() == '|self|'


# class test_Call_Flow__Exporter__Mermaid__fixtures(TestCase):                         # Test with different fixtures
#
#     @classmethod
#     def setUpClass(cls):
#         cls.qa = QA__Call_Flow__Test_Data()

    def test__export__simple_class(self):                                            # Test simple class export
        with self.qa as _:
            fixture = _.create_complete_fixture__simple()
            mermaid = fixture['mermaid']

            assert 'flowchart TD' in mermaid
            assert 'Simple_Class' in mermaid

    def test__export__multiple_self_calls(self):                                     # Test multiple self calls
        with self.qa as _:
            fixture = _.create_complete_fixture__multiple_self_calls()
            mermaid = fixture['mermaid']

            assert 'flowchart TD' in mermaid

    def test__export__deep_calls(self):                                              # Test deep call chain
        with self.qa as _:
            fixture = _.create_complete_fixture__deep_calls()
            mermaid = fixture['mermaid']

            assert 'flowchart TD' in mermaid
            assert 'Deep_Calls'   in mermaid

    def test__all_fixtures__export(self):                                            # Test all fixtures export
        with self.qa as _:
            all_fixtures = _.create_all_fixtures()

            for name, fixture in all_fixtures.items():
                mermaid = fixture['mermaid']
                assert 'flowchart' in mermaid                                        # All produce valid output