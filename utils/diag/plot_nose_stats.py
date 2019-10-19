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

YEAR='010'
if len(sys.argv) >= 3: YEAR=sys.argv[2]
indir= '/network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT'+'/noseasons_pumagt_arcb/'
outdir='data/stats_noseasons_ex1/'
filename='PUMAG.'+YEAR+'.nc'
#if len(sys.argv) == 3: filename=sys.argv[2]

print filename
outname=''
if len(sys.argv) == 1:
  #ncfile = os.environ['HDD']+'/runs/PUMA_test/pumagt_dialy/pumag010.nc'
  #ncfile = os.environ['HDD']+'/runs/PUMA_test/pumag/pumag010.nc'
  #ncfile = os.environ['HDD']+'/runs/puma_lat64_ntspd240_lev20_rot1_nS/puma010.nc'
  ncfile = '/network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT'+'/pumagt_arcb_parameters/rev53_r0.5_res64_radius1.00_taufr10.0_psurf1.0_pref1.0_taus10.00_tausurf36_nmu1/PUMAG.010.nc'
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
  str10='solcon'
  rotpos=string.find(str1)
  respos=string.find(str2)
  radpos=string.find(str3)
  tfrpos=string.find(str4)
  pspos =string.find(str5)
  prpos =string.find(str6)
  tspos =string.find(str7)
  tsupos=string.find(str8)
  nmupos=string.find(str9)
  solpos=string.find(str10)
  rotfac=string[rotpos+len(str1):respos]#0
  resfac=string[respos+len(str2):radpos]#1
  radfac=string[radpos+len(str3):tfrpos]#2
  tfrfac=string[tfrpos+len(str4):pspos ]#3
  psfac =string[pspos +len(str5):prpos ]#4
  prfac =string[prpos +len(str6):tspos ]#5
  tsfac =string[tspos +len(str7):tsupos]#6
  tsufac=string[tsupos+len(str8):nmupos]#7
  nmufac=string[nmupos+len(str9):nmupos+len(str9)+1]#8
  solfac=1.0#solfac=string[solpos+len(str10):len(string)]#9
  facs=[rotfac,resfac,radfac,tfrfac,psfac,prfac,tsfac,tsufac,nmufac,solfac]
  facs=[float(i) for i in facs]
  print facs
  outname = sys.argv[1]
  afac = float(radfac)#float(sys.argv[2])
  pfac = float(psfac)#float(sys.argv[3])
  #sys.exit(1)

if len(sys.argv) == 3:
  outname = sys.argv[1]+sys.argv[2]



from argparse import ArgumentParser
parser = ArgumentParser()


#from netCDF4 import Dataset
#>>> f = MFDataset('mftest*nc')
#>>> print f.variables['x'][:]

parser.add_argument("-s","--start",action="store",type=int)
parser.add_argument("-d","--days",action="store",type=int)
parser.add_argument("-i","--it",action="store",type=int)

args, unknown = parser.parse_known_args()
  

if args.start ==None:
  print "enter start"
  sys.exit(1)
else:
  start=args.start


if args.days ==None:
  days = 30
else:
  days = args.days

if args.it ==None:
  print "enter iter" 
  sys.exit(1)
else:
  iter = args.it

t1=start
t2=start+days



print(ncfile,outname,afac,pfac)


a = 6400000.0*afac#/20.0
g = 9.8
kappa = 0.286
M_air = 28.98
k = 1.38E-23
R=8.3144621
p0=100000*pfac


f = netcdf.netcdf_file(ncfile,'r',mmap=False)

#FOLDER="rotsize7/"
#FILE="rotsize7_r0.125_a8.00000.010.nc"
#FILE2="rotsize7_r8.0_a0.12500.010.nc"
#ncfilexx=FOLDER+FILE2

#f= netcdf.netcdf_file(ncfilexx,'r')

time = f.variables['time']
lat = f.variables['lat']
lon = f.variables['lon']
lev = f.variables['lev'] #* pfac
t = f.variables['ta']
u = f.variables['ua']
v = f.variables['va']
lev = lev[:] #* pfac

print lev[:]

#print lat.shape
#print lon.shape
#print t.shape
#print u.shape

nlat = lat.shape[0]
nlon = lon.shape[0]
ntime = time.shape[0]
nlev = lev.shape[0]


ieq = nlat/2


#print 'a'

tmt = np.mean(t[t1:t2,:,:,:], axis=0)
tmtmlon = np.mean(tmt[:,:,:], axis=2)
#ttt = np.mean(np.mean(tmt[:,:,:], axis=1), axis=1)

#print 'a2'

#potential temperature
#theta = np.zeros((lev.shape[0],lat.shape[0]))
#for i in range(0,lev.shape[0]):
#  theta[i,:] = tmtmlon[i,:]*(p0/100/lev[i])**kappa

#print 'b'

umt = np.mean(u[t1:t2,:,:,:], axis=0)
umtmlon = np.mean(umt[:,:,:], axis=2)

    #vmt = np.mean(v[:,:,:,:], axis=0)
    #vmtmlon = np.mean(vmt[:,:,:], axis=2)

vmt = np.mean(v[t1:t2,:,:,:], axis=0)
vmtmlon = np.mean(vmt[:,:,:], axis=2)


umglob = np.mean(umt)
vmglob = np.mean(vmt)
tmglob = np.mean(tmt)

deg=int(np.ceil(nlat/18.0))
phi1 = ieq-deg
phi2 = ieq+deg
p1   = 7
p2   = nlev

umeq = np.mean(umtmlon[:,phi1:phi2])
vmeq = np.mean(vmtmlon[:,phi1:phi2])
tmeq = np.mean(tmtmlon[:,phi1:phi2])

umst = np.mean(umtmlon[p1:p2,:])
vmst = np.mean(vmtmlon[p1:p2,:])
tmst = np.mean(tmtmlon[p1:p2,:])

umeqst = np.mean(umtmlon[p1:p2,phi1:phi2])
vmeqst = np.mean(vmtmlon[p1:p2,phi1:phi2])
tmeqst = np.mean(tmtmlon[p1:p2,phi1:phi2])

umeqstmax= np.max(umtmlon[p1:p2,phi1:phi2])
umeqstmin= np.min(umtmlon[p1:p2,phi1:phi2])


uout = [umglob,umeq,umst,umeqst,umeqstmax,umeqstmin]
vout = [vmglob,vmeq,vmst,vmeqst,0,0]
tout = [tmglob,tmeq,tmst,tmeqst,0,0]

uoutname=outdir+'ustats_ex1'+'_rot'+str(rotfac)+'_ps'+str(psfac)+'_nmu'+str(nmufac)+'_tsw'+str(tsfac)+'_sol'+str(solfac)+'_dt'+str(days)+'.txt'
try:
  with open(uoutname) as x:
    outfile=open(uoutname,'a')
    outfile.write('%8d  %8d  %8d  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  \n' % (int(args.it), int(YEAR), int(args.start), uout[0], uout[1], uout[2], uout[3], uout[4], uout[5] ) )
except:
  with open(uoutname,'w') as outfile:
    outfile.write('%8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  \n' % ('step','year','time','uglob','ueq','ust','ueqst','umeqstmax','umeqstmin'))
    outfile.write('%8d  %8d  %8d  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  \n' % (int(args.it), int(YEAR), int(args.start), uout[0], uout[1], uout[2], uout[3], uout[4], uout[5] ) )

