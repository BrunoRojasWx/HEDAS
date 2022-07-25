# This code plots all the mean wind profiles/hodographs
# This may be modified later to have a shear profile 
# by calculating the mean height of each pressure sfc 
# and then using the height differences between p sfcs
# to use as the shear depth

import os
srcpath=os.getcwd()
os.chdir(srcpath)
import glob
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from HEDAS_pkg import HEDASds

os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian')

for findex, hfile in enumerate(sorted(glob.glob("*.nc"))):
    os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian')
    ds=HEDASds(hfile) #read in the the netCDF file

    circle1 = plt.Circle((0, 0), 5, color='grey',fill=False, alpha=0.5)
    plt.gca().add_patch(circle1)
    circle2 = plt.Circle((0, 0), 10, color='grey',fill=False, alpha=0.5)
    plt.gca().add_patch(circle2)
    circle3 = plt.Circle((0, 0), 15, color='grey',fill=False, alpha=0.5)
    plt.gca().add_patch(circle3)
    plt.plot(ds.meanwindprofile()[0][3:],ds.meanwindprofile()[1][3:],'k')
    plt.scatter(ds.meanwindprofile()[0][3:],ds.meanwindprofile()[1][3:],c=ds.plvs()[3:],cmap=cm.jet)
    plt.title(f'Mean Wind Profile (m/s)\n{ds.getime()}')
    plt.xlabel('Zonal Mean Wind')
    plt.ylabel('Meridional Mean Wind')
    plt.plot(0,0,'k+')
    plotradius=15
    plt.xlim(-plotradius,plotradius)
    plt.ylim(-plotradius,plotradius)
    cb=plt.colorbar()
    cb.ax.set_title('mb')
    os.chdir('/rita/s0/bsr5234/Lapenta/MeanWind_hodos')
    plt.savefig('MeanWind_Hodograph_r15_%s.png' % ds.datetimestring, bbox_inches="tight", dpi=500)
    plt.clf()
    print(ds.getime()) #prints the time of each file once all 4 plots are done for that time
