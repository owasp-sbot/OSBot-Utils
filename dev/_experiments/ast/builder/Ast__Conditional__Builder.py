from typing import List, Any, Dict


class Ast__Conditional__Builder:
    """Builder for if/elif/else blocks"""

    def __init__(self, block_type: str, condition: str, parent_builder):
        self.block_type = block_type  # 'if', 'elif', 'else'
        self.condition = condition
        self.parent = parent_builder
        self.body_statements = []

    def assign(self, target: str, value: Any):
        return self._add_statement('assign', target, value)

    def call(self, function: str, args: List[Any] = None, kwargs: Dict[str, Any] = None):
        return self._add_statement('call', function, args, kwargs)

    def returns(self, value: Any):
        return self._add_statement('return', value)

    def elif_(self, condition: str) -> 'Ast__Conditional__Builder':
        """Add elif block"""
        self._finalize_current_block()
        return Ast__Conditional__Builder('elif', condition, self.parent)

    def else_(self) -> 'ConditionalBuilder':
        """Add else block"""
        self._finalize_current_block()
        return Ast__Conditional__Builder('else', None, self.parent)

    def end_if(self):
        """End the conditional block"""
        self._finalize_current_block()
        return self.parent

