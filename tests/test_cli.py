from click.testing import CliRunner
import pytest

from whatsonpypi import __version__, cli


@pytest.mark.parametrize(
    "options",
    [
        ([]),
        (["-h"]),
        (["--help"]),
        (["what", "-h"]),
        (["what", "--help"]),
    ],
)
def test_help(options):
    result = CliRunner().invoke(cli.main, options)
    assert result.exit_code == 0
    assert result.output.startswith("Usage: ")
    assert "-h, --help" in result.output


@pytest.mark.parametrize(
    "options",
    [
        (["-v"]),
        (["--version"]),
    ],
)
def test_version(options):
    result = CliRunner().invoke(cli.main, options)
    assert result.exit_code == 0
    assert __version__ in result.output
