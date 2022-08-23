import pathlib
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

from .localdata import read_cle_file

import matplotlib.dates as mdates

from ..utils import clean_dir
from ..paths import processed_data_path, external_data_path


plt.close('all')
fig, ax = plt.subplots()

mngr = plt.get_current_fig_manager()
mngr.window.setGeometry = (50, 100, 640, 545)

plt.show(block=False)


def manual_labels(input_filepath=None, output_filepath=None, year=None, dataset_name=None, save_X_y=True,
                  analysis_freq='1d'):
    """Manually label NPF events

    """

    if year is None:
        raise Exception('Year is needed!')
    else:
        year = str(year)

    if input_filepath is None:
        input_filepath = pathlib.Path(external_data_path)
    else:
        input_filepath = pathlib.Path(input_filepath)

    if output_filepath is None:
        output_filepath = processed_data_path / f'events-{year}.csv'

    clean_dir(processed_data_path / year)

    data, flag = read_cle_file(input_filepath / dataset_name / f'DMPSmbiocle{year}.dat',
                               has_flag=True,
                               year=year,
                               utc_time=False)

    for idx, day in data.groupby(pd.Grouper(freq=analysis_freq)):
        plt.cla()

        plt.pcolor(day.index,
                   day.columns,
                   (np.log10(np.absolute(np.asarray(day)) + 10))[::1, ::1].T,
                   cmap='jet')

        plt.clim(0, 4)
        plt.axhline(y=25, color='r', linestyle='-')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        date_str = idx.strftime('%Y-%m-%d')
        plt.title(date_str)
        fig.autofmt_xdate()

        plt.yscale('log')
        plt.draw()

        rta = input('¿Usar? (s/n): ')

        if rta == 's':
            with open(output_filepath, 'a') as fo:
                rta2 = input('¿Hay evento?')
                if rta2 == 's':
                    ask_input = True
                    while ask_input:
                        start = input('Inicio: ')
                        end = input('Fin: ')
                        start = f'{start[0:2]}:{start[2:]}:00'
                        end = f'{end[0:2]}:{end[2:]}:00'
                        fo.write(f'{date_str},{start},{end},e\n')
                        rta3 = input('¿Otro?: ')
                        if rta3 == 'n':
                            ask_input = False
                else:
                    fo.write(f'{date_str},00:00:00,23:59:00,ne\n')
            if save_X_y:
                day.to_csv(processed_data_path / year / f'{date_str}.csv')
        elif rta == 'n':
            continue
        elif rta == 'f':
            break


if __name__ == '__main__':
    manual_labels()

