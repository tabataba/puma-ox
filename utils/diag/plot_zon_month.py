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
indir= '/media/Seagate5TB/puma'+'/pumagt_arcb_parameters/'
outdir='plots/'
filename='PUMAG.'+YEAR+'.nc'
#if len(sys.argv) == 3: filename=sys.argv[2]

print filename
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

if len(sys.argv) == 3:
  outname = sys.argv[1]+sys.argv[2]



from argparse import ArgumentParser
parser = ArgumentParser()


i#from netCDF4 import Dataset
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

#print 'a'

tmt = np.mean(t[t1:t2,:,:,:], axis=0)
tmtmlon = np.mean(tmt[:,:,:], axis=2)
ttt = np.mean(np.mean(tmt[:,:,:], axis=1), axis=1)

#print 'a2'

#potential temperature
theta = np.zeros((lev.shape[0],lat.shape[0]))
for i in range(0,lev.shape[0]):
  theta[i,:] = tmtmlon[i,:]*(p0/100/lev[i])**kappa

#print 'b'

umt = np.mean(u[t1:t2,:,:,:], axis=0)
umtmlon = np.mean(umt[:,:,:], axis=2)

    #vmt = np.mean(v[:,:,:,:], axis=0)
    #vmtmlon = np.mean(vmt[:,:,:], axis=2)

vmt = np.mean(v[t1:t2,:,:,:], axis=0)
vmtmlon = np.mean(vmt[:,:,:], axis=2)

#print 'c'
h=np.zeros((nlev,nlat))
h=R*tmtmlon[:,:]/(M_air*g)*p0/100
h=29.26*tmtmlon[:,:]
#print h,R,tmtmlon,M_air,g
vml=np.zeros((nlev,nlat))
for i in range(1,nlev-1):
  for j in range(nlat):
    vml[i,j] = np.sum(vmtmlon[i:nlev,j])*p0/10.0 * np.exp(-p0/10.0/h[i,j])# 10000 thickness of one layer in Pa

strm = np.zeros((nlev,nlat))
for i in range(nlev):
  for j in range(nlat):
    strm[i,j] = 2*np.pi*a*math.cos(lat[j]*np.pi/180.0)*vml[i,j]*p0/(g*h[i,j])

#strm=strm*1E-6

uprime = u[:,:,:,:] - np.reshape(np.mean(u[:,:,:,:],axis=3),(ntime,nlev,nlat,1))
vprime = v[:,:,:,:] - np.reshape(np.mean(v[:,:,:,:],axis=3),(ntime,nlev,nlat,1))

#print 'd'

edmomflx= np.mean(np.mean(uprime[t1:t2,:,:,:]*vprime[t1:t2,:,:,:],axis=3) * 
           np.cos(np.reshape(lat[:],(1,1,nlat))/180.0*np.pi) ,axis=0)

#print 'e'

#fig, axarr = plt.subplots(2, 2, sharex='col', sharey='row',figsize=(12,10))i
#fig, axarr = plt.subplots(1, 2, sharex='col', figsize=(12,5))
fig, axarr = plt.subplots(2, 1, sharex='col', figsize=(10,12))

origin = 'lower'
#extends = ["neither", "both", "min", "max"]
#cmap = plt.cm.get_cmap("winter")
#cmap.set_under("magenta")
#cmap.set_over("yellow")

titles=['(a) mass streamfunction/zonal mean zonal wind',' (b) zonal mean temperature','(d) meridional eddy momentum flux']


bins=15

tmin=np.min(tmtmlon)
tmax=np.max(tmtmlon)
templevels=[]

tmaxsav=tmax
tminsav=tmin

strmmin=np.min(strm)
#print strmmin
strmmax=np.max(strm)
#print strmmax
stmaxsav=np.max([strmmax,-strmmin])
#print strmmin,strmmax,stmax
aaa=2.0/18.0
#strmlevels=np.around(np.arange(-1,1.01,aaa)*stmax,2)
#print strmlevels

#smaxsav=stmax

umin=np.min(umtmlon)
#print strmmin
umax=np.max(umtmlon)
#print strmmax
umaxsav=np.max([umax,-umin])
#print strmmin,strmmax,stmax
aaa=2.0/12.0
#ulevels=np.around(np.arange(-1,1.01,aaa)*umax,2)

#umaxsav=umax

emin=np.min(edmomflx)
#print strmmin
emax=np.max(edmomflx)
#print strmmax
emaxsav=np.max([emax,-emin])
#print strmmin,strmmax,stmax
aaa=2.0/12.0
#emflevels=np.around(np.arange(-1,1.01,aaa)*stmax,2)

