# this is needed due to the circular dependencyes between the Ast_Node and the
#     clases that use it as a base class

import ast
from osbot_utils.helpers.Type_Registry      import type_registry
from osbot_utils.utils.ast.Ast_Argument     import Ast_Argument
from osbot_utils.utils.ast.Ast_Arguments    import Ast_Arguments
from osbot_utils.utils.ast.Ast_Assign import Ast_Assign
from osbot_utils.utils.ast.Ast_Attribute import Ast_Attribute
from osbot_utils.utils.ast.Ast_Call import Ast_Call
from osbot_utils.utils.ast.Ast_Class_Def    import Ast_Class_Def
from osbot_utils.utils.ast.Ast_Constant     import Ast_Constant
from osbot_utils.utils.ast.Ast_Dict import Ast_Dict
from osbot_utils.utils.ast.Ast_Expr import Ast_Expr
from osbot_utils.utils.ast.Ast_Function_Def import Ast_Function_Def
from osbot_utils.utils.ast.Ast_Load import Ast_Load
from osbot_utils.utils.ast.Ast_Module       import Ast_Module
from osbot_utils.utils.ast.Ast_Name         import Ast_Name
from osbot_utils.utils.ast.Ast_Return       import Ast_Return
from osbot_utils.utils.ast.Ast_Store import Ast_Store

ast_types = {
    ast.Assign      : Ast_Assign       ,
    ast.Attribute   : Ast_Attribute    ,
    ast.arg         : Ast_Argument     ,
    ast.arguments   : Ast_Arguments    ,
    ast.Call        : Ast_Call         ,
    ast.ClassDef    : Ast_Class_Def    ,
    ast.Constant    : Ast_Constant     ,
    ast.Dict        : Ast_Dict         ,
    ast.Expr        : Ast_Expr         ,
    ast.FunctionDef : Ast_Function_Def ,
    ast.Load        : Ast_Load         ,
    ast.Module      : Ast_Module       ,
    ast.Name        : Ast_Name         ,
    ast.Return      : Ast_Return       ,
    ast.Store       : Ast_Store
}

for key, value in ast_types.items():
    type_registry.register(key, value)