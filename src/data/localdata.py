"""
Custom dataset processing/generation functions should be added to this file
"""
import logging

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ..paths import raw_data_path


def read_cle_file(filename, has_flag=True, col_names=None, year=None, utc_time=True,
                  resample_freq='10T', keep_valid=True):
    """Read a DMPS inverted .cle file

    Data is multiple space-delimited. The file contains processed particle number size
    distributions with the original time resolution of the instrument.

    Parameters
    ----------
    filename: path-like

    has_flag: boolean
        if true, last column is treated as a flag
    col_names: arry-like, optional
        list of column names to use. Duplicates in this list are not allowed
    resample_freq: str
        frequency to resample the data. Mean is used
    keep_valid: bool
        if true, return only data with flag 0 and replace the rest with nan's

    Returns
    -------
    data: DataFrame

    """

    # Infere year from filename
    # year = int(filename.stem[2:6])
    if year is None:
        raise Exception('Year is needed!')
    else:
        year = int(year)

    df = pd.read_csv(filename, delim_whitespace=True)

    if col_names is None:
        # Rename columns
        df.columns.values[0] = 'datetime'
        df.columns.values[1] = 'tot_conc'

        if has_flag:
            df.columns.values[-1] = 'flag'
    else:
        df.columns = col_names

    # Convert decimal day of year to datetime column to dataframe index
    df['datetime'] = df['datetime'].apply(lambda ddoy: datetime(year - 1, 12, 31) + timedelta(days=ddoy))
    df.set_index('datetime', inplace=True)

    if resample_freq is not None:
        df = df.resample(resample_freq).mean()

    df.drop('tot_conc', axis=1, inplace=True)

    flags = df['flag']

    if keep_valid:
        df.loc[flags == 1] = np.nan
        df.loc[flags == 2] = np.nan
        df.loc[flags == 3] = np.nan
        df.loc[flags == 4] = np.nan

    df.drop('flag', axis=1, inplace=True)

    df.columns = [float(i) * 1e9 for i in df.columns]

    if not utc_time:
        df.index = df.index - timedelta(hours=3)
        # df.index = df.index.tz_localize(tz='UTC').tz_convert(tz='America/Argentina/Buenos_Aires')

    return df, flags


def read_raw_dmps(date) -> pd.DataFrame:
    """ Reads raw data from directory ../data/raw and returns a pandas DataFrame

    """
    
    fi = raw_data_path / date.strftime(format="DM%Y%m%d.DAT")

    logging.info('File name: ' + fi)

    year = date.year
    month = date.month
    day = date.day

    # Read odd rows (starting with first line)
    names_odd_rows = ['hour', 'minute', 'second',
                      'temp', 'press', 'hum', 'NA', 'excess', 'sample',
                      'voltage_1', 'voltage_2', 'voltage_3', 'voltage_4', 'voltage_5', 'voltage_6', 'voltage_7',
                      'voltage_8', 'voltage_9', 'voltage_10',
                      'voltage_11', 'voltage_12', 'voltage_13', 'voltage_14', 'voltage_15', 'voltage_16', 'voltage_17',
                      'voltage_18', 'voltage_19', 'voltage_20',
                      'voltage_21', 'voltage_22', 'voltage_23', 'voltage_24', 'voltage_25']
    
    data_even_rows = pd.read_csv(fi, sep='\t', skiprows=lambda x: x % 2 == 1, names=names_odd_rows)

    data_even_rows['year'] = year
    data_even_rows['month'] = month
    data_even_rows['day'] = day
    data_even_rows.index = pd.to_datetime(data_even_rows[['year', 'month', 'day', 'hour', 'minute', 'second']])

    names_even_rows = ['hour', 'minute', 'second',
                       'temp', 'press', 'hum', 'NA', 'excess', 'sample',
                       'concentration_1', 'concentration_2', 'concentration_3', 'concentration_4', 'concentration_5',
                       'concentration_6', 'concentration_7', 'concentration_8', 'concentration_9', 'concentration_10',
                       'concentration_11', 'concentration_12', 'concentration_13', 'concentration_14',
                       'concentration_15', 'concentration_16', 'concentration_17', 'concentration_18',
                       'concentration_19', 'concentration_20',
                       'concentration_21', 'concentration_22', 'concentration_23', 'concentration_24',
                       'concentration_25']

    data_odd_rows = pd.read_csv(fi, sep='\t', skiprows=lambda x: x % 2 == 0, names=names_even_rows)
    data_odd_rows['year'] = year
    data_odd_rows['month'] = month
    data_odd_rows['day'] = day
    data_odd_rows.index = pd.to_datetime(data_odd_rows[['year', 'month', 'day', 'hour', 'minute', 'second']])

    data = pd.concat([data_even_rows, data_odd_rows], axis=1)
    data = data.drop(['year', 'month', 'day', 'hour', 'minute', 'second'], axis=1)
    data = data.loc[:, ~data.columns.duplicated()]

    return data
