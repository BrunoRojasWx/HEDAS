#this code makes the North-South and East-West cross sections
# of tangential and radial wind using the 700mb centers from the 
# stored centers .npy file

import os
srcpath=os.getcwd()
os.chdir(srcpath)
import netCDF4 as NC
import numpy as np
import matplotlib as mpl
import glob
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import datetime as dt
from HEDAS_pkg import HEDASds

fname="stored_centers_Dorian.npy" #stored centers file

center_file = np.load(fname) 

cxs=center_file[:,0] # all x stacks
cys=center_file[:,1] # all y stacks

#make the directories the files will go into
# there needs to be no 'CrossSectionsNSEW' directory before running this code
os.mkdir('CrossSectionsNSEW')
os.chdir("CrossSectionsNSEW") 
os.mkdir('TanWindNS')
os.mkdir('TanWindEW')
os.mkdir('RadWindNS')
os.mkdir('RadWindEW')
os.mkdir('VertVelNS')
os.mkdir('VertVelEW')

#colorbar ranges
cbrange_Vr=np.arange(-20,20.0001,.5)
cbrange_Vt=np.arange(0,100,2)
cbrange_VtC=np.arange(0,90,5)
cbrange_W=np.arange(-10,10.0001,.2)


os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian') #go to the folder with the netCDF HEDAS data

def Xsecplotter(inputwind,windtype,orientation):
    thinnedplvs=[100,200,300,400,500,600,700,800,900,1000]
    xsec_yaxis_ticks=np.log(thinnedplvs)
    xsec_yaxis=np.log(ds.plvs())
    
    if orientation=='EW':
        XSec=inputwind[:,ctr[1],:]
        xsec_xaxis=ds.Edist[ctr[0],:] #use for WE xsec
        # xsec_xaxis=ds.xdist[ctr[0],:] #use for WE xsec

    if orientation=='NS':
        XSec=inputwind[:,:,ctr[0]]
        xsec_xaxis=ds.Ndist[:,ctr[1]] #use for SN xsec
        # xsec_xaxis=ds.ydist[:,ctr[1]] #use for SN xsec

    XSec,xsec_xaxis=ds.crosssection_nan_err_check(XSec,xsec_xaxis)

    if windtype=='rad': #for radial wind
        PT=plt.contourf(xsec_xaxis,xsec_yaxis,XSec,levels=cbrange_Vr,cmap=cm.seismic, extend='both')
        if orientation=='EW':
            plt.title('Radial Wind W-E cross-section\n%s'%(ds.getime()))
        if orientation=='NS':
            plt.title('Radial Wind S-N cross-section\n%s'%(ds.getime()))

    if windtype=='vvl': #for vertical velocity
        PT=plt.contourf(xsec_xaxis,xsec_yaxis,XSec,levels=cbrange_W,cmap=cm.seismic, extend='both')
        if orientation=='EW':
            plt.title('Vertical Velocity W-E cross-section\n%s'%(ds.getime()))
        if orientation=='NS':
            plt.title('Vertical Velocity S-N cross-section\n%s'%(ds.getime()))

    if windtype=='tan': #for tangential wind
        PT=plt.contourf(xsec_xaxis,xsec_yaxis,XSec,levels=cbrange_Vt,cmap=cm.jet, extend='both')
        if orientation=='EW':
            plt.title('Tangential Wind W-E cross-section\n%s'%(ds.getime()))
        if orientation=='NS':
            plt.title('Tangential Wind S-N cross-section\n%s'%(ds.getime()))

    plt.ylim(max(xsec_yaxis),min(xsec_yaxis[1:]))
    plt.xlim(np.nanmin(xsec_xaxis),np.nanmax(xsec_xaxis))
    # plt.xlim(-150,150)
    plt.yticks(xsec_yaxis_ticks,thinnedplvs) #positions, labels
    cb1=plt.colorbar(PT)
    cb1.set_label(r'ms$^{-1}$')
    plt.vlines(0, ymax=max(xsec_yaxis),ymin=min(xsec_yaxis),colors='k')
    plt.xlabel('Horizontal distance from storm center (km)')
    plt.ylabel('Pressure (hPa)')

    PTG=plt.gcf()
    PTG.set_size_inches(12,5)
    if windtype=='tan' and orientation=='EW':
        os.chdir(srcpath+'/'+"CrossSectionsNSEW/TanWindEW") 
        plt.savefig('TangentialWind_EWxsec_%s.png' % ds.datetimestring, bbox_inches="tight", dpi=600)
    if windtype=='tan' and orientation=='NS':
        os.chdir(srcpath+'/'+"CrossSectionsNSEW/TanWindNS") 
        plt.savefig('TangentialWind_NSxsec_%s.png' % ds.datetimestring, bbox_inches="tight", dpi=600)
    if windtype=='rad' and orientation=='EW':
        os.chdir(srcpath+'/'+"CrossSectionsNSEW/RadWindEW") 
        plt.savefig('RadialWind_EWxsec_%s.png' % ds.datetimestring, bbox_inches="tight", dpi=600)
    if windtype=='rad' and orientation=='NS':
        os.chdir(srcpath+'/'+"CrossSectionsNSEW/RadWindNS") 
        plt.savefig('RadialWind_NSxsec_%s.png' % ds.datetimestring, bbox_inches="tight", dpi=600)
    if windtype=='vvl' and orientation=='EW':
        os.chdir(srcpath+'/'+"CrossSectionsNSEW/VertVelEW") 
        plt.savefig('VertVel_EWxsec_%s.png' % ds.datetimestring, bbox_inches="tight", dpi=600)
    if windtype=='vvl' and orientation=='NS':
        os.chdir(srcpath+'/'+"CrossSectionsNSEW/VertVelNS") 
        plt.savefig('VertVel_NSxsec_%s.png' % ds.datetimestring, bbox_inches="tight", dpi=600)
    plt.clf()

#64:96 is (ATL1-GreatAbaco)
for findex, hfile in enumerate(sorted(glob.glob("*.nc"))[64:96]):
    os.chdir('/rita/s0/scratch/bsr5234/HEDAS/Dorian')

    cxsi=cxs[findex+64] #need to add 64, since findex starts at 0 after the slice,
    cysi=cys[findex+64] #without slicing findex would be correct
    ctr=(cxsi[6],cysi[6]) #grabs the 700mb level and sets it as the TC center
    ds=HEDASds(hfile) #read in the the netCDF file
    ds.center_relative_winds(ctr) #calculate wind fields
    Vrad=ds.radwind(ctr) #radial wind
    Vtan=ds.tanwind(ctr) #tangential wind
    VerVel=ds.get_pvbl('DZDT') #tangential wind
    
    #plot the 4 kinds of cross sections using the function
    Xsecplotter(Vrad,'rad','NS') 
    Xsecplotter(Vrad,'rad','EW')
    Xsecplotter(Vtan,'tan','NS')
    Xsecplotter(Vtan,'tan','EW')
    Xsecplotter(VerVel,'vvl','NS') 
    Xsecplotter(VerVel,'vvl','EW')
    print(ds.getime()) #prints the time of each file once all 4 plots are done for that time



