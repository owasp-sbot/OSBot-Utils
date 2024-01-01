# this is needed due to the circular dependencyes between the Ast_Node and the
#     clases that use it as a base class

import ast
from osbot_utils.helpers.Type_Registry      import type_registry
from osbot_utils.utils.ast.Ast_Argument     import Ast_Argument
from osbot_utils.utils.ast.Ast_Arguments    import Ast_Arguments
from osbot_utils.utils.ast.Ast_Constant     import Ast_Constant
from osbot_utils.utils.ast.Ast_Function_Def import Ast_Function_Def
from osbot_utils.utils.ast.Ast_Module       import Ast_Module
from osbot_utils.utils.ast.Ast_Return       import Ast_Return

type_registry.register(ast.arguments    , Ast_Arguments    )
type_registry.register(ast.arg          , Ast_Argument     )
type_registry.register(ast.Constant     , Ast_Constant     )
type_registry.register(ast.FunctionDef  , Ast_Function_Def )
type_registry.register(ast.Module       , Ast_Module       )
type_registry.register(ast.Return       , Ast_Return       )

