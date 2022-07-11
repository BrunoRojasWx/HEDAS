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
import concurrent.futures


fname="stored_centers_Dorian.npy" 

center_file = np.load(fname)


cxs=center_file[:,0] # all x stacks
cys=center_file[:,1] # all y stacks
# stacklvs=[100, 200, 300, 400, 500, 600, 700, 800, 900]
stacklvs=[200, 300, 400, 500, 600, 700, 800, 900]

os.mkdir('CrossSectionsNSEW')
os.chdir(srcpath+'\\'+"CrossSectionsNSEW") 
os.mkdir('TanWindNS')
os.mkdir('TanWindEW')
os.mkdir('RadWindNS')
os.mkdir('RadWindEW')


for i in range(len(cxs)):
    cxsi=cxs[i][1:]
    cysi=cys[i][1:]

    ctr=(cxsi[-1],cysi[-1]) #grabs the lowest level and sets it as the TC center

    adjcxs=cxsi-ctr[0]
    adjcys=cysi-ctr[1]

    plt.scatter(adjcxs,adjcys,c=stacklvs,cmap=cm.jet)
    plt.plot(adjcxs,adjcys,'k')

    plt.colorbar()
    plotradius=50
    plt.xlim(-plotradius,plotradius)
    plt.ylim(-plotradius,plotradius)

    plt.title(f'{i}')

    # plt.show()
    plt.savefig("tilttest_%i.png"%i, bbox_inches="tight") #, dpi=400
    plt.clf()


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
