#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')

import numpy as np
from scipy.io import netcdf
import math
import matplotlib.pyplot as plt
import sys
import os
from matplotlib import cm
from mpl_toolkits.axes_grid1 import AxesGrid
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from matplotlib.ticker import MultipleLocator

from argparse import ArgumentParser
parser = ArgumentParser()

from netCDF4 import Dataset


parser.add_argument("-n","--name",action="store",type=str)
parser.add_argument("-p","--path",action="store",type=str)
parser.add_argument("-e","--eddypath",action="store",type=str)
parser.add_argument("-o","--output",action="store",type=str)

args, unknown = parser.parse_known_args()

afac=1
pfac=1

plt.rc('legend',**{'fontsize':14})

outdir='plots/'
outname='testplot'

dir1='/network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/'
dirs=['pumagt_arcb_parameters/','noseasons_pumagt_arcb/']
filenames1=[dir1+dirs[0]+'rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu1/PUMAG.024.nc',dir1+dirs[0]+'rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu0/PUMAG.024.nc',dir1+dirs[1]+'rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu1/PUMAG.012.nc',dir1+dirs[1]+'rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu0/PUMAG.012.nc']

fig, axarr = plt.subplots(3, 1, sharex='col', figsize=(8,16))

for i,ncfile in enumerate(filenames1):

  a = 6400000.0*afac#/20.0
  g = 9.8
  kappa = 0.286
  M_air = 28.98
  k = 1.38E-23
  R=8.3144621
  p0=100000*pfac
  R_spec = R/M_air*1000 # 1000g per kg
  cp = 1003
  f = netcdf.netcdf_file(ncfile,'r',mmap=False)

  time = f.variables['time']
  lat = f.variables['lat']
  lon = f.variables['lon']
  lev = f.variables['lev'] #* pfac
  t = f.variables['ta']
  u = f.variables['ua']
  v = f.variables['va']
  o = f.variables['wap']
  lev = lev[:] #* pfac
  p =lev[:]
  print lev[:]

  nlat = lat.shape[0]
  nlon = lon.shape[0]
  ntime = time.shape[0]
  nlev = lev.shape[0]
  nlate = nlat/2

  dens = np.zeros((ntime,nlev,nlat,nlon))
  dens = np.reshape(p[:],(1,nlev,1,1))/(R_spec*t[:,:,:,:])
  M_mars = 43.49 #g/mol # Mars

  s = cp * t[:,:,:,:] + np.reshape(p[:],(1,nlev,1,1)) * dens[:,:,:,:]
  

  #s_tm = np.reshape(np.mean(s[:,:,:,:],axis=0),(1,nlev,nlat,nlon))
  #v_tm = np.reshape(np.mean(v[:,:,:,:],axis=0),(1,nlev,nlat,nlon))

  #s_tmzm = np.reshape(np.mean(s_tm,axis=3),(1,nlev,nlat,1))
  #v_tmzm = np.reshape(np.mean(v_tm,axis=3),(1,nlev,nlat,1))

  #s_tmdev = s[:,:,:,:] - s_tm
  #v_tmdev = v[:,:,:,:] - v_tm

  #\overline{vs} total

  total = np.mean(np.mean(np.mean(v[:,:,:,:]*s[:,:,:,:],axis=0),axis=2),axis=0)
  total2 = np.sum(np.sum(np.mean(v[:,:,:,:]*s[:,:,:,:],axis=0),axis=2),axis=0)

  #axarr[0].plot(lat[ieq:nlat],total)
  axarr[0].plot(lat[0:nlate],total2[0:nlate])

  #\overline{v} \overline {s} mean

  mean= np.sum(np.sum(np.mean(v[:,:,:,:],axis=0)*np.mean(s[:,:,:,:],axis=0),axis=2),axis=0)

  axarr[1].plot(lat[0:nlate],mean[0:nlate])

  #\overline{v's'} eddy

  eddy =np.sum(np.sum(np.mean((v[:,:,:,:]-np.reshape(np.mean(v[:,:,:,:],axis=0),(1,nlev,nlat,nlon)))*(s[:,:,:,:]-np.reshape(np.mean(s[:,:,:,:],axis=0),(1,nlev,nlat,nlon))),axis=0),axis=2),axis=0)

  axarr[2].plot(lat[0:nlate],eddy[0:nlate])

plt.tight_layout()
plt.savefig(outdir+outname+'.png',format='png')



