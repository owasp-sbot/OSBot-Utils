from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_Class_Def(Ast_Node):

    def info(self):
        #self.print()
        return {'Ast_Class_Def': {'bases': self.bases()  ,
                                  'body' : self.body()   ,
                                  'name' : self.node.name }}        # we need to use the actual node.name value here
