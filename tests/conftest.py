"""
Pytest 設定檔

這個檔案用於定義共用的 fixtures 和測試設定。
"""

import pytest


# 設定 pytest-asyncio 的預設模式
pytest_plugins = ["pytest_asyncio"]


@pytest.fixture
def mock_gma_host():
    """提供測試用的 grandMA2 主機 IP"""
    return "127.0.0.1"


@pytest.fixture
def mock_gma_port():
    """提供測試用的 grandMA2 連接埠"""
    return 30000


@pytest.fixture
def mock_gma_credentials():
    """提供測試用的 grandMA2 登入憑證"""
    return {
        "user": "administrator",
        "password": "admin"
    }

