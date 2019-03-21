from netCDF4 import Dataset
import os
import sys
import numpy as np

#Set Path to the folder containing this script
script_dir = '.'

sys.path.append(os.path.abspath(script_dir))

import index_forcing as indf

#Set time index of climate fields read from nc files
#Might need to be adjusted to your input file
time_idx = 1

#Define NC files containing climate and topography information
LGM_file = '/FILE/CONTAINING/LGM_CLIMATE.nc'
LGM_precip_name = 'precip_1'
LGM_temp_name = 'airtemp_1'
LGM_topo_name = 'usurf_1'

PD_file = '/FILE/CONTAINING/PD_CLIMATE.nc'
PD_precip_name = 'precip_0'
PD_temp_name = 'airtemp_0'
PD_topo_name = 'usurf_0'

#If not set PD topography is used...
current_file = None
current_topo_name = 'usurf'

#Set index
index = 0.5

#Set other parameters
temp_lapse_rate_K_km = 5. #K/km
precip_decay_rate_1_km = np.log(2.) #1/km
precip_thresh_height_km = 5. #km


####################################################################
####################################################################
#Loading the data

#Load LGM climate
try:
    with Dataset(LGM_file) as ncLGM:
        precip1 = ncLGM.variables[LGM_precip_name][time_idx,:,:]
        temp1 = ncLGM.variables[LGM_temp_name][time_idx,:,:]
        h1 = ncLGM.variables[LGM_topo_name][:,:]
except:
    print("Error reading LGM data!")
    raise

#Load PD climate
try:
    with Dataset(PD_file) as ncPD:
        precip0 = ncPD.variables[PD_precip_name][time_idx,:,:]
        temp0 = ncPD.variables[PD_temp_name][time_idx,:,:]
        h0 = ncPD.variables[PD_topo_name][:,:]
except:
    print("Error reading PD data!")
    raise

#Load PD climate
try:
    with Dataset(current_file) as ncCur:
        h = ncCur.variables[current_topo_name][:]
except:
    print("No current topography found -> Using PD topography instead")
    h = h1.copy()

####################################################################

###################################################################
#Do not edit, taking care of correct units!
temp_lapse_rate = temp_lapse_rate_K_km / 1.e3 #K/m
precip_decay_rate = precip_decay_rate_1_km / 1.e3 #1/m
precip_thresh_height = precip_thresh_height_km * 1.e3 #m
###################################################################

####################################################################
####################################################################
#Call actual function

temp_cur, precip_cur = indf.index_forcing(precip0, 
                                          temp0, 
                                          h0,
                                          precip1, 
                                          temp1, 
                                          h1,
                                          h, 
                                          index, 
                                          temp_lapse_rate, 
                                          precip_decay_rate, 
                                          precip_thresh_height)
