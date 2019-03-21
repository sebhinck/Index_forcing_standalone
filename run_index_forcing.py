from netCDF4 import Dataset
import os
import sys
import numpy as np

#Set Path to the folder containing this script
script_dir = '.'

sys.path.append(os.path.abspath(script_dir))

import index_forcing as indf

#Define NC files containing climate and topography information
LGM_file = '/scratch/users/shinck/IceModelling/data/processed/NorthAmerica/Index/NGRIP_PI_LGM_forcing_120ky_50y_20km.nc'
PD_file = '/scratch/users/shinck/IceModelling/data/processed/NorthAmerica/Index/NGRIP_PI_LGM_forcing_120ky_50y_20km.nc'
current_file = None

#Set index
index = 0.5

#Set other parameters
temp_lapse_rate = 5. #K/km
precip_decay_rate = np.log(2.) #1/km
precip_thresh_height = 5. #km

time_idx = 1

#Load LGM climate
try:
    with Dataset(LGM_file) as ncLGM:
        precip1 = ncLGM.variables['precip_1'][time_idx,:,:]
        temp1 = ncLGM.variables['airtemp_1'][time_idx,:,:]
        h1 = ncLGM.variables['usurf_1'][:,:]
except:
    print("Error reading LGM data!")
    raise

#Load PD climate
try:
    with Dataset(PD_file) as ncPD:
        precip0 = ncPD.variables['precip_0'][time_idx,:,:]
        temp0 = ncPD.variables['airtemp_0'][time_idx,:,:]
        h0 = ncPD.variables['usurf_0'][:,:]
except:
    print("Error reading PD data!")
    raise

#Load PD climate
try:
    with Dataset(current_file) as ncCur:
        h = ncCur.variables['topo'][:]
except:
    print("Error reading current topography! Use PD topography instead")
    h = h1.copy()


temp_cur, precip_cur = indf.index_forcing(precip0, 
                                          temp0, 
                                          precip1, 
                                          temp1, 
                                          h, 
                                          index, 
                                          temp_lapse_rate, 
                                          precip_decay_rate, 
                                          precip_thresh_height)

