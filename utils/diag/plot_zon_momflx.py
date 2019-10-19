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
indir= '/network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT'+'/pumagt_arcb_parameters/'
outdir='plots/momflx2_ex2/'
filename='PUMAG.'+YEAR+'.nc'
if len(sys.argv) == 4: filename=sys.argv[3]
#if len(sys.argv) == 3: filename=sys.argv[2]


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

if len(sys.argv) >= 3:
  outname = sys.argv[1]+sys.argv[2]
  

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
o = f.variables['wap']
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

tmt = np.mean(t[:,:,:,:], axis=0)
tmtmlon = np.mean(tmt[:,:,:], axis=2)
ttt = np.mean(np.mean(tmt[:,:,:], axis=1), axis=1)

#print 'a2'

#potential temperature
theta = np.zeros((lev.shape[0],lat.shape[0]))
for i in range(0,lev.shape[0]):
  theta[i,:] = tmtmlon[i,:]*(p0/100/lev[i])**kappa

#print 'b'

umt = np.mean(u[:,:,:,:], axis=0)
umtmlon = np.mean(umt[:,:,:], axis=2)

    #vmt = np.mean(v[:,:,:,:], axis=0)
    #vmtmlon = np.mean(vmt[:,:,:], axis=2)

vmt = np.mean(v[:,:,:,:], axis=0)
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
M = a * u[:,:,:,:] * np.cos(np.reshape(lat[:],(1,1,nlat,1))/180.0*np.pi)

#u_tm = np.reshape(np.mean(u[:,:,:,:],axis=0),(1,nlev,nlat,nlon))
M_tm = np.reshape(np.mean(M[:,:,:,:],axis=0),(1,nlev,nlat,nlon))
v_tm = np.reshape(np.mean(v[:,:,:,:],axis=0),(1,nlev,nlat,nlon))
o_tm = np.reshape(np.mean(o[:,:,:,:],axis=0),(1,nlev,nlat,nlon))

#u_zm = np.reshape(np.mean(u_tm,axis=3),(ntime,nlev,nlat,1))
M_tmzm = np.reshape(np.mean(M_tm,axis=3),(1,nlev,nlat,1))
v_tmzm = np.reshape(np.mean(v_tm,axis=3),(1,nlev,nlat,1))
o_tmzm = np.reshape(np.mean(o_tm,axis=3),(1,nlev,nlat,1))

#u_tmdev = u[:,:,:,:] - u_tm
M_tmdev = M[:,:,:,:] - M_tm
v_tmdev = v[:,:,:,:] - v_tm
o_tmdev = o[:,:,:,:] - o_tm
#print 'd'

M_tmzmdev = M_tm - M_tmzm
v_tmzmdev = v_tm - v_tmzm
o_tmzmdev = o_tm - o_tmzm

#u_zm = np.reshape(np.mean(u[:,:,:,:],axis=3),(ntime,nlev,nlat,1))
M_zm = np.reshape(np.mean(M[:,:,:,:],axis=3),(ntime,nlev,nlat,1))
v_zm = np.reshape(np.mean(v[:,:,:,:],axis=3),(ntime,nlev,nlat,1))
o_zm = np.reshape(np.mean(o[:,:,:,:],axis=3),(ntime,nlev,nlat,1))

#u_zmdev = u[:,:,:,:] - u_zm
M_zmdev = M[:,:,:,:] - M_zm
v_zmdev = v[:,:,:,:] - v_zm
o_zmdev = o[:,:,:,:] - o_zm 

#Mom      = u * np.cos(np.reshape(lat[:],(1,1,nlat,1))/180.0*np.pi)

#Momprime = Mon[:,:,:,:] - 


#edmomflx [vM] = [v*u*a*cos(phi)]
#total [_v_M]

