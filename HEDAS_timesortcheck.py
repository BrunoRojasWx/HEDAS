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

# os.chdir(srcpath+'\\'+"HEDAS") 
# print(os.getcwd())


os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian') 
# print(os.getcwd())

analysis_present=[]
for findex, file in enumerate(sorted(glob.glob("*.nc"))):
# for findex, file in enumerate(sorted(glob.glob("*.nc"))[0:39]): 
### ^ EXAMPLE option for Windward file times

    # ds=HEDASds(file)
    # print(ds.getime())
    # analysis_present.append(ds.getime())

    # pass
    # # print(file)

    filestrparts=file.split('_')
    # print(filestrparts[1])
    datetimestring=filestrparts[1]
    # yr=int(datetimestring[0:4])
    # mo=int(datetimestring[4:6])
    # dy=int(datetimestring[6:8])
    # hr=int(datetimestring[8:10])
    # mn=int(datetimestring[10:12])
    # fdatetime=dt.datetime(year=yr,month=mo,day=dy,hour=hr,minute=mn)    #file date time object
    # print(fdatetime)
    # analysis_present.append(fdatetime)
    print(findex,datetimestring)


## WINDWARD         0-38 [0:39]
## E CARIB          39-45 [39:46]
## PUERTO RICO      46-63 [46:64]
## ATL1             64-67 [64:68]
## ATL2             68-71 [64:68]
## ATL3             72-76 [64:68]
## ATL4             77-79 [64:68]
## ATL5             80-85 [64:68]
## ATL-Bahamas      86-91 [64:68] 08-31:2300 - 09-01:0130
## GREAT ABACO      92-95 [92:96] 09-01:1300 - 09-01:1500
## GRAND BHMA1      96-103 [96:104]
## GRAND BHMA2      104-108 [104:109]
## GULF STRM FL     109-117 [109:118]
## GULF STRM GA/SC  118-127 [118:128]
## GULF STRM SC/NC  128-136 [128:137]