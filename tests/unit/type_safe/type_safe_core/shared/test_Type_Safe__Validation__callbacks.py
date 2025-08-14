import pytest
import re
from unittest                        import TestCase
from typing                          import Dict, Any, Callable
from osbot_utils.type_safe.Type_Safe import Type_Safe

# Generic node and edge classes for testing
class GraphNode(Type_Safe):
    node_id: str
    value  : Any

    def __init__(self, node_id: str = "", value: Any = None):
        super().__init__()
        self.node_id = node_id
        self.value = value

class GraphEdge(Type_Safe):
    edge_id: str
    value  : Any

    def __init__(self, edge_id: str = "", value: Any = None):
        super().__init__()
        self.edge_id = edge_id
        self.value = value

class GraphExportConfig(Type_Safe):
    format_type: str
    options   : Dict[str, Any]

    def __init__(self, format_type: str = "dot", options: Dict[str, Any] = None):
        super().__init__()
        self.format_type = format_type
        self.options = options or {}

class GraphExporter(Type_Safe):
    config     : GraphExportConfig
    on_node   : Callable[[GraphNode, Dict[str, Any]], Dict[str, Any]]
    on_edge   : Callable[[GraphEdge, GraphNode, GraphNode], Dict[str, Any]]

class test_Type_Safe__callbacks(TestCase):

    def setUp(self):
        self.node_1 = GraphNode(node_id="n1", value="First Node")
        self.node_2 = GraphNode(node_id="n2", value="Second Node")
        self.edge = GraphEdge(edge_id="e1", value="Connects 1-2")
        self.config = GraphExportConfig()

    def valid_node_callback(self, node: GraphNode, attrs: Dict[str, Any]) -> Dict[str, Any]:
        return {"label": node.value, **attrs}

    def valid_edge_callback(self, edge: GraphEdge, source: GraphNode, target: GraphNode) -> Dict[str, Any]:
        return {"label": edge.value}

    def test_valid_callbacks(self):
        exporter = GraphExporter()

        exporter.config = self.config
        exporter.on_node = self.valid_node_callback         # FAILS HERE
        exporter.on_edge = self.valid_edge_callback

        # Test node callback
        result = exporter.on_node(self.node_1, {"shape": "box"})

        self.assertEqual(result["label"], "First Node")
        self.assertEqual(result["shape"], "box")

        # Test edge callback
        result = exporter.on_edge(self.edge, self.node_1, self.node_2)
        self.assertEqual(result["label"], "Connects 1-2")

    def test_invalid_node_callback_signature(self):
        exporter = GraphExporter()
        exporter.config = self.config

        # Invalid callback with wrong parameter types
        def invalid_callback(node: str, attrs: Dict[str, Any]) -> Dict[str, Any]:
            return attrs

        with self.assertRaises(ValueError) as context:
            exporter.on_node = invalid_callback
        self.assertIn("Invalid type for attribute", str(context.exception))

    def test_invalid_edge_callback_signature(self):
        exporter = GraphExporter()
        exporter.config = self.config

        # Invalid callback with wrong number of parameters
        def invalid_callback(edge: GraphEdge) -> Dict[str, Any]:
            return {"label": edge.value}

        with self.assertRaises(ValueError) as context:
            exporter.on_edge = invalid_callback
        self.assertIn("Invalid type for attribute", str(context.exception))

    def test_none_callbacks(self):
        exporter = GraphExporter()
        exporter.config = self.config

        # Should be able to set callbacks to None
        exporter.on_node = None
        exporter.on_edge = None

        self.assertIsNone(exporter.on_node)
        self.assertIsNone(exporter.on_edge)

    def test_lambda_callbacks(self):
        exporter = GraphExporter()
        exporter.config = self.config

        # Valid lambda callbacks
        exporter.on_node = lambda node, attrs: {"label": node.value, **attrs}
        exporter.on_edge = lambda edge, source, target: {"label": edge.value}

        result = exporter.on_node(self.node_1, {"shape": "box"})
        self.assertEqual(result["label"], "First Node")
        self.assertEqual(result["shape"], "box")

        result = exporter.on_edge(self.edge, self.node_1, self.node_2)
        self.assertEqual(result["label"], "Connects 1-2")

    def test_method_callbacks(self):
        class CallbackContainer:
            def node_callback(self, node: GraphNode, attrs: Dict[str, Any]) -> Dict[str, Any]:
                return {"label": node.value, **attrs}

            def edge_callback(self, edge: GraphEdge, source: GraphNode, target: GraphNode) -> Dict[str, Any]:
                return {"label": edge.value}

        container = CallbackContainer()
        exporter = GraphExporter()
        exporter.config = self.config

        # Bind instance methods as callbacks
        exporter.on_node = container.node_callback
        exporter.on_edge = container.edge_callback

        result = exporter.on_node(self.node_1, {"shape": "box"})
        self.assertEqual(result["label"], "First Node")

        result = exporter.on_edge(self.edge, self.node_1, self.node_2)
        self.assertEqual(result["label"], "Connects 1-2")

    def test_callback_return_type_validation(self):
        exporter = GraphExporter()
        exporter.config = self.config

        # Callback returning wrong type
        def invalid_return_callback(node: GraphNode, attrs: Dict[str, Any]) -> str:
            return "invalid"

        expected_error = "Invalid type for attribute 'on_node'. Expected 'typing.Callable[[test_Type_Safe__Validation__callbacks.GraphNode, typing.Dict[str, typing.Any]], typing.Dict[str, typing.Any]]' but got '<class 'function'>'"
        with pytest.raises(ValueError, match=re.escape(expected_error)):
            exporter.on_node = invalid_return_callback

    def test_callback_chaining(self):
        exporter = GraphExporter()
        exporter.config = self.config

        # Create a chain of callbacks
        def add_shape(node: GraphNode, attrs: Dict[str, Any]) -> Dict[str, Any]:
            return {"shape": "box", **attrs}

        def add_label(node: GraphNode, attrs: Dict[str, Any]) -> Dict[str, Any]:
            return {"label": node.value, **attrs}

        def add_style(node: GraphNode, attrs: Dict[str, Any]) -> Dict[str, Any]:
            return {"style": "filled", **attrs}

        # Chain callbacks
        exporter.on_node = lambda n, a: add_style(n, add_label(n, add_shape(n, a)))

        result = exporter.on_node(self.node_1, {})
        self.assertEqual(result["shape"], "box")
        self.assertEqual(result["label"], "First Node")
        self.assertEqual(result["style"], "filled")

    def test_callback_with_default_arguments(self):
        exporter = GraphExporter()
        exporter.config = self.config

        def node_callback_with_defaults(node: GraphNode, attrs: Dict[str, Any] = None) -> Dict[str, Any]:
            attrs = attrs or {}
            return {"label": node.value, **attrs}

        exporter.on_node = node_callback_with_defaults

        # Test with and without providing the optional argument
        result1 = exporter.on_node(self.node_1)
        self.assertEqual(result1["label"], "First Node")

        result2 = exporter.on_node(self.node_1, {"color": "red"})
        self.assertEqual(result2["label"], "First Node")
        self.assertEqual(result2["color"], "red")

    def test_callback_type_coercion(self):
        exporter = GraphExporter()
        exporter.config = self.config

        def node_callback_with_coercion(node: GraphNode, attrs: Dict[str, Any]) -> Dict[str, Any]:
            return {
                "id": str(node.node_id),      # node_id is already a string
                "value": int(node.value) if node.value.isdigit() else 0,
                **attrs
            }

        exporter.on_node = node_callback_with_coercion

        # Test with numeric value - using string for node_id to respect type annotation
        numeric_node = GraphNode(node_id="1", value="42")
        result = exporter.on_node(numeric_node, {})

        self.assertEqual(result["id"], "1")
        self.assertEqual(result["value"], 42)

        # Test with non-numeric value
        text_node = GraphNode(node_id="2", value="text")
        result = exporter.on_node(text_node, {})

        self.assertEqual(result["id"], "2")
        self.assertEqual(result["value"], 0)