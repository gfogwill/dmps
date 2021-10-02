from src import __version__

import src.data.labels

import click

LOGO = rf"""
______ ___  _________  _____ 
|  _  \|  \/  || ___ \/  ___|
| | | || .  . || |_/ /\ `--. 
| | | || |\/| ||  __/  `--. \
| |/ / | |  | || |    /\__/ /
|___/  \_|  |_/\_|    \____/ 
                            v{__version__}
"""


@click.group(context_settings=dict(help_option_names=["-h", "--help"]), name="DMPS")
@click.version_option(__version__, "--version", "-V", help="Show version and exit")
def cli():  
    """dmps is a CLI for working with DMPS observations data. For more
    information, type ``dmps info``.
    """
    pass


@cli.command()
def info():
    """Get more information about dmps."""
    click.secho(LOGO, fg="green")
    click.echo(
        "\n"
    )


@cli.command()
@click.option('--input-filepath', type=click.Path(exists=True), default=None)
@click.option('--output-filepath', type=click.Path(), default=None)
@click.option('--year', type=int)
@click.option('--dataset-name', type=str)
def npf(input_filepath, output_filepath, year, dataset_name):
    """Mannualy label new particle formation events of DMPS files

        input_filepath: path
        output_filepath: path
    # """

    if year is None:
        year = click.prompt("Year to process?")

    if dataset_name is None:
        dataset_name = click.prompt("Dataset name?")

    src.data.labels.manual_labels(input_filepath=input_filepath,
                              output_filepath=output_filepath,
                              year=year,
                              dataset_name=dataset_name)

