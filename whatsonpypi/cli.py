# -*- coding: utf-8 -*-

"""
Console script
"""

import click

from whatsonpypi import __version__


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(__version__, '-v', '--version')
@click.argument('package')
def main(package):
    """
    CLI tool to

    Example usages:


    """
    try:
        click.secho(package, fg='green', bold=True, underline=True)
    except Exception as e:
        # all other exceptions
        raise click.ClickException(e)


if __name__ == "__main__":
    main()  # pragma: no cover