edmomflx      = np.mean(np.mean(M*v[:,:,:,:],axis=0),axis=2) # dim=(nlev,nlat)
edmomflx_mmc  = np.mean(np.mean(M,axis=0),axis=2) * np.mean(np.mean(v[:,:,:,:],axis=0),axis=2)
#edmomflx_swav = np.mean(np.mean(M_zmdev,axis=0),axis=2) * np.mean(np.mean(v_zmdev,axis=0),axis=2)
edmomflx_swav = np.mean(np.mean(M_tmzmdev*v_tmzmdev,axis=0),axis=2)
edmomflx_twav = np.mean(np.mean(M_tmdev*v_tmdev,axis=0),axis=2)

emf = np.empty([4,nlev,nlat])
emf = np.array([edmomflx, edmomflx_mmc, edmomflx_swav, edmomflx_twav])

vertmomflx      = np.mean(np.mean(M*o[:,:,:,:],axis=0),axis=2)
vertmomflx_mmc  = np.mean(np.mean(M,axis=0),axis=2) * np.mean(np.mean(o[:,:,:,:],axis=0),axis=2)
#vertmomflx_swav = np.mean(np.mean(M_zmdev,axis=0),axis=2) * np.mean(np.mean(o_zmdev,axis=0),axis=2)
vertmomflx_swav = np.mean(np.mean(M_tmzmdev*o_tmzmdev,axis=0),axis=2) 
vertmomflx_twav = np.mean(np.mean(M_tmdev*o_tmdev,axis=0),axis=2)

vmf = np.empty([4,nlev,nlat])
vmf = np.array([vertmomflx, vertmomflx_mmc, vertmomflx_swav, vertmomflx_twav])

print vmf[0,0,32],np.mean(M[:,0,32,:]),np.mean(o[:,0,32,:])

print vmf[0,0,:]

#print emf


#print vmf

#edmomflx     = np.mean(np.mean(u*v,axis=0) * 
#                       np.cos(np.reshape(lat[:],(1,nlat,1))/180.0*np.pi) ,axis=2) # dim=(nlev,nlat)
#edmomflx_mmc = vprimet


strmmin=np.min(emf)
#print strmmin
strmmax=np.max(emf)
#print strmmax
stmax=np.max([strmmax,-strmmin])
#print strmmin,strmmax,stmax
aaa=2.0/12.0
emflevels=np.around(np.arange(-1,1.01,aaa)*stmax,2)

strmmin=np.min(vmf)
#print strmmin
strmmax=np.max(vmf)
#print strmmax
stmax=np.max([strmmax,-strmmin])
print stmax
#print strmmin,strmmax,stmax
aaa=2.0/12.0
vmflevels=np.around(np.arange(-1,1.01,aaa)*stmax,4)
print vmflevels


fig, axarr = plt.subplots(4, 1, sharex='col', figsize=(8,22))

origin = 'lower'

titles1=[r"(a) $[\overline{vM}]$", r"(b) $[\overline{v}][\overline{M}]$", r"(c) $[\overline{v}^*\overline{M}^*]$", r"(d) $[\overline{v'M'}]$" ]
titles2=[r"(a) $[\overline{\omega M}]$", r"(b) $[\overline{\omega}][\overline{M}]$", r"(c) $[\overline{\omega}^*\overline{M}^*]$", r"(d) $[\overline{\omega'M'}]$" ]

for ax,title,i in zip(axarr.ravel(),titles1,[0,1,2,3]):
    a=0
    b=0
    if i ==0: b=umtmlon
    a = emf[i]
    bin = emflevels
    if i==0: ax.text(1+0.2,1+0.05, ncfile, fontsize=9,
        horizontalalignment='right',
        verticalalignment='bottom',
        transform=ax.transAxes)
    cmap = plt.cm.get_cmap("bwr")
    cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
    if i ==0:
      cs2=ax.contour(lat[:],lev[:],b[:,:],8, colors = 'k')
      plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    if i ==0: col=plt.colorbar(cs, cax=cax)#, format='%0.0e')
    else: col=plt.colorbar(cs, cax=cax)
    #lab=r'mPa/s^2'
    lab=r'm$^2$/s$^2$'
    col.set_label(lab)
    #fig.colorbar(cs, ax=ax, shrink=0.9)
    ax.set_title(title)
    ax.xaxis.set_ticks([-60,-30,0,30,60])
    ax.set_ylim([1000*pfac,50*pfac])
    #plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure (hPa)')