#emaxsav=max

maxsav=[[tminsav,tmaxsav,stmaxsav,umaxsav,emaxsav]]

with open('max_file.txt','a') as f_handle:
  np.savetxt(f_handle,maxsav)


sys.exit(1)


templevels=[]
dag=5
for i in range(100,400,dag):
  #print i
  if i > tmin-dag and i < tmax+dag: templevels.append(i)
  #print templevels

strmlevels=np.around(np.arange(-1,1.01,aaa)*stmax,2)
ulevels=np.around(np.arange(-1,1.01,aaa)*umax,2)
emflevels=np.around(np.arange(-1,1.01,aaa)*stmax,2)



#plt.text(0, 0, ncfile, fontsize=8)

#fig, axs = plt.subplots(2,2)
for ax,title,i in zip(axarr.ravel(),titles,[0,1]):
    a=0
    b=0
    if i ==0: a=strm
    if i ==0: b=umtmlon
    if i ==0: ax.text(-100, 0, ncfile, fontsize=7, horizontalalignment='left',verticalalignment='top')
    if i ==1: a=tmtmlon
    if i !=1: cmap = plt.cm.get_cmap("BrBG")
    else: cmap = plt.cm.get_cmap("jet")
    #if i ==3: a=edmomflx
    if i!=1: bin=10#bins
    else: bin=10#templevels
    if i==0: bin=18#strmlevelsi
    #if i==2: bin=ulevels
    #cmap = plt.cm.get_cmap("BrBG")
    cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
    if i ==0: 
      cs2=ax.contour(lat[:],lev[:],b[:,:],8, colors = 'k')
      plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    if i ==0: col=plt.colorbar(cs, cax=cax, format='%0.0e')
    else: col=plt.colorbar(cs, cax=cax)
    if i==0: lab=r'kg/s'
    if i==1: lab='K'
    col.set_label(lab)
    #fig.colorbar(cs, ax=ax, shrink=0.9)
    ax.set_title(title)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure (hPa)')
    ax.locator_params(nbins=4)
    ax.invert_yaxis()

#plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(outdir+'2'+outname+'.pdf',format='pdf')



matplotlib.rcParams.update({'font.size': 13})
fig, axarr = plt.subplots(2, 1, sharex='col', figsize=(6,8))
for ax,title,i in zip(axarr.ravel(),titles,[0,1]):
    a=0
    b=0
    if i ==0: a=strm
    if i ==0: b=umtmlon
    #if i ==0: ax.text(-100, 0, ncfile, fontsize=7, horizontalalignment='left',verticalalignment='top')
    if i ==1: a=tmtmlon
    if i !=1: cmap = plt.cm.get_cmap("bwr")
    else: cmap = plt.cm.get_cmap("jet")
    #if i ==3: a=edmomflx
    if i!=1: bin=10#bins
    else: bin=10#templevels
    if i==0: bin=18#strmlevelsi
    #if i==2: bin=ulevels
    #cmap = plt.cm.get_cmap("BrBG")
    cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
    if i ==0:
      cs2=ax.contour(lat[:],lev[:],b[:,:],8, colors = 'k')
      plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    if i ==0: col=plt.colorbar(cs, cax=cax, format='%0.0e')
    else: col=plt.colorbar(cs, cax=cax)
    if i==0: lab=r'kg/s'
    if i==1: lab='K'
    col.set_label(lab)
    #fig.colorbar(cs, ax=ax, shrink=0.9)
    ax.set_title(title)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure (hPa)')
    ax.locator_params(nbins=4)
    ax.invert_yaxis()

#plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(outdir+'2x'+outname+'.pdf',format='pdf')







#sys.exit(0)

titles2=['(a) mass streamfunction',' (b) zonal mean temperature', '(c) zonal mean zonal wind','(d) meridional eddy momentum flux']


