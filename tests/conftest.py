from collections.abc import Generator

import pytest


@pytest.fixture(scope="session", autouse=True)
def cleanup() -> Generator[None, None, None]:
    yield
    print("cleanup")
