# Index forcing

The Python function `index_forcing` in `index_forcing.py` applies the same forcing as the PISM atmosphere model `index`.

The function takes following arguments:
- precip0 - Precipitation field at PD
- temp0 - Air temperature field at PD
- h0 - Surface elevation field at PD
- precip1 - Precipitation field at LGM
- temp1 - Air temperature field at LGM
- h1 - Surface elevation field at LGM
- h - Surface elevation field at which results should be given
- index - Index used for interpolation: 0 = PD, 1 = LGM
- temp_lapse_rate - Rate at which temperature decreases with height [K/km]
- precip_decay_rate - Rate at which the precipitation decays above precip_thresh_height
- precip_thresh_height - Height above which precipitation exponentially decays


The Script `run_index_forcing` sets all parameters and loads the data used by the `index_forcing` function, and calls it.
To get in working the path `script_dir` needs to be set to the folder that contains the scripts.
The netCDF-files and respective variable names must be defined to read the PD and LGM climate states.

The part where the actual data is read from the file might need to be adjusted to the format of input files.
