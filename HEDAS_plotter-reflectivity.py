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
    ds=HEDASds(file)
    # print(ds.getime())
    print(ds.number_of_files)
    filestrparts=file.split('_')
    datetimestring=filestrparts[1]
    analysis_present.append(ds.getime())

    land=ds.get_vbl('LAND_surface')[0]

    ref=ds.get_vbl('REFC_atmoscol')[0]
    # lv=32
    cbrange_dbz=np.arange(0,65.0001,1)

    plt.contourf(ref, levels=cbrange_dbz, cmap=cm.jet, extend='both')
    cl=plt.colorbar()
    cl.ax.set_title('dBZ')

    plt.contour(land,levels=1,colors='black')
    plt.title('Composite Reflectivity\n%s UTC'%(ds.getime()))
    # plt.plot(ctr[0], ctr[1],'ro')

    PTG=plt.gcf()
    PTG.set_size_inches(7,6) 

    # plt.savefig('Datacoverage-HEDAS_%03d.png'%ds.number_of_files, bbox_inches="tight", dpi=500)
    plt.savefig('Datacoverage-HEDAS_%s.png'%datetimestring, bbox_inches="tight", dpi=500)
    plt.clf()

    # pass
    # print(file)
    # filestrparts=file.split('_')
    # print(filestrparts[1])
    # datetimestring=filestrparts[1]



