# this is the server version it has more capability
# the titles are labeled by date/time and the plot is more fleshed out
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
from HEDAS_pkg import HEDASds

fname="stored_centers_Dorian.npy" 

center_file = np.load(fname)

cxs=center_file[:,0] # all x stacks
cys=center_file[:,1] # all y stacks
# stacklvs=[100, 200, 300, 400, 500, 600, 700, 800, 900]
stacklvs=[200, 300, 400, 500, 600, 700, 800, 900]

os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian') #go to the folder with the netCDF HEDAS data
for findex, hfile in enumerate(sorted(glob.glob("*.nc"))):
    os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian') #go to the folder with the netCDF HEDAS data

    cxsi=cxs[findex][1:] #the [1:] removes the 100mb level center from being plotted
    cysi=cys[findex][1:] #because the center stack goes from 100mb to 900mb

    ctr=(cxsi[-1],cysi[-1]) #grabs the lowest level (900mb) and sets it as the TC center

    adjcxs=cxsi-ctr[0]
    adjcys=cysi-ctr[1]

    ds=HEDASds(hfile) #read in the the netCDF file
    ds.center_relative_winds(ctr) #calculate wind fields
    # lat=ds.get_vbl('NLAT_surface')[0]
    # lon=ds.get_vbl('ELON_surface')[0]
    plt.contour(ds.radius,levels=[25,50],colors='gray')
    # PT=plt.scatter(adjcxs,adjcys,c=stacklvs,cmap=cm.jet)
    # plt.plot(adjcxs,adjcys,'k')
    PT=plt.scatter(cxsi,cysi,c=stacklvs,cmap=cm.jet)
    plt.plot(cxsi,cysi,'k')
    cb1=plt.colorbar(PT)
    cb1.set_label('mb')
    plotradius=50 #50 grid boxes
    # plt.xlim(ctr[0]-plotradius,ctr[0]+plotradius)
    # plt.ylim(ctr[1]-plotradius,ctr[1]+plotradius)
    plt.xlim(ctr[0]-plotradius,ctr[0]+plotradius)
    plt.ylim(ctr[1]-plotradius,ctr[1]+plotradius)
    plt.title(f'Vortex centers by pressure level\n{ds.getime()}')

    # plt.show()
    print(ds.getime())
    os.chdir(srcpath)
    plt.savefig("tilt_%s.png"%ds.datetimestring, bbox_inches="tight") #, dpi=400
    plt.clf()

