from src import __version__

from src.data.localdata import read_raw_dmps
from src.data.inverter import invert

import src.data.labels

import click
import logging

from datetime import date

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


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
    click.echo("\n")


@cli.command()
@click.option('--input-filepath', type=click.Path(exists=True), default=None)
@click.option('--output-filepath', type=click.Path(), default=None)
@click.option('--year', type=int)
@click.option('--dataset-name', type=str, default='mbi-cle')
@click.option('--analysis-freq', type=str, default='1d')
def npf(input_filepath, output_filepath, year, dataset_name, analysis_freq):
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
                                  dataset_name=dataset_name,
                                  analysis_freq=analysis_freq)


@cli.command()
@click.option('--start-date', type=click.DateTime(formats=["%Y-%m-%d"]), default=str(date.today()))
@click.option('--end-date', type=click.DateTime(formats=["%Y-%m-%d"]), default=None)
@click.option('--output-filepath', type=click.Path(), default=None)
def plot(start_date, end_date, output_filepath):
    """Plot DMPS inverted data

        start-date: datetime
        end-date: datetime
    # """
    data = []
    
    if end_date is None:
        data = read_raw_dmps(start_date)
    
    else:
        datelist = pd.date_range(start=start_date, end=end_date).to_pydatetime().tolist()

        for d in datelist:
            try:
                df = read_raw_dmps(d)
                
            except FileNotFoundError:
                logging.warning(f"File not found for date: {d}")
                continue
        
            data.append(df)    
            
        data = pd.concat(data, axis=0)

    inv_data = invert(data)
    
    plt.pcolor(inv_data.index, inv_data.columns, np.log10(abs(inv_data.values[::1, ::1].T)+1e-6), cmap='jet')

    plt.clim(0, 4)
    plt.yscale('log')
    
    if output_filepath is None:
        plt.show()
    else:
        plt.savefig(output_filepath)


if __name__ == '__main__':
    cli()
