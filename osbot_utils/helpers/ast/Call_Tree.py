import ast
import inspect
from osbot_utils.utils.Str import str_dedent


class Call_Tree:

    def get_called_methods(self, func):
        source = inspect.getsource(func)
        source = str_dedent(source)
        tree    = ast.parse(source)


        class CallVisitor(ast.NodeVisitor):
            def __init__(self):
                self.called_methods = []

            def visit_FunctionDef(self, node):
                node.name = 'aaaaa'
                print(node)


            def visit_Call(self, node):


                if isinstance(node.func, ast.Attribute):        # This handles method calls like obj.method()
                    self.called_methods.append(node.func.attr)
                elif isinstance(node.func, ast.Name):           # This handles direct function calls like func()
                    self.called_methods.append(node.func.id)
                self.generic_visit(node)

        visitor = CallVisitor()
        visitor.visit(tree)

        print()
        #print(ast.dump(tree, indent=2))
        return ast.unparse(tree)            #todo: finish implementation
        return visitor.called_methods