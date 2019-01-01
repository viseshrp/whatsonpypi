# -*- coding: utf-8 -*-

"""
Console script
"""

import click

from .whatsonpypi import run


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.argument('package')
def main(package):
    """
    CLI tool to

    Example usages:


    """
    try:
        run(package)
    except Exception as e:
        # all other exceptions
        raise click.ClickException(e)


if __name__ == "__main__":
    main()  # pragma: no cover
