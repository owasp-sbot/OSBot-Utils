from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__NaCl__Public_Key  import Safe_Str__NaCl__Public_Key
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__NaCl__Private_Key import Safe_Str__NaCl__Private_Key

class Schema__NaCl__Keys(Type_Safe):
    public_key : Safe_Str__NaCl__Public_Key  = None
    private_key: Safe_Str__NaCl__Private_Key = None