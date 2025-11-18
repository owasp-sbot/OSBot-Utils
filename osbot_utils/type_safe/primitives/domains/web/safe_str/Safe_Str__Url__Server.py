import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                 import Safe_Str
from osbot_utils.type_safe.primitives.core.enums.Enum__Safe_Str__Regex_Mode         import Enum__Safe_Str__Regex_Mode
from osbot_utils.type_safe.primitives.domains.network.safe_str.Safe_Str__IP_Address import Safe_Str__IP_Address
from osbot_utils.type_safe.primitives.domains.network.safe_uint.Safe_UInt__Port     import Safe_UInt__Port

TYPE_SAFE_STR__URL__SERVER__MAX_LENGTH = 270                                                # scheme (8) + domain (253) + port (6) + buffer

TYPE_SAFE_STR__URL__SERVER__REGEX = re.compile(
    r'^https?://'                                      # Scheme
    r'[a-zA-Z0-9.\-]+'                                 # Domain/IP (permissive)
    r'(:[0-9]{1,5})?$'                                 # Optional port
)


class Safe_Str__Url__Server(Safe_Str):
    regex             = TYPE_SAFE_STR__URL__SERVER__REGEX
    regex_mode        = Enum__Safe_Str__Regex_Mode.MATCH
    max_length        = TYPE_SAFE_STR__URL__SERVER__MAX_LENGTH
    trim_whitespace   = True
    strict_validation = True
    allow_empty       = True

    def __new__(cls, value=None):
        if value is None or value == '':
            return super().__new__(cls, value)                          # Allow empty if permitted

        instance = super().__new__(cls, value)                          # Perform basic regex validation
        cls._validate_server_components(str(instance))                 # Then validate host/port structure

        return instance

    @classmethod
    def _validate_server_components(cls, server_str):
        if not server_str or server_str == '':
            return

        if '://' in server_str:                                         # Remove scheme (e.g., http://)
            parts     = server_str.split('://', 1)
            host_port = parts[1]
        else:
            host_port = server_str

        if ':' in host_port:                                            # Split host:port
            host     , port_str = host_port.rsplit(':', 1)

            try:
                port = Safe_UInt__Port(int(port_str))                   # Validate port using Safe_UInt__Port
                if port == 0:
                    raise ValueError("Port 0 is not allowed (see Safe_UInt__Port.allow_none)")
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid port in server URL '{server_str}': {e}") from None
        else:
            host = host_port

        cls._validate_host(host, server_str)                            # Validate host (domain or IP)

    @classmethod
    def _validate_host(cls, host, original_server):
        """Validate host (domain or IP)"""
        # Try IP address first
        try:
            Safe_Str__IP_Address(host)
            return  # Valid IP
        except (ValueError, TypeError):
            pass  # Not a valid IP, try domain

        # Check if it looks like an IP but failed validation
        # (all numeric labels = IP-like)
        if cls._is_ip_like(host):
            raise ValueError(
                f"Invalid host in server URL '{original_server}': "
                f"'{host}' appears to be an invalid IP address"
            )

        # Try domain validation
        if not cls._is_valid_domain(host):
            raise ValueError(
                f"Invalid host in server URL '{original_server}': "
                f"'{host}' is neither a valid IP address nor domain name"
            )

    @classmethod
    def _is_ip_like(cls, host):
        """
        Check if host looks like an IP address (all numeric labels).
        This catches invalid IPs like 256.1.1.1, 1.1.1 (too few), or 1.1.1.1.1 (too many).
        """
        if not host:
            return False

        labels = host.split('.')

        if not labels:
            return False

        # All labels must be numeric for it to be IP-like
        for label in labels:
            if not label:
                return False
            if not label.isdigit():
                return False  # Contains non-numeric, so it's a domain

        return True  # All labels are numeric = looks like an IP attempt

    @classmethod
    def _is_valid_domain(cls, domain):
        """Validate domain name structure"""
        if not domain or len(domain) > 253:
            return False

        if domain == 'localhost':
            return True

        labels = domain.split('.')
        if not labels:
            return False

        for label in labels:
            if not label or len(label) > 63:
                return False
            if label.startswith('-') or label.endswith('-'):
                return False
            if not re.match(r'^[a-zA-Z0-9\-]+$', label):
                return False

        return True



    def __add__(self, other):
        from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url              import Safe_Str__Url
        from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Path        import Safe_Str__Url__Path
        from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Path_Query  import Safe_Str__Url__Path_Query

        if isinstance(other, Safe_Str__Url__Path):                        # Concatenate server + path
            server = str(self).rstrip('/')
            path   = str(other)
            if not path.startswith('/'):
                path = '/' + path
            result = f"{server}{path}"
            return Safe_Str__Url(result)

        elif isinstance(other, Safe_Str__Url__Path_Query):               # Concatenate server + path?query
            server     = str(self).rstrip('/')
            path_query = str(other)
            if not path_query.startswith('/'):
                path_query = '/' + path_query
            result = f"{server}{path_query}"
            return Safe_Str__Url(result)

        elif isinstance(other, str) and other.startswith('/'):          # Handle raw string path
            result = f"{self.rstrip('/')}{other}"
            return Safe_Str__Url(result)

        else:                                                            # Fallback to base string add
            return super().__add__(other)
