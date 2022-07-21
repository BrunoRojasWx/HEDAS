# this code runs the M. Fischer TC center finding
# algorithm that gets the center at each vertical 
# level and stores it in a .npy file. This code 
# also uses multiprocessing (MP) and is much faster
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
from tdr_tc_centering_with_example import recenter_tc

import concurrent.futures #package that will do the MP

#navigate to where the HEDAS netCDF files are located
os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian') 

list_of_HEDASfiles=[]
allstacks=[]

for findex, file in enumerate(sorted(glob.glob("*.nc"))):
# for findex, file in enumerate(sorted(glob.glob("*.nc"))[0:39]): 
### ^ EXAMPLE option for Windward file times
    list_of_HEDASfiles.append(file)

#create a function that does all the steps to run on one core
def MP_centerstack_function(file):
    ds=HEDASds(file)        #create a HEDASds instance of the data
    print(ds.datetimestring) #prints date/time string each time a new file is being processed
    cstack=ds.get_centerstack() #all center stack returns from TCR center finder
    ctrxys=np.array([cstack[6],cstack[5]]) #get the x and y grid indices into an array
    return ctrxys

### MP section (see: https://www.youtube.com/watch?v=fKl2JW_qrso)
with concurrent.futures.ProcessPoolExecutor() as executor:
    results = executor.map(MP_centerstack_function, list_of_HEDASfiles)
    for result in results:
        allstacks.append(result) #put all these arrays into a big list

os.chdir(srcpath) #change dir back to original directory

#store that big list into the .npy file
np.save('stored_centers_Dorian', allstacks)
print('Save complete!')

#started at 5:07PM Completed 5:49  = ~42 minutes
