import pytest
from unittest                                                                   import TestCase
from osbot_utils.type_safe.primitives.safe_str.Safe_Str                         import Safe_Str
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive                                 import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.safe_str.filesystem.Safe_Str__File__Name  import Safe_Str__File__Name
from osbot_utils.type_safe.primitives.safe_str.text.Safe_Str__Text              import Safe_Str__Text
from osbot_utils.type_safe.primitives.safe_str.web.Safe_Str__IP_Address         import Safe_Str__IP_Address
from osbot_utils.utils.Objects                                                  import __, base_types



class test_Safe_Str__IP_Address(TestCase):

    def test_Safe_Str__IP_Address_class(self):
        # Valid IPv4 addresses
        assert str(Safe_Str__IP_Address('192.168.1.1'    )) == '192.168.1.1'
        assert str(Safe_Str__IP_Address('10.0.0.1'       )) == '10.0.0.1'
        assert str(Safe_Str__IP_Address('172.16.254.1'   )) == '172.16.254.1'
        assert str(Safe_Str__IP_Address('255.255.255.255')) == '255.255.255.255'
        assert str(Safe_Str__IP_Address('0.0.0.0'        )) == '0.0.0.0'
        assert str(Safe_Str__IP_Address('127.0.0.1'      )) == '127.0.0.1'
        assert str(Safe_Str__IP_Address('1.1.1.1'        )) == '1.1.1.1'
        assert str(Safe_Str__IP_Address('8.8.8.8'        )) == '8.8.8.8'

        # Valid IPv6 addresses
        assert str(Safe_Str__IP_Address('::1'                                    )) == '::1'
        assert str(Safe_Str__IP_Address('::'                                     )) == '::'
        assert str(Safe_Str__IP_Address('2001:db8::1'                            )) == '2001:db8::1'
        assert str(Safe_Str__IP_Address('fe80::1'                                )) == 'fe80::1'
        assert str(Safe_Str__IP_Address('2001:0db8:0000:0000:0000:0000:0000:0001')) == '2001:db8::1'                    # Canonical form
        assert str(Safe_Str__IP_Address('2001:db8:85a3::8a2e:370:7334'           )) == '2001:db8:85a3::8a2e:370:7334'
        assert str(Safe_Str__IP_Address('::ffff:192.0.2.1'                       )) != '::ffff:192.0.2.1'               # although this is sometimes used (in logs) this is not correct since ::ffff:192.0.2.1 is neither an IPV4 or IPV6 address
        assert str(Safe_Str__IP_Address('::ffff:192.0.2.1'                       )) == '::ffff:c000:201'                # this is the correct canonical representation in IPV6 of ::ffff:192.0.2.1

        # Spaces trimming
        assert str(Safe_Str__IP_Address('  192.168.1.1  '          )) == '192.168.1.1'
        assert str(Safe_Str__IP_Address('  2001:db8::1  '          )) == '2001:db8::1'
        assert str(Safe_Str__IP_Address('\t10.0.0.1\n'             )) == '10.0.0.1'

        # Empty values allowed
        assert Safe_Str__IP_Address(None) == ''
        assert Safe_Str__IP_Address('')   == ''
        assert Safe_Str__IP_Address('  ') == ''  # After trimming

        # Invalid IP addresses - IPv4
        with pytest.raises(ValueError, match="Invalid IP address: 256.1.1.1"):
            Safe_Str__IP_Address('256.1.1.1')  # Octet out of range

        with pytest.raises(ValueError, match="Invalid IP address: 192.168.1"):
            Safe_Str__IP_Address('192.168.1')  # Missing octet

        with pytest.raises(ValueError, match="Invalid IP address: 192.168.1.1.1"):
            Safe_Str__IP_Address('192.168.1.1.1')  # Too many octets

        with pytest.raises(ValueError, match="Invalid IP address: 192.168.-1.1"):
            Safe_Str__IP_Address('192.168.-1.1')  # Negative octet

        with pytest.raises(ValueError, match="Invalid IP address: 192.168.a.1"):
            Safe_Str__IP_Address('192.168.a.1')  # Non-numeric octet

        # Invalid IP addresses - IPv6
        with pytest.raises(ValueError, match="Invalid IP address: ::g"):
            Safe_Str__IP_Address('::g')  # Invalid hex character

        with pytest.raises(ValueError, match="Invalid IP address: 2001:db8:::1"):
            Safe_Str__IP_Address('2001:db8:::1')  # Too many colons

        with pytest.raises(ValueError, match="Invalid IP address: 2001:db8::1::2"):
            Safe_Str__IP_Address('2001:db8::1::2')  # Multiple ::

        # Invalid IP addresses - General
        with pytest.raises(ValueError, match="Invalid IP address: not-an-ip"):
            Safe_Str__IP_Address('not-an-ip')

        with pytest.raises(ValueError, match="Invalid IP address: example.com"):
            Safe_Str__IP_Address('example.com')  # Domain name, not IP

        with pytest.raises(ValueError, match="Invalid IP address: 192.168.1.1/24"):
            Safe_Str__IP_Address('192.168.1.1/24')  # CIDR notation not allowed

        # Type errors
        with pytest.raises(TypeError, match="Value provided must be a string, and it was <class 'int'>"):
            Safe_Str__IP_Address(192168001001)  # Integer not allowed

        with pytest.raises(TypeError, match="Value provided must be a string, and it was <class 'float'>"):
            Safe_Str__IP_Address(192.168)  # Float not allowed

        with pytest.raises(TypeError, match="Value provided must be a string, and it was <class 'list'>"):
            Safe_Str__IP_Address(['192', '168', '1', '1'])  # List not allowed

    def test_ipv6_canonicalization(self):                                       # Test that IPv6 addresses are canonicalized.
        # Zero compression
        assert str(Safe_Str__IP_Address('2001:0db8:0000:0000:0000:0000:0000:0001' )) == '2001:db8::1'
        assert str(Safe_Str__IP_Address('2001:db8:0:0:0:0:0:1'                    )) == '2001:db8::1'
        assert str(Safe_Str__IP_Address('0000:0000:0000:0000:0000:0000:0000:0001' )) == '::1'

        # Lowercase
        assert str(Safe_Str__IP_Address('2001:DB8::1'       )) == '2001:db8::1'
        assert str(Safe_Str__IP_Address('FE80::1'           )) == 'fe80::1'
        assert str(Safe_Str__IP_Address('::FFFF:192.0.2.1'  )) == '::ffff:c000:201'

        # Leading zeros removed
        assert str(Safe_Str__IP_Address('2001:0db8::0001'   )) == '2001:db8::1'

    def test_inheritance(self):                                                 # Test class inheritance chain.
        ip_addr = Safe_Str__IP_Address('192.168.1.1')
        assert isinstance(ip_addr, Safe_Str__IP_Address)
        assert isinstance(ip_addr, Type_Safe__Primitive)
        assert isinstance(ip_addr, str)
        assert base_types(ip_addr) == [Type_Safe__Primitive, str, object, object]

    def test_usage_in_Type_Safe(self):                                          # Test usage within Type_Safe classes."""
        class Server_Config(Type_Safe):
            server_ip: Safe_Str__IP_Address = Safe_Str__IP_Address('127.0.0.1')
            gateway_ip: Safe_Str__IP_Address

        # Test instantiation with default
        config = Server_Config()
        assert str(config.server_ip  ) == '127.0.0.1'
        assert str(config.gateway_ip ) == ''
        assert type(config.server_ip ) is Safe_Str__IP_Address
        assert type(config.gateway_ip) is Safe_Str__IP_Address

        # Test updating with valid value
        config.server_ip  = Safe_Str__IP_Address('192.168.1.100')
        config.gateway_ip = Safe_Str__IP_Address('192.168.1.1')
        assert str(config.server_ip ) == '192.168.1.100'
        assert str(config.gateway_ip) == '192.168.1.1'

        # Test obj() method
        assert config.obj() == __(server_ip  = Safe_Str__IP_Address('192.168.1.100'),
                                  gateway_ip = Safe_Str__IP_Address('192.168.1.1'  ))
        assert config.obj() == __(server_ip  = '192.168.1.100',
                                  gateway_ip = '192.168.1.1' )

        # Test serialization
        config_json = config.json()
        assert config_json == { 'server_ip': '192.168.1.100',
                               'gateway_ip': '192.168.1.1'}
        assert type(config_json.get('server_ip')) is str

        # Round trip test
        config_round_trip = Server_Config.from_json(config_json)
        assert config_round_trip.obj()            == config.obj()
        assert type(config_round_trip.server_ip ) is Safe_Str__IP_Address
        assert type(config_round_trip.gateway_ip) is Safe_Str__IP_Address

    def test_ipv4_edge_cases(self):                                                 # Test IPv4 edge cases.
        # Boundary values
        assert str(Safe_Str__IP_Address('0.0.0.0'        )) == '0.0.0.0'
        assert str(Safe_Str__IP_Address('255.255.255.255')) == '255.255.255.255'

        # Common private ranges
        assert str(Safe_Str__IP_Address('10.0.0.0'       )) == '10.0.0.0'
        assert str(Safe_Str__IP_Address('172.16.0.0'     )) == '172.16.0.0'
        assert str(Safe_Str__IP_Address('192.168.0.0'    )) == '192.168.0.0'

        # Loopback
        assert str(Safe_Str__IP_Address('127.0.0.1'      )) == '127.0.0.1'
        assert str(Safe_Str__IP_Address('127.255.255.255')) == '127.255.255.255'

    def test_ipv6_edge_cases(self):                                                 # Test IPv6 edge cases."""
        # All zeros
        assert str(Safe_Str__IP_Address('::'                )) == '::'
        assert str(Safe_Str__IP_Address('0:0:0:0:0:0:0:0'   )) == '::'

        # Loopback
        assert str(Safe_Str__IP_Address('::1'               )) == '::1'
        assert str(Safe_Str__IP_Address('0:0:0:0:0:0:0:1'   )) == '::1'

        # IPv4-mapped IPv6
        assert str(Safe_Str__IP_Address('::ffff:192.0.2.1'  )) == '::ffff:c000:201'
        assert str(Safe_Str__IP_Address('::ffff:0:192.0.2.1')) == '::ffff:0:c000:201'  # Different representation

        # Link-local
        assert str(Safe_Str__IP_Address('fe80::'            )) == 'fe80::'
        assert str(Safe_Str__IP_Address('fe80::1'           )) == 'fe80::1'

    def test__safe_str_ip_address__string_representation(self):                         # Test string representation methods."""
        # IPv4
        ipv4 = Safe_Str__IP_Address("192.168.1.1")
        assert str(ipv4)            == "192.168.1.1"
        assert f"Server IP: {ipv4}" == "Server IP: 192.168.1.1"
        assert repr(ipv4)           == "Safe_Str__IP_Address('192.168.1.1')"

        # IPv6
        ipv6 = Safe_Str__IP_Address("2001:db8::1")
        assert str(ipv6)            == "2001:db8::1"
        assert f"Server IP: {ipv6}" == "Server IP: 2001:db8::1"
        assert repr(ipv6)           == "Safe_Str__IP_Address('2001:db8::1')"

        # Empty
        empty = Safe_Str__IP_Address("")
        assert str(empty)           == ""
        assert f"IP: [{empty}]"     == "IP: []"
        assert repr(empty)          == "Safe_Str__IP_Address('')"

    def test__str_concat_not_supported(self):                                           # Test that string concatenation returns regular str, not Safe_Str__IP_Address."""
        ip1 = Safe_Str__IP_Address('192.168.1.1')

        # Concatenation should return regular str
        result = ip1 + ':8080'
        assert type(result) is str                                                      # Not Safe_Str__IP_Address
        assert result       == '192.168.1.1:8080'

        # Same with other operations
        result2 = ip1 + '/24'
        assert type(result2) is str
        assert result2       == '192.168.1.1/24'

    def test_security_patterns(self):                                                   # Test potentially malicious patterns."""
        # These should all fail validation
        malicious_patterns = [
            '192.168.1.1; rm -rf /',
            '192.168.1.1 && whoami',
            '$(whoami)',
            '`id`',
            '192.168.1.1\nmalicious-command',
            '192.168.1.1\x00null-byte',
            '<script>alert(1)</script>',
            'javascript:alert(1)',
            '192.168.1.1%0aSet-Cookie:test=1',
        ]

        for pattern in malicious_patterns:
            with pytest.raises(ValueError) as exc_info:
                Safe_Str__IP_Address(pattern)
            assert "Invalid IP address:" in str(exc_info.value)

    def test_type_safety_enforcement(self):                                             # Test that type safety is enforced.
        # Only strings should be accepted
        with pytest.raises(TypeError):
            Safe_Str__IP_Address(3232235521)  # Integer representation of 192.168.1.1

        with pytest.raises(TypeError):
            Safe_Str__IP_Address(b'192.168.1.1')  # Bytes

        with pytest.raises(TypeError):
            Safe_Str__IP_Address({'ip': '192.168.1.1'})  # Dict


    def test__ip_address_concat_with_regular_str(self):                                 # Test IP address concatenation with regular strings
        ip = Safe_Str__IP_Address('192.168.1.1')

        # IP + str → str
        result = ip + ':8080'
        assert type(result) is str
        assert result == '192.168.1.1:8080'

        result = ip + '/24'
        assert type(result) is str
        assert result == '192.168.1.1/24'

        result = ip + ' (primary)'
        assert type(result) is str
        assert result == '192.168.1.1 (primary)'

        # str + IP → str
        result = 'http://' + ip
        assert type(result) is str
        assert result == 'http://192.168.1.1'

        result = 'Server: ' + ip
        assert type(result) is str
        assert result == 'Server: 192.168.1.1'

    def test__ip_address_concat_with_safe_str_types(self):                              # Test IP address concatenation with other Safe_Str types.
        ip = Safe_Str__IP_Address('192.168.1.1')

        # IP + Safe_Str → str
        safe_str = Safe_Str('_server')
        result = ip + safe_str
        assert type(result) is str
        assert result       == '192.168.1.1_server'

        # Safe_Str + IP → Safe_Str (left operand wins)
        result = safe_str + ip
        assert type(result) is Safe_Str
        assert result       == '_server192_168_1_1'

        # IP + Safe_Str__Text → str
        text = Safe_Str__Text(' - production')
        result = ip + text
        assert type(result) is str
        assert result       == '192.168.1.1 - production'

        # Safe_Str__Text + IP → Safe_Str__Text (left operand wins)
        result = text + ip
        assert type(result) is Safe_Str__Text
        assert result       == ' - production192.168.1.1'

        # IP + Safe_Str__File__Name → str
        filename = Safe_Str__File__Name('_config.json')
        result = ip + filename
        assert type(result) is str
        assert result       == '192.168.1.1_config.json'

        # Safe_Str__File__Name + IP → Safe_Str__File__Name (left operand wins)
        result = filename + ip
        assert type(result) is Safe_Str__File__Name
        assert result       == '_config.json192.168.1.1'

    def test__ip_address_concat_with_another_ip(self):      # Test IP address concatenation with another IP address.
        ip1 = Safe_Str__IP_Address('192.168.1.1')
        ip2 = Safe_Str__IP_Address('10.0.0.1'   )

        # IP + IP → str
        result = ip1 + ip2
        assert type(result) is str
        assert result == '192.168.1.110.0.0.1'

        result = ip2 + ip1
        assert type(result) is str
        assert result == '10.0.0.1192.168.1.1'

        # With separator
        result = ip1 + ',' + ip2
        assert type(result) is str
        assert result == '192.168.1.1,10.0.0.1'

    def test__ipv6_address_concatenation(self):             # est IPv6 address concatenation.
        ipv6 = Safe_Str__IP_Address('2001:db8::1')

        # IPv6 + str → str
        result = ipv6 + '/64'
        assert type(result) is str
        assert result == '2001:db8::1/64'

        result = ipv6 + ':8080'
        assert type(result) is str
        assert result == '2001:db8::1:8080'

        # Note: This creates an ambiguous IPv6 representation!
        # In practice, IPv6 with port should be [2001:db8::1]:8080
        result = '[' + ipv6 + ']:8080'
        assert type(result) is str
        assert result == '[2001:db8::1]:8080'

    def test__complex_concatenation_chains(self):           # Test more complex concatenation scenarios
        ip = Safe_Str__IP_Address('192.168.1.1')
        text = Safe_Str__Text('server')
        port = ':8080'

        # Chain of concatenations
        result = 'http://' + ip + port + '/api'
        assert type(result) is str
        assert result == 'http://192.168.1.1:8080/api'

        # Mixed types in chain
        result = text + '_' + ip + port
        assert type(result) is Safe_Str__Text               # since text is Safe_Str__Text, it picks up the final value
        assert result == 'server_192.168.1.1:8080'

    def test__empty_ip_concatenation(self):                 #  Test concatenation with empty IP addresses."""
        empty_ip = Safe_Str__IP_Address('')

        # Empty IP + str → str
        result = empty_ip + ':8080'
        assert type(result) is str
        assert result == ':8080'

        # str + Empty IP → str
        result = 'Server: ' + empty_ip
        assert type(result) is str
        assert result == 'Server: '

    def test__concatenation_preserves_canonicalization(self):   # Test that canonicalized forms are preserved in concatenation
        # IPv6 with canonical form
        ipv6 = Safe_Str__IP_Address('2001:0db8:0000:0000:0000:0000:0000:0001')
        assert str(ipv6) == '2001:db8::1'                       # Canonicalized

        result = ipv6 + '/64'
        assert type(result) is str
        assert result       == '2001:db8::1/64'                 # Uses canonical form

        # IPv4-mapped IPv6
        ipv6_mapped = Safe_Str__IP_Address('::ffff:192.0.2.1')
        assert str(ipv6_mapped) == '::ffff:c000:201'            # Canonical hex form

        result = ipv6_mapped + ':80'
        assert type(result) is str
        assert result == '::ffff:c000:201:80'                   # Uses canonical form

    def test__url_building_scenario(self):                      # Test a realistic URL building scenario.
        ip       = Safe_Str__IP_Address('192.168.1.100')
        protocol = 'https://'
        port     = ':443'
        path     = '/admin/login'

        # Building a URL
        url = protocol + ip + port + path
        assert type(url) is str
        assert url       == 'https://192.168.1.100:443/admin/login'

        # Can't create Safe_Str__Url from concatenation with IP
        # because the result is just str
        result_type = type(ip + port)
        assert result_type is str, f"Expected str but got {result_type}"

    def test__asymmetric_behavior_documentation(self):          # Document the asymmetric behavior of concatenation.
        ip       = Safe_Str__IP_Address('10.0.0.1')
        text     = Safe_Str__Text      ('_server' )
        filename = Safe_Str__File__Name('config_' )

        # Left operand determines behavior
        assert type(ip + text) is str                           # IP on left → str
        assert type(text + ip) is Safe_Str__Text                # Text on left → Safe_Str__Text

        assert type(ip + filename) is str                       # IP on left → str
        assert type(filename + ip) is Safe_Str__File__Name      # Filename on left → Safe_Str__File__Name

        # This asymmetry is intentional:
        # - IP addresses downgrade to str when concatenated (they're no longer valid IPs)
        # - Other Safe_Str types preserve their type (they can still be valid after concat)