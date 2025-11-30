"""
Telnet Client Module Tests

Tests for GMA2TelnetClient connection, login, command sending, and other functionality.
Uses mocks to simulate Telnet connections and avoid actual network calls.

使用 pytest-asyncio 進行非同步測試
"""

import asyncio

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch


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
    """Tests for GMA2TelnetClient connection functionality (async)."""

    @pytest.mark.asyncio
    @patch("src.telnet_client.telnetlib3.open_connection")
    async def test_connect_success(self, mock_open_connection):
        """Test successful connection establishment."""
        from src.telnet_client import GMA2TelnetClient

        # 配置 mock 行為 - 模擬 telnetlib3 的 reader/writer
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_open_connection.return_value = (mock_reader, mock_writer)

        client = GMA2TelnetClient(host="192.168.1.100")
        await client.connect()

        # 驗證 open_connection 被正確呼叫
        mock_open_connection.assert_called_once_with(
            host="192.168.1.100",
            port=30000,
        )
        assert client._connection is not None
        assert client._reader is mock_reader
        assert client._writer is mock_writer

    @pytest.mark.asyncio
    @patch("src.telnet_client.telnetlib3.open_connection")
    async def test_login_success(self, mock_open_connection):
        """Test successful login."""
        from src.telnet_client import GMA2TelnetClient

        # 配置 mock 行為
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        # 模擬非同步讀取
        mock_reader.read = AsyncMock(return_value="Login successful")
        mock_open_connection.return_value = (mock_reader, mock_writer)

        client = GMA2TelnetClient(host="192.168.1.100")
        await client.connect()
        result = await client.login()

        # 驗證登入指令被發送
        expected_cmd = 'login "administrator" "admin"\r\n'
        mock_writer.write.assert_called_with(expected_cmd)
        assert result is True

    @pytest.mark.asyncio
    @patch("src.telnet_client.telnetlib3.open_connection")
    async def test_send_command(self, mock_open_connection):
        """Test sending a command."""
        from src.telnet_client import GMA2TelnetClient

        # 配置 mock 行為
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_reader.read = AsyncMock(return_value="OK")
        mock_open_connection.return_value = (mock_reader, mock_writer)

        client = GMA2TelnetClient(host="192.168.1.100")
        await client.connect()
        await client.send_command("selfix fixture 1 thru 10")

        # 驗證指令被正確發送
        expected_cmd = "selfix fixture 1 thru 10\r\n"
        mock_writer.write.assert_called_with(expected_cmd)

    @pytest.mark.asyncio
    @patch("src.telnet_client.telnetlib3.open_connection")
    async def test_disconnect(self, mock_open_connection):
        """Test closing connection."""
        from src.telnet_client import GMA2TelnetClient

        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_open_connection.return_value = (mock_reader, mock_writer)

        client = GMA2TelnetClient(host="192.168.1.100")
        await client.connect()
        await client.disconnect()

        # 驗證連線已關閉
        mock_writer.close.assert_called_once()
        assert client._connection is None


class TestGMA2TelnetClientContextManager:
    """Tests for GMA2TelnetClient as an async context manager."""

    @pytest.mark.asyncio
    @patch("src.telnet_client.telnetlib3.open_connection")
    async def test_async_context_manager(self, mock_open_connection):
        """Test managing connection with async with statement."""
        from src.telnet_client import GMA2TelnetClient

        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_reader.read = AsyncMock(return_value="OK")
        mock_open_connection.return_value = (mock_reader, mock_writer)

        async with GMA2TelnetClient(host="192.168.1.100") as client:
            await client.send_command("test command")

        # 驗證離開 context 時連線已關閉
        mock_writer.close.assert_called_once()
