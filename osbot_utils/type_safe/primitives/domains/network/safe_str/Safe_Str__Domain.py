import re
from osbot_utils.type_safe.primitives.core.Safe_Str                         import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode import Enum__Safe_Str__Regex_Mode

TYPE_SAFE_STR__DOMAIN__MAX_LENGTH = 253  # RFC 1035 max domain length
TYPE_SAFE_STR__DOMAIN__REGEX      = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$')

class Safe_Str__Domain(Safe_Str):
    """
    Safe string class for domain names (without scheme or port).

    Validates according to RFC 1035 and RFC 1123:
    - Each label max 63 characters
    - Total max 253 characters
    - Labels: alphanumeric + hyphens (not at start/end)
    - At least one dot (except 'localhost')

    Examples:
    - "example.com"
    - "api.example.com"
    - "sub.domain.example.com"
    - "localhost"
    - "my-site.co.uk"

    Not valid:
    - "https://example.com" (use Safe_Str__Url__Server)
    - "192.168.1.1" (use Safe_Str__IP_Address)
    - "example.com:8080" (use Safe_Str__Url__Server)
    """
    regex             = TYPE_SAFE_STR__DOMAIN__REGEX
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    max_length        = TYPE_SAFE_STR__DOMAIN__MAX_LENGTH
    trim_whitespace   = True
    strict_validation = True
    allow_empty       = True

    def __new__(cls, value=None):
        if value is None or value == '':
            return super().__new__(cls, value)

        # Basic regex validation via parent
        instance = super().__new__(cls, value)

        # Additional validation
        cls._validate_domain(str(instance))

        return instance

    @classmethod
    def _validate_domain(cls, domain):
        """Validate domain name structure"""
        if not domain or domain == '':
            return

        # Special case: localhost
        if domain == 'localhost':
            return

        # Must have at least one dot
        if '.' not in domain:
            raise ValueError(f"Invalid domain '{domain}': must contain at least one dot (or be 'localhost')")

        # Split and validate each label
        labels = domain.split('.')

        for label in labels:
            # Each label must be 1-63 characters
            if not label or len(label) > 63:
                raise ValueError(f"Invalid domain '{domain}': label '{label}' length must be 1-63 characters")

            # Cannot start or end with hyphen
            if label.startswith('-') or label.endswith('-'):
                raise ValueError(f"Invalid domain '{domain}': label '{label}' cannot start or end with hyphen")

            # Must be alphanumeric + hyphens
            if not re.match(r'^[a-zA-Z0-9\-]+$', label):
                raise ValueError(f"Invalid domain '{domain}': label '{label}' contains invalid characters")

    def __add__(self, other):
        """Enable composability with URL components"""
        from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Server import Safe_Str__Url__Server

        # Domain + "https://" prefix = Server
        if isinstance(other, str) and other.startswith('http'):
            return Safe_Str__Url__Server(f"{other}{self}")

        # Default string concatenation
        return str(self) + str(other)

    def __radd__(self, other):
        """Reverse addition: scheme + domain = server"""
        from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Server import Safe_Str__Url__Server

        if isinstance(other, str):
            if other in ('https://', 'http://'):
                return Safe_Str__Url__Server(f"{other}{self}")

        return str(other) + str(self)