plt.tight_layout()
plt.savefig(outdir+'2emf'+outname+'.pdf',format='pdf')

fig, axarr = plt.subplots(4, 1, sharex='col', figsize=(8,22))


for ax,title,i in zip(axarr.ravel(),titles1,[0,1,2,3]):
    a=0
    b=0
    if i ==0: b=umtmlon
    a = emf[i]
    bin = 10#emflevels
    if i==0: ax.text(1+0.2,1+0.05, ncfile, fontsize=9,
        horizontalalignment='right',
        verticalalignment='bottom',
        transform=ax.transAxes)
    cmap = plt.cm.get_cmap("bwr")
    cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
    if i ==0:
      cs2=ax.contour(lat[:],lev[:],b[:,:],8, colors = 'k')
      plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    if i ==0: col=plt.colorbar(cs, cax=cax)#, format='%0.0e')
    else: col=plt.colorbar(cs, cax=cax)
    #lab=r'mPa/s^2'
    lab=r'm$^2$/s$^2$'
    col.set_label(lab)
    #fig.colorbar(cs, ax=ax, shrink=0.9)
    ax.set_title(title)
    ax.xaxis.set_ticks([-60,-30,0,30,60])
    ax.set_ylim([1000*pfac,50*pfac])
    #plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure (hPa)')

plt.tight_layout()
plt.savefig(outdir+'2zemf'+outname+'.pdf',format='pdf')









fig, axarr = plt.subplots(4, 1, sharex='col', figsize=(8,22))

for ax,title,i in zip(axarr.ravel(),titles2,[0,1,2,3]):
    a=0
    b=0
    if i ==0: b=umtmlon
    a = vmf[i]
    bin = vmflevels
    if i==0: ax.text(1+0.2,1+0.05, ncfile, fontsize=9,
        horizontalalignment='right',
        verticalalignment='bottom',
        transform=ax.transAxes)
    cmap = plt.cm.get_cmap("bwr")
    cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    if i ==0: col=plt.colorbar(cs, cax=cax)#, format='%0.0e')
    else: col=plt.colorbar(cs, cax=cax)
    lab=r'mPa/s$^2$'
    #lab=r'm^2/s^2'
    col.set_label(lab)
    #fig.colorbar(cs, ax=ax, shrink=0.9)
    ax.set_title(title)
    ax.xaxis.set_ticks([-60,-30,0,30,60])
    ax.set_ylim([1000*pfac,50*pfac])
    #plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure (hPa)')

plt.tight_layout()
plt.savefig(outdir+'2vmf'+outname+'.pdf',format='pdf')

#fig, axarr = plt.subplots(4, 1, sharex='col', figsize=(8,22))


fig, axarr = plt.subplots(4, 1, sharex='col', figsize=(8,22))

for ax,title,i in zip(axarr.ravel(),titles2,[0,1,2,3]):
    a=0
    b=0
    a = vmf[i]
    bin = 10#vmflevels
    if i==0: ax.text(1+0.2,1+0.05, ncfile, fontsize=9,
        horizontalalignment='right',
        verticalalignment='bottom',
        transform=ax.transAxes)
    cmap = plt.cm.get_cmap("bwr")
    cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    if i ==0: col=plt.colorbar(cs, cax=cax)#, format='%0.0e')
    else: col=plt.colorbar(cs, cax=cax)
    lab=r'mPa/s$^2$'
    #lab=r'm^2/s^2'
    col.set_label(lab)
    #fig.colorbar(cs, ax=ax, shrink=0.9)
    ax.set_title(title)
    ax.xaxis.set_ticks([-60,-30,0,30,60])
    ax.set_ylim([1000*pfac,50*pfac])
    #plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure (hPa)')

plt.tight_layout()
plt.savefig(outdir+'2zvmf'+outname+'.pdf',format='pdf')


