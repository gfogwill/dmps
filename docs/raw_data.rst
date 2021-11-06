Raw data description
====================

## .DAT files

DMPS raw files contain the raw particle number concentration measured in a size bin as reported by
the condensation particle counter (CPC) in the system, i.e. without applying any inversion and not normalised
to any size bin width.

Raw files naming convention is 'DM' followed by the date in format 'YYYMMDD.DAT'. For example ``DM20170204.DAT``.


names_odd_rows = ['hour', 'minute', 'second',
                  'AT', 'AP', 'RH', 'NA', 'excess_flow', 'sample_flow',
                  'voltage_1', 'voltage_2', 'voltage_3', 'voltage_4', 'voltage_5', 'voltage_6', 'voltage_7',
                  'voltage_8', 'voltage_9', 'voltage_10',
                  'voltage_11', 'voltage_12', 'voltage_13', 'voltage_14', 'voltage_15', 'voltage_16', 'voltage_17',
                  'voltage_18', 'voltage_19', 'voltage_20',
                  'voltage_21', 'voltage_22', 'voltage_23', 'voltage_24', 'voltage_25']


names_even_rows = ['hour', 'minute', 'second',
                   'AT', 'AP', 'RH', 'NA', 'excess_flow', 'sample_flow',
                   'concentration_1', 'concentration_2', 'concentration_3', 'concentration_4', 'concentration_5',
                   'concentration_6', 'concentration_7', 'concentration_8', 'concentration_9', 'concentration_10',
                   'concentration_11', 'concentration_12', 'concentration_13', 'concentration_14',
                   'concentration_15', 'concentration_16', 'concentration_17', 'concentration_18',
                   'concentration_19', 'concentration_20',
                   'concentration_21', 'concentration_22', 'concentration_23', 'concentration_24',
                   'concentration_25']



## .LOG files