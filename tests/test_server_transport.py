"""
Server Transport Configuration Tests

Tests for MCP_TRANSPORT, MCP_HOST, and MCP_PORT environment variable handling
in the server's main() function.
"""

import pytest
from unittest.mock import patch, MagicMock


class TestTransportSelection:
    """Tests for transport selection via MCP_TRANSPORT env var."""

    @patch("src.server.mcp")
    def test_default_transport_is_stdio(self, mock_mcp):
        """Default transport should be stdio when MCP_TRANSPORT is not set."""
        from src.server import main

        with patch.dict("os.environ", {}, clear=False):
            # Ensure MCP_TRANSPORT is not set
            with patch.dict("os.environ", {"MCP_TRANSPORT": ""}, clear=False):
                pass
            import os

            os.environ.pop("MCP_TRANSPORT", None)
            main()

        mock_mcp.run.assert_called_once()
        call_kwargs = mock_mcp.run.call_args
        assert call_kwargs[1]["transport"] == "stdio"

    @patch("src.server.mcp")
    def test_streamable_http_transport(self, mock_mcp):
        """MCP_TRANSPORT=streamable-http should pass streamable-http to mcp.run()."""
        from src.server import main

        with patch.dict(
            "os.environ", {"MCP_TRANSPORT": "streamable-http"}, clear=False
        ):
            main()

        mock_mcp.run.assert_called_once()
        call_kwargs = mock_mcp.run.call_args
        assert call_kwargs[1]["transport"] == "streamable-http"

    @patch("src.server.mcp")
    def test_invalid_transport_falls_back_to_stdio(self, mock_mcp):
        """Invalid MCP_TRANSPORT value should log warning and fall back to stdio."""
        from src.server import main

        with patch.dict("os.environ", {"MCP_TRANSPORT": "invalid-transport"}, clear=False):
            main()

        mock_mcp.run.assert_called_once()
        call_kwargs = mock_mcp.run.call_args
        assert call_kwargs[1]["transport"] == "stdio"


class TestHttpHostPort:
    """Tests for MCP_HOST and MCP_PORT configuration with streamable-http."""

    @patch("src.server.mcp")
    def test_default_host_and_port_for_http(self, mock_mcp):
        """Default host should be 127.0.0.1 and port 8000 for streamable-http."""
        from src.server import main

        with patch.dict(
            "os.environ", {"MCP_TRANSPORT": "streamable-http"}, clear=False
        ):
            # Remove MCP_HOST and MCP_PORT if set
            import os

            os.environ.pop("MCP_HOST", None)
            os.environ.pop("MCP_PORT", None)
            main()

        mock_mcp.run.assert_called_once()
        call_kwargs = mock_mcp.run.call_args[1]
        assert call_kwargs["host"] == "127.0.0.1"
        assert call_kwargs["port"] == 8000

    @patch("src.server.mcp")
    def test_custom_host_and_port_for_http(self, mock_mcp):
        """Custom MCP_HOST and MCP_PORT should be passed through."""
        from src.server import main

        with patch.dict(
            "os.environ",
            {
                "MCP_TRANSPORT": "streamable-http",
                "MCP_HOST": "0.0.0.0",
                "MCP_PORT": "9090",
            },
            clear=False,
        ):
            main()

        mock_mcp.run.assert_called_once()
        call_kwargs = mock_mcp.run.call_args[1]
        assert call_kwargs["host"] == "0.0.0.0"
        assert call_kwargs["port"] == 9090

    @patch("src.server.mcp")
    def test_host_port_ignored_for_stdio(self, mock_mcp):
        """MCP_HOST and MCP_PORT should be ignored when transport is stdio."""
        from src.server import main

        with patch.dict(
            "os.environ",
            {
                "MCP_TRANSPORT": "stdio",
                "MCP_HOST": "0.0.0.0",
                "MCP_PORT": "9090",
            },
            clear=False,
        ):
            main()

        mock_mcp.run.assert_called_once()
        call_kwargs = mock_mcp.run.call_args[1]
        assert call_kwargs["transport"] == "stdio"
        assert "host" not in call_kwargs
        assert "port" not in call_kwargs
