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

parser.add_argument("-i","--inputdir",action="store",type=int)
parser.add_argument("-d","--filedir",action="store",type=int)
parser.add_argument("-f","--filename",action="store",type=int)

args, unknown = parser.parse_known_args()

if args.inputdir ==None:
  args.inputdir="/network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/pumagt_arcb_parameters_backup/"

if args.filedir==None:
  args.filedir="rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu1"

if args.filename==None:
  args.filename="PUMAG_NWPD12_M.005.nc"

if True:
  string=args.filedir
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
  print facs
  facs=[float(i) for i in facs]
  print facs
  outname = args.filedir
  afac = float(radfac)#float(sys.argv[2])
  pfac = float(psfac)#float(sys.argv[3])

ncfile=args.inputdir+'/'+args.filedir+'/'+args.filename

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

  print outname
  print ntime,nlev,nlat,nlon
  #rotfac = 0.0625#1.0#rotspds[ii]
  day = 24.0 * 60.0 * 60.0 # 1 day in seconds
  rotationrate = float(rotfac) *  2.0 * np.pi / day

  radius = 6400000.0
  #radius = 6371000.0
  g = 9.8
  p0= 100000*pfac

  #lev=950
  zg0=zg[:,0,:,:]
  #sys.exit(1)


  test1=np.fft.fft2(zg0[:,32,:])
  origin = 'lower'
  cmap = plt.cm.get_cmap("jet")

  matplotlib.rcParams.update({'font.size': 13})
  fig, axarr = plt.subplots(2, 1, sharex='col', figsize=(10,12))
  bin=15
  ax=axarr[0]
  cs = ax.contourf(lon[:],time[:],test1[:,:],bin, cmap=cmap, origin=origin)
  plt.tight_layout()
  plt.savefig('2x'+outname+'.pdf',format='pdf')

  #contourf()
  print test1
  print test1.shape

