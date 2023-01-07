"""
Console script
"""

import click

from . import __version__
from .utils import pretty, parse_pkg_string
from .whatsonpypi import run_query


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__, "-v", "--version")
@click.argument("package")
@click.option(
    "-m",
    "--more",
    is_flag=True,
    required=True,
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
    "-a",
    "--add",
    is_flag=True,
    required=False,
    default=False,
    help="Flag to enable adding of dependencies to requirement files."
    " By default, it searches for files with names matching requirements*.txt"
    " in the current working directory and adds the dependency to the end of the"
    " file. If you want the dependency to be added to a specific line,"
    " mention the comment '#wopp' on its own line which will be replaced with the dependency."
    " Existing dependencies will be replaced with newer versions. Dependency version"
    " by default is the latest unless specified explicitly with 'whatsonpypi package==version'."
    " Directory to search for requirement files can be specified with --req-dir",
)
@click.option(
    "-r",
    "--req-dir",
    type=click.Path(
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        writable=True,
        resolve_path=True,
        allow_dash=False,
    ),
    required=False,
    default=".",
    show_default=True,
    help="Directory to search for requirement files. Only used when --add is used.",
)
@click.option(
    "-p",
    "--req-pattern",
    type=str,
    required=True,
    default="requirements*.txt",
    show_default=True,
    help="Filename pattern for searching requirements files.",
)
@click.option(
    "-c",
    "--comment",
    type=str,
    required=False,
    show_default=False,
    help="Comment to be added for the dependency when using --add.",
)
@click.option(
    "--ee",
    "spec",
    flag_value="==",
    required=False,
    help="use == when adding to requirements.",
)
@click.option(
    "--le", "spec", flag_value="<=", help="use <= when adding to requirements."
)
@click.option(
    "--ge", "spec", flag_value=">=", help="use >= when adding to requirements."
)
@click.option(
    "--te", "spec", flag_value="~=", help="use ~= when adding to requirements."
)
def main(package, more, docs, add, req_dir, req_pattern, comment, spec):
    """
    CLI tool to get package info from PyPI and/or manipulate requirements.

    Example usages:

    $ whatsonpypi django
    """
    try:
        # get version if given
        package_, version, spec_ = parse_pkg_string(package)
        result = run_query(
            package_ or package,  # parsed package name can be None
            version,
            more,
            docs,
            add,
            req_dir,
            req_pattern,
            comment,
            spec or spec_,  # override with CLI spec if present
        )
        # output is not always expected and might be None sometimes.
        if result:
            pretty(result)
    except Exception as e:
        raise click.ClickException(str(e))


if __name__ == "__main__":
    main()  # pragma: no cover
