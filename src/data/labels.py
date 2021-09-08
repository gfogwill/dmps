import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from src.data.localdata import read_interim_file
from datetime import timedelta
import matplotlib.dates as mdates
import matplotlib
from src.utils import clean_dir
from src.paths import processed_data_path, external_data_path, interim_data_path


plt.close('all')
fig, ax = plt.subplots()

mngr = plt.get_current_fig_manager()
mngr.window.setGeometry = (50, 100, 640, 545)

plt.show(block=False)


def manual_labels(input_filepath=None, output_filepath=None, year=None, dataset_name=None, save_X_y=True):
    """Manually label NPF events

    """
    if year is None:
        raise Exception('Year is needed!')
    else:
        year = str(year)

    if input_filepath is None:
        input_filepath = interim_data_path

    if output_filepath is None:
        output_filepath = processed_data_path / f'events-{year}.csv'

    clean_dir(processed_data_path / year)

    data, flags = read_interim_file(input_filepath / dataset_name / f'DMPSmbiocle{year}.dat',
                                    has_flag=True,
                                    year=year,
                                    utc_time=False)

    # for idx, day in data.groupby(pd.Grouper(freq='1d', origin='start')):
    # for file in input_filepath.glob('*.cle'):
    # for idx, day in data.groupby(data.index.date):
    for idx, day in data.groupby(pd.Grouper(freq='1d')):
        plt.cla()
        # fig, ax = plt.subplots()
        plt.pcolor(day.index,
                   day.columns,
                   (np.log10(np.absolute(np.asarray(day)) + 10))[::1, ::1].T,
                   cmap='jet')

        plt.clim(0, 4)
        plt.axhline(y=25, color='r', linestyle='-')
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
        date_str = idx.strftime('%Y-%m-%d')
        plt.title(date_str)

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


# def onclick(event):
#     global ix, iy
#     ix, iy = event.xdata, event.ydata
#     # ix = mdates.num2date(ix)
#
#     # assign global variable to access outside of function
#     global coords
#     coords.append((ix, iy))
#
#     # Disconnect after 2 clicks
#     if len(coords) == 2:
#         fig.canvas.mpl_disconnect(cid)
#         plt.close(1)
#     return
#
#
# coords = []
#
# plt.close('all')
# fig, ax = plt.subplots()
#
# cid = fig.canvas.mpl_connect('button_press_event', onclick)
#
# mngr = plt.get_current_fig_manager()
# mngr.window.setGeometry = (50, 100, 640, 545)
#
# plt.show(block=False)
#
#
# def manual_labels(input_filepath=None, output_filepath=None, year=None, save_X_y=True, freq='7D'):
#     """Manually label NPF events
#
#     """
#     if input_filepath is None:
#         input_filepath = external_data_path / f'DMPSmbiocle{year}.dat'
#
#     if output_filepath is None:
#         output_filepath = processed_data_path / f'events-{year}.csv'
#
#     if year is None:
#         raise Exception('Year is needed!')
#     else:
#         year = str(year)
#
#     clean_dir(processed_data_path / year)
#
#     data, flags = read_interim_file(input_filepath,
#                                     has_flag=True, year=year, utc_time=False)
#
#     # for idx, day in data.groupby(pd.Grouper(freq='1d', origin='start')):
#     # for file in input_filepath.glob('*.cle'):
#     # for idx, day in data.groupby(data.index.date):
#     for idx, day in data.groupby(pd.Grouper(freq=freq)):
#         plt.cla()
#         # fig, ax = plt.subplots()
#         plt.pcolor(day.index,
#                    day.columns,
#                    (np.log10(np.absolute(np.asarray(day)) + 10))[::1, ::1].T,
#                    cmap='jet')
#
#         plt.clim(0, 4)
#         plt.axhline(y=25, color='r', linestyle='-')
#         ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
#         date_str = idx.strftime('%Y-%m-%d')
#         plt.title(date_str)
#
#         plt.yscale('log')
#         plt.draw()
#
#         rta = input('Ingrese una opcion (s/e/d/f):  ')
#
#         if rta == 's':
#             print('la')
#         elif rta == 'e':
#
#
#         else:
#             break
#         # if rta == 's':
#         #     with open(output_filepath, 'a') as fo:
#         #         rta2 = input('¿Hay evento?')
#         #         if rta2 == 's':
#         #             ask_input = True
#         #             while ask_input:
#         #                 start = input('Inicio: ')
#         #                 end = input('Fin: ')
#         #                 start = f'{start[0:2]}:{start[2:]}:00'
#         #                 end = f'{end[0:2]}:{end[2:]}:00'
#         #                 fo.write(f'{date_str},{start},{end},e\n')
#         #                 rta3 = input('¿Otro?: ')
#         #                 if rta3 == 'n':
#         #                     ask_input = False
#         #         else:
#         #             fo.write(f'{date_str},00:00:00,23:59:00,ne\n')
#         #     if save_X_y:
#         #         day.to_csv(processed_data_path / year / f'{date_str}.csv')
#         # elif rta == 'n':
#         #     continue
#         # elif rta == 'f':
#         #     break

if __name__ == '__main__':
    manual_labels(year=2015)
