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

os.chdir(srcpath+'\\'+"HEDAS") 


fname="stored_centers_Dorian.npy" 

center_file = np.load(fname)
# print(center_file[:,0]) # all x stacks
# print(center_file[:,1]) # all y stacks
os.chdir(srcpath+'\\'+"Dorian") 

cxs=center_file[:,0] # all x stacks
cys=center_file[:,1] # all y stacks
# stacklvs=[100, 200, 300, 400, 500, 600, 700, 800, 900]
stacklvs=[200, 300, 400, 500, 600, 700, 800, 900]

# print(len(cxs))


# ctr=(cxs[6],cys[6])
for i in range(len(cxs)):
    cxsi=cxs[i][1:]
    cysi=cys[i][1:]

    ctr=(cxsi[-1],cysi[-1]) #grabs the lowest level and sets it as the TC center

    adjcxs=cxsi-ctr[0]
    adjcys=cysi-ctr[1]


    # hundreds_levels=np.arange(1,34,4)
    # stacklvs=plvs[hundreds_levels]
    # angle = np.linspace( 0 , 2 * np.pi , 150 ) 
    
    # radius = 25
    
    # x = radius * np.cos( angle ) 
    # y = radius * np.sin( angle )

    # plt.plot(x, y)

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

