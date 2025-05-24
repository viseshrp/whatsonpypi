import pytest

from whatsonpypi.whatsonpypi import run_query


def test_run_query_basic() -> None:
    result = run_query("requests", version=None, more_out=False, launch_docs=False, open_page=False)
    assert result is not None
    assert isinstance(result, dict)
    assert "name" in result
    assert "current_version" in result
    assert "summary" in result


def test_run_query_more_flag() -> None:
    result = run_query("requests", version=None, more_out=True, launch_docs=False, open_page=False)
    assert result is not None
    assert "dependencies" in result
    assert "project_urls" in result
    assert isinstance(result["dependencies"], str)


def test_run_query_invalid_package() -> None:
    with pytest.raises(Exception, match="couldn't be found"):
        run_query("fakepkg-that-does-not-exist", None, False, False, False)
