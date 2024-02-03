from osbot_utils.base_classes.Kwargs_To_Self                       import Kwargs_To_Self
from osbot_utils.graphs.mermaid.models.Mermaid__Node__Shape import Mermaid__Node__Shape


class Mermaid__Node__Config(Kwargs_To_Self):
    node_shape       : Mermaid__Node__Shape = Mermaid__Node__Shape.default
    wrap_with_quotes : bool = True               # add support for only using quotes when needed
