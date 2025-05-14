from click.testing import CliRunner
import pytest

from whatsonpypi import __version__, cli


@pytest.mark.parametrize(
    "options",
    [
        (["-h"]),
        (["--help"]),
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


@pytest.mark.parametrize(
    "work, option, valid",
    [
        (["building workedon"], ["-s"], True),
        (["studying for the GRE"], ["--last"], True),
        (["talking to my brother", "@ 3pm 3 years ago"], ["--last"], False),
    ],
)
def test_save_and_fetch_last(work, option, valid, cleanup):
    # save
    result = CliRunner().invoke(cli.main, work)
    assert result.output.startswith("Work saved.")
    # fetch
    result = CliRunner().invoke(cli.what, option)
    assert result.exit_code == 0
    assert "" in result.output
