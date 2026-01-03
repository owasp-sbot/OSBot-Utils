from typing                                                                          import List
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph                 import Schema__Call_Graph
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Node           import Schema__Call_Graph__Node
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type  import Enum__Call_Graph__Edge_Type
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label   import Safe_Str__Label


class Call_Flow__Exporter__Mermaid(Type_Safe):                                       # Export call graph to Mermaid format
    graph           : Schema__Call_Graph                                             # Graph to export
    direction       : Safe_Str__Label           = Safe_Str__Label('TD')              # TD (top-down) or LR (left-right)
    show_modules    : bool                      = False                              # Include module names
    show_depth      : bool                      = True                               # Show depth indicators
    show_contains   : bool                      = True                               # Show CONTAINS edges
    max_label_len   : int                       = 30                                 # Truncate long labels
    font_size       : int                       = 14                                 # Node font size in pixels

    def export(self) -> str:                                                         # Generate Mermaid flowchart
        lines = list()
        lines.append(f"flowchart {self.direction}")
        lines.append("")

        lines.extend(self.generate_node_definitions())                               # Node definitions
        lines.append("")

        lines.extend(self.generate_edge_definitions())                               # Edge connections

        return '\n'.join(lines)

    def generate_node_definitions(self) -> List[str]:                                # Generate node definition lines
        lines    = []
        by_depth = {}                                                                # Group by depth for subgraphs

        for node in self.graph.nodes.values():
            depth = int(node.depth)
            if depth not in by_depth:
                by_depth[depth] = []
            by_depth[depth].append(node)

        for depth in sorted(by_depth.keys()):                                        # Output grouped by depth
            if self.show_depth:
                lines.append(f"    subgraph depth_{depth}[Depth {depth}]")

            for node in by_depth[depth]:
                node_def = self.format_node(node)
                prefix   = "        " if self.show_depth else "    "
                lines.append(f"{prefix}{node_def}")

            if self.show_depth:
                lines.append("    end")
                lines.append("")

        return lines

    def format_node(self, node: Schema__Call_Graph__Node) -> str:                    # Format single node definition
        node_id = self.sanitize_id(str(node.node_id))
        label   = self.make_label(node)

        node_type_str = str(node.node_type.value) if hasattr(node.node_type, 'value') else str(node.node_type)

        if node.is_entry and node_type_str == 'class':                               # Entry class: stadium shape
            return f'{node_id}(["{label}"])'
        elif node.is_entry:                                                          # Entry point: double circle
            return f'{node_id}(("{label}"))'
        elif node.is_external:                                                       # External: parallelogram
            return f'{node_id}[/"{label}"/]'
        elif node_type_str == 'class':                                               # Class: stadium shape
            return f'{node_id}(["{label}"])'
        elif node_type_str == 'method':                                              # Method: rounded box
            return f'{node_id}("{label}")'
        else:                                                                        # Function: rectangle
            return f'{node_id}["{label}"]'

    def make_label(self, node: Schema__Call_Graph__Node) -> str:                     # Create display label for node
        if self.show_modules and str(node.module):
            label = f"{node.module}.{node.name}"
        else:
            label = str(node.name)                                                   # Use short name by default

        if len(label) > self.max_label_len:                                          # Truncate if too long
            label = label[:self.max_label_len - 3] + "..."

        return self.escape_label(label)

    def generate_edge_definitions(self) -> List[str]:                                # Generate edge connection lines
        lines = []

        for edge in self.graph.edges:
            from_id   = self.sanitize_id(str(edge.from_node))
            to_id     = self.sanitize_id(str(edge.to_node))
            edge_type = edge.edge_type

            if edge_type == Enum__Call_Graph__Edge_Type.CONTAINS:                    # CONTAINS: thin arrow
                if self.show_contains:
                    lines.append(f"    {from_id} -.->|contains| {to_id}")
            elif edge_type == Enum__Call_Graph__Edge_Type.SELF:                      # SELF: normal arrow
                lines.append(f"    {from_id} -->|self| {to_id}")
            elif edge_type == Enum__Call_Graph__Edge_Type.CHAIN:                     # CHAIN: dotted arrow
                lines.append(f"    {from_id} -.-> {to_id}")
            else:                                                                    # CALLS: normal arrow
                lines.append(f"    {from_id} --> {to_id}")

        return lines

    def sanitize_id(self, node_id: str) -> str:                                      # Make ID safe for Mermaid
        sanitized = node_id.replace('.', '_').replace('-', '_')
        sanitized = sanitized.replace('<', '').replace('>', '')
        sanitized = sanitized.replace(' ', '_')
        return sanitized

    def escape_label(self, label: str) -> str:                                       # Escape special chars in labels
        return label.replace('"', "'").replace('<', '&lt;').replace('>', '&gt;')

    def get_title(self) -> str:                                                      # Get display title for graph
        full_name = str(self.graph.name)
        if '.' in full_name:
            return full_name.split('.')[-1]                                          # Just the class/function name
        return full_name

    def to_html(self) -> str:                                                        # Generate standalone HTML with Mermaid
        mermaid_code = self.export()
        title        = self.get_title()
        return f'''<!DOCTYPE html>
<html>
<head>
    <title>Call Flow: {self.escape_label(title)}</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {{ font-family: sans-serif; padding: 20px; }}
        h1 {{ color: #333; }}
        .stats {{ background: #f5f5f5; padding: 10px; border-radius: 5px; margin-bottom: 20px; }}
        .mermaid {{ background: white; }}
    </style>
</head>
<body>
    <h1>{self.escape_label(title)}</h1>
    <div class="stats">
        <strong>Nodes:</strong> {self.graph.node_count()} |
        <strong>Edges:</strong> {self.graph.edge_count()} |
        <strong>Max Depth:</strong> {self.graph.max_depth_found}
    </div>
    <div class="mermaid">
{mermaid_code}
    </div>
    <script>
        mermaid.initialize({{
            startOnLoad: true,
            theme: 'default',
            flowchart: {{
                nodeSpacing: 50,
                rankSpacing: 50
            }},
            themeVariables: {{
                fontSize: '{self.font_size}px'
            }}
        }});
    </script>
</body>
</html>'''