sys.exit(0)



for ixx in range(0,360,30):

    edmomflx      = np.mean(np.mean(M*v[:,:,:,:],axis=0),axis=2) # dim=(nlev,nlat)
    edmomflx_mmc  = np.mean(np.mean(M,axis=0),axis=2) * np.mean(np.mean(v[:,:,:,:],axis=0),axis=2)
    #edmomflx_swav = np.mean(np.mean(M_zmdev,axis=0),axis=2) * np.mean(np.mean(v_zmdev,axis=0),axis=2)
    edmomflx_swav = np.mean(np.mean(M_tmzmdev*v_tmzmdev,axis=0),axis=2)
    edmomflx_twav = np.mean(np.mean(M_tmdev*v_tmdev,axis=0),axis=2)

    vertmomflx      = np.mean(np.mean(M*o[:,:,:,:],axis=0),axis=2)
    vertmomflx_mmc  = np.mean(np.mean(M,axis=0),axis=2) * np.mean(np.mean(o[:,:,:,:],axis=0),axis=2)
    #vertmomflx_swav = np.mean(np.mean(M_zmdev,axis=0),axis=2) * np.mean(np.mean(o_zmdev,axis=0),axis=2)
    vertmomflx_swav = np.mean(np.mean(M_tmzmdev*o_tmzmdev,axis=0),axis=2)
    vertmomflx_twav = np.mean(np.mean(M_tmdev*o_tmdev,axis=0),axis=2)


    fig, axarr = plt.subplots(4, 1, sharex='col', figsize=(8,22))

    for ax,title,i in zip(axarr.ravel(),titles2,[0,1,2,3]):
        a=0
        b=0
        a = vmf[i]
        bin = 10#vmflevels
        if i==0: ax.text(1+0.2,1+0.05, ncfile, fontsize=9,
            horizontalalignment='right',
            verticalalignment='bottom',
            transform=ax.transAxes)
        cmap = plt.cm.get_cmap("bwr")
        cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", "5%", pad="3%")
        if i ==0: col=plt.colorbar(cs, cax=cax)#, format='%0.0e')
        else: col=plt.colorbar(cs, cax=cax)
        lab=r'mPa/s$^2$'
        #lab=r'm^2/s^2'
        col.set_label(lab)
        #fig.colorbar(cs, ax=ax, shrink=0.9)
        ax.set_title(title)
        ax.xaxis.set_ticks([-60,-30,0,30,60])
        ax.set_ylim([1000*pfac,50*pfac])
        #plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
        ax.set_xlabel('Latitude')
        ax.set_ylabel('Pressure (hPa)')

    plt.tight_layout()
    plt.savefig(outdir+'2zvmf'+outname+'_m'+str(ixx)+'.pdf',format='pdf')



    for ax,title,i in zip(axarr.ravel(),titles1,[0,1,2,3]):
        a=0
        b=0
        if i ==0: b=umtmlon
        a = emf[i]
        bin = 10#emflevels
        if i==0: ax.text(1+0.2,1+0.05, ncfile, fontsize=9,
            horizontalalignment='right',
            verticalalignment='bottom',
            transform=ax.transAxes)
        cmap = plt.cm.get_cmap("bwr")
        cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
        if i ==0:
            cs2=ax.contour(lat[:],lev[:],b[:,:],8, colors = 'k')
            plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", "5%", pad="3%")
        if i ==0: col=plt.colorbar(cs, cax=cax)#, format='%0.0e')
        else: col=plt.colorbar(cs, cax=cax)
        #lab=r'mPa/s^2'
        lab=r'm$^2$/s$^2$'
        col.set_label(lab)
        #fig.colorbar(cs, ax=ax, shrink=0.9)
        ax.set_title(title)
        ax.xaxis.set_ticks([-60,-30,0,30,60])
        ax.set_ylim([1000*pfac,50*pfac])
        #plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
        ax.set_xlabel('Latitude')
        ax.set_ylabel('Pressure (hPa)')

    plt.tight_layout()
    plt.savefig(outdir+'2zemf'+outname+'_m'+str(ixx)+'.pdf',format='pdf')



















