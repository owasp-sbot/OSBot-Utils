from osbot_utils.graphs.mgraph.MGraph__Node import MGraph__Node
from osbot_utils.utils.Str import safe_str

LINE_PADDING = '    '

class Mermaid__Node(MGraph__Node):

    def cast(self, node):
        self.__dict__ = node.__dict__
        return self

    def render_node(self, include_padding=True):
        node_shape = self.attributes.get('node_shape')
        if node_shape == 'round-edge':
            left_char, right_char = '(', ')'
        elif node_shape == 'rhombus':
            left_char, right_char = '{', '}'
        else:
            left_char, right_char = '[', ']'
        if self.attributes.get('wrap_with_quotes') is False:
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
        self.attributes['wrap_with_quotes'] = value
        return self