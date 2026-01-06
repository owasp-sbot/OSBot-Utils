# ═══════════════════════════════════════════════════════════════════════════════
# QA__Call_Flow__Test_Data - Comprehensive test data for python_call_flow
#
# Provides factory methods for creating test fixtures:
#   - Sample Python classes and functions for analysis
#   - Pre-built analyzer results with known structure
#   - Configured analyzers with various settings
#   - Expected Mermaid outputs for comparison
#   - Serialized/deserialized results for storage tests
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                           import Dict, Any, List, Type

from osbot_utils.helpers.python_call_flow.core.Call_Flow__Builder import Call_Flow__Builder
from osbot_utils.helpers.python_call_flow.core.Call_Flow__Ontology import Call_Flow__Ontology
from osbot_utils.helpers.python_call_flow.core.Call_Flow__Storage import Call_Flow__Storage
from osbot_utils.helpers.python_call_flow.export.Call_Flow__Exporter__Mermaid import Call_Flow__Exporter__Mermaid
from osbot_utils.helpers.python_call_flow.extract.Call_Flow__Analyzer import Call_Flow__Analyzer
from osbot_utils.type_safe.Type_Safe                                                  import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                        import type_safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                      import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id              import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id              import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph         import Schema__Semantic_Graph
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Config           import Schema__Call_Flow__Config
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Result           import Schema__Call_Flow__Result


# ═══════════════════════════════════════════════════════════════════════════════
# QA Test Data Factory
# ═══════════════════════════════════════════════════════════════════════════════