#print vmf[0,0,32],np.mean(np.mean(M[:,0,32,:],axis=3),axis=0),o_tm


sys.exit(1)










edmomflx= np.mean(np.mean(uprime*vprime,axis=3) * 
           np.cos(np.reshape(lat[:],(1,1,nlat))/180.0*np.pi) ,axis=0)
vertmomflx1= np.mean(np.mean(uprime*oprime,axis=3),axis=0) #* 
           #np.cos(np.reshape(lat[:],(1,1,nlat))/180.0*np.pi) ,axis=0)
vertmomflx2= np.mean(np.mean(vprime*oprime,axis=3),axis=0)# * 
           #np.cos(np.reshape(lat[:],(1,1,nlat))/180.0*np.pi) ,axis=0)


edmomflxt= np.mean(np.mean(uprimet*vprimet,axis=3) * 
           np.cos(np.reshape(lat[:],(1,1,nlat))/180.0*np.pi) ,axis=0)
vertmomflxt1= np.mean(np.mean(uprimet*oprimet,axis=3),axis=0) #* 
           #np.cos(np.reshape(lat[:],(1,1,nlat))/180.0*np.pi) ,axis=0)
vertmomflxt2= np.mean(np.mean(vprimet*oprimet,axis=3),axis=0)# * 
           #np.cos(np.reshape(lat[:],(1,1,nlat))/180.0*np.pi) ,axis=0)


#print 'e'

#fig, axarr = plt.subplots(2, 2, sharex='col', sharey='row',figsize=(12,10))i
#fig, axarr = plt.subplots(1, 2, sharex='col', figsize=(12,5))
fig, axarr = plt.subplots(2, 1, sharex='col', figsize=(10,12))

origin = 'lower'
#extends = ["neither", "both", "min", "max"]
#cmap = plt.cm.get_cmap("winter")
#cmap.set_under("magenta")
#cmap.set_over("yellow")

#titles=['(a) mass streamfunction/zonal mean zonal wind',' (b) zonal mean temperature','(d) meridional eddy momentum flux']
titles=[r"(a) $[\overline{u*\omega*}]$", r"(b) $[\overline{v*\omega*}]$"]

bins=15

tmin=np.min(tmtmlon)
tmax=np.max(tmtmlon)
templevels=[]
dag=5
for i in range(100,400,dag):
  #print i
  if i > tmin-dag and i < tmax+dag: templevels.append(i)
  #print templevels

strmmin=np.min(strm)
#print strmmin
strmmax=np.max(strm)
#print strmmax
stmax=np.max([strmmax,-strmmin])
#print strmmin,strmmax,stmax
aaa=2.0/18.0
strmlevels=np.around(np.arange(-1,1.01,aaa)*stmax,2)
#print strmlevels

strmmin=np.min(umtmlon)
#print strmmin
strmmax=np.max(umtmlon)
#print strmmax
stmax=np.max([strmmax,-strmmin])
#print strmmin,strmmax,stmax
aaa=2.0/12.0
ulevels=np.around(np.arange(-1,1.01,aaa)*stmax,2)

strmmin=np.min(edmomflx)
#print strmmin
strmmax=np.max(edmomflx)
#print strmmax
stmax=np.max([strmmax,-strmmin])
#print strmmin,strmmax,stmax
aaa=2.0/12.0
emflevels=np.around(np.arange(-1,1.01,aaa)*stmax,2)

strmmin=np.min(vertmomflx1)
#print strmmin
strmmax=np.max(vertmomflx1)
#print strmmax
stmax=np.max([strmmax,-strmmin])
print stmax
#print strmmin,strmmax,stmax
aaa=2.0/12.0
vmf1levels=np.around(np.arange(-1,1.01,aaa)*stmax,4)
print vmf1levels

