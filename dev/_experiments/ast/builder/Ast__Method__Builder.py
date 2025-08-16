from typing import List, Any

from osbot_utils.helpers.ast.builder.Ast__Class__Builder import Ast__Class__Builder
from osbot_utils.helpers.ast.builder.Ast__Conditional__Builder import Ast__Conditional__Builder


class Ast__Method__Builder:
    """Builder for methods and functions"""

    def __init__(self, name: str, args: List[str], parent_builder):
        self.name = name
        self.args = args
        self.parent = parent_builder
        self.body_statements = []
        self.decorators = []
        self.return_annotation = None
        self.docstring = None
        self.is_static = False
        self.is_classmethod = False
        self.is_async = False

    # === DECORATORS ===
    def add_decorator(self, decorator: str):
        self.decorators.append(decorator)
        return self

    def property_getter(self):
        return self.add_decorator('@property')

    def static_method(self):
        self.is_static = True
        return self

    def class_method(self):
        self.is_classmethod = True
        return self

    def async_method(self):
        self.is_async = True
        return self

    # === DOCUMENTATION ===
    def with_docstring(self, docstring: str):
        self.docstring = docstring
        return self

    def with_return_type(self, return_type: str):
        self.return_annotation = return_type
        return self

    # === BODY STATEMENTS ===
    def assign(self, target: str, value: Any):
        """Add assignment: target = value"""
        stmt = self._create_assignment(target, value)
        self.body_statements.append(stmt)
        return self

    def call(self, function: str, args: List[Any] = None, kwargs: Dict[str, Any] = None):
        """Add function call as statement"""
        call_stmt = self._create_call_statement(function, args or [], kwargs or {})
        self.body_statements.append(call_stmt)
        return self

    def returns(self, value: Any):
        """Add return statement"""
        return_stmt = self._create_return_statement(value)
        self.body_statements.append(return_stmt)
        return self

    def returns_call(self, function: str, args: List[Any] = None, kwargs: Dict[str, Any] = None):
        """Return the result of a function call"""
        return self.returns(self._create_call_expression(function, args or [], kwargs or {}))

    def returns_string_concat(self, parts: List[str]):
        """Return concatenated strings"""
        concat_expr = self._create_string_concat(parts)
        return self.returns(concat_expr)

    def add_if(self, condition: str) -> Ast__Conditional__Builder:
        """Add if statement"""
        return Ast__Conditional__Builder('if', condition, self)

    def add_for(self, variable: str, iterable: str) -> Ast__Loop__Builder:
        """Add for loop"""
        return Ast__Loop__Builder('for', variable, iterable, self)

    def add_while(self, condition: str) -> Ast__Loop__Builder:
        """Add while loop"""
        return Ast__Loop__Builder('while', condition, None, self)

    def add_try(self) -> Ast__Try__Builder:
        """Add try block"""
        return Ast__Try__Builder(self)

    def add_variable(self, name: str, value: Any):
        """Add local variable"""
        return self.assign(name, value)

    def raise_exception(self, exception_type: str, message: str = None):
        """Add raise statement"""
        raise_stmt = self._create_raise_statement(exception_type, message)
        self.body_statements.append(raise_stmt)
        return self

    # === CONTEXT MANAGEMENT ===
    def end_method(self):
        """Finish building the method"""
        method_node = self._build_method_ast()
        if isinstance(self.parent, Ast__Class__Builder):
            self.parent.methods.append(method_node)
            return self.parent
        else:  # Function at module level
            self.parent.module.node.body.append(method_node)
            self.parent._context_stack.pop()
            return self.parent