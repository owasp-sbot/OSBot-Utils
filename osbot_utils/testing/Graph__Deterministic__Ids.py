import inspect
from contextlib     import contextmanager
from unittest.mock  import patch

from osbot_utils.type_safe.Type_Safe import Type_Safe

TEST_ID_PREFIX__GRAPH = 'a'
TEST_ID_PREFIX__NODE  = 'c'
TEST_ID_PREFIX__EDGE  = 'e'
TEST_ID_PREFIX__OTHER = 'f'

@contextmanager
def graph_deterministic_ids():              # Context manager for deterministic sequential ID generation in tests
    deterministic_ids = MGraph__Test__Ids()

    from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id

    original_new = Obj_Id.__new__

    def patched_new(cls, *args, **kwargs):
        return str.__new__(cls, deterministic_ids.next_id_from_context())

    with patch.object(Obj_Id, '__new__', patched_new):
        yield deterministic_ids

class Graph__Deterministic__Ids(Type_Safe):
    counter_graph : int = 0
    counter_node  : int = 0
    counter_edge  : int = 0
    counter_obj   : int = 0

    def reset(self):
        self.counter_graph = 0
        self.counter_node  = 0
        self.counter_edge  = 0
        self.counter_obj   = 0
        return self

    def next_graph_id(self) -> str:
        self.counter_graph += 1
        return f"{TEST_ID_PREFIX__GRAPH}{self.counter_graph:07d}"

    def next_node_id(self) -> str:
        self.counter_node += 1
        return f"{TEST_ID_PREFIX__NODE}{self.counter_node:07d}"

    def next_edge_id(self) -> str:
        self.counter_edge += 1
        return f"{TEST_ID_PREFIX__EDGE}{self.counter_edge:07d}"

    def next_obj_id(self) -> str:
        self.counter_obj += 1
        return f"{TEST_ID_PREFIX__OTHER}{self.counter_obj:07d}"

    def next_id_from_context(self) -> str:
        """Inspect call stack to determine which ID type to generate."""
        frame = inspect.currentframe()
        try:
            # Go up the stack to find the calling line
            caller_frame    = frame.f_back.f_back  # Skip this method and __new__
            code_context    = inspect.getframeinfo(caller_frame).code_context
            caller_f_locals = caller_frame.f_locals
            if 'value' in caller_f_locals:
                return caller_f_locals.get('value')
            if code_context:
                source_line = code_context[0]
                if 'Graph_Id' in source_line:
                    return self.next_graph_id()
                elif 'Node_Id' in source_line:
                    return self.next_node_id()
                elif 'Edge_Id' in source_line:
                    return self.next_edge_id()

            return self.next_obj_id()  # Fallback for direct Obj_Id() calls
        finally:
            del frame

# these are legacy (to be removed) since this is what this classed used to be called (when in the MGraph-DB project)

mgraph_test_ids   = graph_deterministic_ids
MGraph__Test__Ids = Graph__Deterministic__Ids

# here are other experiments in trying to find the best way to use this

deterministic_ids  = graph_deterministic_ids
fixed_graph_ids    = graph_deterministic_ids
test_graph_ids     = graph_deterministic_ids