import os
srcpath=os.getcwd()
os.chdir(srcpath)
import netCDF4 as NC
import numpy as np
import matplotlib as mpl
import sys
import glob
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import datetime as dt
import xarray as xr
# from metpy import calc
from HEDAS_pkg import HEDASds
from tdr_tc_centering_with_example import recenter_tc

import concurrent.futures

# os.chdir(srcpath+'\\'+"HEDAS") 
# print(os.getcwd())


os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian') 
# print(os.getcwd())

list_of_HEDASfiles=[]
allstacks=[]

for findex, file in enumerate(sorted(glob.glob("*.nc"))):
# for findex, file in enumerate(sorted(glob.glob("*.nc"))[0:39]): 
### ^ EXAMPLE option for Windward file times
    list_of_HEDASfiles.append(file)


def MP_centerstack_function(file):
    ds=HEDASds(file)
    filestrparts=file.split('_')
    datetimestring=filestrparts[1]
    print(datetimestring) #prints each time a new file is being processes
    cstack=ds.get_centerstack() #all center stack returns from TCR center finder
    ctrxys=np.array([cstack[6],cstack[5]]) #get the x and y grid indices into an array
    return ctrxys

with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(MP_centerstack_function, list_of_HEDASfiles)

    for result in results:
        allstacks.append(result) #put all these arrays into a big list

#started at 5:07PM Completed 5:49  = ~42 minutes
os.chdir(srcpath)

#store that into the .npy file
np.save('stored_centers_Dorian', allstacks)
print('Save complete!')


## WINDWARD         0-38 [0:39]
## E CARIB          39-45 [39:46]
## PUERTO RICO      46-63 [46:64]
## ATL1             64-67 [64:68]
## ATL2             68-71 [64:68]
## ATL3             71-76 [64:68]
## ATL4             77-79 [64:68]
## ATL5             80-85 [64:68]
## ATL-Bahamas      86-91 [64:68] 08-31 2300 => 09-01 0130
## GREAT ABACO      92-95 [92:96] 0901 1300 0901 1500
## GRAND BHMA1      96-103 [96:104]
## GRAND BHMA2      104-108 [104:109]
## GULF STRM FL     109-117 [109:118]
## GULF STRM GA/SC  118-127 [118:128]
## GULF STRM SC/NC  128-136 [128:137]