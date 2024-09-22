from typing import Generator
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api import deps


async def override_reddit_dependency() -> MagicMock:
    mock = MagicMock()
    reddit_stub = {
        "learning_path": [
            "2085: all learning paths (https://portswigger.net/web-security/learning-paths)",
        ],
        "easylevels": [
            "74: sql injection paths (https://portswigger.net/web-security/learning-paths/sql-injection)",
        ],
        "Toplevels": [
            "132: advance_lp (https://portswigger.net/web-security/learning-paths/authentication-vulnerabilities)",
        ],
    }
    mock.get_reddit_top.return_value = reddit_stub
    return mock


@pytest.fixture
def client() -> Generator:
    with TestClient(app) as client:
        app.dependency_overrides[deps.get_reddit_client] = override_reddit_dependency
        yield client
        app.dependency_overrides = {}
