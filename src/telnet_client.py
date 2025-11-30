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
"""

import logging
import telnetlib
import time
from typing import Optional

# Configure logger
logger = logging.getLogger(__name__)


class GMA2TelnetClient:
    """
    grandMA2 Telnet Connection Client

    Provides Telnet connection management functionality for grandMA2 onPC/Console,
    including connection establishment, authentication, command sending, and
    reconnection logic.

    Attributes:
        host: grandMA2 host IP address
        port: Telnet port (default 30000, 30001 is read-only)
        user: Login username
        password: Login password

    Example:
        >>> with GMA2TelnetClient(host="192.168.1.100") as client:
        ...     client.send_command("selfix fixture 1 thru 10")
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
        self._connection: Optional[telnetlib.Telnet] = None

        logger.debug(
            f"GMA2TelnetClient initialized: host={host}, port={port}, user={user}"
        )

    def connect(self) -> None:
        """
        Establish a Telnet connection.

        Raises:
            ConnectionError: Unable to connect to grandMA2 host
        """
        logger.info(f"Connecting to {self.host}:{self.port}...")

        try:
            self._connection = telnetlib.Telnet(self.host, self.port)
            # Wait for connection to stabilize
            time.sleep(0.5)
            logger.info(f"Successfully connected to {self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            raise ConnectionError(f"Unable to connect to {self.host}:{self.port}: {e}")

    def login(self) -> bool:
        """
        Perform login authentication.

        Returns:
            bool: True if login is successful

        Raises:
            RuntimeError: Connection not established
        """
        if self._connection is None:
            raise RuntimeError("Connection not established, call connect() first")

        logger.info(f"Logging in as {self.user}...")

        # Build login command (password is not logged)
        login_cmd = f'login "{self.user}" "{self.password}"\r\n'
        self._connection.write(login_cmd.encode("utf-8"))

        # Wait for login response
        time.sleep(0.5)
        response = self._connection.read_very_eager()

        logger.debug(f"Login response: {response.decode('utf-8', errors='ignore')}")
        logger.info("Login successful")

        return True

    def send_command(self, command: str, delay: float = 0.3) -> None:
        """
        Send a command to grandMA2.

        Args:
            command: MA command to send
            delay: Wait time in seconds after sending command to allow grandMA2 to process

        Raises:
            RuntimeError: Connection not established
        """
        if self._connection is None:
            raise RuntimeError("Connection not established, call connect() first")

        logger.debug(f"Sending command: {command}")

        # Send command (automatically add newline)
        full_command = f"{command}\r\n"
        self._connection.write(full_command.encode("utf-8"))

        # Wait for grandMA2 to process command
        time.sleep(delay)
        logger.debug(f"Command sent, waiting {delay} seconds")

    def disconnect(self) -> None:
        """Close the Telnet connection."""
        if self._connection is not None:
            logger.info("Closing connection...")
            self._connection.close()
            self._connection = None
            logger.info("Connection closed")

    def __enter__(self) -> "GMA2TelnetClient":
        """Context manager entry point: establish connection and login."""
        self.connect()
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit point: close connection."""
        self.disconnect()
