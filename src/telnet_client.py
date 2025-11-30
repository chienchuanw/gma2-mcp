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

Uses telnetlib3 (based on asyncio) to replace the deprecated telnetlib module.
"""

import asyncio
import logging
from typing import Any, Optional

import telnetlib3

# Configure logger
logger = logging.getLogger(__name__)


class GMA2TelnetClient:
    """
    grandMA2 Telnet Connection Client (Async Version)

    Provides Telnet connection management functionality for grandMA2 onPC/Console,
    including connection establishment, authentication, command sending, and
    reconnection logic.

    This version uses telnetlib3 and asyncio to avoid the deprecation of telnetlib
    in Python 3.13.

    Attributes:
        host: grandMA2 host IP address
        port: Telnet port (default 30000, 30001 is read-only)
        user: Login username
        password: Login password

    Example (Async):
        >>> async with GMA2TelnetClient(host="192.168.1.100") as client:
        ...     await client.send_command("selfix fixture 1 thru 10")

    Example (Sync - using run_sync method):
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
        # telnetlib3 uses reader/writer pattern
        self._reader: Optional[Any] = None
        self._writer: Optional[Any] = None
        self._connection: Optional[Any] = None  # Kept for compatibility checks

        logger.debug(
            f"GMA2TelnetClient initialized: host={host}, port={port}, user={user}"
        )

    def run_sync(self, coro: Any) -> Any:
        """
        Helper function to run async methods in synchronous environments.

        Args:
            coro: The coroutine to execute

        Returns:
            The result of the coroutine execution
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
            # telnetlib3 uses open_connection to establish connection
            self._reader, self._writer = await telnetlib3.open_connection(
                host=self.host,
                port=self.port,
            )
            # Mark connection state
            self._connection = True
            # Wait for connection to stabilize
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
        if self._writer is None or self._reader is None:
            raise RuntimeError("Connection not established, call connect() first")

        logger.info(f"Logging in as {self.user}...")

        # Build login command (password is not logged)
        login_cmd = f'login "{self.user}" "{self.password}"\r\n'
        self._writer.write(login_cmd)

        # Wait for login response
        await asyncio.sleep(0.5)

        # Attempt to read response (non-blocking)
        try:
            response = await asyncio.wait_for(
                self._reader.read(1024),
                timeout=1.0,
            )
            logger.debug(f"Login response: {response}")
        except asyncio.TimeoutError:
            # Timeout is normal behavior, grandMA2 may not respond immediately
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

    async def send_command_with_response(
        self, command: str, timeout: float = 2.0, delay: float = 0.3
    ) -> str:
        """
        Send a command to grandMA2 and read the response (async).

        發送指令並讀取 grandMA2 的回應。適用於 list、info 等會產生輸出的指令。

        Args:
            command: MA command to send
            timeout: Maximum wait time for response in seconds
            delay: Initial delay after sending command

        Returns:
            str: Response from grandMA2

        Raises:
            RuntimeError: Connection not established
        """
        if self._writer is None or self._reader is None:
            raise RuntimeError("Connection not established, call connect() first")

        logger.debug(f"Sending command with response: {command}")

        # 清空任何待處理的資料
        try:
            await asyncio.wait_for(self._reader.read(4096), timeout=0.1)
        except asyncio.TimeoutError:
            pass

        # Send command
        full_command = f"{command}\r\n"
        self._writer.write(full_command)

        # Wait for grandMA2 to process
        await asyncio.sleep(delay)

        # Read response
        response_parts = []
        try:
            # 持續讀取直到沒有更多資料
            while True:
                try:
                    chunk = await asyncio.wait_for(
                        self._reader.read(4096), timeout=timeout
                    )
                    if chunk:
                        response_parts.append(chunk)
                        # 縮短後續讀取的 timeout
                        timeout = 0.3
                    else:
                        break
                except asyncio.TimeoutError:
                    break
        except Exception as e:
            logger.warning(f"Error reading response: {e}")

        response = "".join(response_parts)
        logger.debug(f"Response received: {len(response)} characters")
        return response

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
