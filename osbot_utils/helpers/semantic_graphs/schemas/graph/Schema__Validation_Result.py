from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Validation_Errors  import List__Validation_Errors


class Schema__Validation_Result(Type_Safe):                                          # Result of graph validation
    valid  : bool                                                                    # True if graph passed validation
    errors : List__Validation_Errors                                                 # List of error messages (empty if valid)