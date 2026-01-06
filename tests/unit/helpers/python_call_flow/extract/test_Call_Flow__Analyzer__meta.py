from unittest                                                               import TestCase
from osbot_utils.helpers.python_call_flow.extract.Call_Flow__Analyzer       import Call_Flow__Analyzer
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Config import Schema__Call_Flow__Config
from osbot_utils.helpers.python_call_flow.testing.QA__Call_Flow__Test_Data  import QA__Call_Flow__Test_Data


class test_Call_Flow__Analyzer__meta(TestCase):                                      # Meta tests - analyzer analyzing itself

    @classmethod
    def setUpClass(cls):                                                             # Analyze analyzer once
        config = Schema__Call_Flow__Config(max_depth=3)

        with Call_Flow__Analyzer(config=config) as analyzer:
            cls.result = analyzer.analyze(Call_Flow__Analyzer)

    def test__meta__finds_class(self):                                               # Verify class is found
        assert 'Call_Flow__Analyzer' in self.result.entry_point

    def test__meta__discovers_methods(self):                                         # Verify methods discovered
        node_names = [str(n.name) for n in self.result.graph.nodes.values()]

        assert 'Call_Flow__Analyzer' in node_names or any('Analyzer' in n for n in node_names)
        assert self.result.total_nodes >= 5                                          # Class + several methods

    def test__meta__has_contains_edges(self):                                        # Verify contains edges exist
        qa          = QA__Call_Flow__Test_Data()
        contains_id = qa.get_predicate_id__contains()
        count       = qa.count_edges_by_predicate(self.result, contains_id)

        assert count >= 3                                                            # At least several methods