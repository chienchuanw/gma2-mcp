"""
Pytest Configuration File

This file is used to define shared fixtures and test configuration.
"""

import pytest


# Configure pytest-asyncio default mode
pytest_plugins = ["pytest_asyncio"]


@pytest.fixture
def mock_gma_host():
    """Provide test grandMA2 host IP."""
    return "127.0.0.1"


@pytest.fixture
def mock_gma_port():
    """Provide test grandMA2 port."""
    return 30000


@pytest.fixture
def mock_gma_credentials():
    """Provide test grandMA2 login credentials."""
    return {"user": "administrator", "password": "admin"}
