# this code makes azimuthal average plots
import os
srcpath=os.getcwd()
os.chdir(srcpath)
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from HEDAS_pkg import HEDASds

fname="stored_centers_Dorian.npy" #stored centers file

center_file = np.load(fname) 

cxs=center_file[:,0] # all x stacks
cys=center_file[:,1] # all y stacks

os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian')

for findex, hfile in enumerate(sorted(glob.glob("*.nc"))[64:96]):
    os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian')
    cxsi=cxs[findex+64] #need to add 64, since findex starts at 0 after the slice,
    cysi=cys[findex+64] #without slicing findex would be correct
    ctr=(cxsi[6],cysi[6]) #grabs the 700mb level and sets it as the TC center
    
    ds=HEDASds(hfile) #read in the the netCDF file
    ds.center_relative_winds(ctr)
    # aziav=ds.azimuthal_average(ds.radwind())
    aziav=ds.azimuthal_average(ds.tanwind())
    # aziav=ds.azimuthal_average(ds.thetae())

    rzmean_xaxis=ds.range_bins[:-1]
    thinnedplvs=[100,200,300,400,500,600,700,800,900,1000]
    rzmean_yaxis_ticks=np.log(thinnedplvs)
    rzmean_yaxis=np.log(ds.plvs())

    cbrange_Vr=np.arange(-20,20.0001,.5)
    cbrange_Vt=np.arange(0,100,2)
    cbrange_VtC=np.arange(0,90,5)
    cbrange_ThE=np.arange(320,390,2)


    # plt.title(f"Azimuthal Average of Radial Wind\n{ds.getime()} UTC")
    # plt.contourf(rzmean_xaxis, rzmean_yaxis, aziav, levels=cbrange_Vr,cmap=cm.seismic, extend='both') #VR

    plt.title(f"Azimuthal Average of Tangential Wind\n{ds.getime()} UTC")
    plt.contourf(rzmean_xaxis, rzmean_yaxis, aziav, levels=cbrange_Vt,cmap=cm.jet, extend='both')

    # plt.title(f"Azimuthal Average of Theta-E\n{ds.getime()} UTC")
    # plt.contourf(rzmean_xaxis, rzmean_yaxis, aziav, levels=cbrange_ThE, cmap=cm.jet, extend='both') # 

    plt.xlim(0,150)
    plt.xlabel("Radius (km)")
    plt.ylabel("Pressure (hPa)")
    plt.ylim(max(rzmean_yaxis),min(rzmean_yaxis[1:]))
    plt.yticks(rzmean_yaxis_ticks,thinnedplvs) #positions, labels
    cb=plt.colorbar()
    cb.ax.set_title(r'ms$^{-1}$')
    # cb.ax.set_title('K')
    plt.tight_layout()

    # os.chdir('/rita/s0/bsr5234/Lapenta/AzimuthalAverages/RadialWind')
    os.chdir('/rita/s0/bsr5234/Lapenta/AzimuthalAverages/TangentialWind')
    # os.chdir('/rita/s0/bsr5234/Lapenta/AzimuthalAverages/ThetaE')

    plt.savefig('AzimuthalAverage_TangentialWind_%s.png' % ds.datetimestring, bbox_inches="tight", dpi=500)
    plt.clf()
    print(ds.getime()) #prints the time of each file once all 4 plots are done for that time