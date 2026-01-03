import sys
from typing                                                                         import Set
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config        import Schema__Call_Graph__Config
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe

STDLIB_BUILTINS: Set[str] = {'print', 'len', 'str', 'int', 'list', 'dict', 'set',  # Python builtins to filter
                             'tuple', 'range', 'enumerate', 'zip', 'map', 'filter',
                             'sorted', 'reversed', 'type', 'isinstance', 'hasattr',
                             'getattr', 'setattr', 'delattr', 'super', 'open',
                             'abs', 'all', 'any', 'bin', 'bool', 'bytes', 'callable',
                             'chr', 'complex', 'dir', 'divmod', 'float', 'format',
                             'frozenset', 'hash', 'hex', 'id', 'input', 'iter',
                             'max', 'min', 'next', 'object', 'oct', 'ord', 'pow',
                             'repr', 'round', 'slice', 'sum', 'vars', 'append',
                             'extend', 'insert', 'remove', 'pop', 'clear', 'copy',
                             'update', 'keys', 'values', 'items', 'get'}

class Call_Flow__Call__Filter(Type_Safe):                                            # Filters calls based on configuration
    config : Schema__Call_Graph__Config                                              # Filter configuration



    def should_skip(self, call_name: str) -> bool:                                   # Check if call should be filtered out
        if self.is_dunder(call_name) and not self.config.include_dunder:
            return True

        if self.is_private(call_name) and not self.config.include_private:
            return True

        if self.is_stdlib(call_name) and not self.config.include_stdlib:
            return True

        if self.is_blocked(call_name):
            return True

        if not self.is_allowed(call_name):
            return True

        return False

    def is_dunder(self, call_name: str) -> bool:                                     # Check if name is dunder method
        base_name = call_name.split('.')[-1] if '.' in call_name else call_name
        return base_name.startswith('__') and base_name.endswith('__')

    def is_private(self, call_name: str) -> bool:                                    # Check if name is private (single underscore)
        base_name = call_name.split('.')[-1] if '.' in call_name else call_name
        return base_name.startswith('_') and not base_name.startswith('__')

    def is_stdlib(self, call_name: str) -> bool:                                     # Check if name is Python stdlib
        base_name = call_name.split('.')[-1] if '.' in call_name else call_name
        return base_name in STDLIB_BUILTINS

    def is_stdlib_module(self, module: str) -> bool:                                 # Check if module is stdlib
        if not module:
            return False

        stdlib_modules = set(sys.stdlib_module_names) if hasattr(sys, 'stdlib_module_names') else set()
        base_module    = module.split('.')[0]
        return base_module in stdlib_modules

    def is_external(self, module: str) -> bool:                                      # Check if module is external (pip package)
        return not self.is_stdlib_module(module) if module else True

    def is_blocked(self, call_name: str) -> bool:                                    # Check if target is in any blocklist
        if not self.config.module_blocklist and not self.config.class_blocklist:
            return False

        for blocked in self.config.module_blocklist:
            if call_name.startswith(str(blocked)):
                return True

        for blocked in self.config.class_blocklist:
            if call_name.startswith(str(blocked)):
                return True

        return False

    def is_allowed(self, call_name: str) -> bool:                                    # Check if target passes allowlists
        if not self.config.module_allowlist and not self.config.class_allowlist:
            return True                                                              # No allowlist = allow all

        for allowed in self.config.module_allowlist:
            if call_name.startswith(str(allowed)):
                return True

        for allowed in self.config.class_allowlist:
            if call_name.startswith(str(allowed)):
                return True

        return False

    def should_include_method(self, method_name: str) -> bool:                       # Check if method should be included
        if self.is_dunder(method_name) and not self.config.include_dunder:
            return False

        if self.is_private(method_name) and not self.config.include_private:
            return False

        return True
