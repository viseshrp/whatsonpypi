import pytest

from whatsonpypi.whatsonpypi import do_stuff


@pytest.mark.parametrize(
    "option",
    ["test1", "test2"],
)
def test_do_stuff(option: str) -> None:
    assert do_stuff(option) == option
