import ast

from osbot_utils.helpers.Type_Registry import type_registry
from osbot_utils.utils.Dev import pprint
from osbot_utils.utils.Lists import list_stats
from osbot_utils.utils.Objects              import type_base_classes, obj_info, obj_data
from osbot_utils.utils.ast.Ast_Base import Ast_Base


class Ast_Node(Ast_Base):

    def __repr__(self):
        return f"[Ast_Node][????] {self._type}"

    def args(self):
        return self.ast_nodes(self.node.args)

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
        return value

    def ast_nodes(self, nodes):
        ast_nodes = []
        for node in nodes:
            ast_node = self.ast_node(node)
            ast_nodes.append(ast_node.info())           # todo: see the use of .info() here (should be better to return the ast_node)
        return ast_nodes

    def all_ast_nodes(self):
        nodes = []
        for node in ast.walk(self.node):
            node = self.ast_node(node)
            nodes.append(node)
        return nodes

    def bases(self): return self.ast_nodes(self.node.bases)

    def body(self):
        if self.node.body:
            if type(self.node.body) is list:                # handle the case where body is a list of nodes
                return self.ast_nodes(self.node.body)
            return self.ast_node(self.node.body)            # and when it is not (like on Ast_If_Exp)

    def cause       (self): return self.ast_value(self.node.cause       )
    def comparators (self): return self.ast_nodes(self.node.comparators )
    def context_expr(self): return self.ast_node (self.node.context_expr)
    def ctx         (self): return self.ast_node (self.node.ctx         )

    def dims        (self): return self.ast_nodes(self.node.dims        )

    def elt         (self): return self.ast_node (self.node.elt         )
    def elts        (self): return self.ast_nodes(self.node.elts        )
    def exc         (self):
        if self.node.exc:
            return self.ast_node (self.node.exc         )

    def func        (self): return self.ast_node (self.node.func        )

    def ifs         (self): return self.ast_nodes(self.node.ifs         )

    def info(self):
        vars_to_del = ['col_offset', 'end_col_offset', 'lineno', 'end_lineno', 'type_comment']
        data = self.obj_data()
        for var_to_del in vars_to_del:
            if data.get(var_to_del):
                del data[var_to_del]
        return data

    def items     (self): return self.ast_nodes(self.node.items     )
    def iter      (self): return self.ast_node (self.node.iter      )
    def generators(self): return self.ast_nodes(self.node.generators)
    def finalbody (self): return self.ast_nodes(self.node.finalbody )
    def handlers  (self): return self.ast_nodes(self.node.handlers  )
    def keys      (self): return self.ast_nodes(self.node.keys      )
    def keywords  (self): return self.ast_nodes(self.node.keywords  )

    def left(self):
        return self.ast_node(self.node.left)

    def lower(self):
        return self.ast_node (self.node.lower)

    def names(self):
        return self.ast_nodes(self.node.names)

    def op      (self): return self.ast_node (self.node.op      )
    def operand (self): return self.ast_node (self.node.operand )
    def ops     (self): return self.ast_nodes(self.node.ops     )
    def orelse  (self):
        if type(self.node.orelse) is list:
            return self.ast_nodes(self.node.orelse  )
        return self.ast_node(self.node.orelse)

    def right(self):
        return self.ast_node(self.node.right)

    def print(self):
        obj_info(self.node)
        return self

    def msg(self):
        return self.ast_value(self.node.msg)

    def slice(self):
        return self.ast_node(self.node.slice)

    def source_code(self):
        return ast.unparse(self.node)

    def target(self):
        return self.ast_node(self.node.target)

    def targets(self):
        return self.ast_nodes(self.node.targets)

    def test(self):
        return self.ast_node(self.node.test)

    def type(self):
        if self.node.type:
            return self.ast_node(self.node.type)

    def upper(self):
        return self.ast_node (self.node.upper)

    def value(self):
        return self.ast_value(self.node.value)

    def values(self):
        return self.ast_nodes(self.node.values)



    def stats(self):

        ast_node_types   = []
        node_types       = []
        all_keys         = []
        all_values       = []
        for ast_node in self.all_ast_nodes():
            ast_node_types.append(ast_node     .__class__.__name__)
            node_types    .append(ast_node.node.__class__.__name__)

            for _,info in ast_node.info().items():
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

        # pprint(list_stats(all_keys))
        # pprint(list_stats(all_values))

        stats = {'all_keys'       : list_stats(all_keys)        ,
                 'all_values'     : list_stats(all_values)      ,
                 'ast_node_types' : list_stats(ast_node_types ) ,
                 'node_types'     : list_stats(node_types) }

        #pprint(stats)
        return stats

    # def returns(self):                                    # todo: add this when looking at type hints (which is what this is )
    #     if self.node.returns:
    #         return self.ast_node(self.node.returns)

