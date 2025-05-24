from __future__ import annotations

from click.testing import CliRunner
import pytest

from whatsonpypi import __version__, cli


@pytest.mark.parametrize("options", [["-h"], ["--help"]])
def test_help(options: list[str]) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.main, options)

    assert result.exit_code == 0, f"Help options {options} failed with exit code {result.exit_code}"
    assert result.output.startswith(
        "Usage: "
    ), f"Help output for {options} did not start with 'Usage:'"
    assert "-h, --help" in result.output, f"Help flags missing from output for {options}"


@pytest.mark.parametrize("options", [["-v"], ["--version"]])
def test_version(options: list[str]) -> None:
    runner = CliRunner()
    result = runner.invoke(cli.main, options)

    assert (
        result.exit_code == 0
    ), f"Version options {options} failed with exit code {result.exit_code}"
    assert (
        __version__ in result.output
    ), f"Expected version {__version__} not found in output for {options}"


def test_more_flag_output() -> None:
    result = CliRunner().invoke(cli.main, ["requests", "--more"])
    assert result.exit_code == 0
    assert "DEPENDENCIES" in result.output  # or other expanded field


def test_docs_flag_opens_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("webbrowser.open", lambda url: True)  # simulate success
    result = CliRunner().invoke(cli.main, ["requests", "--docs"])
    assert result.exit_code == 0


def test_open_flag_opens_pypi(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("webbrowser.open", lambda url: True)
    result = CliRunner().invoke(cli.main, ["requests", "--open"])
    assert result.exit_code == 0


@pytest.mark.parametrize("arg", ["--history=3", "--history=-3"])
def test_history_with_value(arg: str) -> None:
    result = CliRunner().invoke(cli.main, ["django", arg])
    assert result.exit_code == 0
    assert "SDIST" in result.output


def test_history_old() -> None:
    result = CliRunner().invoke(cli.main, ["django", "--history=-5"])
    assert result.exit_code == 0
    assert "SDIST" in result.output and "BDIST" not in result.output and "1.2" in result.output


def test_history_new() -> None:
    result = CliRunner().invoke(cli.main, ["django", "--history=5"])
    assert result.exit_code == 0
    assert "SDIST" in result.output and "BDIST" in result.output and "1.2" not in result.output


def test_invalid_package() -> None:
    result = CliRunner().invoke(cli.main, ["nonexistent_package_12345"])
    assert result.exit_code != 0
    assert "couldn't be found" in result.output.lower()
