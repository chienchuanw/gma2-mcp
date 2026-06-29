"""
Telnet Client Module Tests

Tests for GMA2TelnetClient connection, login, command sending, and other functionality.
Uses mocks to simulate Telnet connections and avoid actual network calls.

Uses pytest-asyncio for async testing.
"""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


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

        # Configure mock behavior - simulate telnetlib3 reader/writer
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_open_connection.return_value = (mock_reader, mock_writer)

        client = GMA2TelnetClient(host="192.168.1.100")
        await client.connect()

        # Verify open_connection was called correctly
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

        # Configure mock behavior
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        # Simulate async read
        mock_reader.read = AsyncMock(return_value="Login successful")
        mock_open_connection.return_value = (mock_reader, mock_writer)

        client = GMA2TelnetClient(host="192.168.1.100")
        await client.connect()
        result = await client.login()

        # Verify login command was sent
        expected_cmd = 'login "administrator" "admin"\r\n'
        mock_writer.write.assert_called_with(expected_cmd)
        assert result is True

    @pytest.mark.asyncio
    @patch("src.telnet_client.telnetlib3.open_connection")
    async def test_send_command(self, mock_open_connection):
        """Test sending a command."""
        from src.telnet_client import GMA2TelnetClient

        # Configure mock behavior
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_reader.read = AsyncMock(return_value="OK")
        mock_open_connection.return_value = (mock_reader, mock_writer)

        client = GMA2TelnetClient(host="192.168.1.100")
        await client.connect()
        await client.send_command("selfix fixture 1 thru 10")

        # Verify command was sent correctly
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

        # Verify connection was closed
        mock_writer.close.assert_called_once()
        assert client._connection is None


class TestGMA2TelnetClientCommandLock:
    """Tests for asyncio.Lock command serialization in GMA2TelnetClient."""

    def _setup_client_skip_health_check(self, client):
        """Set last successful command time to skip health check in _ensure_connected."""
        import time

        client._last_successful_command_time = time.monotonic()

    @pytest.mark.asyncio
    @patch("src.telnet_client.telnetlib3.open_connection")
    async def test_concurrent_send_command_serialized(self, mock_open_connection):
        """Test that concurrent send_command() calls are serialized via lock."""
        from src.telnet_client import GMA2TelnetClient

        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_open_connection.return_value = (mock_reader, mock_writer)

        client = GMA2TelnetClient(host="192.168.1.100")
        await client.connect()
        self._setup_client_skip_health_check(client)

        # Track the order of command execution
        execution_order = []

        original_write = mock_writer.write

        def tracking_write(cmd):
            execution_order.append(cmd.strip())
            return original_write(cmd)

        mock_writer.write = tracking_write

        # Send two commands concurrently
        await asyncio.gather(
            client.send_command("command1", delay=0.01),
            client.send_command("command2", delay=0.01),
        )

        # Both commands should have been sent (serialized, not interleaved)
        assert len(execution_order) == 2
        assert "command1" in execution_order
        assert "command2" in execution_order

    @pytest.mark.asyncio
    @patch("src.telnet_client.telnetlib3.open_connection")
    async def test_concurrent_send_command_with_response_serialized(self, mock_open_connection):
        """Test that concurrent send_command_with_response() calls are serialized."""
        from src.telnet_client import GMA2TelnetClient

        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_reader.read = AsyncMock(side_effect=asyncio.TimeoutError)
        mock_open_connection.return_value = (mock_reader, mock_writer)

        client = GMA2TelnetClient(host="192.168.1.100")
        await client.connect()
        self._setup_client_skip_health_check(client)

        execution_order = []
        original_write = mock_writer.write

        def tracking_write(cmd):
            execution_order.append(cmd.strip())
            return original_write(cmd)

        mock_writer.write = tracking_write

        await asyncio.gather(
            client.send_command_with_response("cmd1", timeout=0.1, delay=0.01),
            client.send_command_with_response("cmd2", timeout=0.1, delay=0.01),
        )

        assert len(execution_order) == 2
        assert "cmd1" in execution_order
        assert "cmd2" in execution_order

    @pytest.mark.asyncio
    @patch("src.telnet_client.telnetlib3.open_connection")
    async def test_mixed_concurrent_calls_serialized(self, mock_open_connection):
        """Test mixed concurrent send_command + send_command_with_response are serialized."""
        from src.telnet_client import GMA2TelnetClient

        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_reader.read = AsyncMock(side_effect=asyncio.TimeoutError)
        mock_open_connection.return_value = (mock_reader, mock_writer)

        client = GMA2TelnetClient(host="192.168.1.100")
        await client.connect()
        self._setup_client_skip_health_check(client)

        execution_order = []
        original_write = mock_writer.write

        def tracking_write(cmd):
            execution_order.append(cmd.strip())
            return original_write(cmd)

        mock_writer.write = tracking_write

        await asyncio.gather(
            client.send_command("fire_cmd", delay=0.01),
            client.send_command_with_response("resp_cmd", timeout=0.1, delay=0.01),
        )

        assert len(execution_order) == 2
        assert "fire_cmd" in execution_order
        assert "resp_cmd" in execution_order

    @pytest.mark.asyncio
    @patch("src.telnet_client.telnetlib3.open_connection")
    async def test_lock_no_deadlock_single_call(self, mock_open_connection):
        """Test that single-client usage works normally with the lock (no deadlock)."""
        from src.telnet_client import GMA2TelnetClient

        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_open_connection.return_value = (mock_reader, mock_writer)

        client = GMA2TelnetClient(host="192.168.1.100")
        await client.connect()
        self._setup_client_skip_health_check(client)

        # Should complete without deadlock
        await client.send_command("test", delay=0.01)

        mock_writer.write.assert_called_with("test\r\n")

    @pytest.mark.asyncio
    @patch("src.telnet_client.telnetlib3.open_connection")
    async def test_lock_exists_on_client(self, mock_open_connection):
        """Test that the client has an asyncio.Lock attribute."""
        from src.telnet_client import GMA2TelnetClient

        client = GMA2TelnetClient(host="192.168.1.100")
        assert hasattr(client, "_lock")
        assert isinstance(client._lock, asyncio.Lock)


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

        # Verify connection was closed when exiting context
        mock_writer.close.assert_called_once()


class TestExecute:
    """Tests for the verified execute() path."""

    @pytest.mark.asyncio
    async def test_execute_success_returns_ok_result(self):
        from src.execution import ExecutionResult
        from src.telnet_client import GMA2TelnetClient

        client = GMA2TelnetClient(host="192.168.1.100")
        client.send_command_with_response = AsyncMock(
            return_value="Executing : \x1b[32mClear\x1b[37m\n\r [Fixture]>\x1b[K"
        )

        result = await client.execute("Clear")

        assert isinstance(result, ExecutionResult)
        assert result.ok is True
        assert result.error_code is None
        client.send_command_with_response.assert_awaited_once_with("Clear")

    @pytest.mark.asyncio
    async def test_execute_surfaces_console_error(self):
        from src.telnet_client import GMA2TelnetClient

        client = GMA2TelnetClient(host="192.168.1.100")
        client.send_command_with_response = AsyncMock(
            return_value=(
                'Executing : List Preset "color"\n\rError #14: OBJECT DOES NOT EXIST\n\r [Fixture]>'
            )
        )

        result = await client.execute('List Preset "color"')

        assert result.ok is False
        assert result.error_code == 14
        assert result.error_text == "OBJECT DOES NOT EXIST"