class QA__Call_Flow__Test_Data(Type_Safe):                                           # Test data factory for python_call_flow

    # ═══════════════════════════════════════════════════════════════════════════
    # Deterministic Seeds for Reproducible Tests
    # ═══════════════════════════════════════════════════════════════════════════

    SEED__GRAPH_SIMPLE       = Safe_Str__Id__Seed('test-graph-simple')
    SEED__GRAPH_SELF_CALLS   = Safe_Str__Id__Seed('test-graph-self-calls')
    SEED__GRAPH_CHAIN_CALLS  = Safe_Str__Id__Seed('test-graph-chain-calls')
    SEED__GRAPH_DEEP         = Safe_Str__Id__Seed('test-graph-deep')
    SEED__GRAPH_FUNCTION     = Safe_Str__Id__Seed('test-graph-function')

    # Node seeds for manual graph building
    SEED__NODE_CLASS_A       = Safe_Str__Id__Seed('test-node-class-a')
    SEED__NODE_METHOD_FOO    = Safe_Str__Id__Seed('test-node-method-foo')
    SEED__NODE_METHOD_BAR    = Safe_Str__Id__Seed('test-node-method-bar')
    SEED__NODE_FUNC_HELPER   = Safe_Str__Id__Seed('test-node-func-helper')
    SEED__NODE_EXTERNAL      = Safe_Str__Id__Seed('test-node-external')

    # ═══════════════════════════════════════════════════════════════════════════
    # ID Generation Helpers
    # ═══════════════════════════════════════════════════════════════════════════

    def _id_from_seed(self, seed: Safe_Str__Id__Seed) -> Obj_Id:
        return Obj_Id.from_seed(seed)

    # ═══════════════════════════════════════════════════════════════════════════
    # Sample Class Accessors
    # ═══════════════════════════════════════════════════════════════════════════

    def get_sample_class__simple(self) -> Type:
        """Class with no internal calls"""
        return Sample__Simple_Class

    def get_sample_class__self_calls(self) -> Type:
        """Class with self.method() calls"""
        return Sample__Self_Calls

    def get_sample_class__multiple_self_calls(self) -> Type:
        """Class with multiple self.method() calls"""
        return Sample__Multiple_Self_Calls

    def get_sample_class__chain_calls(self) -> Type:
        """Class with chain calls"""
        return Sample__Chain_Calls

    def get_sample_class__conditional_calls(self) -> Type:
        """Class with conditional calls"""
        return Sample__Conditional_Calls

    def get_sample_class__deep_calls(self) -> Type:
        """Class with deep call chains"""
        return Sample__Deep_Calls

    def get_sample_class__recursive(self) -> Type:
        """Class with recursive calls"""
        return Sample__Recursive

    def get_sample_class__with_builtins(self) -> Type:
        """Class that uses builtin functions"""
        return Sample__With_Builtins

    def get_sample_class__external_calls(self) -> Type:
        """Class that calls external functions"""
        return Sample__External_Calls

    def get_sample_function__standalone(self):
        """Standalone function"""
        return sample_standalone_function

    def get_sample_function__helper(self):
        """Helper function"""
        return sample_helper_function

    def get_all_sample_classes(self) -> List[Type]:
        """All sample classes for iteration"""
        return [Sample__Simple_Class         ,
                Sample__Self_Calls           ,
                Sample__Multiple_Self_Calls  ,
                Sample__Chain_Calls          ,
                Sample__Conditional_Calls    ,
                Sample__Deep_Calls           ,
                Sample__Recursive            ,
                Sample__With_Builtins        ,
                Sample__External_Calls       ]

    # ═══════════════════════════════════════════════════════════════════════════
    # Ontology Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_ontology(self) -> Call_Flow__Ontology:
        """Create and setup call flow ontology"""
        return Call_Flow__Ontology().setup()

    def get_node_type_id__class(self) -> Node_Type_Id:
        """Get class node type ID"""
        return self.create_ontology().node_type_id__class()

    def get_node_type_id__method(self) -> Node_Type_Id:
        """Get method node type ID"""
        return self.create_ontology().node_type_id__method()

    def get_node_type_id__function(self) -> Node_Type_Id:
        """Get function node type ID"""
        return self.create_ontology().node_type_id__function()

    def get_node_type_id__module(self) -> Node_Type_Id:
        """Get module node type ID"""
        return self.create_ontology().node_type_id__module()

    def get_node_type_id__external(self) -> Node_Type_Id:
        """Get external node type ID"""
        return self.create_ontology().node_type_id__external()

    def get_predicate_id__contains(self) -> Predicate_Id:
        """Get contains predicate ID"""
        return self.create_ontology().predicate_id__contains()

    def get_predicate_id__calls(self) -> Predicate_Id:
        """Get calls predicate ID"""
        return self.create_ontology().predicate_id__calls()

    def get_predicate_id__calls_self(self) -> Predicate_Id:
        """Get calls_self predicate ID"""
        return self.create_ontology().predicate_id__calls_self()

    def get_predicate_id__calls_chain(self) -> Predicate_Id:
        """Get calls_chain predicate ID"""
        return self.create_ontology().predicate_id__calls_chain()

    # ═══════════════════════════════════════════════════════════════════════════
    # Config Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_config__default(self) -> Schema__Call_Flow__Config:
        """Default configuration"""
        return Schema__Call_Flow__Config()

    @type_safe
    def create_config__include_builtins(self) -> Schema__Call_Flow__Config:
        """Config that includes builtin calls"""
        return Schema__Call_Flow__Config(include_builtins=True)

    @type_safe
    def create_config__exclude_external(self) -> Schema__Call_Flow__Config:
        """Config that excludes external calls"""
        return Schema__Call_Flow__Config(include_external=False)

    @type_safe
    def create_config__shallow(self) -> Schema__Call_Flow__Config:      # Config with shallow depth (max_depth=1)
        return Schema__Call_Flow__Config(max_depth=1)

    @type_safe
    def create_config__deep(self) -> Schema__Call_Flow__Config:
        """Config with deep depth (max_depth=20)"""
        return Schema__Call_Flow__Config(max_depth=20)

    @type_safe
    def create_config__full(self) -> Schema__Call_Flow__Config:
        """Config with all options enabled"""
        return Schema__Call_Flow__Config(max_depth         = 20  ,
                                         include_builtins  = True,
                                         include_external  = True)

    # ═══════════════════════════════════════════════════════════════════════════
    # Builder Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_builder(self) -> Call_Flow__Builder:
        """Create and setup a builder"""
        return Call_Flow__Builder().setup()

    @type_safe
    def create_builder_with_class(self                                              ,
                                  class_name  : str = 'test.TestClass'              ,
                                  method_names: List[str] = None                    ) -> Call_Flow__Builder:
        """Create builder with a class and methods"""
        builder = self.create_builder()
        builder.add_class(qualified_name=class_name)

        method_names = method_names or ['method_a', 'method_b']
        for method_name in method_names:
            qualified_method = f"{class_name}.{method_name}"
            builder.add_method(qualified_name=qualified_method)
            builder.add_contains(class_name, qualified_method)

        return builder

    @type_safe
    def create_builder_with_self_calls(self) -> Call_Flow__Builder:
        """Create builder with a class that has self.method() calls"""
        builder = self.create_builder()

        class_name = 'test.MyClass'
        builder.add_class(qualified_name=class_name)

        builder.add_method(qualified_name=f'{class_name}.caller')
        builder.add_method(qualified_name=f'{class_name}.callee')

        builder.add_contains(class_name, f'{class_name}.caller')
        builder.add_contains(class_name, f'{class_name}.callee')

        builder.add_calls_self(f'{class_name}.caller', f'{class_name}.callee')

        return builder

    @type_safe
    def create_graph__empty(self) -> Schema__Semantic_Graph:
        """Create empty semantic graph"""
        return self.create_builder().build()

    @type_safe
    def create_graph__simple_class(self) -> Schema__Semantic_Graph:
        """Create graph with simple class structure"""
        return self.create_builder_with_class().build()

    @type_safe
    def create_graph__with_self_calls(self) -> Schema__Semantic_Graph:
        """Create graph with self.method() calls"""
        return self.create_builder_with_self_calls().build()

    # ═══════════════════════════════════════════════════════════════════════════
    # Analyzer Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_analyzer__default(self) -> Call_Flow__Analyzer:
        """Create analyzer with default config"""
        analyzer = Call_Flow__Analyzer()
        analyzer.setup()
        return analyzer

    @type_safe
    def create_analyzer__with_config(self                                           ,
                                     config: Schema__Call_Flow__Config              ) -> Call_Flow__Analyzer:
        """Create analyzer with specified config"""
        analyzer = Call_Flow__Analyzer(config=config)
        analyzer.setup()
        return analyzer

    # ═══════════════════════════════════════════════════════════════════════════
    # Analysis Result Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_result__simple_class(self) -> Schema__Call_Flow__Result:
        """Analyze Sample__Simple_Class and return result"""
        with Call_Flow__Analyzer() as analyzer:
            return analyzer.analyze(Sample__Simple_Class)

    @type_safe
    def create_result__self_calls(self) -> Schema__Call_Flow__Result:
        """Analyze Sample__Self_Calls and return result"""
        with Call_Flow__Analyzer() as analyzer:
            return analyzer.analyze(Sample__Self_Calls)

    @type_safe
    def create_result__multiple_self_calls(self) -> Schema__Call_Flow__Result:
        """Analyze Sample__Multiple_Self_Calls and return result"""
        with Call_Flow__Analyzer() as analyzer:
            return analyzer.analyze(Sample__Multiple_Self_Calls)

    @type_safe
    def create_result__chain_calls(self) -> Schema__Call_Flow__Result:
        """Analyze Sample__Chain_Calls and return result"""
        config = Schema__Call_Flow__Config(include_external=True)
        with Call_Flow__Analyzer(config=config) as analyzer:
            return analyzer.analyze(Sample__Chain_Calls)

    @type_safe
    def create_result__deep_calls(self) -> Schema__Call_Flow__Result:
        """Analyze Sample__Deep_Calls and return result"""
        with Call_Flow__Analyzer() as analyzer:
            return analyzer.analyze(Sample__Deep_Calls)

    @type_safe
    def create_result__function(self) -> Schema__Call_Flow__Result:
        """Analyze sample_standalone_function and return result"""
        config = Schema__Call_Flow__Config(include_external=True)
        with Call_Flow__Analyzer(config=config) as analyzer:
            return analyzer.analyze(sample_standalone_function)

    @type_safe
    def create_result__with_config(self                                              ,
                                   target                                            ,
                                   config: Schema__Call_Flow__Config = None          ) -> Schema__Call_Flow__Result:
        """Analyze any target with optional config"""
        config = config or Schema__Call_Flow__Config()
        with Call_Flow__Analyzer(config=config) as analyzer:
            return analyzer.analyze(target)

    # ═══════════════════════════════════════════════════════════════════════════
    # Exporter Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_exporter__default(self                                                ,
                                 result: Schema__Call_Flow__Result                   ) -> Call_Flow__Exporter__Mermaid:
        """Create Mermaid exporter with result"""
        exporter = Call_Flow__Exporter__Mermaid(result=result)
        exporter.setup()
        return exporter

    @type_safe
    def create_exporter__left_right(self                                             ,
                                    result: Schema__Call_Flow__Result                ) -> Call_Flow__Exporter__Mermaid:
        """Create Mermaid exporter with LR direction"""
        exporter = Call_Flow__Exporter__Mermaid(result=result, direction='LR')
        exporter.setup()
        return exporter

    @type_safe
    def create_exporter__no_contains(self                                            ,
                                     result: Schema__Call_Flow__Result               ) -> Call_Flow__Exporter__Mermaid:
        """Create Mermaid exporter without contains edges"""
        exporter = Call_Flow__Exporter__Mermaid(result=result, show_contains=False)
        exporter.setup()
        return exporter

    # ═══════════════════════════════════════════════════════════════════════════
    # Expected Mermaid Outputs (for comparison tests)
    # ═══════════════════════════════════════════════════════════════════════════

    def get_expected_mermaid__header_td(self) -> str:
        """Expected Mermaid header for TD direction"""
        return 'flowchart TD'

    def get_expected_mermaid__header_lr(self) -> str:
        """Expected Mermaid header for LR direction"""
        return 'flowchart LR'

    def get_expected_mermaid__self_call_arrow(self) -> str:
        """Expected arrow style for self calls"""
        return '-.->'

    def get_expected_mermaid__self_call_label(self) -> str:
        """Expected label for self calls"""
        return '|self|'

    def get_expected_mermaid__chain_call_arrow(self) -> str:
        """Expected arrow style for chain calls"""
        return '==>'

    def get_expected_mermaid__contains_arrow(self) -> str:
        """Expected arrow style for contains edges"""
        return '-->'

    # ═══════════════════════════════════════════════════════════════════════════
    # Storage Factory
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_storage(self) -> Call_Flow__Storage:                         # Create storage instance
        return Call_Flow__Storage()

    @type_safe
    def create_serialized_result(self) -> str:                              # Create a serialized result JSON string
        result = self.create_result__self_calls()
        storage = self.create_storage()
        return storage.to_json(result)

    # ═══════════════════════════════════════════════════════════════════════════
    # Complete Test Fixtures
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def create_complete_fixture__simple(self) -> Dict[str, Any]:            # Create complete fixture for simple class
        result = self.create_result__simple_class()
        exporter = self.create_exporter__default(result)

        return {'target'   : Sample__Simple_Class       ,
                'config'   : self.create_config__default(),
                'result'   : result                      ,
                'exporter' : exporter                    ,
                'mermaid'  : exporter.export()           ,
                'ontology' : self.create_ontology()      }

    @type_safe
    def create_complete_fixture__self_calls(self) -> Dict[str, Any]:        # Create complete fixture for self calls class
        result = self.create_result__self_calls()
        exporter = self.create_exporter__default(result)

        return {'target'   : Sample__Self_Calls          ,
                'config'   : self.create_config__default(),
                'result'   : result                       ,
                'exporter' : exporter                     ,
                'mermaid'  : exporter.export()            ,
                'ontology' : self.create_ontology()       }

    @type_safe
    def create_complete_fixture__multiple_self_calls(self) -> Dict[str, Any]:   # Create complete fixture for multiple self calls class
        result = self.create_result__multiple_self_calls()
        exporter = self.create_exporter__default(result)

        return {'target'   : Sample__Multiple_Self_Calls ,
                'config'   : self.create_config__default(),
                'result'   : result                       ,
                'exporter' : exporter                     ,
                'mermaid'  : exporter.export()            ,
                'ontology' : self.create_ontology()       }

    @type_safe
    def create_complete_fixture__deep_calls(self) -> Dict[str, Any]:            # Create complete fixture for deep calls class
        result = self.create_result__deep_calls()
        exporter = self.create_exporter__default(result)

        return {'target'   : Sample__Deep_Calls          ,
                'config'   : self.create_config__default(),
                'result'   : result                       ,
                'exporter' : exporter                     ,
                'mermaid'  : exporter.export()            ,
                'ontology' : self.create_ontology()       }

    @type_safe
    def create_all_fixtures(self) -> Dict[str, Dict[str, Any]]:
        """Create all fixtures for comprehensive testing"""
        return {'simple'              : self.create_complete_fixture__simple()            ,
                'self_calls'          : self.create_complete_fixture__self_calls()        ,
                'multiple_self_calls' : self.create_complete_fixture__multiple_self_calls(),
                'deep_calls'          : self.create_complete_fixture__deep_calls()        }

    # ═══════════════════════════════════════════════════════════════════════════
    # Assertion Helpers
    # ═══════════════════════════════════════════════════════════════════════════

    def assert_result_has_nodes(self                                                  ,
                                result     : Schema__Call_Flow__Result                ,
                                min_count  : int = 1                                  ) -> bool:
        """Assert result has minimum number of nodes"""
        return result.total_nodes >= min_count

    def assert_result_has_edges(self                                                  ,
                                result     : Schema__Call_Flow__Result                ,
                                min_count  : int = 1                                  ) -> bool:
        """Assert result has minimum number of edges"""
        return result.total_edges >= min_count

    def assert_result_has_entry_point(self                                            ,
                                      result : Schema__Call_Flow__Result              ,
                                      name   : str                                    ) -> bool:
        """Assert result entry point contains name"""
        return name in result.entry_point

    def assert_mermaid_has_header(self                                                ,
                                  mermaid   : str                                     ,
                                  direction : str = 'TD'                              ) -> bool:
        """Assert Mermaid output has correct header"""
        return f'flowchart {direction}' in mermaid

    def assert_mermaid_has_node(self                                                  ,
                                mermaid : str                                         ,
                                name    : str                                         ) -> bool:
        """Assert Mermaid output contains node with name"""
        return name in mermaid

    def assert_mermaid_has_self_call(self, mermaid: str) -> bool:
        """Assert Mermaid output contains self call styling"""
        return '-.->' in mermaid and '|self|' in mermaid

    def count_edges_by_predicate(self                                                 ,
                                 result       : Schema__Call_Flow__Result             ,
                                 predicate_id : Predicate_Id                          ) -> int:
        """Count edges with specific predicate"""
        count = 0
        for edge in result.graph.edges:
            if str(edge.predicate_id) == str(predicate_id):
                count += 1
        return count

    def get_node_names(self, result: Schema__Call_Flow__Result) -> List[str]:
        """Get list of node names from result"""
        return [str(node.name) for node in result.graph.nodes.values()]

    def get_edge_count(self, result: Schema__Call_Flow__Result) -> int:
        """Get total edge count from result"""
        return len(result.graph.edges)

