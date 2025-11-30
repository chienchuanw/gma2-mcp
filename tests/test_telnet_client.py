"""
Telnet Client 模組測試

測試 GMA2TelnetClient 的連線、登入、發送指令等功能。
使用 mock 來模擬 Telnet 連線，避免實際網路呼叫。
"""

import pytest
from unittest.mock import Mock, patch, MagicMock


class TestGMA2TelnetClientInit:
    """測試 GMA2TelnetClient 初始化"""

    def test_client_init_with_default_values(self):
        """測試使用預設值初始化 client"""
        from src.telnet_client import GMA2TelnetClient

        client = GMA2TelnetClient(host="192.168.1.100")

        assert client.host == "192.168.1.100"
        assert client.port == 30000  # 預設 port
        assert client.user == "administrator"  # 預設使用者
        assert client.password == "admin"  # 預設密碼
        assert client._connection is None

    def test_client_init_with_custom_values(self):
        """測試使用自訂值初始化 client"""
        from src.telnet_client import GMA2TelnetClient

        client = GMA2TelnetClient(
            host="10.0.0.1",
            port=30001,
            user="custom_user",
            password="custom_pass"
        )

        assert client.host == "10.0.0.1"
        assert client.port == 30001
        assert client.user == "custom_user"
        assert client.password == "custom_pass"


class TestGMA2TelnetClientConnection:
    """測試 GMA2TelnetClient 連線功能"""

    @patch("src.telnet_client.telnetlib.Telnet")
    def test_connect_success(self, mock_telnet_class):
        """測試成功建立連線"""
        from src.telnet_client import GMA2TelnetClient

        # 設定 mock 行為
        mock_connection = MagicMock()
        mock_telnet_class.return_value = mock_connection

        client = GMA2TelnetClient(host="192.168.1.100")
        client.connect()

        # 驗證 Telnet 被正確呼叫
        mock_telnet_class.assert_called_once_with("192.168.1.100", 30000)
        assert client._connection is not None

    @patch("src.telnet_client.telnetlib.Telnet")
    def test_login_success(self, mock_telnet_class):
        """測試成功登入"""
        from src.telnet_client import GMA2TelnetClient

        # 設定 mock 行為
        mock_connection = MagicMock()
        mock_connection.read_very_eager.return_value = b"Login successful"
        mock_telnet_class.return_value = mock_connection

        client = GMA2TelnetClient(host="192.168.1.100")
        client.connect()
        result = client.login()

        # 驗證登入指令被發送
        expected_cmd = 'login "administrator" "admin"\r\n'
        mock_connection.write.assert_called_with(expected_cmd.encode("utf-8"))
        assert result is True

    @patch("src.telnet_client.telnetlib.Telnet")
    def test_send_command(self, mock_telnet_class):
        """測試發送指令"""
        from src.telnet_client import GMA2TelnetClient

        # 設定 mock 行為
        mock_connection = MagicMock()
        mock_telnet_class.return_value = mock_connection

        client = GMA2TelnetClient(host="192.168.1.100")
        client.connect()
        client.send_command("selfix fixture 1 thru 10")

        # 驗證指令被正確發送
        expected_cmd = "selfix fixture 1 thru 10\r\n"
        mock_connection.write.assert_called_with(expected_cmd.encode("utf-8"))

    @patch("src.telnet_client.telnetlib.Telnet")
    def test_disconnect(self, mock_telnet_class):
        """測試斷開連線"""
        from src.telnet_client import GMA2TelnetClient

        mock_connection = MagicMock()
        mock_telnet_class.return_value = mock_connection

        client = GMA2TelnetClient(host="192.168.1.100")
        client.connect()
        client.disconnect()

        # 驗證連線被關閉
        mock_connection.close.assert_called_once()
        assert client._connection is None


class TestGMA2TelnetClientContextManager:
    """測試 GMA2TelnetClient 作為 context manager 使用"""

    @patch("src.telnet_client.telnetlib.Telnet")
    def test_context_manager(self, mock_telnet_class):
        """測試使用 with 語句管理連線"""
        from src.telnet_client import GMA2TelnetClient

        mock_connection = MagicMock()
        mock_connection.read_very_eager.return_value = b"OK"
        mock_telnet_class.return_value = mock_connection

        with GMA2TelnetClient(host="192.168.1.100") as client:
            client.send_command("test command")

        # 驗證離開 context 時連線被關閉
        mock_connection.close.assert_called_once()