matplotlib.rcParams.update({'font.size': 20})
fig, axarr = plt.subplots(2, 2, sharex='col', figsize=(16,12))
for ax,title,i in zip(axarr.ravel(),titles2,[0,1,2,3]):
    a=0
    b=0
    if i ==0: a=strm
    #if i ==0: b=umtmlon
    if i ==0: ax.text(-100, 0, ncfile, fontsize=7, horizontalalignment='left',verticalalignment='top')
    if i ==1: a=tmtmlon
    if i ==1: b=theta
    if i !=1: cmap = plt.cm.get_cmap("bwr")
    else: cmap = plt.cm.get_cmap("CMRmap")
    #if i==2: plt.cm.get_cmap("CMRmap")
    if i ==2: a=umtmlon
    if i ==3: a=edmomflx
    #if i ==3: a=edmomflx
    if i!=1: bin=10#bins
    else: bin=14#templevels
    if i==0: bin=18#strmlevels
    if i==2: bin=ulevels
    if i==3: bin=emflevels
    #cmap = plt.cm.get_cmap("BrBG")
    amin=np.min(a)
    amax=np.max(a)
    aamax=np.max([amax,-amin])
    cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
    #cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin,vmin=-aamax,vmax=aamax)
    if i ==1:
      cs2=ax.contour(lat[:],lev[:],b[:,:],8, colors = 'k')
      plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    if i ==0: col=plt.colorbar(cs, cax=cax, format='%0.0e')
    else: col=plt.colorbar(cs, cax=cax)
    if i==0: lab=r'kg/s'
    if i==1: lab='K'
    if i==2: lab='m/s'
    if i==3: lab=r'm$^2$/s$^2$'
    col.set_label(lab)
    #fig.colorbar(cs, ax=ax, shrink=0.9)
    ax.set_title(title)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure (hPa)')
    ax.locator_params(nbins=4)
    ax.invert_yaxis()

plt.tight_layout()
plt.savefig(outdir+'4'+outname+'.pdf',format='pdf')




fig, axarr = plt.subplots(2, 2, sharex='col', figsize=(16,12))
for ax,title,i in zip(axarr.ravel(),titles2,[0,1,2,3]):
    a=0
    b=0
    if i ==0: a=strm
    #if i ==0: b=umtmlon
    #if i ==0: ax.text(-100, 0, ncfile, fontsize=7, horizontalalignment='left',verticalalignment='top')
    if i ==1: a=tmtmlon
    if i ==1: b=theta
    if i !=1: cmap = plt.cm.get_cmap("bwr")
    else: cmap = plt.cm.get_cmap("jet")
    #if i==2: plt.cm.get_cmap("CMRmap")
    if i ==2: a=umtmlon
    if i ==3: a=edmomflx
    #if i ==3: a=edmomflx
    if i!=1: bin=10#bins
    else: bin=14#templevels
    if i==0: bin=18#strmlevels
    if i==2: bin=ulevels
    if i==3: bin=emflevels
    #cmap = plt.cm.get_cmap("BrBG")
    amin=np.min(a)
    amax=np.max(a)
    aamax=np.max([amax,-amin])
    cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
    #cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin,vmin=-aamax,vmax=aamax)
    if i ==1:
      cs2=ax.contour(lat[:],lev[:],b[:,:],8, colors = 'k')
      plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    if i ==0: col=plt.colorbar(cs, cax=cax, format='%0.0e')
    else: col=plt.colorbar(cs, cax=cax)
    if i==0: lab=r'kg/s'
    if i==1: lab='K'
    if i==2: lab='m/s'
    if i==3: lab=r'm$^2$/s$^2$'
    col.set_label(lab)
    #fig.colorbar(cs, ax=ax, shrink=0.9)
    ax.set_title(title)
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure (hPa)')
    ax.locator_params(nbins=4)
    ax.invert_yaxis()

plt.tight_layout()
plt.savefig(outdir+'4x'+outname+'.pdf',format='pdf')




sys.exit(0)

fig = plt.figure(figsize=(10,6))
ax = plt.gca()
#cs = plt.contourf(lon[:],lat[:],t[310,0,:,:],15)
cs.set_clim(vmin=tmin,vmax=tmax)
divider=make_axes_locatable(ax)
cax = divider.append_axes("right", "5%", pad="3%")
col =fig.colorbar(cs,cax=cax)
col.set_label('K')
ax.set_xlabel('Latitude')
ax.set_ylabel('Pressure (hPa)')
plt.tight_layout()
plt.savefig('4'+outname+'.pdf',format='pdf')


#vmin=np.min(v[:,:,:,:])
#vmax=np.max(v[:,:,:,:])


fig = plt.figure(figsize=(10,6))
ax = plt.gca()
cs = plt.contourf(lon[:],lat[:],v[310,0,:,:],15)
#cs.set_clim(vmin=vmin,vmax=vmax)
divider=make_axes_locatable(ax)
cax = divider.append_axes("right", "5%", pad="3%")
col =fig.colorbar(cs,cax=cax)
col.set_label('m/s')
ax.set_xlabel('Latitude')
ax.set_ylabel('Pressure (hPa)')
plt.tight_layout()
plt.savefig(outname+'3.pdf',format='pdf')