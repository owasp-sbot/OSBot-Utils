import re
import pytest
from typing                          import Dict, Any, Callable, Optional
from unittest                        import TestCase
from osbot_utils.type_safe.Type_Safe import Type_Safe


class test_Type_Safe__regression__callable(TestCase):
    """Tests documenting bugs in Type_Safe Callable type validation."""

    def test__regression__callable_with_none_return_type__fails_validation(self):
        """
        BUG: When a Callable annotation specifies `None` as return type,
        and the assigned function has explicit `-> None` annotation,
        Type_Safe validation fails with AttributeError.

        Root cause:
        - The annotation `Callable[[...], None]` has return type `type(None)` (NoneType)
        - When inspecting the actual function's signature, `sig.return_annotation` is `None` (the value)
        - In `are_types_compatible_for_assigment(None, NoneType)`, the code tries to access `None.__mro__`
        - This raises: AttributeError: 'NoneType' object has no attribute '__mro__'

        The validation should recognize that:
        - A function with `-> None` annotation has `sig.return_annotation = type(None)`
        - A function without return annotation has `sig.return_annotation = inspect.Parameter.empty`
        - Both should be compatible with `Callable[[...], None]`
        """

        # Simple domain classes for testing
        class GraphNode(Type_Safe):
            node_id: str = ""

        class GraphEdge(Type_Safe):
            edge_id: str = ""

        # Class with Callable that returns None - THIS IS THE BUG
        class GraphExporter__Bug(Type_Safe):
            on_add_edge: Callable[[GraphEdge, GraphNode, GraphNode, Dict[str, Any]], None]  # Returns None

        # Valid callback function that returns None - WITH explicit annotation
        def valid_edge_callback(edge: GraphEdge, from_node: GraphNode, to_node: GraphNode, data: Dict[str, Any]) -> None:
            data['processed'] = True
            # No return statement = returns None

        # BUG: This should work but fails with AttributeError
        exporter = GraphExporter__Bug()
        # with pytest.raises(AttributeError, match="'NoneType' object has no attribute '__mro__'"):
        #     exporter.on_add_edge = valid_edge_callback  # BUG: Should succeed but crashes
        exporter.on_add_edge = valid_edge_callback          # FIXED

    def test__lambda_without_return_annotation_works(self):
        """
        Lambdas work because they don't have return type annotations.

        When a lambda is inspected, `sig.return_annotation` is `inspect.Parameter.empty`,
        which bypasses the return type validation that causes the bug.
        """

        class SimpleCallback(Type_Safe):
            on_event: Callable[[str], None]

        obj = SimpleCallback()

        # Lambda that implicitly returns None - NO annotation means no validation
        obj.on_event = lambda x: print(x)  # WORKS: No return annotation to validate

        # Verify it's assigned and callable
        assert obj.on_event is not None
        assert callable(obj.on_event)

    def test__regression__callable_with_none_return__explicit_annotation_fails(self):
        """
        BUG: Functions with explicit `-> None` annotation fail.

        The key distinction is:
        - Lambda without annotation: works (no return type to validate)
        - Function without `-> None`: works (no return type to validate)
        - Function WITH `-> None`: FAILS (triggers the bug)
        """

        class EventHandler:
            def handle(self, message: str) -> None:  # Explicit -> None
                print(f"Handling: {message}")

        class EventProcessor(Type_Safe):
            on_message: Callable[[str], None]

        handler = EventHandler()
        processor = EventProcessor()

        # BUG: Explicit -> None annotation triggers the bug
        # with pytest.raises(AttributeError, match="'NoneType' object has no attribute '__mro__'"):
        #     processor.on_message = handler.handle  # BUG: Should work
        processor.on_message = handler.handle       # FIXED

    def test__workaround__callable_without_type_params_works(self):
        """
        WORKAROUND: Using bare `Callable` without type parameters bypasses the bug.

        This works because without type parameters, no return type validation occurs.
        However, this sacrifices type safety.
        """

        class GraphNode(Type_Safe):
            node_id: str = ""

        class GraphEdge(Type_Safe):
            edge_id: str = ""

        class GraphExporter__Workaround(Type_Safe):
            on_add_edge: Callable  # No type parameters = no validation

        def valid_edge_callback(edge: GraphEdge, from_node: GraphNode, to_node: GraphNode, data: Dict[str, Any]) -> None:
            data['processed'] = True

        exporter = GraphExporter__Workaround()
        exporter.on_add_edge = valid_edge_callback  # WORKS: No type validation

        # Verify callback is assigned and callable
        assert exporter.on_add_edge is valid_edge_callback
        test_data = {}
        exporter.on_add_edge(GraphEdge(), GraphNode(), GraphNode(), test_data)
        assert test_data.get('processed') is True

    def test__regression__callable_with_any_return_also_fails(self):
        """
        BUG: Using `Any` as return type does NOT work as a workaround.

        Even when the Callable annotation uses `Any` as return type,
        if the actual function has `-> None`, the bug still triggers because:
        - `sig.return_annotation` from the function is still `None` (the value)
        - The comparison `are_types_compatible_for_assigment(None, Any)` still fails
        """

        class CallbackHolder(Type_Safe):
            on_event: Callable[[str], Any]  # Any instead of None

        def void_callback(message: str) -> None:  # Explicit -> None
            print(message)

        holder = CallbackHolder()

        # BUG: Still fails because the function has -> None annotation
        # with pytest.raises(AttributeError, match="'NoneType' object has no attribute '__mro__'"):
        #     holder.on_event = void_callback  # BUG: Should work with Any
        holder.on_event = void_callback     # FIXED

    def test__workaround__function_without_return_annotation_works(self):
        """
        WORKAROUND: Functions WITHOUT explicit `-> None` work.

        When a function has no return annotation, `sig.return_annotation`
        is `inspect.Parameter.empty`, which bypasses the buggy code path.
        """

        class CallbackHolder(Type_Safe):
            on_event: Callable[[str], Any]

        def void_callback_no_annotation(message: str):  # NO -> None annotation
            print(message)

        holder = CallbackHolder()
        holder.on_event = void_callback_no_annotation  # WORKS: No annotation to validate

        assert holder.on_event is void_callback_no_annotation

    def test__regression__optional_callable_with_none_return__different_error(self):
        """
        BUG: Optional[Callable[[...], None]] fails with ValueError, not AttributeError.

        This is a different code path - the Union type handling catches the
        AttributeError earlier and converts it to a validation failure.
        """

        class OptionalCallback(Type_Safe):
            on_event: Optional[Callable[[str], None]] = None

        obj = OptionalCallback()

        # Assigning None works (that's what Optional allows)
        obj.on_event = None
        assert obj.on_event is None

        # But assigning an actual function with -> None fails with ValueError
        def explicit_none_callback(x: str) -> None:
            print(x)

        # expected_error = "invalid type for attribute 'on_event'"
        # with pytest.raises(ValueError, match=expected_error):
        #     obj.on_event = explicit_none_callback  # BUG: Should work
        obj.on_event = explicit_none_callback           # FIXED

    def test__regression__optional_callable__lambda_fails(self):

        class OptionalCallback(Type_Safe):
            on_event: Optional[Callable[[str], None]] = None

        obj = OptionalCallback()

        # Lambda without return annotation doesn't work
        error_message = "On OptionalCallback, invalid type for attribute 'on_event'. Expected 'typing.Optional[typing.Callable[[str], NoneType]]' but got '<class 'function'>'"
        # with pytest.raises(ValueError, match=re.escape(error_message)):
        #     obj.on_event = lambda x: print(x)                           # BUG
        obj.on_event = lambda x: print(x)
        assert obj.on_event is not None                                   # FIXED

    def test__callable_with_non_none_return_type_works(self):
        """
        COMPARISON: Callable with non-None return types work correctly.

        This confirms the bug is specifically in handling None return type.
        """

        class DataProcessor(Type_Safe):
            transform: Callable[[str], str]                    # Returns str
            compute  : Callable[[int, int], int]               # Returns int
            fetch    : Callable[[str], Dict[str, Any]]         # Returns Dict

        def upper(s: str) -> str:
            return s.upper()

        def add(a: int, b: int) -> int:
            return a + b

        def get_data(key: str) -> Dict[str, Any]:
            return {"key": key, "value": 42}

        processor = DataProcessor()

        # All these work because return type is not None
        processor.transform = upper
        processor.compute = add
        processor.fetch = get_data

        assert processor.transform("hello") == "HELLO"
        assert processor.compute(2, 3) == 5
        assert processor.fetch("test") == {"key": "test", "value": 42}

    def test__regression__real_world_scenario__mgraph_export_dot(self):
        """
        BUG: Real-world scenario from MGraph__Export__Dot.

        This replicates the exact pattern that fails in the MGraph-AI codebase:
        - Domain classes for nodes and edges
        - Exporter class with callback for edge processing
        - Callback returns None (void function pattern)
        """

        # Simplified domain classes matching MGraph pattern
        class Domain__MGraph__Node(Type_Safe):
            node_id: str = ""

        class Domain__MGraph__Edge(Type_Safe):
            edge_id: str = ""

        # Exporter class matching MGraph__Export__Dot pattern
        class MGraph__Export__Dot(Type_Safe):
            # This is the exact signature that fails
            on_add_edge: Callable[[Domain__MGraph__Edge, Domain__MGraph__Node, Domain__MGraph__Node, Dict[str, Any]], None]

        # Configuration class that creates the callback
        class Render__Config(Type_Safe):

            def _create_edge_callback(self) -> Callable[[Domain__MGraph__Edge, Domain__MGraph__Node, Domain__MGraph__Node, Dict[str, Any]], None]:
                def on_add_edge(edge: Domain__MGraph__Edge,
                               from_node: Domain__MGraph__Node,
                               to_node: Domain__MGraph__Node,
                               edge_data: Dict[str, Any]) -> None:
                    edge_data['configured'] = True
                return on_add_edge

            def configure_dot_export(self, dot: MGraph__Export__Dot) -> MGraph__Export__Dot:
                # This line fails in the real codebase
                dot.on_add_edge = self._create_edge_callback()
                return dot

        dot = MGraph__Export__Dot()
        config = Render__Config()

        # BUG: This should work but fails
        # with pytest.raises(AttributeError, match="'NoneType' object has no attribute '__mro__'"):
        #     config.configure_dot_export(dot)
        config.configure_dot_export(dot) # FIXED

    def test__expected_behavior__after_fix(self):
        """
        EXPECTED: After the fix, all these should work.

        This test documents the expected behavior once the bug is fixed.
        Currently all these raise errors.
        """

        class EventSystem(Type_Safe):
            on_start   : Callable[[], None]                           # No params, returns None
            on_data    : Callable[[str], None]                        # One param, returns None
            on_complete: Callable[[str, int, Dict[str, Any]], None]   # Multiple params, returns None

        # These are all valid void callbacks WITH explicit -> None
        def start_handler() -> None:
            print("Started")

        def data_handler(data: str) -> None:
            print(f"Data: {data}")

        def complete_handler(status: str, code: int, details: Dict[str, Any]) -> None:
            print(f"Complete: {status}, {code}, {details}")

        system = EventSystem()

        # BUG: All of these should work after fix but currently fail
        # with pytest.raises(AttributeError):
        #     system.on_start = start_handler
        #
        # with pytest.raises(AttributeError):
        #     system.on_data = data_handler
        #
        # with pytest.raises(AttributeError):
        #     system.on_complete = complete_handler

        system.on_start    = start_handler          # FIXED
        system.on_data     = data_handler           # FIXED
        system.on_complete = complete_handler       # FIXED



    """Additional edge cases for Callable type validation."""

    def test__function_without_return_annotation_bypasses_validation(self):
        """
        Functions without return type annotation bypass the buggy code path.

        When a function has no `-> ...` annotation, `sig.return_annotation`
        is `inspect.Parameter.empty`, which doesn't trigger the __mro__ access.
        """

        class Handler(Type_Safe):
            callback: Callable[[str], None]

        # Function without return annotation
        def no_annotation_callback(message: str):  # Note: no -> None
            print(message)

        handler = Handler()

        # This WORKS because no return annotation means no return type validation
        handler.callback = no_annotation_callback

        assert handler.callback is no_annotation_callback

    def test__callable_none_vs_nonetype_confusion(self):
        """
        Documents the None vs NoneType confusion at the heart of the bug.

        In Python:
        - `None` is a value (the singleton instance)
        - `type(None)` is `NoneType` (the type)
        - `-> None` in annotations means return type is `type(None)`
        - `sig.return_annotation` for `-> None` should be `type(None)`, not `None`

        The bug occurs because somewhere the value `None` is being compared
        against the type `NoneType`, and then `None.__mro__` is accessed.
        """

        # Demonstrate the difference
        assert None is not type(None)
        assert type(None).__name__ == 'NoneType'
        assert hasattr(type(None), '__mro__')  # type(None) has __mro__
        assert not hasattr(None, '__mro__')     # None does NOT have __mro__

        # This is why the bug occurs:
        # The validation code does: source_type.__mro__
        # Where source_type is None (the value) instead of type(None) (the type)

    def test__summary_of_what_works_and_what_fails(self):
        """
        Summary table of what works and what fails.

        | Callable Annotation          | Function Has -> None | Result        |
        |------------------------------|---------------------|---------------|
        | Callable (bare)              | Yes                 | WORKS         |
        | Callable (bare)              | No                  | WORKS         |
        | Callable[[...], None]        | Yes                 | BUG: FAILS    |
        | Callable[[...], None]        | No                  | WORKS         |
        | Callable[[...], Any]         | Yes                 | BUG: FAILS    |
        | Callable[[...], Any]         | No                  | WORKS         |
        | Callable[[...], str]         | Yes (-> str)        | WORKS         |
        | Optional[Callable[..., None]]| Yes                 | BUG: FAILS    |
        | Optional[Callable[..., None]]| No (lambda)         | WORKS         |

        The pattern: If the FUNCTION has explicit `-> None`, validation fails.
        If the function has no return annotation (lambda or omitted), it works.
        """

        class TestHolder(Type_Safe):
            bare_callable     : Callable
            typed_none_return : Callable[[str], None]
            typed_str_return  : Callable[[str], str]

        holder = TestHolder()

        # Functions WITH -> None annotation
        def with_none(s: str) -> None: pass
        def with_str(s: str) -> str: return s

        # Functions WITHOUT return annotation
        def without_annotation(s: str): pass

        # Test bare Callable - always works
        holder.bare_callable = with_none  # WORKS
        holder.bare_callable = without_annotation  # WORKS

        # Test typed None return - depends on function
        # with pytest.raises(AttributeError):
        #     holder.typed_none_return = with_none  # BUG: FAILS
        holder.typed_none_return = with_none  # FIXED
        holder.typed_none_return = without_annotation  # WORKS

        # Test typed str return - works when types match
        holder.typed_str_return = with_str  # WORKS