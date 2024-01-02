from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Try(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Try]'

    def info(self):
        return {'Ast_Try': {'body'     : self.body     (),
                            'finalbody': self.finalbody(),
                            'handlers' : self.handlers (),
                            'orelse'   : self.orelse   ()}}