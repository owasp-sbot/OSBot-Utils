from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Class_Def(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Class_Def]'

    def info(self):
        #self.print()
        return {'Ast_Class_Def': {'bases': self.bases()  ,
                                  'body' : self.body()   ,
                                  'name' : self.node.name }}        # we need to use the actual node.name value here
