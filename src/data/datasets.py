import json
import os
import pathlib
from functools import partial
from collections import Counter, defaultdict
from collections.abc import MutableMapping
import pandas as pd
import datetime


from ..logging import logger
from ..utils import load_json, save_json


__all__ = [
    'read_cle'
]


def read_cle(filename, has_flag=False, col_names=None):
    """Read a DMPS inverted .cle file

    Data is multiple space-delimited. The file contains processed particle number size
    distributions with the original time resolution of the instrument.

    Parameters
    ----------

    has_flag: boolean
        if true, last column is treated as a flag

    col_names: arry-like, optional
        list of column names to use. Duplicates in this list are not allowed.

    Returns
    -------
    (data, flag, metadata)
    """

    # Infere year from filename
    year = int(filename.stem[2:6])

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

    df.drop('tot_conc', axis=1, inplace=True)
    df.drop('flag', axis=1, inplace=True)

    df.columns = [float(i) * 1e9 for i in df.columns]

    return df
