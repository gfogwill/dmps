# -*- coding: utf-8 -*-
import pathlib

import click
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

from ..paths import processed_data_path, catalog_path
from .labels import manual_labels

from ..log import logger


@click.command()
@click.option('--input_filepath', type=click.Path(exists=True), default=None)
@click.option('--output_filepath', type=click.Path(), default=None)
@click.option('--year', type=int)
def main(input_filepath, output_filepath, year):
    """ uns script to mannualy label new particle formation events of DMPS files

        (../raw) intoleaned data ready to be analyzed (saved in ../processed).

        input_filepath: path
        output_filepath: path
    # """

    if year is None:
        click.prompt("Year to process: ", type=int)

    manual_labels(input_filepath=input_filepath,
                  output_filepath=output_filepath,
                  year=year)


if __name__ == '__main__':
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
