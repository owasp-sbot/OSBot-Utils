import ast
from osbot_utils.helpers.Type_Registry  import type_registry
from osbot_utils.utils.Lists            import list_stats
from osbot_utils.helpers.ast.Ast_Base   import Ast_Base


class Ast_Node(Ast_Base):

    def __repr__(self):
        if self.__class__ is Ast_Node:
            return f"[Ast_Node][????] {self.node.__class__}"
        return super().__repr__()

    def ast_node(self, node):
        type_key      = type(node)
        resolved_type = type_registry.resolve(type_key)
        if resolved_type:
           return resolved_type(node)
        return Ast_Node(node)

    def ast_value(self, value):
        if value is None:
            return None
        if hasattr(value, '__module__') and value.__module__ == 'ast':
            return self.ast_node(value)
        if type(value) is list:
            return self.ast_nodes(value)
        return value

    def ast_nodes(self, nodes):
        ast_nodes = []
        for node in nodes:
            ast_node = self.ast_node(node)
            ast_nodes.append(ast_node)           # todo: see the use of .info() here (should be better to return the ast_node)
        return ast_nodes

    def all_ast_nodes(self):
        nodes = []
        for node in ast.walk(self.node):
            node = self.ast_node(node)
            nodes.append(node)
        return nodes

    def stats(self):
        ast_node_types   = []
        node_types       = []
        all_keys         = []
        all_values       = []
        for ast_node in self.all_ast_nodes():
            ast_node_types.append(ast_node     .__class__.__name__)
            node_types    .append(ast_node.node.__class__.__name__)

            for _,info in ast_node.info().items():
                if type(info) is dict:
                    for key,value in info.items():
                        if not isinstance(value, Ast_Node):
                            if type(value) not in [list, dict, tuple]:
                                if type(value) is str:
                                    value = value[:20].strip()
                                if value and 'ast.Constant' in str(value):
                                    print(key, str(value))
                                all_keys  .append(key)
                                all_values.append(value)

                    assert _ == ast_node.__class__.__name__     # todo: revove after refactoring

        stats = {'all_keys'       : list_stats(all_keys)        ,
                 'all_values'     : list_stats(all_values)      ,
                 'ast_node_types' : list_stats(ast_node_types ) ,
                 'node_types'     : list_stats(node_types) }

        #pprint(stats)
        return stats


    # node vars mappings
    def args        (self): return self.ast_value(self.node.args        )
    def bases       (self): return self.ast_value(self.node.bases       )
    def body        (self): return self.ast_value(self.node.body        )
    def cause       (self): return self.ast_value(self.node.cause       )
    def comparators (self): return self.ast_value(self.node.comparators )
    def context_expr(self): return self.ast_value(self.node.context_expr)
    def ctx         (self): return self.ast_value(self.node.ctx         )
    def dims        (self): return self.ast_value(self.node.dims        )
    def elt         (self): return self.ast_value(self.node.elt         )
    def elts        (self): return self.ast_value(self.node.elts        )
    def exc         (self): return self.ast_value (self.node.exc        )
    def func        (self): return self.ast_value(self.node.func        )
    def id          (self): return self.ast_value(self.node.id          )
    def ifs         (self): return self.ast_value(self.node.ifs         )
    def items       (self): return self.ast_value(self.node.items       )
    def iter        (self): return self.ast_value(self.node.iter        )
    def generators  (self): return self.ast_value(self.node.generators  )
    def finalbody   (self): return self.ast_value(self.node.finalbody   )
    def handlers    (self): return self.ast_value(self.node.handlers    )
    def keys        (self): return self.ast_value(self.node.keys        )
    def keywords    (self): return self.ast_value(self.node.keywords    )
    def left        (self): return self.ast_value(self.node.left        )
    def level       (self): return self.ast_value(self.node.level       )
    def lower       (self): return self.ast_value(self.node.lower       )
    def module      (self): return self.ast_value(self.node.module      )
    def name        (self): return self.ast_value(self.node.name        )
    def names       (self): return self.ast_value(self.node.names       )
    def op          (self): return self.ast_value(self.node.op          )
    def operand     (self): return self.ast_value(self.node.operand     )
    def ops         (self): return self.ast_value(self.node.ops         )
    def orelse      (self): return self.ast_value(self.node.orelse      )
    def right       (self): return self.ast_value(self.node.right       )
    def msg         (self): return self.ast_value(self.node.msg         )
    def slice       (self): return self.ast_value(self.node.slice       )
    def target      (self): return self.ast_value(self.node.target      )
    def targets     (self): return self.ast_value(self.node.targets     )
    def test        (self): return self.ast_value(self.node.test        )
    def type        (self): return self.ast_value(self.node.type        )
    def upper       (self): return self.ast_value (self.node.upper      )
    def value       (self): return self.ast_value(self.node.value       )
    def values      (self): return self.ast_value(self.node.values      )
