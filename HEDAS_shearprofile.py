# This code plots local height shear by calculating the
# mean height of each pressure sfc 
# and then using the height differences between pres sfcs
# to use as the shear depth

import os
srcpath=os.getcwd()
os.chdir(srcpath)
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from HEDAS_pkg import HEDASds

os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian')

for findex, hfile in enumerate(sorted(glob.glob("*.nc"))):
    os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian')
    ds=HEDASds(hfile) #read in the the netCDF file

    heights=ds.meanheights()

    thicknesses=np.array(ds.thicknesses)
    shearmag=np.array(ds.shearprofile()[1]/thicknesses)
    shearthousand = shearmag * 1000

    plt.plot(shearthousand,np.log(ds.midplvs),'g')
    plt.ylim(np.log(1000),np.log(100))
    thinnedplvs=[100,200,300,400,500,600,700,800,900,1000]
    plt.yticks(np.log(thinnedplvs),thinnedplvs) #positions, labels
    plt.xlim(0,6)       # turn off for flexible axes (flexax)
    plt.title(f"Vertical Wind Shear Profile\n{ds.getime()} UTC")
    plt.ylabel('Pressure (hPa)')
    plt.xlabel(r'Layer shear magnitude ($\times 10^3 s^{-1}$)')

    PTG=plt.gcf()
    PTG.set_size_inches(3.25,6)
    plt.tight_layout()  # needs to be called after setting the size

    os.chdir('/rita/s0/bsr5234/Lapenta/ShearProfiles_fixedaxes')
    plt.savefig('ShearProfile_fixax%s.png' % ds.datetimestring, bbox_inches="tight", dpi=500)
    plt.clf()
    print(ds.getime()) #prints the time of each file once all 4 plots are done for that time
