Data
====

Data can be in


Raw
===
DMPS raw files contain the raw particle number concentration measured in a size bin as reported by
the condensation particle counter (CPC) in the system, i.e. without applying any inversion and not normalised
to any size bin width.

Raw files naming convention is 'DM' followed by the date in format 'YYYMMDD.DAT'. For example ``DM20170204.DAT``.

Interim
=======
DMPS interim files  contain processed particle number size distributions with the original time resolution
of the instrument.

The entire process includes:

- inversion from electrical particle mobility distribution to particle number size distribution (conversion to dN/dlogDp and multiple charge correction)
- correction for CPC counting efficiency
- correction for internal losses due to particle diffusion
- correction for particle losses from the aerosol inlet to the instrument


Files .cle:
--------------------
1. Row: geometric mean diameters [m]
2. Column: DOY (1.1. at noon = 1.5)
3. Column: Total number concentration /cm3
4. 3 rd to 2 nd last column: dN/dLog(Dp)
5. Last column: Flag

==== ===========
Flag Description
==== ===========
0    Good data, use only this!
1    wind from polluted sector 0-90 degrees
2    wind speed too low, <1 m/s
3    suspect instrument problem
4    suspect local pollution
999  instrument problem or local pollution (years 2015, 2017 data, these were not separated)
==== ===========

Files .sum
----------
Files .sum are the same as .cke without the flag column.

Files .amb
----------
1. Column: DOY (1.1. at noon = 1.5)
2. Column: T [K], measured with TSI on sheath loop
3. Column: press [Pa], measured with press sensor on sheath loop
4. Column: RH [%], measured with humicap on sheath loop
5. Column: sheath flow rate [LPM], measured with TSI on sheath loop
6. Column: sample flow rate [LPM], measured with diff_P on inlet, not exact but indicative!!!

