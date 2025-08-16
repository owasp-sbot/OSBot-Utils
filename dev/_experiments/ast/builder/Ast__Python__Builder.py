# todo: NOTE this is a first pass at creating a helper for the AST classes and at the moment
#       there are lots of problems with it
#            - missing methods and classes
#            - circular dependencies issues (we will need a number of base classes,
#              and maybe use the osbot_utils.helpers.Type_Registry.type_registry that is
#              used in the main ast code
#              needs tests

from typing                                              import List, Any
from osbot_utils.helpers.ast                             import Ast_Module
from osbot_utils.helpers.ast.builder.Ast__Class__Builder import Ast__Class__Builder


class Ast__Python__Builder:
    """Main entry point for building Python code"""

    def __init__(self):
        self.module = Ast_Module("")  # Empty module from OSBot-Utils
        self._context_stack = []  # Track nested contexts

    # === IMPORTS ===
    def add_import(self, module_name: str, alias: str = None):
        """Add: import module_name [as alias]"""
        return self._add_import_node(module_name, alias)

    def add_from_import(self, module: str, names: List[str]):
        """Add: from module import name1, name2, ..."""
        return self._add_from_import_node(module, names)

    def add_imports(self, modules: List[str]):
        """Add multiple imports at once"""
        for module in modules:
            self.add_import(module)
        return self

    # === CLASSES ===
    def add_class(self, name: str) -> Ast__Class__Builder:
        """Start building a class"""
        class_builder = Ast__Class__Builder(name, self)
        self._context_stack.append(class_builder)
        return class_builder

    # === FUNCTIONS ===
    def add_function(self, name: str, args: List[str] = None) -> Ast__Function__Builder:
        """Start building a function"""
        function_builder = Ast__Function__Builder(name, args or [], self)
        self._context_stack.append(function_builder)
        return function_builder

    # === VARIABLES ===
    def add_variable(self, name: str, value: Any):
        """Add module-level variable"""
        return self._add_assignment(name, value)

    # === BUILD ===
    def build(self) -> str:
        """Generate the final Python code"""
        return self.module.source_code()

    def build_and_save(self, filename: str):
        """Generate and save to file"""
        code = self.build()
        with open(filename, 'w') as f:
            f.write(code)
        return self

    def build_and_execute(self):
        """Generate and execute the code"""
        return self.module.execute_code()