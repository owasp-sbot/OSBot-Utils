import re
from osbot_utils.type_safe.primitives.core.Safe_Str                         import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode

TYPE_SAFE_STR__URL__MAX_LENGTH = 8192   # Modern URL length limit (8192 characters)
                                        # - Old IE11 limit was 2,083 (obsolete as of 2022)
                                        # - Modern browsers support 64K+ characters
                                        # - Common server defaults: Apache (8K), Nginx (4-8K)
                                        # - CDN limits: Cloudflare (16K), AWS API Gateway (10K)
                                        # - Handles OAuth/SAML redirects (typically 3-6K)
                                        # - Handles marketing/analytics URLs (typically 2-4K)
                                        # - Still protects against abuse (8K+ is suspicious)

TYPE_SAFE_STR__URL__REGEX = re.compile(
    r'^https?://'                           # Scheme
    r'[a-zA-Z0-9.\-]+'                      # Domain/IP
    r'(:[0-9]{1,5})?'                       # Optional port
    r'(/[a-zA-Z0-9/\-._~%]*)?'              # Optional path
    r'(\?[a-zA-Z0-9=&\-._~%+]*)?'           # Optional query
    r'(#[a-zA-Z0-9\-._~%]*)?$'              # Optional fragment
)

class Safe_Str__Url(Safe_Str):
    """
    Safe string class for complete URLs.

    Examples:
    - "https://example.com"
    - "http://localhost:8080/api/users?page=1"
    - "https://api.example.com/v1/products/123?format=json"
    """
    regex                      = TYPE_SAFE_STR__URL__REGEX
    regex_mode                 = Enum__Safe_Str__Regex_Mode.MATCH
    max_length                 = TYPE_SAFE_STR__URL__MAX_LENGTH
    trim_whitespace            = True
    strict_validation          = True
    allow_empty                = True
    allow_all_replacement_char = False