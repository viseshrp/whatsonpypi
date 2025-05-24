"""
Console script
"""

from __future__ import annotations

import click

from . import __version__
from .utils import parse_pkg_string, pretty
from .whatsonpypi import run_query


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(__version__, "-v", "--version")
@click.argument("package")
@click.option(
    "-m",
    "--more",
    is_flag=True,
    required=False,
    default=False,
    show_default=True,
    help="Flag to enable expanded output",
)
@click.option(
    "-d",
    "--docs",
    is_flag=True,
    required=False,
    default=False,
    help="Flag to open docs or homepage of project",
)
@click.option(
    "-o",
    "--open",
    "page",
    is_flag=True,
    required=False,
    default=False,
    help="Flag to open PyPI page",
)
@click.option(
    "-H",
    "--history",
    required=False,
    default=None,
    type=int,
    help="Show release history. Use positive number for most"
    " recent, negative for oldest. E.g. '--history -10' or '--history 10'",
)
def main(
    package: str,
    more: bool,
    docs: bool,
    page: bool,
    history: int | None,
) -> None:
    """
    CLI tool to get package info from PyPI and/or manipulate requirements.

    Example usages:

    $ whatsonpypi django

    OR

    $ wopp django
    """
    try:
        # get version if given
        package_, version, _ = parse_pkg_string(package)
        result = run_query(
            package_ or package,  # parsed package name can be None
            version,
            more,
            docs,
            page,
            history,
        )
        # output is not always expected and might be None sometimes.
        if result:
            pretty(result)
    except Exception as e:
        raise click.ClickException(str(e)) from e


if __name__ == "__main__":
    main()  # pragma: no cover
