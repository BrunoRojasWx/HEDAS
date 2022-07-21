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
import cartopy.crs as ccrs

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

    # adjust the center stack to be relative to the 900mb center
    adjcxs=cxsi-ctr[0]
    adjcys=cysi-ctr[1]

    ds=HEDASds(hfile) #read in the the netCDF file
    ds.center_relative_winds(ctr) #calculate wind fields
    lat=ds.get_vbl('NLAT_surface')[0]
    lon=ds.get_vbl('ELON_surface')[0]
    fig=plt.figure(figsize=(8,8))
    ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
    # plt.contour(ds.radius,levels=[25,50],colors='gray')
    plt.contour(lon,lat,ds.radius,transform=ccrs.PlateCarree(),levels=[5,10,15,20,25],colors='gray')

    # PT=plt.scatter(adjcxs,adjcys,c=stacklvs,cmap=cm.jet)
    # plt.plot(adjcxs,adjcys,'k')

    #convert the centers from grid coords to lat/lon
    ctr_lon=lon[ctr[1],ctr[0]]
    ctr_lat=lat[ctr[1],ctr[0]]
    cxsi_lon=lon[cysi,cxsi]
    cysi_lat=lat[cysi,cxsi]
    # print(cysi_lat,cxsi_lon)
    PT=ax.scatter(cxsi_lon,cysi_lat,transform=ccrs.PlateCarree(),c=stacklvs,cmap=cm.jet)
    ax.plot(cxsi_lon,cysi_lat,'k',transform=ccrs.PlateCarree())
    cb1=plt.colorbar(PT)
    cb1.set_label('mb')
    ax.gridlines(draw_labels=True)

    plotradius=25 # km
    lonradius=plotradius/111.321 * np.cos(np.deg2rad(ctr_lat))
    latradius=plotradius/111.321

    ax.set_extent([ctr_lon-lonradius, ctr_lon+lonradius, ctr_lat-latradius,ctr_lat+latradius], crs=ccrs.PlateCarree())

    plt.title(f'Vortex centers by pressure level\n{ds.getime()}')

    print(ds.getime())
    os.chdir(srcpath+'/tilt_images_zoomed')
    plt.savefig("tilt_%s.png"%ds.datetimestring, bbox_inches="tight") #, dpi=400
    plt.clf()