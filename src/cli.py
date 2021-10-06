import pandas

from datetime import date

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
@click.option('--start-date', type=click.DateTime(formats=["%Y-%m-%d"]), default=str(date.today()))
@click.option('--end-date', type=click.DateTime(formats=["%Y-%m-%d"]), default=str(date.today()))
@click.option('--dataset-name', type=str, default='mbi-ea')
@click.option('--analysis-freq', type=str, default='1d')
def npf(input_filepath, output_filepath, start_date, end_date, dataset_name, analysis_freq):
    """Mannualy label new particle formation events of DMPS files

        input_filepath: path
        output_filepath: path
    # """

    src.data.labels.manual_labels(input_filepath=input_filepath,
                                  output_filepath=output_filepath,
                                  dataset_name=dataset_name,
                                  analysis_freq=analysis_freq)


if __name__ == '__main__':
    cli()
