from enum import Enum

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.graphs.mgraph.MGraph__Node import MGraph__Node
from osbot_utils.utils.Str import safe_str

LINE_PADDING = '    '

class Mermaid__Node__Shape(Enum):
    default = ('[', ']')

class Mermaid__Node__Config(Kwargs_To_Self):
    node_shape       : Mermaid__Node__Shape = Mermaid__Node__Shape.default
    wrap_with_quotes : bool = True               # add support for only using quotes when needed

class Mermaid__Node(MGraph__Node):

    config : Mermaid__Node__Config

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)

    # def cast(self, source):
    #     self.__dict__ = source.__dict__
    #     return self


        #for key,value in source.__dict__.items():
        #   setattr(self, key, value)



#        return self

    def get_node_shape_chars(self):
        node_shape = self.attributes.get('node_shape')
        if node_shape == 'round-edge':
            left_char, right_char = '(', ')'
        elif node_shape == 'rhombus':
            left_char, right_char = '{', '}'
        else:
            left_char, right_char = '[', ']'
        return left_char, right_char

    def render_node(self, include_padding=True):
        left_char, right_char = self.get_node_shape_chars()

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

    def shape(self, value):
        self.attributes['node_shape'] = value
        return self

    def wrap_with_quotes(self, value=True):
        self.config.wrap_with_quotes = value
        return self

    def show_label(self, value=True):
        self.attributes['show_label'] = value
        return self