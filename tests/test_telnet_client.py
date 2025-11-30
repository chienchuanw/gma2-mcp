"""
Telnet Client Module Tests

Tests for GMA2TelnetClient connection, login, command sending, and other functionality.
Uses mocks to simulate Telnet connections and avoid actual network calls.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestGMA2TelnetClientInit:
    """Tests for GMA2TelnetClient initialization."""

    def test_client_init_with_default_values(self):
        """Test initializing client with default values."""
        from src.telnet_client import GMA2TelnetClient

        client = GMA2TelnetClient(host="192.168.1.100")

        assert client.host == "192.168.1.100"
        assert client.port == 30000  # default port
        assert client.user == "administrator"  # default user
        assert client.password == "admin"  # default password
        assert client._connection is None

    def test_client_init_with_custom_values(self):
        """Test initializing client with custom values."""
        from src.telnet_client import GMA2TelnetClient

        client = GMA2TelnetClient(
            host="10.0.0.1", port=30001, user="custom_user", password="custom_pass"
        )

        assert client.host == "10.0.0.1"
        assert client.port == 30001
        assert client.user == "custom_user"
        assert client.password == "custom_pass"


class TestGMA2TelnetClientConnection:
    """Tests for GMA2TelnetClient connection functionality."""

    @patch("src.telnet_client.telnetlib.Telnet")
    def test_connect_success(self, mock_telnet_class):
        """Test successful connection establishment."""
        from src.telnet_client import GMA2TelnetClient

        # Configure mock behavior
        mock_connection = MagicMock()
        mock_telnet_class.return_value = mock_connection

        client = GMA2TelnetClient(host="192.168.1.100")
        client.connect()

        # Verify Telnet was called correctly
        mock_telnet_class.assert_called_once_with("192.168.1.100", 30000)
        assert client._connection is not None

    @patch("src.telnet_client.telnetlib.Telnet")
    def test_login_success(self, mock_telnet_class):
        """Test successful login."""
        from src.telnet_client import GMA2TelnetClient

        # Configure mock behavior
        mock_connection = MagicMock()
        mock_connection.read_very_eager.return_value = b"Login successful"
        mock_telnet_class.return_value = mock_connection

        client = GMA2TelnetClient(host="192.168.1.100")
        client.connect()
        result = client.login()

        # Verify login command was sent
        expected_cmd = 'login "administrator" "admin"\r\n'
        mock_connection.write.assert_called_with(expected_cmd.encode("utf-8"))
        assert result is True

    @patch("src.telnet_client.telnetlib.Telnet")
    def test_send_command(self, mock_telnet_class):
        """Test sending a command."""
        from src.telnet_client import GMA2TelnetClient

        # Configure mock behavior
        mock_connection = MagicMock()
        mock_telnet_class.return_value = mock_connection

        client = GMA2TelnetClient(host="192.168.1.100")
        client.connect()
        client.send_command("selfix fixture 1 thru 10")

        # Verify command was sent correctly
        expected_cmd = "selfix fixture 1 thru 10\r\n"
        mock_connection.write.assert_called_with(expected_cmd.encode("utf-8"))

    @patch("src.telnet_client.telnetlib.Telnet")
    def test_disconnect(self, mock_telnet_class):
        """Test closing connection."""
        from src.telnet_client import GMA2TelnetClient

        mock_connection = MagicMock()
        mock_telnet_class.return_value = mock_connection

        client = GMA2TelnetClient(host="192.168.1.100")
        client.connect()
        client.disconnect()

        # Verify connection was closed
        mock_connection.close.assert_called_once()
        assert client._connection is None


class TestGMA2TelnetClientContextManager:
    """Tests for GMA2TelnetClient as a context manager."""

    @patch("src.telnet_client.telnetlib.Telnet")
    def test_context_manager(self, mock_telnet_class):
        """Test managing connection with with statement."""
        from src.telnet_client import GMA2TelnetClient

        mock_connection = MagicMock()
        mock_connection.read_very_eager.return_value = b"OK"
        mock_telnet_class.return_value = mock_connection

        with GMA2TelnetClient(host="192.168.1.100") as client:
            client.send_command("test command")

        # Verify connection was closed when exiting context
        mock_connection.close.assert_called_once()
