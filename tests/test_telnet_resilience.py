import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from src.telnet_client import GMA2TelnetClient, ConnectionState


class TestConnectionState:
    def test_initial_state_is_disconnected(self):
        client = GMA2TelnetClient(host="127.0.0.1")
        assert client.state == ConnectionState.DISCONNECTED

    @pytest.mark.asyncio
    async def test_state_connected_after_connect(self):
        client = GMA2TelnetClient(host="127.0.0.1")
        with patch("telnetlib3.open_connection", new_callable=AsyncMock) as mock_conn:
            mock_conn.return_value = (MagicMock(), MagicMock())
            await client.connect()
            assert client.state == ConnectionState.CONNECTED

    @pytest.mark.asyncio
    async def test_state_disconnected_after_disconnect(self):
        client = GMA2TelnetClient(host="127.0.0.1")
        with patch("telnetlib3.open_connection", new_callable=AsyncMock) as mock_conn:
            mock_conn.return_value = (MagicMock(), MagicMock())
            await client.connect()
            await client.disconnect()
            assert client.state == ConnectionState.DISCONNECTED


class TestCheckConnection:
    @pytest.mark.asyncio
    async def test_returns_true_on_healthy_connection(self):
        client = GMA2TelnetClient(host="127.0.0.1")
        with patch("telnetlib3.open_connection", new_callable=AsyncMock) as mock_conn:
            mock_reader = MagicMock()
            mock_writer = MagicMock()
            mock_reader.read = AsyncMock(return_value="[user]>")
            mock_conn.return_value = (mock_reader, mock_writer)
            await client.connect()
            result = await client.check_connection()
            assert result is True

    @pytest.mark.asyncio
    async def test_returns_false_when_disconnected(self):
        client = GMA2TelnetClient(host="127.0.0.1")
        result = await client.check_connection()
        assert result is False

    @pytest.mark.asyncio
    async def test_returns_false_on_dead_connection(self):
        client = GMA2TelnetClient(host="127.0.0.1")
        with patch("telnetlib3.open_connection", new_callable=AsyncMock) as mock_conn:
            mock_reader = MagicMock()
            mock_writer = MagicMock()
            mock_writer.write = MagicMock(side_effect=Exception("broken pipe"))
            mock_conn.return_value = (mock_reader, mock_writer)
            await client.connect()
            result = await client.check_connection()
            assert result is False

    @pytest.mark.asyncio
    async def test_never_raises(self):
        client = GMA2TelnetClient(host="127.0.0.1")
        with patch("telnetlib3.open_connection", new_callable=AsyncMock) as mock_conn:
            mock_reader = MagicMock()
            mock_writer = MagicMock()
            mock_writer.write = MagicMock(side_effect=RuntimeError("boom"))
            mock_conn.return_value = (mock_reader, mock_writer)
            await client.connect()
            # Should not raise, just return False
            result = await client.check_connection()
            assert result is False


class TestAutoReconnect:
    def test_default_retry_parameters(self):
        client = GMA2TelnetClient(host="127.0.0.1")
        assert client.max_retries == 3
        assert client.retry_base_delay == 1.0

    def test_custom_retry_parameters(self):
        client = GMA2TelnetClient(host="127.0.0.1", max_retries=5, retry_base_delay=0.5)
        assert client.max_retries == 5
        assert client.retry_base_delay == 0.5

    @pytest.mark.asyncio
    async def test_reconnect_on_first_retry(self):
        """send_command() should reconnect transparently if health check fails but reconnect succeeds."""
        client = GMA2TelnetClient(host="127.0.0.1", max_retries=3, retry_base_delay=0.01)
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_reader.read = AsyncMock(return_value="[user]>")

        with patch("telnetlib3.open_connection", new_callable=AsyncMock) as mock_conn:
            mock_conn.return_value = (mock_reader, mock_writer)
            await client.connect()
            await client.login()

            # Now simulate dead connection on health check, but reconnect succeeds
            call_count = 0

            async def check_side_effect():
                nonlocal call_count
                call_count += 1
                if call_count == 1:
                    return False  # first check fails
                return True  # after reconnect, check succeeds

            async def reconnect_side_effect():
                client._state = ConnectionState.CONNECTED
                client._reader = mock_reader
                client._writer = mock_writer

            with patch.object(client, "check_connection", side_effect=check_side_effect):
                with patch.object(client, "connect", side_effect=reconnect_side_effect) as mock_reconnect:
                    with patch.object(client, "login", new_callable=AsyncMock):
                        await client.send_command("test command")
                        mock_reconnect.assert_called_once()

    @pytest.mark.asyncio
    async def test_connection_error_after_all_retries_exhausted(self):
        """send_command() should raise ConnectionError after max_retries failures."""
        client = GMA2TelnetClient(host="127.0.0.1", max_retries=3, retry_base_delay=0.01)
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_reader.read = AsyncMock(return_value="[user]>")

        with patch("telnetlib3.open_connection", new_callable=AsyncMock) as mock_conn:
            mock_conn.return_value = (mock_reader, mock_writer)
            await client.connect()

            # Health check always fails, reconnect always fails
            with patch.object(client, "check_connection", new_callable=AsyncMock, return_value=False):
                with patch.object(client, "connect", new_callable=AsyncMock, side_effect=ConnectionError("refused")):
                    with pytest.raises(ConnectionError, match="failed to reconnect after 3 attempts"):
                        await client.send_command("test command")

    @pytest.mark.asyncio
    async def test_state_transitions_during_reconnection(self):
        """State should be RECONNECTING during reconnect attempt."""
        client = GMA2TelnetClient(host="127.0.0.1", max_retries=3, retry_base_delay=0.01)
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_reader.read = AsyncMock(return_value="[user]>")

        observed_states = []

        with patch("telnetlib3.open_connection", new_callable=AsyncMock) as mock_conn:
            mock_conn.return_value = (mock_reader, mock_writer)
            await client.connect()

            async def spy_connect():
                observed_states.append(client.state)
                client._state = ConnectionState.CONNECTED
                client._reader = mock_reader
                client._writer = mock_writer

            with patch.object(client, "check_connection", new_callable=AsyncMock, return_value=False):
                with patch.object(client, "connect", side_effect=spy_connect):
                    with patch.object(client, "login", new_callable=AsyncMock):
                        with patch.object(client, "disconnect", new_callable=AsyncMock):
                            await client.send_command("test")
                            assert ConnectionState.RECONNECTING in observed_states


