"""
Telnet Client 模組

這個模組負責與 grandMA2 建立 Telnet 連線，處理登入驗證，
以及發送指令。這是專案中唯一允許直接操作 Telnet 的模組。

根據 coding-standards.md，Telnet client 是唯一可以：
- 開啟連線
- 執行登入指令
- 執行重連邏輯
- 發送原始 MA 指令
"""

import logging
import telnetlib
import time
from typing import Optional

# 設定 logger
logger = logging.getLogger(__name__)


class GMA2TelnetClient:
    """
    grandMA2 Telnet 連線客戶端

    提供與 grandMA2 onPC/Console 的 Telnet 連線管理功能，
    包含連線建立、登入驗證、指令發送、以及斷線重連。

    Attributes:
        host: grandMA2 主機 IP 位址
        port: Telnet 連接埠（預設 30000，30001 為唯讀）
        user: 登入使用者名稱
        password: 登入密碼

    Example:
        >>> with GMA2TelnetClient(host="192.168.1.100") as client:
        ...     client.send_command("selfix fixture 1 thru 10")
    """

    # 預設設定值
    DEFAULT_PORT = 30000
    DEFAULT_USER = "administrator"
    DEFAULT_PASSWORD = "admin"

    def __init__(
        self,
        host: str,
        port: int = DEFAULT_PORT,
        user: str = DEFAULT_USER,
        password: str = DEFAULT_PASSWORD,
    ):
        """
        初始化 Telnet Client

        Args:
            host: grandMA2 主機 IP 位址
            port: Telnet 連接埠（預設 30000）
            user: 登入使用者名稱（預設 "administrator"）
            password: 登入密碼（預設 "admin"）
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self._connection: Optional[telnetlib.Telnet] = None

        logger.debug(f"GMA2TelnetClient 初始化: host={host}, port={port}, user={user}")

    def connect(self) -> None:
        """
        建立 Telnet 連線

        Raises:
            ConnectionError: 無法連線到 grandMA2 主機
        """
        logger.info(f"正在連線到 {self.host}:{self.port}...")

        try:
            self._connection = telnetlib.Telnet(self.host, self.port)
            # 等待連線穩定
            time.sleep(0.5)
            logger.info(f"成功連線到 {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"連線失敗: {e}")
            raise ConnectionError(f"無法連線到 {self.host}:{self.port}: {e}")

    def login(self) -> bool:
        """
        執行登入驗證

        Returns:
            bool: 登入成功回傳 True

        Raises:
            RuntimeError: 尚未建立連線
        """
        if self._connection is None:
            raise RuntimeError("尚未建立連線，請先呼叫 connect()")

        logger.info(f"正在以 {self.user} 身份登入...")

        # 組建登入指令（密碼不記錄到 log）
        login_cmd = f'login "{self.user}" "{self.password}"\r\n'
        self._connection.write(login_cmd.encode("utf-8"))

        # 等待登入回應
        time.sleep(0.5)
        response = self._connection.read_very_eager()

        logger.debug(f"登入回應: {response.decode('utf-8', errors='ignore')}")
        logger.info("登入成功")

        return True

    def send_command(self, command: str) -> None:
        """
        發送指令到 grandMA2

        Args:
            command: 要發送的 MA 指令

        Raises:
            RuntimeError: 尚未建立連線
        """
        if self._connection is None:
            raise RuntimeError("尚未建立連線，請先呼叫 connect()")

        logger.debug(f"發送指令: {command}")

        # 發送指令（自動加上換行符號）
        full_command = f"{command}\r\n"
        self._connection.write(full_command.encode("utf-8"))

    def disconnect(self) -> None:
        """斷開 Telnet 連線"""
        if self._connection is not None:
            logger.info("正在斷開連線...")
            self._connection.close()
            self._connection = None
            logger.info("已斷開連線")

    def __enter__(self) -> "GMA2TelnetClient":
        """Context manager 進入點：建立連線並登入"""
        self.connect()
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager 離開點：斷開連線"""
        self.disconnect()