# ═══════════════════════════════════════════════════════════════════════════════
# Sample Classes for Testing
# ═══════════════════════════════════════════════════════════════════════════════

class Sample__Simple_Class:
    """Simple class with no method calls"""

    def method_a(self):
        return 1

    def method_b(self):
        return 2


class Sample__Self_Calls:
    """Class with self.method() calls"""

    def do_work(self, data):
        return self.process(data)

    def process(self, data):
        return data * 2


class Sample__Multiple_Self_Calls:
    """Class with multiple self.method() calls"""

    def run(self, items):
        validated = self.validate(items)
        transformed = self.transform(validated)
        return self.output(transformed)

    def validate(self, items):
        return [i for i in items if i is not None]

    def transform(self, items):
        return [i * 2 for i in items]

    def output(self, items):
        return {'count': len(items), 'items': items}


class Sample__Chain_Calls:
    """Class with chain calls (obj.attr.method())"""

    def __init__(self):
        self.helper = Sample__Self_Calls()

    def execute(self, data):
        return self.helper.do_work(data)


class Sample__Conditional_Calls:
    """Class with calls inside conditionals"""

    def process(self, value):
        if value > 0:
            return self.handle_positive(value)
        else:
            return self.handle_negative(value)

    def handle_positive(self, value):
        return value * 2

    def handle_negative(self, value):
        return value * -1


class Sample__Deep_Calls:
    """Class with deep call chains"""

    def level_1(self):
        return self.level_2()

    def level_2(self):
        return self.level_3()

    def level_3(self):
        return self.level_4()

    def level_4(self):
        return "deep"


class Sample__Recursive:
    """Class with recursive calls"""

    def factorial(self, n):
        if n <= 1:
            return 1
        return n * self.factorial(n - 1)


class Sample__With_Builtins:
    """Class that calls builtin functions"""

    def process(self, items):
        count = len(items)
        total = sum(items)
        return print(f"Count: {count}, Total: {total}")


class Sample__External_Calls:
    """Class that calls external functions"""

    def process(self, data):
        result = external_helper(data)
        return self.finalize(result)

    def finalize(self, data):
        return data


def sample_standalone_function(x, y):
    """Standalone function"""
    result = sample_helper_function(x)
    return result + y


def sample_helper_function(value):
    """Helper function"""
    return value * 10


def external_helper(data):
    """External helper (for Sample__External_Calls)"""
    return data * 2
