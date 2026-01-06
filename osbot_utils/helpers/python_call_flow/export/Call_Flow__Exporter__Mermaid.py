# ═══════════════════════════════════════════════════════════════════════════════
# Call Flow Exporter - Mermaid
# Exports call flow graphs to Mermaid diagram format
# ═══════════════════════════════════════════════════════════════════════════════

from typing                                                                     import Dict, Optional
from osbot_utils.helpers.python_call_flow.core.Call_Flow__Ontology              import Call_Flow__Ontology
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Result     import Schema__Call_Flow__Result
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph   import Schema__Semantic_Graph

class Call_Flow__Exporter__Mermaid(Type_Safe):                                   # Export call flow result to Mermaid diagram
    result        : Schema__Call_Flow__Result  = None                            # The call flow result to export
    graph         : Schema__Semantic_Graph     = None                            # Direct graph reference (alternative to result)
    ontology      : Call_Flow__Ontology        = None                            # Ontology for ID lookups
    direction     : str                        = 'TD'                            # Diagram direction: TD, LR, BT, RL
    show_contains : bool                       = True                            # Show CONTAINS edges
    show_calls    : bool                       = True                            # Show CALLS edges
    node_id_map   : Dict[str, str]             = None                            # Map node IDs to sanitized Mermaid IDs

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.node_id_map is None:
            self.node_id_map = {}

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, *args):
        pass

    def setup(self) -> 'Call_Flow__Exporter__Mermaid':                           # Initialize exporter
        self.ontology = Call_Flow__Ontology().setup()
        self.node_id_map = {}

        if self.result and not self.graph:                                       # Get graph from result if provided
            self.graph = self.result.graph

        return self

    # ═══════════════════════════════════════════════════════════════════════════
    # Main Export Methods
    # ═══════════════════════════════════════════════════════════════════════════

    def export(self) -> str:                                                     # Export graph to Mermaid flowchart string
        if not self.graph:
            return f"flowchart {self.direction}\n    empty[No graph data]"

        lines = [f"flowchart {self.direction}"]

        self._build_node_id_map()                                                # Build sanitized ID mappings

        for node_id in list(self.graph.nodes.keys()):                            # Render nodes
            node = self.graph.nodes[node_id]
            node_line = self._render_node(node_id, node)
            if node_line:
                lines.append(f"    {node_line}")

        for edge in self.graph.edges:                                            # Render edges
            edge_line = self._render_edge(edge)
            if edge_line:
                lines.append(f"    {edge_line}")

        return '\n'.join(lines)

    def to_html(self                                                             ,
                title  : str = 'Call Flow Diagram'                               ,
                width  : str = '100%'                                            ,
                height : str = '600px'                                           ) -> str:
        mermaid_code = self.export()                                             # Generate standalone HTML page with Mermaid diagram

        return f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .mermaid {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            margin-bottom: 20px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="mermaid" style="width: {width}; min-height: {height};">
{mermaid_code}
    </div>
    <script>
        mermaid.initialize({{ startOnLoad: true, theme: 'default' }});
    </script>
</body>
</html>'''

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Rendering
    # ═══════════════════════════════════════════════════════════════════════════

    def _build_node_id_map(self):                                                # Build mapping from node IDs to Mermaid-safe IDs
        counter = 0
        for node_id in list(self.graph.nodes.keys()):                            # Convert to list for iteration
            safe_id = f"n{counter}"
            self.node_id_map[str(node_id)] = safe_id
            counter += 1

    def _render_node(self, node_id, node) -> str:                                # Render a single node to Mermaid format
        safe_id    = self.node_id_map.get(str(node_id), str(node_id))
        name       = str(node.name) if node.name else 'unnamed'
        node_type  = self._get_node_type_ref(node.node_type_id)
        shape      = self._get_node_shape(node_type, name)

        return f"{safe_id}{shape}"

    def _get_node_type_ref(self, node_type_id) -> str:                           # Get node type reference string from ID
        node_type_id_str = str(node_type_id)

        type_map = {str(self.ontology.node_type_id__class())   : 'class'    ,    # Map IDs to type refs
                    str(self.ontology.node_type_id__method())  : 'method'   ,
                    str(self.ontology.node_type_id__function()): 'function' ,
                    str(self.ontology.node_type_id__module())  : 'module'   ,
                    str(self.ontology.node_type_id__external()): 'external' }

        return type_map.get(node_type_id_str, 'unknown')

    def _get_node_shape(self, node_type: str, name: str) -> str:                 # Get Mermaid shape for node type
        escaped_name = self._escape_name(name)

        shapes = {'class'   : f'["{escaped_name}"]'                              ,    # Rectangle
                  'method'  : f'("{escaped_name}")'                              ,    # Rounded rectangle (stadium)
                  'function': f'("{escaped_name}")'                              ,    # Rounded rectangle
                  'module'  : f'[["{escaped_name}"]]'                            ,    # Subroutine shape
                  'external': f'>"{escaped_name}"]'                              }    # Asymmetric (flag)

        return shapes.get(node_type, f'["{escaped_name}"]')

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Rendering
    # ═══════════════════════════════════════════════════════════════════════════

    def _render_edge(self, edge) -> Optional[str]:                               # Render a single edge to Mermaid format
        predicate_ref = self._get_predicate_ref(edge.predicate_id)

        if predicate_ref == 'contains' and not self.show_contains:               # Filter edges based on settings
            return None
        if predicate_ref in ('calls', 'calls_self', 'calls_chain') and not self.show_calls:
            return None

        from_id = self.node_id_map.get(str(edge.from_node_id), str(edge.from_node_id))
        to_id   = self.node_id_map.get(str(edge.to_node_id), str(edge.to_node_id))

        arrow = self._get_edge_arrow(predicate_ref)
        label = self._get_edge_label(predicate_ref)

        if label:
            return f"{from_id} {arrow}|{label}| {to_id}"
        else:
            return f"{from_id} {arrow} {to_id}"

    def _get_predicate_ref(self, predicate_id) -> str:                           # Get predicate reference string from ID
        predicate_id_str = str(predicate_id)

        predicate_map = {str(self.ontology.predicate_id__contains())   : 'contains'    ,
                         str(self.ontology.predicate_id__calls())      : 'calls'       ,
                         str(self.ontology.predicate_id__calls_self()) : 'calls_self'  ,
                         str(self.ontology.predicate_id__calls_chain()): 'calls_chain' }

        return predicate_map.get(predicate_id_str, 'unknown')

    def _get_edge_arrow(self, predicate_ref: str) -> str:                        # Get Mermaid arrow style for predicate
        arrows = {'contains'   : '-->'                                           ,    # Solid arrow
                  'calls'      : '-->'                                           ,    # Solid arrow
                  'calls_self' : '-.->'                                          ,    # Dotted arrow
                  'calls_chain': '==>'                                           }    # Thick arrow

        return arrows.get(predicate_ref, '-->')

    def _get_edge_label(self, predicate_ref: str) -> Optional[str]:              # Get edge label for predicate
        labels = {'contains'   : None                                            ,    # No label for containment
                  'calls'      : None                                            ,    # No label for simple calls
                  'calls_self' : 'self'                                          ,    # Label self calls
                  'calls_chain': 'chain'                                         }    # Label chain calls

        return labels.get(predicate_ref)

    # ═══════════════════════════════════════════════════════════════════════════
    # Utilities
    # ═══════════════════════════════════════════════════════════════════════════

    def _escape_name(self, name: str) -> str:                                    # Escape special characters for Mermaid
        return (name.replace('"', "'")                                           # Replace quotes
                    .replace('<', '&lt;')                                         # Escape HTML entities
                    .replace('>', '&gt;'))

    def _sanitize_id(self, name: str) -> str:                                    # Sanitize name for Mermaid node ID
        return (name.replace('.', '_')
                    .replace(' ', '_')
                    .replace('-', '_')
                    .replace(':', '_')
                    .replace('<', '')
                    .replace('>', ''))
