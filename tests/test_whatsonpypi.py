from __future__ import annotations

import pytest

from whatsonpypi.whatsonpypi import run_query


@pytest.mark.parametrize("pkg", ["requests", "httpx", "rich"])
def test_run_query_returns_expected_keys(pkg: str) -> None:
    result = run_query(pkg, version=None, more_out=False, launch_docs=False, open_page=False)
    assert result is not None
    assert "name" in result
    assert "current_version" in result
    assert "summary" in result


@pytest.mark.parametrize("pkg", ["requests", "httpx"])
def test_run_query_more_outputs(pkg: str) -> None:
    result = run_query(pkg, version=None, more_out=True, launch_docs=False, open_page=False)
    assert result is not None
    assert "dependencies" in result
    assert "project_urls" in result
    assert "license" in result
    assert "releases" in result
    assert isinstance(result["dependencies"], str)
    assert isinstance(result["project_urls"], dict)
    assert result["license"] is None or isinstance(result["license"], str)
    assert isinstance(result["releases"], str)


@pytest.mark.parametrize("version", ["2.31.0", "1.0.0"])
def test_run_query_specific_version(version: str) -> None:
    result = run_query(
        "requests", version=version, more_out=True, launch_docs=False, open_page=False
    )
    assert result is not None
    assert "current_version" in result
    assert result["current_version"] == version


def test_run_query_missing_package_raises() -> None:
    with pytest.raises(Exception, match="couldn't be found"):
        run_query("this-package-does-not-exist-1234", None, False, False, False)


def test_run_query_typical_with_more() -> None:
    result = run_query("rich", version=None, more_out=True, launch_docs=False, open_page=False)
    assert result is not None
    assert isinstance(result["dependencies"], str)
    assert "sha256" in str(result["current_package_info"]).lower()
