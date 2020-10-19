import pytest
from app import app


@pytest.fixture
def test_app() -> app:
    return app


@pytest.fixture
def big_list() -> [int]:
    return list(range(10000001))
