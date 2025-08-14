import pytest
from unittest                                                   import TestCase
from osbot_utils.type_safe.Type_Safe                            import Type_Safe
from osbot_utils.type_safe.primitives.safe_uint.Safe_UInt__Port import Safe_UInt__Port, TYPE_SAFE_UINT__PORT__MIN_VALUE, TYPE_SAFE_UINT__PORT__MAX_VALUE


class test_Safe_UInt__Port(TestCase):

    def test_Safe_UInt__Port_class(self):
        # Valid port numbers
        assert int(Safe_UInt__Port(0)) == 0      # Min port
        assert int(Safe_UInt__Port(80)) == 80     # HTTP
        assert int(Safe_UInt__Port(443)) == 443    # HTTPS
        assert int(Safe_UInt__Port(8080)) == 8080   # Common alternative
        assert int(Safe_UInt__Port(22)) == 22     # SSH
        assert int(Safe_UInt__Port(3306)) == 3306   # MySQL
        assert int(Safe_UInt__Port(5432)) == 5432   # PostgreSQL
        assert int(Safe_UInt__Port(65535)) == 65535  # Max port

        # String conversion
        assert int(Safe_UInt__Port('80')) == 80
        assert int(Safe_UInt__Port('443')) == 443
        assert int(Safe_UInt__Port('8080')) == 8080
        assert int(Safe_UInt__Port('65535')) == 65535

        # Out of range - too high
        with pytest.raises(ValueError, match="Safe_UInt__Port must be <= 65535, got 65536"):
            Safe_UInt__Port(65536)
        with pytest.raises(ValueError, match="Safe_UInt__Port must be <= 65535, got 70000"):
            Safe_UInt__Port(70000)
        with pytest.raises(ValueError, match="Safe_UInt__Port must be <= 65535, got 100000"):
            Safe_UInt__Port(100000)

        # Out of range - negative
        with pytest.raises(ValueError, match="Safe_UInt__Port must be >= 0, got -1"):
            Safe_UInt__Port(-1)
        with pytest.raises(ValueError, match="Safe_UInt__Port must be >= 0, got -80"):
            Safe_UInt__Port(-80)

        # Invalid types
        with pytest.raises(TypeError, match="Safe_UInt__Port requires an integer value, got float"):
            Safe_UInt__Port(80.5)
        with pytest.raises(ValueError, match="Cannot convert 'http' to integer"):
            Safe_UInt__Port('http')
        with pytest.raises(TypeError, match="Safe_UInt__Port does not allow boolean values"):
            Safe_UInt__Port(True)

        # None not allowed
        with pytest.raises(ValueError, match="Safe_UInt__Port does not allow None values"):
            Safe_UInt__Port(None)

    def test_common_port_numbers(self):
        """Test common well-known port numbers."""
        # System ports (0-1023)
        assert int(Safe_UInt__Port(20)) == 20    # FTP data
        assert int(Safe_UInt__Port(21)) == 21    # FTP control
        assert int(Safe_UInt__Port(22)) == 22    # SSH
        assert int(Safe_UInt__Port(23)) == 23    # Telnet
        assert int(Safe_UInt__Port(25)) == 25    # SMTP
        assert int(Safe_UInt__Port(53)) == 53    # DNS
        assert int(Safe_UInt__Port(80)) == 80    # HTTP
        assert int(Safe_UInt__Port(110)) == 110   # POP3
        assert int(Safe_UInt__Port(143)) == 143   # IMAP
        assert int(Safe_UInt__Port(443)) == 443   # HTTPS
        assert int(Safe_UInt__Port(445)) == 445   # SMB
        assert int(Safe_UInt__Port(587)) == 587   # SMTP (submission)

        # Registered ports (1024-49151)
        assert int(Safe_UInt__Port(1433)) == 1433  # MS SQL Server
        assert int(Safe_UInt__Port(3000)) == 3000  # Dev server
        assert int(Safe_UInt__Port(3306)) == 3306  # MySQL
        assert int(Safe_UInt__Port(5432)) == 5432  # PostgreSQL
        assert int(Safe_UInt__Port(5672)) == 5672  # RabbitMQ
        assert int(Safe_UInt__Port(6379)) == 6379  # Redis
        assert int(Safe_UInt__Port(8080)) == 8080  # HTTP alternate
        assert int(Safe_UInt__Port(8443)) == 8443  # HTTPS alternate
        assert int(Safe_UInt__Port(9200)) == 9200  # Elasticsearch
        assert int(Safe_UInt__Port(27017)) == 27017 # MongoDB

        # Dynamic/private ports (49152-65535)
        assert int(Safe_UInt__Port(50000)) == 50000
        assert int(Safe_UInt__Port(60000)) == 60000

    def test_usage_in_Type_Safe(self):
        class Server_Config(Type_Safe):
            http_port  : Safe_UInt__Port = Safe_UInt__Port(80)
            https_port : Safe_UInt__Port = Safe_UInt__Port(443)
            ssh_port   : Safe_UInt__Port = Safe_UInt__Port(22)
            custom_port: Safe_UInt__Port = None

        config = Server_Config(custom_port=Safe_UInt__Port(8080))
        assert int(config.http_port) == 80
        assert int(config.https_port) == 443
        assert int(config.ssh_port) == 22
        assert int(config.custom_port) == 8080

        # Update port
        config.custom_port = Safe_UInt__Port(9000)
        assert int(config.custom_port) == 9000

        # Invalid port
        with pytest.raises(ValueError, match="Safe_UInt__Port must be <= 65535, got 70000"):
            config.custom_port = Safe_UInt__Port(70000)

        # Serialization
        config_json = config.json()
        assert config_json == {
            'http_port': 80,
            'https_port': 443,
            'ssh_port': 22,
            'custom_port': 9000
        }

        config_restored = Server_Config.from_json(config_json)
        assert type(config_restored.http_port) is Safe_UInt__Port
        assert int(config_restored.custom_port) == 9000

    def test_arithmetic_operations(self):
        port1 = Safe_UInt__Port(8080)
        port2 = Safe_UInt__Port(100)

        # Addition that stays in range
        result = port1 + port2
        assert type(result) is Safe_UInt__Port
        assert int(result) == 8180

        # Addition that exceeds range
        port3 = Safe_UInt__Port(65000)
        port4 = Safe_UInt__Port(1000)
        result = port3 + port4  # 66000 > 65535
        assert type(result) is int  # Falls back to regular int
        assert result == 66000

        # Subtraction
        result = port1 - port2
        assert type(result) is Safe_UInt__Port
        assert int(result) == 7980

    def test_boundary_values(self):
        # Minimum boundary
        assert int(Safe_UInt__Port(TYPE_SAFE_UINT__PORT__MIN_VALUE)) == 0

        # Maximum boundary
        assert int(Safe_UInt__Port(TYPE_SAFE_UINT__PORT__MAX_VALUE)) == 65535

        # Just outside boundaries
        with pytest.raises(ValueError):
            Safe_UInt__Port(TYPE_SAFE_UINT__PORT__MIN_VALUE - 1)
        with pytest.raises(ValueError):
            Safe_UInt__Port(TYPE_SAFE_UINT__PORT__MAX_VALUE + 1)

    def test__safe_int__constrained_types(self):
        # Port number (0-65535)
        port = Safe_UInt__Port(8080)

        result = port + 100
        assert type(result) is Safe_UInt__Port
        assert result == 8180

        # Should fall back to regular int when exceeding constraints
        result = port + 60000  # Would exceed 65535
        assert type(result) is int  # Falls back to int
        assert result == 68080

    def test__safe_int_port__string_representation(self):
        # Port number
        port = Safe_UInt__Port(8080)
        assert str(port) == "8080"
        assert f"localhost:{port}" == "localhost:8080"
        assert repr(port) == "Safe_UInt__Port(8080)"

        # Well-known port
        http = Safe_UInt__Port(80)
        assert str(http) == "80"
        assert f"http://example.com:{http}" == "http://example.com:80"