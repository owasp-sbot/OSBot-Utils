# this is needed due to the circular dependencyes between the Ast_Node and the
#     clases that use it as a base class

import ast
from osbot_utils.helpers.Type_Registry      import type_registry
from osbot_utils.utils.ast.Ast_Add          import Ast_Add
from osbot_utils.utils.ast.Ast_Alias        import Ast_Alias
from osbot_utils.utils.ast.Ast_Argument     import Ast_Argument
from osbot_utils.utils.ast.Ast_Arguments    import Ast_Arguments
from osbot_utils.utils.ast.Ast_Assert       import Ast_Assert
from osbot_utils.utils.ast.Ast_Assign       import Ast_Assign
from osbot_utils.utils.ast.Ast_Attribute    import Ast_Attribute
from osbot_utils.utils.ast.Ast_Aug_Assign   import Ast_Aug_Assign
from osbot_utils.utils.ast.Ast_BinOn        import Ast_BinOp
from osbot_utils.utils.ast.Ast_Call         import Ast_Call
from osbot_utils.utils.ast.Ast_Class_Def    import Ast_Class_Def
from osbot_utils.utils.ast.Ast_Compare      import Ast_Compare
from osbot_utils.utils.ast.Ast_Comprehension import Ast_Comprehension
from osbot_utils.utils.ast.Ast_Constant     import Ast_Constant
from osbot_utils.utils.ast.Ast_Dict         import Ast_Dict
from osbot_utils.utils.ast.Ast_Eq           import Ast_Eq
from osbot_utils.utils.ast.Ast_Expr         import Ast_Expr
from osbot_utils.utils.ast.Ast_For          import Ast_For
from osbot_utils.utils.ast.Ast_Function_Def import Ast_Function_Def
from osbot_utils.utils.ast.Ast_Gt import Ast_Gt
from osbot_utils.utils.ast.Ast_If           import Ast_If
from osbot_utils.utils.ast.Ast_Import       import Ast_Import
from osbot_utils.utils.ast.Ast_Import_From  import Ast_Import_From
from osbot_utils.utils.ast.Ast_Is           import Ast_Is
from osbot_utils.utils.ast.Ast_IsNot import Ast_IsNot
from osbot_utils.utils.ast.Ast_Keyword import Ast_Keyword
from osbot_utils.utils.ast.Ast_List         import Ast_List
from osbot_utils.utils.ast.Ast_Load         import Ast_Load
from osbot_utils.utils.ast.Ast_Mod          import Ast_Mod
from osbot_utils.utils.ast.Ast_Module       import Ast_Module
from osbot_utils.utils.ast.Ast_Name         import Ast_Name
from osbot_utils.utils.ast.Ast_NotEq import Ast_NotEq
from osbot_utils.utils.ast.Ast_Return       import Ast_Return
from osbot_utils.utils.ast.Ast_Slice        import Ast_Slice
from osbot_utils.utils.ast.Ast_Store        import Ast_Store
from osbot_utils.utils.ast.Ast_Sub          import Ast_Sub
from osbot_utils.utils.ast.Ast_Subscript    import Ast_Subscript
from osbot_utils.utils.ast.Ast_Try          import Ast_Try
from osbot_utils.utils.ast.Ast_Tuple        import Ast_Tuple
from osbot_utils.utils.ast.Ast_While        import Ast_While

ast_types = {
    ast.Add          : Ast_Add          ,
    ast.alias        : Ast_Alias        ,
    ast.Assert       : Ast_Assert       ,
    ast.Assign       : Ast_Assign       ,
    ast.Attribute    : Ast_Attribute    ,
    ast.arg          : Ast_Argument     ,
    ast.arguments    : Ast_Arguments    ,
    ast.AugAssign    : Ast_Aug_Assign   ,
    ast.BinOp        : Ast_BinOp        ,
    ast.Call         : Ast_Call         ,
    ast.ClassDef     : Ast_Class_Def    ,
    ast.Compare      : Ast_Compare      ,
    ast.Constant     : Ast_Constant     ,
    ast.comprehension: Ast_Comprehension,
    ast.Dict         : Ast_Dict         ,
    ast.Expr         : Ast_Expr         ,
    ast.Eq           : Ast_Eq           ,
    ast.Gt           : Ast_Gt           ,
    ast.Import       : Ast_Import       ,
    ast.ImportFrom   : Ast_Import_From  ,
    ast.Is           : Ast_Is           ,
    ast.IsNot        : Ast_IsNot        ,
    ast.If           : Ast_If           ,
    ast.For          : Ast_For          ,
    ast.FunctionDef  : Ast_Function_Def ,
    ast.keyword      : Ast_Keyword      ,
    ast.List         : Ast_List         ,
    ast.Load         : Ast_Load         ,
    ast.Mod          : Ast_Mod          ,
    ast.Module       : Ast_Module       ,
    ast.Name         : Ast_Name         ,
    ast.NotEq        : Ast_NotEq        ,
    ast.Return       : Ast_Return       ,
    ast.Slice        : Ast_Slice        ,
    ast.Store        : Ast_Store        ,
    ast.Sub          : Ast_Sub          ,
    ast.Subscript    : Ast_Subscript    ,
    ast.Try          : Ast_Try          ,
    ast.Tuple        : Ast_Tuple        ,
    ast.While        : Ast_While        ,
}

for key, value in ast_types.items():
    type_registry.register(key, value)