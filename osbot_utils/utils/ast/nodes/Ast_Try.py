from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Try(Ast_Node):

    def info(self):
        return {'Ast_Try': {'body'     : self.body     (),
                            'finalbody': self.finalbody(),
                            'handlers' : self.handlers (),
                            'orelse'   : self.orelse   ()}}