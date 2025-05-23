from collections.abc import Generator

import pytest


def do_cleanup() -> None:
    """Perform any necessary cleanup after tests."""
    # Add your cleanup code here
    pass


@pytest.fixture(scope="session", autouse=True)
def cleanup() -> Generator[None, None, None]:
    yield
    do_cleanup()