class TestHealthCheckTTL:
    @pytest.mark.asyncio
    async def test_skips_health_check_within_ttl(self):
        """Commands within TTL should not trigger health check."""
        client = GMA2TelnetClient(host="127.0.0.1", health_check_ttl=5.0, max_retries=3, retry_base_delay=0.01)
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_reader.read = AsyncMock(return_value="[user]>")

        with patch("telnetlib3.open_connection", new_callable=AsyncMock) as mock_conn:
            mock_conn.return_value = (mock_reader, mock_writer)
            await client.connect()
            await client.login()

            with patch.object(client, "check_connection", new_callable=AsyncMock, return_value=True) as mock_check:
                # First command triggers health check
                await client.send_command("cmd1")
                first_check_count = mock_check.call_count

                # Second command within TTL should skip
                await client.send_command("cmd2")
                assert mock_check.call_count == first_check_count  # no additional check

    @pytest.mark.asyncio
    async def test_triggers_health_check_after_ttl(self):
        """Commands after TTL should trigger health check."""
        client = GMA2TelnetClient(host="127.0.0.1", health_check_ttl=0.01, max_retries=3, retry_base_delay=0.01)
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        mock_reader.read = AsyncMock(return_value="[user]>")

        with patch("telnetlib3.open_connection", new_callable=AsyncMock) as mock_conn:
            mock_conn.return_value = (mock_reader, mock_writer)
            await client.connect()
            await client.login()

            with patch.object(client, "check_connection", new_callable=AsyncMock, return_value=True) as mock_check:
                await client.send_command("cmd1")
                first_check_count = mock_check.call_count

                # Wait for TTL to expire
                import asyncio as aio
                await aio.sleep(0.02)

                await client.send_command("cmd2")
                assert mock_check.call_count > first_check_count  # health check triggered

    @pytest.mark.asyncio
    async def test_send_command_with_response_updates_ttl(self):
        """send_command_with_response() should also update the TTL timestamp."""
        import asyncio

        client = GMA2TelnetClient(host="127.0.0.1", health_check_ttl=5.0, max_retries=3, retry_base_delay=0.01)
        mock_reader = MagicMock()
        mock_writer = MagicMock()
        # Return data once for each read phase, then timeout to break the loop
        mock_reader.read = AsyncMock(
            side_effect=["[user]>", "[user]>", "response data", asyncio.TimeoutError()]
        )

        with patch("telnetlib3.open_connection", new_callable=AsyncMock) as mock_conn:
            mock_conn.return_value = (mock_reader, mock_writer)
            await client.connect()
            await client.login()

            with patch.object(client, "check_connection", new_callable=AsyncMock, return_value=True) as mock_check:
                # First call with response triggers health check
                await client.send_command_with_response("list")
                first_check_count = mock_check.call_count

                # Second call (regular send_command) within TTL should skip
                await client.send_command("cmd2")
                assert mock_check.call_count == first_check_count  # TTL from response cmd still valid
