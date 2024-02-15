from enum import auto, Enum


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