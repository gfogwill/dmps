
import click
from click.utils import get_os_args

LOGO = rf"""
DMPS
v{version}
"""


@click.group(context_settings=CONTEXT_SETTINGS, name="DMPS")
@click.version_option(version, "--version", "-V", help="Show version and exit")
def cli():  # pragma: no cover
    """dmps is a CLI for working with DMPS observations data. For more
    information, type ``dmps info``.a
    """
    pass


@cli.command()
def info():
    """Get more information about kedro."""
    click.secho(LOGO, fg="green")
    click.echo(
        "\n"
    )
