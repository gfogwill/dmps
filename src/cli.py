from src import __version__ as version

import click

LOGO = rf"""
______ ___  _________  _____ 
|  _  \|  \/  || ___ \/  ___|
| | | || .  . || |_/ /\ `--. 
| | | || |\/| ||  __/  `--. \
| |/ / | |  | || |    /\__/ /
|___/  \_|  |_/\_|    \____/ 
                            v{version}
"""


@click.group(context_settings=dict(help_option_names=["-h", "--help"]), name="DMPS")
@click.version_option(version, "--version", "-V", help="Show version and exit")
def cli():  
    """dmps is a CLI for working with DMPS observations data. For more
    information, type ``dmps info``.
    """
    pass


@cli.command()
def info():
    """Get more information about kedro."""
    click.secho(LOGO, fg="green")
    click.echo(
        "\n"
    )
