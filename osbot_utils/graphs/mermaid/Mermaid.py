from enum                                       import Enum, auto
from osbot_utils.graphs.mermaid.Mermaid__Graph  import Mermaid__Graph
from osbot_utils.graphs.mermaid.Mermaid__Node import LINE_PADDING, Mermaid__Node
from osbot_utils.utils.Python_Logger            import Python_Logger
from osbot_utils.base_classes.Kwargs_To_Self    import Kwargs_To_Self
from osbot_utils.utils.Str                      import safe_str



class Diagram__Type(Enum):
    class_diagram                = auto()
    entity_relationship_diagram  = auto()
    flowchart                    = auto()
    gantt                        = auto()
    git_graph                    = auto()
    graph                        = auto()
    mermaid_map                  = auto()
    mindmap                      = auto()
    pie_chart                    = auto()
    requirement_diagram          = auto()
    sequence_diagram             = "sequenceDiagram"
    state_diagram                = 'stateDiagram-v2'
    user_journey                 = auto()

class Diagram__Direction(Enum):
    BT = auto()
    LR = auto()
    TB = auto()
    TD = auto()
    RL = auto()

class Mermaid__Type:
    pass

class Mermaid(Kwargs_To_Self):

    diagram_direction : Diagram__Direction  = Diagram__Direction.LR
    diagram_type      : Diagram__Type = Diagram__Type.graph
    mermaid_code      : list
    graph             : Mermaid__Graph
    config__add_nodes : bool = True
    logger            : Python_Logger

    def __init__(self):
        super().__init__()
        #self.logger.disable()

    def add_edge(self, from_node_key, to_node_key, label=None,attributes=None):
        nodes_by_id = self.graph.data().nodes__by_key()
        from_node   = nodes_by_id.get(from_node_key)
        to_node     = nodes_by_id.get(to_node_key)
        if not from_node:
            from_node = self.add_node(key=from_node_key)
        if not to_node:
            to_node = self.add_node(key=to_node_key)
        new_edge = self.graph.add_edge(from_node, to_node, label=label,attributes=attributes)
        return new_edge

    def add_node(self, **kwargs):
        mgraph_node = self.graph.add_node(**kwargs)
        return Mermaid__Node().cast(mgraph_node)

    def add_line(self, line):
        self.mermaid_code.append(line)
        return line

    def code(self):
        self.code_create()
        return '\n'.join(self.mermaid_code)

    def code_create(self, recreate=False):
        with self as _:
            if recreate:                            # if recreate is True, reset the code
                _.reset_code()
            elif self.mermaid_code:                 # if the code has already been created, don't create it
                return self                         #   todo: find a better way to do this, namely around the concept of auto detecting (on change) when the recreation needs to be done (vs being able to use the previously calculated data)
            _.add_line(self.graph_header())
            if self.config__add_nodes:
                for node in _.nodes():
                    node_code = node.render_node()
                    _.add_line(node_code)
                _.add_line('')
            for edge in _.edges():
                edge_code = self.render_edge(edge)
                _.add_line(edge_code)
        return self

    def code_markdown(self):
        self.code_create()
        markdown = ['#### Mermaid Graph',
                    "```mermaid" ,
                    *self.mermaid_code,
                    "```"]

        return '\n'.join(markdown)

    def edges(self):
        return self.graph.edges

    def graph_header(self):
        if type(self.diagram_type.value) is str:
            value = self.diagram_type.value
        else:
            value = self.diagram_type.name
        return f'{value} {self.diagram_direction.name}'

    def print_code(self):
        print(self.code())

    def nodes(self):
        return self.graph.nodes

    def render_edge(self, edge):
        from_node_key = safe_str(edge.from_node.key)
        to_node_key   = safe_str(edge.to_node  .key)
        if edge.attributes.get('output_node_from'):
            from_node_key =  edge.from_node.render_node(include_padding=False) #f'{edge.from_node.key}["{edge.from_node.label}"]'
        if edge.attributes.get('output_node_to'):
            to_node_key   = edge.to_node.render_node(include_padding=False   ) #f'{edge.to_node  .key}["{edge.to_node  .label}"]'
        if edge.attributes.get('edge_mode') == 'lr_using_pipe':
            link_code      = f'-->|{edge.label}|'
        elif edge.label:
            link_code      = f'--"{edge.label}"-->'
        else:
            link_code      = '-->'
        edge_code      = f'{LINE_PADDING}{from_node_key} {link_code} {to_node_key}'
        return edge_code




    def reset_code(self):
        self.mermaid_code = []
        return self

    def set_config__add_nodes(self, value):
        self.config__add_nodes = value
        return self

    def set_direction(self, direction):
        if isinstance(direction, Diagram__Direction):
            self.diagram_direction = direction
        elif isinstance(direction, str) and direction in Diagram__Direction.__members__:
            self.diagram_direction = Diagram__Direction[direction]
        return self                             # If the value can't be set (not a valid name), do nothing

    def set_diagram_type(self, diagram_type):
        if isinstance(diagram_type, Diagram__Type):
            self.diagram_type = diagram_type

    def save(self, target_file=None):
        file_path = target_file or '/tmp/mermaid.md'

        with open(file_path, 'w') as file:
            file.write(self.code_markdown())
        return file_path