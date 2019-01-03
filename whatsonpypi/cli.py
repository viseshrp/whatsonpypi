# -*- coding: utf-8 -*-

"""
Console script
"""

import click

from whatsonpypi import __version__
from .whatsonpypi import get_query_response


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(__version__, '-v', '--version')
@click.argument('package')
def main(package):
    """
    CLI tool to find the latest version of a package on PyPI.

    Example usages:

    $ whatsonpypi django

    """
    try:
        click.secho(get_query_response(package=package), fg='green', bold=True)
    except Exception as e:
        # all other exceptions
        raise click.ClickException(e)


if __name__ == "__main__":
    main()  # pragma: no cover