strmmin=np.min(vertmomflx2)
#print strmmin
strmmax=np.max(vertmomflx2)
#print strmmax
stmax=np.max([strmmax,-strmmin])
print stmax
#print strmmin,strmmax,stmax
aaa=2.0/12.0
vmf2levels=np.around(np.arange(-1,1.01,aaa)*stmax,4)
print vmf2levels
#plt.text(0, 0, ncfile, fontsize=8)

#fig, axs = plt.subplots(2,2)
for ax,title,i in zip(axarr.ravel(),titles,[0,1]):
    a=0
    b=0
    if i ==0: a=vertmomflx1#strm
    #if i ==0: b=umtmlon
    if i==0: ax.text(1+0.2,1+0.05, ncfile, fontsize=9,
        horizontalalignment='right',
        verticalalignment='bottom',
        transform=ax.transAxes)
   # if i ==0: ax.text(-100, 0, ncfile, fontsize=7, horizontalalignment='left',verticalalignment='top')
    if i ==1: a=vertmomflx2#tmtmlon
    #if i !=1: cmap = plt.cm.get_cmap("BrBG")
    #else: cmap = plt.cm.get_cmap("jet")
    #if i ==3: a=edmomflx
    if i==0: bin=vmf1levels#bins
    #else: bin=10#templevels
    if i==1: bin=vmf2levels#strmlevelsi
    #if i==2: bin=ulevels
    cmap = plt.cm.get_cmap("bwr")
    cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
    #if i ==0: 
    #  cs2=ax.contour(lat[:],lev[:],b[:,:],8, colors = 'k')
    #  plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    if i ==0: col=plt.colorbar(cs, cax=cax)#, format='%0.0e')
    else: col=plt.colorbar(cs, cax=cax)
    if i==0: lab=r'mPa/s^2'
    if i==1: lab='mPa/s^2'
    col.set_label(lab)
    #fig.colorbar(cs, ax=ax, shrink=0.9)
    ax.set_title(title)
    ax.xaxis.set_ticks([-60,-30,0,30,60])
    ax.set_ylim([1000*pfac,100*pfac])
    #plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure (hPa)')
    #ax.yaxis.set_ticks([100,500,900])
    #plt.yticks(np.arange(min(lev), max(lev)+1, 200))
    #ax.locator_params(nbins=4)
    #ax.invert_yaxis()

#plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(outdir+'2vmf_edd_'+outname+'.pdf',format='pdf')





strmmin=np.min(edmomflxt)
#print strmmin
strmmax=np.max(edmomflxt)
#print strmmax
stmax=np.max([strmmax,-strmmin])
#print strmmin,strmmax,stmax
aaa=2.0/12.0
emflevelst=np.around(np.arange(-1,1.01,aaa)*stmax,2)

strmmin=np.min(vertmomflxt1)
#print strmmin
strmmax=np.max(vertmomflxt1)
#print strmmax
stmax=np.max([strmmax,-strmmin])
print stmax
#print strmmin,strmmax,stmax
aaa=2.0/12.0
vmf1levelst=np.around(np.arange(-1,1.01,aaa)*stmax,4)
print vmf1levelst

strmmin=np.min(vertmomflxt2)
#print strmmin
strmmax=np.max(vertmomflxt2)
#print strmmax
stmax=np.max([strmmax,-strmmin])
print stmax
#print strmmin,strmmax,stmax
aaa=2.0/12.0
vmf2levelst=np.around(np.arange(-1,1.01,aaa)*stmax,4)
print vmf2levels
#plt.text(0, 0, ncfile, fontsize=8)




fig, axarr = plt.subplots(2, 1, sharex='col', figsize=(10,12))

titles=[r"(a) $[\overline{u'\omega'}]$", r"(b) $[\overline{v'\omega'}]$"]

