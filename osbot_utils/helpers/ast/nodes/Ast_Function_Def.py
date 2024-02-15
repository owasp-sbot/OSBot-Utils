from osbot_utils.helpers.ast.Ast_Node            import Ast_Node
from osbot_utils.helpers.ast.nodes.Ast_Arguments import Ast_Arguments



class Ast_Function_Def(Ast_Node):

    def args(self):
        return Ast_Arguments(self.node.args)           # def convert to Ast_Arguments

    def info(self):
        return {'Ast_Function_Def': {'args'   : self.args()   ,
                                     'body'   : self.body()   ,
                                     'name'   : self.name()}}
                                     #'returns': self.returns()                 # this is for type hints


