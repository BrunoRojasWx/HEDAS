import os
srcpath=os.getcwd()
os.chdir(srcpath)
import netCDF4 as NC
import numpy as np
import datetime as dt


class HEDASds:

    number_of_files = 0 #class variable, increases with each HEDASds instance
    def __init__(self, filename):
        self.filename=filename
        self.data = NC.Dataset(filename)
        self.allvblkeys = self.data.variables.keys()
        HEDASds.number_of_files += 1
        
        self.plvs_initialized=False #pressure levels initialization checker
        self.pvbl_initialized=False #set the initialization to false, gets overwritten to true if get_pvbl is run
        # ^ needs to be an instance variable so it changes with each instance (each file read in)
        self.center_relative_winds_initialized=False #same as above but for rad/tan winds

    def get_vbl(self,key): 
        """
        Grabs the full variable, uses original variable key
        """
        return self.data.variables[key]
    
    def getime(self): 
        """        
        Grabs the time of the analysis based on the file name

        Returns a datetime variable
        """
        fname=self.filename
        filestrparts=fname.split('_')

        self.datetimestring=filestrparts[1]
        yr=int(self.datetimestring[0:4])
        mo=int(self.datetimestring[4:6])
        dy=int(self.datetimestring[6:8])
        hr=int(self.datetimestring[8:10])
        mn=int(self.datetimestring[10:12])
        fdatetime=dt.datetime(year=yr,month=mo,day=dy,hour=hr,minute=mn)

        return fdatetime #file datetime

    def getime2(self): 
        """        
        This is the 'old' way of getting the time via the netCDF units, 
        but they aren't sequential and some files have the same time, not sure why

        Grabs the time of the analysis (differs from the time 
        on the filename by -30min? and from the reference_date by +30min?)
        """
        Yr=int(self.data.variables['time'].units[14:18])
        Mo=int(self.data.variables['time'].units[20:21])
        Dy=int(self.data.variables['time'].units[22:24])
        D=dt.datetime(Yr,Mo,Dy)
        ss=float(self.data.variables['time'][0])
        T=dt.timedelta(seconds=ss)
        F=D+T
        # print(F)
        return F
    
    def vtypes(self): #variable types
        """
        List of all variable types(not including the level part of the keys):

        ['latitude', 'longitude', 'time', 'PRMSL', 'REFC', 'GUST', 'HGT', 'TMP', 'RH',
        'TCDC', 'DPT', 'SPFH', 'VVEL', 'DZDT', 'UGRD', 'VGRD', 'REFD', 'LWHR', 'SWHR',
        'MSLET', 'PRES', 'TSOIL', 'SOILW', 'SOILL', 'MSTAV', 'SOILM', 'WEASD', 'CPRAT',
        'PRATE', 'APCP', 'ACPCP', 'NCPCP', 'CSNOW', 'CICEP', 'CFRZR', 'CRAIN', 'LHTFL',
        'SHTFL', 'GFLUX', 'MFLX', 'EVP', 'PEVAP', 'SFCR', 'FRICV', 'VEG', 'LFTX',
        'CAPE', 'CIN', 'PWAT', 'TCOLW', 'TCOLI', 'TCOLR', 'TCOLS', 'TCOLC', 'LCDC',
        'MCDC', 'HCDC', 'CDLYR', 'CDCON', 'BRTMP', 'DSWRF', 'DLWRF', 'USWRF', 'ULWRF',
        'CSDSF', 'HLCY', 'PLI', 'N4LFTX', 'HPBL', 'NLAT', 'ELON', 'LAND', 'WTMP']
        """
        avtypes=[] 
        for v in self.allvblkeys:
            vname=v.split('_')
            avtypes.append(vname[0])
        self.avtypes=list(dict.fromkeys(avtypes)) #remove duplicates
        return self.avtypes
    
    def plvs(self): 
        """
        Grabs the pressure levels. Returns an array with the integers of each pressure level.

        [  50  100  125  150  175  200  225  250  275  300  325  350  375  400
        425  450  475  500  525  550  575  600  625  650  675  700  725  750
        775  800  825  850  875  900  910  920  930  940  950  960  970  980
        990 1000]
        """
        if self.plvs_initialized==False: #checks if this has been initialized/called before, if not, it will run and make the pressure variable cubes
            temperature_variables=[]
            for v in self.allvblkeys:
                vname=v.split('_')
                if vname[0]==self.vtypes()[7]:
                    temperature_variables.append(v)

            pres_vbls = [s for s in temperature_variables if 'mb' in s] #gets all the full keys containing 'mb'

            pres_levels_str=[]
            for i in pres_vbls:
                plv_a=i.strip('mb')
                plv_b=plv_a.strip(self.vtypes()[7]+'_')
                pres_levels_str.append(int(plv_b))
            self.pres_levels_str=pres_levels_str
            self.pres_levels=np.array(pres_levels_str) #make a numeric version to be able to use as a z/p axis on plot with irregular levels
            self.plvs_initialized=True
        
        return self.pres_levels

    def get_pvbl(self, preskeyvbl=None, sub_sfc_value_mask=True): 
        """
        Grabs the pressure variable, uses variable key type

        Options are the pres_cubes keys:
        ['HGT', 'TMP', 'RH', 'TCDC', 'DPT', 'SPFH', 'VVEL', 'DZDT', 'UGRD', 'VGRD', 'REFD', 'LWHR', 'SWHR']
        
        If no pressure variable type is chosen, function will return all pressure cubes in a dictionary
        """
        if self.pvbl_initialized==False: #checks if this has been initialized/called before, if not, it will run and make the pressure variable cubes
            self.pres_cubes={}
            self.all_pres_vkeys=[]
            for key_vbl_type in self.vtypes()[6:19]:
                matching_variable_type = [s for s in self.allvblkeys if key_vbl_type in s] #gets all the full keys containing the variable type eg. 'HGT'
                matching_variable_type = [s for s in matching_variable_type if 'mb' in s] #gets all the full keys containing 'mb'
                matching_variable_type[:] = [s for s in matching_variable_type if 'ground' not in s] #gets all the full keys not containing 'ground'
                # 'SPFH_30M0mbaboveground' and the 10m U/V variables have an extra 'mb' in them
                temporary_variable_list = []
                for v in matching_variable_type: # starts appending at 50mb [index =0] up to 1000mb [index =43]
                    temporary_variable_list.append(self.data.variables[v][:][0])
                    self.all_pres_vkeys.append(v) # to be used later in removing the pressure vbl keys
                self.pres_cubes[key_vbl_type]=np.ma.array(temporary_variable_list) #'HGT'
                if sub_sfc_value_mask==True:
                    # masks out where the pressure surfaces are "underground" and values are interpolated to fill those grid boxes
                    self.pres_cubes[key_vbl_type]=np.ma.masked_where(self.pres_cubes['HGT'] < 0, self.pres_cubes[key_vbl_type])
            self.pvbl_initialized=True   #set the initalization to true, indicating that this block of code (calculating pressure cubes) 
                                            # doesn't need to be run again and the variables already exist, this is for code efficiency to avoid redundancy

        if preskeyvbl!=None:
            return self.pres_cubes[preskeyvbl] #returns a masked array cube of only the values
        else:
            return self.pres_cubes #returns the full dictionary (each vbl includes values and metadata)

    def get_ws(self): 
        """
        Returns masked cube of wind speed (magnitude)
        """
        Uwnd=self.get_pvbl('UGRD')
        Vwnd=self.get_pvbl('VGRD')
        ws=np.sqrt(Uwnd**2+Vwnd**2)
        return ws 

    def get_center(self,lv): 
        """
        Gets the TC center based on Michael Fischer's center finding algorithm at one level,
        the level (lv) is the vertical index (0 is the top at 50mb / 43 is the last at 1000mb)
        """
        from tdr_tc_centering_with_example import recenter_tc

        tc_sectors=1
        spad=3
        num_iters=50
        #get the lat/lon, U/V wind to feed into the algorithm
        goodlat=self.get_vbl('NLAT_surface')[0]
        goodlon=self.get_vbl('ELON_surface')[0]
        Uwnd=self.get_pvbl('UGRD')
        Vwnd=self.get_pvbl('VGRD')
        #run the algorithm from the tdr_tc_centering_with_example.py
        tc_center_coords = recenter_tc(Uwnd[lv,:,:],Vwnd[lv,:,:],\
            goodlon,goodlat,tc_sectors,\
            spad,num_iters,None,None)
        # it returns: tc_center_lon, tc_center_lat, vt_azi_max, tc_rmw (in km), data_cov (data coverage 0-1), yloc, xloc (grid box indices)
        return tc_center_coords
    
    def get_centerstack(self,all_levels=False): 
        """
        Runs the Michael Fischer TC-Center finding algorithm at all vertical levels
        """
        centerstack=[]

        if all_levels==True:
            plvs = self.plvs()
            for lv, _ in enumerate(plvs):
                tc_center_coords = self.get_center(lv)
                centerstack.append(tc_center_coords)

        else:
            hundreds_levels=np.arange(1,34,4)
            for lv in hundreds_levels:
                tc_center_coords = self.get_center(lv)
                centerstack.append(tc_center_coords)
        
        C_stack_unzip = zip(*centerstack)
        C_stack = list(C_stack_unzip)
        return C_stack

    def nonpkeys(self):
        """
        Returns all the full variable keys that are not part of the pressure cubes (a filter essentially)

        ['latitude', 'longitude', 'time', 'PRMSL_meansealevel', 'REFC_atmoscol', 'GUST_surface', 'MSLET_meansealevel', 'PRES_surface',
            'HGT_surface', 'TMP_surface', 'TSOIL_0M0D1mbelowground', 'SOILW_0M0D1mbelowground', 'SOILL_0M0D1mbelowground',
            'TSOIL_0D1M0D4mbelowground', 'SOILW_0D1M0D4mbelowground', 'SOILL_0D1M0D4mbelowground', 'TSOIL_0D4M1mbelowground',
            'SOILW_0D4M1mbelowground', 'SOILL_0D4M1mbelowground', 'TSOIL_1M2mbelowground', 'SOILW_1M2mbelowground', 'SOILL_1M2mbelowground',
            'TSOIL_3munderground', 'MSTAV_0M1mbelowground', 'SOILM_0M2mbelowground', 'WEASD_surface', 'TMP_2maboveground', 'SPFH_2maboveground',
            'DPT_2maboveground', 'RH_2maboveground', 'UGRD_10maboveground', 'VGRD_10maboveground', 'CPRAT_surface', 'PRATE_surface',
            'APCP_surface', 'ACPCP_surface', 'NCPCP_surface', 'CSNOW_surface', 'CICEP_surface', 'CFRZR_surface', 'CRAIN_surface',
            'LHTFL_surface', 'SHTFL_surface', 'GFLUX_surface', 'MFLX_surface', 'EVP_surface', 'PEVAP_surface', 'SFCR_surface',
            'FRICV_surface', 'VEG_surface', 'LFTX_500M1000mb', 'CAPE_surface', 'CIN_surface', 'PWAT_atmoscol', 'TCOLW_atmoscol',
            'TCOLI_atmoscol', 'TCOLR_atmoscol', 'TCOLS_atmoscol', 'TCOLC_atmoscol', 'LCDC_lowcloudlayer', 'MCDC_middlecloudlayer',
            'HCDC_highcloudlayer', 'TCDC_atmoscol', 'CDLYR_atmoscol', 'CDCON_atmoscol', 'PRES_cloudbase', 'HGT_cloudbase', 'HGT_cloudceiling',
            'PRES_cloudtop', 'HGT_cloudtop', 'TMP_cloudtop', 'BRTMP_topofatmosphere', 'DSWRF_surface', 'DLWRF_surface', 'USWRF_surface',
            'ULWRF_surface', 'ULWRF_topofatmosphere', 'USWRF_topofatmosphere', 'CSDSF_surface', 'HLCY_3000M0maboveground', 'HGT_tropopause',
            'HGT_0Cisotherm', 'HGT_highesttroposphericfreezinglevel', 'SPFH_30M0mbaboveground', 'UGRD_30M0mbaboveground',
            'VGRD_30M0mbaboveground', 'PWAT_30M0mbaboveground', 'PLI_30M0mbaboveground', 'N4LFTX_180M0mbaboveground', 'CAPE_180M0mbaboveground',
            'CIN_180M0mbaboveground', 'HPBL_surface', 'CAPE_90M0mbaboveground', 'CIN_90M0mbaboveground', 'CAPE_255M0mbaboveground',
            'CIN_255M0mbaboveground', 'NLAT_surface', 'ELON_surface', 'LAND_surface', 'WTMP_surface']
        """
        if self.pvbl_initialized==False: #checks if this has been initialized/called before, if not, it will run and make the pressure variable cubes        
            self.get_pvbl() #the method needs to be run at least once before the all_pres_vkeys can be accessed, this ensures that if get_pvbl has not been run, all_pres_vkeys can still be accessed
        non_pres_keys = [s for s in self.allvblkeys if s not in self.all_pres_vkeys] #gets all the full keys not used in the pressure cubes
        return non_pres_keys

    def center_relative_winds(self, center=None):
        """
        Calculates the wind angle difference from perfectly radial/tangential.
        Also calculates variables necessary for other plotting (Distance from center (in NSEW lat/lon))

        Center needs to be a pair of grid indexes (x, y)
        """
        from tdr_tc_centering_with_example import distance

        if self.center_relative_winds_initialized==False: #checks if this has been initialized/called before, if not, it will run and make the pressure variable cubes
            if center==None: #if no center is provided, the function will use:
                *_, tc_yctr, tc_xctr = self.get_center(25) # 700 mb center (~3km/flight level)
                center=(tc_xctr, tc_yctr)

            Uwnd=self.get_pvbl('UGRD')
            Vwnd=self.get_pvbl('VGRD')
            Y,X=np.indices(Uwnd[0].shape)
            self.xdist=X-center[0] #xy
            self.ydist=Y-center[1]
          
            tc_xctr, tc_yctr = center
            # self.radius = np.sqrt(self.xdist**2 + self.ydist**2) #calculates at what
            #  radius each grid box is at (grid box units 1box roughly = 0.7km)
            lat=self.get_vbl('NLAT_surface')[0]
            lon=self.get_vbl('ELON_surface')[0]
            ctr_lon=lon[center[1],center[0]]
            ctr_lat=lat[center[1],center[0]]
            
            # Eastward distance in km (to use for cross section x axis)
            self.Edist=((lon-ctr_lon)*111.321) * np.cos(np.deg2rad(ctr_lat))
            self.Ndist=(lat-ctr_lat)*111.321
            self.radius = distance(lat[tc_yctr,tc_xctr],lon[tc_yctr,tc_xctr],lat,lon) #calculates at what radius each grid box is at
            angr=np.arctan2(self.xdist,self.ydist) #calculate the azimuth in radians
            ang=np.rad2deg(angr) #convert to degrees
            ang=(ang) % 360 #convert to meteo azimuth
            # awx=ang.astype(np.int32) #convert to integers

            self.ws=np.sqrt(Uwnd**2+Vwnd**2) #wind speed (magnitude/scalar)
            wdir_radians=np.arctan2(Vwnd,Uwnd)
            wdir=-(np.rad2deg(wdir_radians)-90) % 360 #vector heading dir
            # adfdeg=(wdir-ang)
            # inflow_angle=(adfdeg+90)

            self.anglediff=np.deg2rad(wdir-ang)# angle difference between azimuth and wind dir, converted to radians
            self.center_relative_winds_initialized=True
        return self.anglediff

    def radwind(self, center=None):
        angdiff=self.center_relative_winds(center)
        Vrad=self.ws*np.cos(angdiff)
        return Vrad

    def tanwind(self, center):
        angdiff=self.center_relative_winds(center)
        Vtan=self.ws*-1*np.sin(angdiff)
        return Vtan

    def crosssection_nan_err_check(self,xsec,xaxis):
        """
        This checks if there is a nan value in the x axis
        and then adjusts the cross section to prevent a 
        broken plot
        """
        keep=~np.ma.getmask(xaxis[:])       # get the mask of the X-axis
        return xsec[:,keep], xaxis[keep]    # Only keep columns that aren't masked out at the x-axis
        
    def deeplayershear(self):
        """
        Calulate the deep layer (850-200mb) windshear over the whole domain

        Returns: shear direction vector heading, shear magnitude, shear U-component, shear V component

        All units are in m/s
        """
        Uwnd=self.get_pvbl('UGRD')
        Vwnd=self.get_pvbl('VGRD')
        #subtract 200mb - 850mb mean winds
        DL_Ushear=np.nanmean(Uwnd[5])-np.nanmean(Uwnd[31])
        DL_Vshear=np.nanmean(Vwnd[5])-np.nanmean(Vwnd[31])

        DLshr_mag=np.sqrt(DL_Ushear**2+DL_Vshear**2)
        DLshr_dir=(np.rad2deg(np.arctan2(DL_Ushear,DL_Vshear)))%360     #Meteo azimuth vector heading
        return DLshr_dir, DLshr_mag, DL_Ushear, DL_Vshear

    def shearprofile(self):
        """
        Calulate the full shear profile over the whole domain

        Returns lists of:
        shear direction vector heading, shear magnitude, shear U-component, shear V component

        All units are in m/s
        """
        Uwnd=self.get_pvbl('UGRD')
        Vwnd=self.get_pvbl('VGRD')
                    
        Ushearprofile=[]
        Vshearprofile=[]
        shearprofile_dir=[]
        shearprofile_mag=[]

        for lv, plv in enumerate(self.plvs()):
            umeanwnd=np.nanmean(Uwnd[lv])
            vmeanwnd=np.nanmean(Vwnd[lv])
            if lv<(len(Uwnd)-1):
                Ushear=np.nanmean(Uwnd[lv])-np.nanmean(Uwnd[lv+1])
                Vshear=np.nanmean(Vwnd[lv])-np.nanmean(Vwnd[lv+1])
                shr_mag=np.sqrt(Ushear**2+Vshear**2)
                shr_dir=(np.rad2deg(np.arctan2(Ushear,Vshear)))%360 
                #Meteo azimuth vector heading

                Ushearprofile.append(Ushear)
                Vshearprofile.append(Vshear)
                shearprofile_dir.append(shr_dir)
                shearprofile_mag.append(shr_mag)
        return shearprofile_dir, shearprofile_mag, Ushearprofile, Vshearprofile
        
    def meanheights(self):
        """
        Calulate the mean height at each level

        Returns list of mean height at each pressure level 

        Units: metres (m)
        """
        hgt=self.get_pvbl('HGT')

        self.heightprofile=[]
        self.thicknesses=[]
        self.midptheights=[]
        self.midplvs=[]
        for lv, plv in enumerate(self.plvs()):
            hgtmean=np.nanmean(hgt[lv])
            self.heightprofile.append(hgtmean)
            if lv < (len(self.plvs())-1):
                hgtmean_l=np.nanmean(hgt[lv+1])
                self.thicknesses.append(hgtmean-hgtmean_l)
                self.midptheights.append((hgtmean+hgtmean_l)/2)
                self.midplvs.append((plv+self.plvs()[lv+1])/2)
        
        return self.heightprofile