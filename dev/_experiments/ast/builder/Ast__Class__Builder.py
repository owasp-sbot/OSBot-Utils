from typing                                                 import List
from osbot_utils.helpers.ast.builder.Ast__Method__Builder   import Ast__Method__Builder
from osbot_utils.helpers.ast.builder.Ast__Property__Builder import Ast__Property__Builder
from osbot_utils.helpers.ast.builder.Ast__Python__Builder   import Ast__Python__Builder


class Ast__Class__Builder:
    """Builder for Python classes"""

    def __init__(self, name: str, parent_builder: Ast__Python__Builder):
        self.name = name
        self.parent = parent_builder
        self.methods = []
        self.base_classes = []
        self.decorators = []
        self.docstring = None

    # === INHERITANCE ===
    def inherits_from(self, *base_classes: str):
        """Set base classes"""
        self.base_classes.extend(base_classes)
        return self

    # === DECORATORS ===
    def add_decorator(self, decorator: str):
        """Add class decorator"""
        self.decorators.append(decorator)
        return self

    def dataclass(self):
        """Add @dataclass decorator"""
        return self.add_decorator('@dataclass')

    # === DOCUMENTATION ===
    def with_docstring(self, docstring: str):
        """Add class docstring"""
        self.docstring = docstring
        return self

    # === METHODS ===
    def add_init(self, args: List[str] = None) -> 'MethodBuilder':
        """Add __init__ method"""
        return self.add_method('__init__', ['self'] + (args or []))

    def add_method(self, name: str, args: List[str] = None) -> 'MethodBuilder':
        """Add regular method"""
        method_builder = Ast__Method__Builder(name, args or ['self'], self)
        return method_builder

    def add_property(self, name: str) -> 'PropertyBuilder':
        """Add property method"""
        return Ast__Property__Builder(name, self)

    def add_static_method(self, name: str, args: List[str] = None) -> 'MethodBuilder':
        """Add static method"""
        method_builder = Ast__Method__Builder(name, args or [], self)
        method_builder.is_static = True
        return method_builder

    def add_class_method(self, name: str, args: List[str] = None) -> 'MethodBuilder':
        """Add class method"""
        method_builder = Ast__Method__Builder(name, ['cls'] + (args or []), self)
        method_builder.is_classmethod = True
        return method_builder

    # === QUICK METHODS ===
    def add_simple_init(self, fields: List[str]):
        """Add simple __init__ that just assigns all fields"""
        init_builder = self.add_init(fields)
        for field in fields:
            init_builder.assign(f'self.{field}', field)
        return init_builder.end_method()

    def add_getter(self, field: str):
        """Add simple getter method"""
        return (self.add_method(f'get_{field}')
                .returns(f'self.{field}')
                .end_method())

    def add_setter(self, field: str):
        """Add simple setter method"""
        return (self.add_method(f'set_{field}', [f'{field}'])
                .assign(f'self.{field}', field)
                .end_method())

    # === CONTEXT MANAGEMENT ===
    def end_class(self) -> Ast__Python__Builder:
        """Finish building the class and return to parent"""
        # Convert this builder to actual AST nodes
        class_node = self._build_class_ast()
        self.parent.module.node.body.append(class_node)
        self.parent._context_stack.pop()
        return self.parent