# -*- coding: utf-8 -*-

"""
Console script
"""
from __future__ import unicode_literals  # unicode support for py2

import click
from whatsonpypi import __version__

from .utils import pretty
from .whatsonpypi import get_query_response


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(__version__, '-v', '--version')
@click.argument('package')
@click.option(
    '-m',
    '--more',
    is_flag=True,
    required=True,
    default=False,
    show_default=True,
    help="Flag to enable expanded output"
)
def main(package, more):
    """
    CLI tool to find the latest version of a package on PyPI.

    Example usages:

    $ whatsonpypi django
    """
    try:
        output = get_query_response(
            package=package,
            more_out=more,
        )
        pretty(output)
    except Exception as e:
        # all other exceptions
        raise click.ClickException(e)


if __name__ == "__main__":
    main()  # pragma: no cover
