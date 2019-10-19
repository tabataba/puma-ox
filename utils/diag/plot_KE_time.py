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

YEAR='010'   #MAKE INPUT
indir= '/media/Seagate5TB/puma'+'/pumagt_arcb_parameters/'
savdir=' ' #MAKE INPUT
outdir='plots/'
filename='PUMAG.'+YEAR+'.nc'

outname=''
if len(sys.argv) == 1:
  #ncfile = os.environ['HDD']+'/runs/PUMA_test/pumagt_dialy/pumag010.nc'
  #ncfile = os.environ['HDD']+'/runs/PUMA_test/pumag/pumag010.nc'
  #ncfile = os.environ['HDD']+'/runs/puma_lat64_ntspd240_lev20_rot1_nS/puma010.nc'
  ncfile = '/media/Seagate5TB/puma'+'/pumagt_arcb_parameters/rev53_r0.5_res64_radius1.00_taufr10.0_psurf1.0_pref1.0_taus10.00_tausurf36_nmu1/PUMAG.010.nc'
  afac=1
  pfac=1
  outname='test'
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
  #sys.exit(1)


print(ncfile,outname,afac,pfac)


a = 6400000.0*afac#/20.0
g = 9.8
kappa = 0.286
M_air = 28.98
k = 1.38E-23
R=8.3144621
p0=100000*pfac

f = netcdf.netcdf_file(ncfile,'r',mmap=False)

time = f.variables['time']
lat = f.variables['lat']
lon = f.variables['lon']
lev = f.variables['lev'] #* pfac
t = f.variables['ta']
u = f.variables['ua']
v = f.variables['va']
lev = lev[:] #* pfac

print lev[:]

nlat = lat.shape[0]
nlon = lon.shape[0]
ntime = time.shape[0]
nlev = lev.shape[0]
