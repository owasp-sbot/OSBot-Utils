from osbot_utils.utils.Objects import obj_info
from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Call(Ast_Node):

    def info(self):
        return {'Ast_Call': { 'args'    : self.args()    ,
                              'func'    : self.func()    ,
                              'keywords': self.keywords()}}

    def name(self):
        func = self.func()
        if type(func).__name__ == 'Ast_Name':
            return func.id()
        if type(func).__name__ == 'Ast_Attribute':
            return func.node.attr
        return None