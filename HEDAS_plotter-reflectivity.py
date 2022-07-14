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
import cartopy.crs as ccrs
import cartopy.feature as cfeat

# os.chdir(srcpath+'\\'+"HEDAS") 
# print(os.getcwd())

fname="stored_centers_Dorian.npy" 
center_file = np.load(fname)

cxs=center_file[:,0] # all x stacks
cys=center_file[:,1] # all y stacks
# stacklvs=[100, 200, 300, 400, 500, 600, 700, 800, 900]
stacklvs=[200, 300, 400, 500, 600, 700, 800, 900]

cbrange_Vr=np.arange(-20,20.0001,.5)
cbrange_Vt=np.arange(0,100,2)
cbrange_VtC=np.arange(0,90,5)
cbrange_dbz=np.arange(0,65.0001,1)

os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian') 
# print(os.getcwd())

for findex, file in enumerate(sorted(glob.glob("*.nc"))):
    os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian') 
    
    cxsi=cxs[findex][1:] #the [1:] removes the 100mb level center from being plotted
    cysi=cys[findex][1:] #because the center stack goes from 100mb to 900mb
    ctr=(cxsi[-1],cysi[-1]) #grabs the lowest level (900mb) and sets it as the TC center

    ds=HEDASds(file)
    print(ds.getime())
    # print(ds.number_of_files)
    datetimestring=ds.datetimestring
    fdatetime=ds.getime()
    plvs=ds.plvs()
    lv=32
    
    ref=ds.get_vbl('REFC_atmoscol')[0]

    lat=ds.get_vbl('NLAT_surface')[0]
    lon=ds.get_vbl('ELON_surface')[0]

    fig=plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())

    plt.title('Composite Reflectivity\n%s UTC'%(ds.getime()))
    PT=ax.contourf(lon,lat,ref,transform=ccrs.PlateCarree(),levels=cbrange_dbz,cmap=cm.jet, extend='both')
    
    ds.center_relative_winds(ctr)
    # Vrad=ds.radwind(ctr)
    # Vtan=ds.tanwind(ctr)

    ### TAN WIND
    # plt.title('Tangential Wind (m/s) at %smb\n%s'%(plvs[lv],fdatetime))
    # PT=ax.contourf(lon,lat,Vtan[lv],transform=ccrs.PlateCarree(),levels=cbrange_Vt,cmap=cm.jet, extend='max')

    ### RAD WIND
    # plt.title('Radial Wind (m/s) at %smb\n%s'%(plvs[lv],fdatetime))
    # PT=ax.contourf(lon,lat,Vrad[lv],transform=ccrs.PlateCarree(),levels=cbrange_Vr,cmap=cm.seismic, extend='both')

    ax.add_feature(cfeat.COASTLINE)
    ax.contour(lon,lat,ds.radius,transform=ccrs.PlateCarree(),levels=[50,100,150,200],colors='gray')
    ax.gridlines(draw_labels=True)
    cl=plt.colorbar(PT,ax=ax)
    cl.ax.set_title('dBZ')
    # plt.plot(ctr[0], ctr[1],'ro')

    PTG=plt.gcf()
    PTG.set_size_inches(7,6) 

    os.chdir(srcpath)
    # plt.savefig('Datacoverage-HEDAS_%03d.png'%ds.number_of_files, bbox_inches="tight", dpi=500)
    # plt.savefig('Tan/RadWind_%s_%s.png'%(plvs[lv],datetimestring), bbox_inches="tight", dpi=500)
    plt.savefig('CompositeReflectivity_%s.png'%(datetimestring), bbox_inches="tight", dpi=500)

    plt.clf()


