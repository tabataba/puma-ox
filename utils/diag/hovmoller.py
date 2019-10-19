#!/usr/bin/python

import matplotlib
#matplotlib.use('Agg')

import numpy as np
from scipy.io import netcdf
import math
import matplotlib.pyplot as plt
import sys
import os
import subprocess as sub
import re
from matplotlib import cm
from mpl_toolkits.axes_grid1 import AxesGrid
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from matplotlib.ticker import MultipleLocator


YEAR='010'
indir= '/network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/'+'/pumagt_arcb_parameters/'
outdir='plots/wav3/'
outdirpng='pics/'


      #path = ''
      ##onlyfiles=os.listdir(path)
      #onlyfiles = sorted(onlyfiles)
if len(sys.argv)>2:
  YEAR=sys.argv[2]


filename='PUMAG.'+YEAR+'.nc'

rotspds=[1.0]
ii=0

ncfile='puma_outxx.nc'
inputfile='MOST.010'
path='/home/octoraid/gfd/tabataba/variable_rotation_rate_noSeasons_T42_NTSPD144'

outname=''
if len(sys.argv) == 1:
  #ncfile = os.environ['HDD']+'/runs/PUMA_test/pumagt_dialy/pumag010.nc'
  #ncfile = os.environ['HDD']+'/runs/PUMA_test/pumag/pumag010.nc'
  #ncfile = os.environ['HDD']+'/runs/puma_lat64_ntspd240_lev20_rot1_nS/puma010.nc'
  ncfile = '/network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT'+'/pumagt_arcb_parameters/rev53_r1.0_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu1/PUMAG.018.nc'
  afac=1
  pfac=1
  outname='test'
  rotfac=1.0
#elif len(sys.argv) == 3: 
#  ncfile = sys.argv[1]
#  outname = sys.argv[2]
#elif len(sys.argv) == 2:
#  ncfile = sys.argv[1]
else:
  ncfile = indir+sys.argv[1]+'/'+filename
  string=sys.argv[1]
  str1='_r'
  str2='_res'
  str3='_radius'
  str4='_taufr'
  str5='_psurf'
  str6='_pref'
  str7='_taus'
  str8='_tausurf'
  str9='_nmu'
  rotpos=string.find(str1)
  respos=string.find(str2)
  radpos=string.find(str3)
  tfrpos=string.find(str4)
  pspos =string.find(str5)
  prpos =string.find(str6)
  tspos =string.find(str7)
  tsupos=string.find(str8)
  nmupos=string.find(str9)
  rotfac=string[rotpos+len(str1):respos]#0
  resfac=string[respos+len(str2):radpos]#1
  radfac=string[radpos+len(str3):tfrpos]#2
  tfrfac=string[tfrpos+len(str4):pspos ]#3
  psfac =string[pspos +len(str5):prpos ]#4
  prfac =string[prpos +len(str6):tspos ]#5
  tsfac =string[tspos +len(str7):tsupos]#6
  tsufac=string[tsupos+len(str8):nmupos]#7
  nmufac=string[nmupos+len(str9):len(string)]#8
  facs=[rotfac,resfac,radfac,tfrfac,psfac,prfac,tsfac,tsufac,nmufac]
  facs=[float(i) for i in facs]
  print facs
  outname = sys.argv[1]
  afac = float(radfac)#float(sys.argv[2])
  pfac = float(psfac)#float(sys.argv[3])
  rotfac = facs[0]

if True:

  #f=netcdf.netcdf_file(ncf.fullpath,'r')
  f = netcdf.netcdf_file(ncfile,'r',mmap=False)
  #print f.variables
  time = f.variables['time']
  lev = f.variables['lev']
  lat = f.variables['lat']
  lon = f.variables['lon']
  #t = f.variables['ta']
  #u = f.variables['ua']
  v = f.variables['va']
  zg= f.variables['zg']

  p=lev[:]*100 #*pfac
  lev = lev[:]#*pfac

  ntime = time.shape[0]
  nlev = lev.shape[0]
  nlat = lat.shape[0]
  nlon = lon.shape[0]

  #rotfac = 0.0625#1.0#rotspds[ii]
  day = 24.0 * 60.0 * 60.0 # 1 day in seconds
  rotationrate = rotfac *  2.0 * np.pi / day

  radius = 6400000.0
  #radius = 6371000.0
  g = 9.8
  p0= 100000*pfac

  #lev=950
  zg0=zg[:,0,:,:]
  #lev=550
  zg4=zg[:,4,:,:]
  #lev=50
  zg9=zg[:,9,:,:]

  #zg4[:,20,:]

  #time lev lat lon

  #zgstar0=zg0[:,:,:] - np.reshape(np.mean(zg0[:,:,:],axis=2),(ntime,nlat,1))
  zgstar=zg[:,:,:,:] - np.reshape(np.mean(zg[:,:,:,:],axis=3),(ntime,nlev,nlat,1))



  #print wavnum.shape,lat[:].shape,x.shape[:]

  #uprime = u[:,:,:,:] - np.reshape(np.mean(u[:,:,:,:],axis=3),(ntime,nlev,nlat,1))
  vprime = v[:,:,:,:] - np.reshape(np.mean(v[:,:,:,:],axis=3),(ntime,nlev,nlat,1))

  #ip=4
  ilat=5#15

  response = input("What ilat?")
  ilat=int(response)
  outname='hovmoller_'+outname

  for ip in range(10):

    fig, axarr = plt.subplots(1, 1, sharex='col', figsize=(6,12))

    cmap = plt.cm.get_cmap("bwr")
    ax=axarr
    #wavnum=np.arange(0,10)

    cs = ax.contourf(lon[:],time[:],vprime[:,ip,ilat,:],10, cmap=cmap, origin='lower')
    plt.title(r'Hovmoller diagram at $p=$'+str(np.round(lev[ip],1))+r' hPa, $\phi=$'+str(np.round(lat[ilat],1))+r"$^\circ$")
    #p = ax.plot(time[:],xt[1,:])
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Time (days)')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")

    col=plt.colorbar(cs, cax=cax)
    lab=r'$v^*$ (m/s)'
    col.set_label(lab)

    plt.tight_layout()
  
    #ourdir='plots/wav_pbot_pbot/'

    plt.savefig(outdir+'1vp'+outname+'_'+str(YEAR)+'_ip'+str(ip)+'.pdf',format='pdf')
    plt.show()

    fig, axarr = plt.subplots(1, 1, sharex='col', figsize=(6,12))

    cmap = plt.cm.get_cmap("bwr")
    ax=axarr
    #wavnum=np.arange(0,10)

    cs = ax.contourf(lon[:],time[:],zg[:,ip,ilat,:],10, cmap=cmap, origin='lower')
    plt.title(r'Hovmoller diagram at $p=$'+str(np.round(lev[ip],1))+r' hPa, $\phi=$'+str(np.round(lat[ilat],1))+r"$^\circ$")
    #p = ax.plot(time[:],xt[1,:])
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Time (days)')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")

    col=plt.colorbar(cs, cax=cax)
    lab=r'geopotential height (m$^2$/s$^2$)'
    col.set_label(lab)

    plt.tight_layout()
  
    #ourdir='plots'
    #outname='hovmoller_'+outname

    plt.savefig(outdir+'1hz'+outname+'_'+str(YEAR)+'_ip'+str(ip)+'.pdf',format='pdf')
    plt.show()

  sys.exit(1)
