from typing import Any

from osbot_utils.helpers.ast.builder.Ast__Class__Builder import Ast__Class__Builder
from osbot_utils.helpers.ast.builder.Ast__Method__Builder import Ast__Method__Builder


class Ast__Property__Builder:
    """Builder for property methods"""

    def __init__(self, name: str, parent_builder: Ast__Class__Builder):
        self.name = name
        self.parent = parent_builder
        self.getter = None
        self.setter = None
        self.deleter = None

    def getter_returns(self, value: Any):
        """Simple getter that returns a value"""
        self.getter = Ast__Method__Builder(self.name, ['self'], self.parent)
        self.getter.property_getter().returns(value)
        return self

    def setter_assigns(self, field: str):
        """Simple setter that assigns to a field"""
        self.setter = Ast__Method__Builder(f'{self.name}', ['self', 'value'], self.parent)
        self.setter.add_decorator(f'@{self.name}.setter').assign(field, 'value')
        return self

    def end_property(self):
        """Finish building the property"""
        if self.getter:
            self.parent.methods.append(self.getter._build_method_ast())
        if self.setter:
            self.parent.methods.append(self.setter._build_method_ast())
        return self.parent