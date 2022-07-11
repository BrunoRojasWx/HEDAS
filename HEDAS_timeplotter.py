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
    # ds=HEDASds(file)
    # print(ds.getime())
    # analysis_present.append(ds.getime())

    # pass
    # print(file)
    filestrparts=file.split('_')
    print(filestrparts[1])
    datetimestring=filestrparts[1]
    yr=int(datetimestring[0:4])
    mo=int(datetimestring[4:6])
    dy=int(datetimestring[6:8])
    hr=int(datetimestring[8:10])
    mn=int(datetimestring[10:12])
    fdatetime=dt.datetime(year=yr,month=mo,day=dy,hour=hr,minute=mn)    #file date time object
    print(fdatetime)
    analysis_present.append(fdatetime)


os.chdir(srcpath)


fig, ax1 = plt.subplots()
# plt.figure(figsize=(10,7))
for analysis in analysis_present:
    ax1.axvline(analysis, color='b') #where analysis is present


ax1.axvline(dt.datetime(2019,8,28,00,00), color='k', alpha=0.6) #where analysis is present
ax1.axvline(dt.datetime(2019,8,29,00,00), color='k', alpha=0.6) #where analysis is present
ax1.axvline(dt.datetime(2019,8,30,00,00), color='k', alpha=0.6) #where analysis is present
ax1.axvline(dt.datetime(2019,8,31,00,00), color='k', alpha=0.6) #where analysis is present
ax1.axvline(dt.datetime(2019,9,1,00,00), color='k', alpha=0.6) #where analysis is present
ax1.axvline(dt.datetime(2019,9,2,00,00), color='k', alpha=0.6) #where analysis is present
ax1.axvline(dt.datetime(2019,9,3,00,00), color='k', alpha=0.6) #where analysis is present
ax1.axvline(dt.datetime(2019,9,4,00,00), color='k', alpha=0.6) #where analysis is present
ax1.axvline(dt.datetime(2019,9,5,00,00), color='k', alpha=0.6) #where analysis is present
ax1.axvline(dt.datetime(2019,9,6,00,00), color='k', alpha=0.6) #where analysis is present 

plt.xticks(rotation=90)
# plt.xlim(analysis_present[0], analysis_present[-1])
ax1.set_xlim(dt.datetime(2019,8,27,00,00),dt.datetime(2019,9,6,12,00)) #bounds the time shown (10th-17th)
PTG=plt.gcf()
PTG.set_size_inches(13,5)
plt.savefig('Datacoverage-HEDAS2.png', bbox_inches="tight", dpi=500)