for ax,title,i in zip(axarr.ravel(),titles,[0,1]):
    a=0
    b=0
    if i ==0: a=vertmomflxt1#strm
    #if i ==0: b=umtmlon
    if i==0: ax.text(1+0.2,1+0.05, ncfile, fontsize=9,
        horizontalalignment='right',
        verticalalignment='bottom',
        transform=ax.transAxes)
   # if i ==0: ax.text(-100, 0, ncfile, fontsize=7, horizontalalignment='left',verticalalignment='top')
    if i ==1: a=vertmomflxt2#tmtmlon
    #if i !=1: cmap = plt.cm.get_cmap("BrBG")
    #else: cmap = plt.cm.get_cmap("jet")
    #if i ==3: a=edmomflx
    if i==0: bin=vmf1levelst#bins
    #else: bin=10#templevels
    if i==1: bin=vmf2levelst#strmlevelsi
    #if i==2: bin=ulevels
    cmap = plt.cm.get_cmap("bwr")
    cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
    #if i ==0: 
    #  cs2=ax.contour(lat[:],lev[:],b[:,:],8, colors = 'k')
    #  plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    if i ==0: col=plt.colorbar(cs, cax=cax)#, format='%0.0e')
    else: col=plt.colorbar(cs, cax=cax)
    if i==0: lab=r'mPa/s^2'
    if i==1: lab='mPa/s^2'
    col.set_label(lab)
    #fig.colorbar(cs, ax=ax, shrink=0.9)
    ax.set_title(title)
    ax.xaxis.set_ticks([-60,-30,0,30,60])
    ax.set_ylim([1000*pfac,100*pfac])
    #plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure (hPa)')
    #ax.yaxis.set_ticks([100,500,900])
    #plt.yticks(np.arange(min(lev), max(lev)+1, 200))
    #ax.locator_params(nbins=4)
    #ax.invert_yaxis()

#plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(outdir+'2vmf_trans_'+outname+'.pdf',format='pdf')












fig, axarr = plt.subplots(2, 1, sharex='col', figsize=(10,12))

titles=[r"(a) $[\overline{u*v*}]$", r"(b) $[\overline{u'v'}]$"]

for ax,title,i in zip(axarr.ravel(),titles,[0,1]):
    a=0
    b=0
    if i ==0: a=edmomflx#strm
    #if i ==0: b=umtmlon
    if i==0: ax.text(1+0.2,1+0.05, ncfile, fontsize=9,
        horizontalalignment='right',
        verticalalignment='bottom',
        transform=ax.transAxes)
   # if i ==0: ax.text(-100, 0, ncfile, fontsize=7, horizontalalignment='left',verticalalignment='top')
    if i ==1: a=edmomflxt#tmtmlon
    #if i !=1: cmap = plt.cm.get_cmap("BrBG")
    #else: cmap = plt.cm.get_cmap("jet")
    #if i ==3: a=edmomflx
    if i==0: bin=emflevels#bins
    #else: bin=10#templevels
    if i==1: bin=emflevelst#strmlevelsi
    #if i==2: bin=ulevels
    cmap = plt.cm.get_cmap("bwr")
    cs = ax.contourf(lat[:],lev[:],a[:,:],bin, cmap=cmap, origin=origin)
    #if i ==0: 
    #  cs2=ax.contour(lat[:],lev[:],b[:,:],8, colors = 'k')
    #  plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    if i ==0: col=plt.colorbar(cs, cax=cax)#, format='%0.0e')
    else: col=plt.colorbar(cs, cax=cax)
    if i==0: lab=r'm^2/s^2'
    if i==1: lab='m^2/s^2'
    col.set_label(lab)
    #fig.colorbar(cs, ax=ax, shrink=0.9)
    ax.set_title(title)
    ax.xaxis.set_ticks([-60,-30,0,30,60])
    ax.set_ylim([1000*pfac,100*pfac])
    #plt.clabel(cs2,fontsize=11,inline=1,fmt='%1.0f')
    ax.set_xlabel('Latitude')
    ax.set_ylabel('Pressure (hPa)')
    #ax.yaxis.set_ticks([100,500,900])
    #plt.yticks(np.arange(min(lev), max(lev)+1, 200))
    #ax.locator_params(nbins=4)
    #ax.invert_yaxis()

#plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(outdir+'2emf_edd_trans_'+outname+'.pdf',format='pdf')




