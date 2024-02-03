from enum import Enum

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.graphs.mermaid.configs.Mermaid__Node__Config import Mermaid__Node__Config
from osbot_utils.graphs.mermaid.models.Mermaid__Node__Shape import Mermaid__Node__Shape
from osbot_utils.graphs.mgraph.MGraph__Node import MGraph__Node
from osbot_utils.utils.Str import safe_str

LINE_PADDING = '    '

class Mermaid__Node(MGraph__Node):

    config : Mermaid__Node__Config

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    # def cast(self, source):
    #     self.__dict__ = source.__dict__
    #     return self


        #for key,value in source.__dict__.items():
        #   setattr(self, key, value)

    def render_node(self, include_padding=True):
        left_char, right_char = self.config.node_shape.value

        if self.attributes.get('show_label') is False:
            node_code = f'{self.key}'
        else:
            if self.config.wrap_with_quotes is False:
                node_code = f'{self.key}{left_char}{self.label}{right_char}'
            else:
                node_code = f'{self.key}{left_char}"{self.label}"{right_char}'

        if include_padding:
            node_code = f'{LINE_PADDING}{node_code}'
        return node_code

    def shape(self, shape=None):
        self.config.node_shape = Mermaid__Node__Shape.get_shape(shape)
        return self

    def shape_circle     (self): self.config.node_shape = Mermaid__Node__Shape.circle       ; return self
    def shape_round_edges(self): self.config.node_shape = Mermaid__Node__Shape.round_edges  ; return self
    def shape_rhombus    (self): self.config.node_shape = Mermaid__Node__Shape.rhombus      ; return self
    def shape_default    (self): self.config.node_shape = Mermaid__Node__Shape.default      ; return self


    def wrap_with_quotes(self, value=True):
        self.config.wrap_with_quotes = value
        return self

    def show_label(self, value=True):
        self.attributes['show_label'] = value
        return self