# -*- coding: utf-8 -*-

import click
import logging
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
from .datasets import process_raw_datasets
from ..log import logger


@click.command()
@click.argument('action')
def main(action, raw_datasets=None):
    """Fetch and/or process the raw data
    Raw files are downloaded into .paths.raw_data_path
    Interim files are generated in .paths.interim_data_path
    Processed data files are saved in .paths.processed_data_path
    action: {'fetch', 'unpack', 'process'}
    """
    process_raw_datasets(raw_datasets=raw_datasets, action=action)


if __name__ == '__main__':
    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()


#
# @click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
# def main(input_filepath, output_filepath):
#     """ Runs data processing scripts to turn raw data from (../raw) into
#         cleaned data ready to be analyzed (saved in ../processed).
#     """
#     logger = logging.getLogger(__name__)
#     logger.info('making final data set from raw data')
#
#
# if __name__ == '__main__':
#     log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     logging.basicConfig(level=logging.INFO, format=log_fmt)
#
#     # not used in this stub but often useful for finding various files
#     project_dir = Path(__file__).resolve().parents[2]
#
#     # find .env automagically by walking up directories until it's found, then
#     # load up the .env entries as environment variables
#     load_dotenv(find_dotenv())
#
#     main()
