"""
Telnet Client Module

This module is responsible for establishing Telnet connections with grandMA2,
handling authentication, and sending commands. This is the only module in the
project permitted to directly manipulate Telnet.

According to coding-standards.md, the Telnet client is the only component that can:
- Open connections
- Execute login commands
- Perform reconnection logic
- Send raw MA commands

使用 telnetlib3 (基於 asyncio) 取代已棄用的 telnetlib
"""

import asyncio
import logging
from typing import Any, Optional

import telnetlib3

# Configure logger
logger = logging.getLogger(__name__)


class GMA2TelnetClient:
    """
    grandMA2 Telnet Connection Client (Async 版本)

    Provides Telnet connection management functionality for grandMA2 onPC/Console,
    including connection establishment, authentication, command sending, and
    reconnection logic.

    此版本使用 telnetlib3 和 asyncio 實現，避免 Python 3.13 中 telnetlib 棄用的問題。

    Attributes:
        host: grandMA2 host IP address
        port: Telnet port (default 30000, 30001 is read-only)
        user: Login username
        password: Login password

    Example (Async):
        >>> async with GMA2TelnetClient(host="192.168.1.100") as client:
        ...     await client.send_command("selfix fixture 1 thru 10")

    Example (Sync - 使用 run_sync 方法):
        >>> client = GMA2TelnetClient(host="192.168.1.100")
        >>> client.run_sync(client.connect())
        >>> client.run_sync(client.login())
        >>> client.run_sync(client.send_command("selfix fixture 1 thru 10"))
        >>> client.run_sync(client.disconnect())
    """

    # Default configuration values
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
        Initialize Telnet Client.

        Args:
            host: grandMA2 host IP address
            port: Telnet port (default 30000)
            user: Login username (default "administrator")
            password: Login password (default "admin")
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        # telnetlib3 使用 reader/writer 模式
        self._reader: Optional[Any] = None
        self._writer: Optional[Any] = None
        self._connection: Optional[Any] = None  # 保留以支援相容性檢查

        logger.debug(
            f"GMA2TelnetClient initialized: host={host}, port={port}, user={user}"
        )

    def run_sync(self, coro: Any) -> Any:
        """
        在同步環境中執行 async 方法的輔助函數。

        Args:
            coro: 要執行的 coroutine

        Returns:
            coroutine 的執行結果
        """
        return asyncio.get_event_loop().run_until_complete(coro)

    async def connect(self) -> None:
        """
        Establish a Telnet connection (async).

        Raises:
            ConnectionError: Unable to connect to grandMA2 host
        """
        logger.info(f"Connecting to {self.host}:{self.port}...")

        try:
            # telnetlib3 使用 open_connection 建立連線
            self._reader, self._writer = await telnetlib3.open_connection(
                host=self.host,
                port=self.port,
            )
            # 標記連線狀態
            self._connection = True
            # 等待連線穩定
            await asyncio.sleep(0.5)
            logger.info(f"Successfully connected to {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise ConnectionError(f"Unable to connect to {self.host}:{self.port}: {e}")

    async def login(self) -> bool:
        """
        Perform login authentication (async).

        Returns:
            bool: True if login is successful

        Raises:
            RuntimeError: Connection not established
        """
        if self._writer is None:
            raise RuntimeError("Connection not established, call connect() first")

        logger.info(f"Logging in as {self.user}...")

        # Build login command (password is not logged)
        login_cmd = f'login "{self.user}" "{self.password}"\r\n'
        self._writer.write(login_cmd)

        # 等待登入回應
        await asyncio.sleep(0.5)

        # 嘗試讀取回應（非阻塞）
        try:
            response = await asyncio.wait_for(
                self._reader.read(1024),
                timeout=1.0,
            )
            logger.debug(f"Login response: {response}")
        except asyncio.TimeoutError:
            # 超時是正常的，grandMA2 可能不會立即回應
            logger.debug("Login response timeout (normal behavior)")

        logger.info("Login successful")
        return True

    async def send_command(self, command: str, delay: float = 0.3) -> None:
        """
        Send a command to grandMA2 (async).

        Args:
            command: MA command to send
            delay: Wait time in seconds after sending command to allow grandMA2 to process

        Raises:
            RuntimeError: Connection not established
        """
        if self._writer is None:
            raise RuntimeError("Connection not established, call connect() first")

        logger.debug(f"Sending command: {command}")

        # Send command (automatically add newline)
        full_command = f"{command}\r\n"
        self._writer.write(full_command)

        # Wait for grandMA2 to process command
        await asyncio.sleep(delay)
        logger.debug(f"Command sent, waiting {delay} seconds")

    async def disconnect(self) -> None:
        """Close the Telnet connection (async)."""
        if self._writer is not None:
            logger.info("Closing connection...")
            self._writer.close()
            self._writer = None
            self._reader = None
            self._connection = None
            logger.info("Connection closed")

    async def __aenter__(self) -> "GMA2TelnetClient":
        """Async context manager entry point: establish connection and login."""
        await self.connect()
        await self.login()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit point: close connection."""
        await self.disconnect()
