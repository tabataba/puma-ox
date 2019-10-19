#!/usr/bin/python

## From energy_boer2.py
from __future__ import print_function
import numpy as np
from scipy.io import netcdf
import math 
import matplotlib.pyplot as plt
import sys 
import os 
import subprocess as sub
import re
import time as tt
from scipy import stats
from scipy.interpolate import interp1d
from scipy.interpolate import piecewise_polynomial_interpolate
from scipy.interpolate import barycentric_interpolate
from scipy import interp

from argparse import ArgumentParser
parser = ArgumentParser()


def time_mean(inp,):
  #print(inp.shape)
  #print(inp.shape[0])
  if inp.shape[0] == 360: 
    #print('360!!')
    ix = 360/12

  if len(inp.shape) == 1:
    #print(1)
    out = np.zeros((12))
    for i in range(12):
      out[i] = np.mean(inp[i*ix:(i+1)*ix],axis=0)
  if len(inp.shape) == 2:
    #print(2)
    out = np.zeros((12,inp.shape[1]))
    for i in range(12):
      out[i,:] = np.mean(inp[i*ix:(i+1)*ix,:],axis=0)
  if len(inp.shape) == 3:
    #print(3)
    out = np.zeros((12,inp.shape[1],inp.shape[2]))
    for i in range(12):
      out[i,:,:] = np.mean(inp[i*ix:(i+1)*ix,:,:],axis=0)
  if len(inp.shape) == 4:
    #print(4)
    out = np.zeros((12,inp.shape[1],inp.shape[2],inp.shape[3]))
    for i in range(12):
      out[i,:,:,:] = np.mean(inp[i*ix:(i+1)*ix,:,:,:],axis=0)
  return out

def time_dept(inp,inp2):
  #print(inp.shape)
  #print(inp2.shape)
  if inp.shape[0] == 360: 
    #print('360!!')
    ix = 360/12

  if len(inp.shape) == 1:
    #print(1)
    out = np.zeros((inp.shape[0]))
    for i in range(12):
      out[i*ix:(i+1)*ix] = inp[i*ix:(i+1)*ix] - inp2[i]
  if len(inp.shape) == 2:
    #print(2)
    out = np.zeros((inp.shape[0],inp.shape[1]))
    for i in range(12):
      out[i*ix:(i+1)*ix,:] = inp[i*ix:(i+1)*ix,:] - np.reshape(inp2[i,:],(1,inp.shape[1]))
  if len(inp.shape) == 3:
    #print(3)
    out = np.zeros((inp.shape[0],inp.shape[1],inp.shape[2]))
    for i in range(12):
      out[i*ix:(i+1)*ix,:,:] = inp[i*ix:(i+1)*ix,:,:] - np.reshape(inp2[i,:,:],(1,inp.shape[1],inp.shape[2]))
  if len(inp.shape) == 4:
    #print(4)
    out = np.zeros((inp.shape[0],inp.shape[1],inp.shape[2],inp.shape[3]))
    for i in range(12):
      #print(inp.shape,inp2.shape)
      x=np.reshape(inp2[i,:,:,:],(1,inp.shape[1],inp.shape[2],inp.shape[3]))
      #print(inp[i:i+ix,:,:,:].shape,inp2[i,:,:,:].shape,x.shape)
      out[i*ix:(i+1)*ix,:,:,:] = inp[i*ix:(i+1)*ix,:,:,:] - np.reshape(inp2[i,:,:,:],(1,inp.shape[1],inp.shape[2],inp.shape[3]))
  return out



def integrate(math,lat,dlam_rad_int,dlat_rad,dp,ieq,ntime,nlev,nlat,nlon,typ='lon'):
  g = 9.81

  if typ=='lon':
    out = np.zeros(ntime)
    outsav = np.zeros((ntime,nlev,nlat,nlon))
    hout = np.zeros((2,ntime))

    for k in range(nlev):
      for j in range(0,nlat):
        for l in range(nlon):
          dm = np.cos(np.pi/180.0*lat[j]) * np.sin(dlat_rad[j]/2.0) * dlam_rad_int * dp[k]# *a**2
          out = out + math[:,k,j,l] * dm
          outsav[:,k,j,l] = math[:,k,j,l]#/g* dm /(4*np.pi*g)#factor????
      #Northern Hemisphere
      for jx in range(0,ieq):
        for l in range(nlon):
          dm = np.cos(np.pi/180.0*lat[jx]) * np.sin(dlat_rad[jx]/2.0) * dlam_rad_int  * dp[k]# *a**2
          hout[0,:] = hout[0,:] + math[:,k,jx,l] * dm
      #Southern Hemisphere
      for jy in range(ieq,nlat):
        for l in range(nlon):
          dm = np.cos(np.pi/180.0*lat[jy]) * np.sin(dlat_rad[jy]/2.0) * dlam_rad_int * dp[k]# *a**2
          hout[1,:] = hout[1,:] + math[:,k,jy,l] * dm

    out = out/(2*np.pi*g)
    hout = hout*2.0/(2*np.pi*g)

  if typ=='zm':
    out = np.zeros(ntime)
    outsav = np.zeros((ntime,nlev,nlat))
    hout = np.zeros((2,ntime))

    for k in range(nlev):
      for j in range(0,nlat):
        for l in range(nlon):
          dm = np.cos(np.pi/180.0*lat[j]) * np.sin(dlat_rad[j]/2.0) * dlam_rad_int * dp[k]# *a**2
          out = out + math[:,k,j] * dm
          outsav[:,k,j] = math[:,k,j]#/g* dm /(4*np.pi*g)#factor????
      #Northern Hemisphere
      for jx in range(0,ieq):
        for l in range(nlon):
          dm = np.cos(np.pi/180.0*lat[jx]) * np.sin(dlat_rad[jx]/2.0) * dlam_rad_int  * dp[k]# *a**2
          hout[0,:] = hout[0,:] + math[:,k,jx] * dm
      #Southern Hemisphere
      for jy in range(ieq,nlat):
        for l in range(nlon):
          dm = np.cos(np.pi/180.0*lat[jy]) * np.sin(dlat_rad[jy]/2.0) * dlam_rad_int * dp[k]# *a**2
          hout[1,:] = hout[1,:] + math[:,k,jy] * dm

    out = out/(2*np.pi*g)
    hout = hout*2.0/(2*np.pi*g)

  if typ=='sig':

    out = np.zeros(ntime)
    outsav = np.zeros((ntime,nlat,nlon))
    hout = np.zeros((2,ntime))

    for j in range(0,nlat):
      for l in range(nlon):
        dsigma = np.cos(np.pi/180.0*lat[j]) * dlam_rad_int * (-1.0) * np.sin(dlat_rad[j]/2.0)
        out = out + math[:,j,l] * dsigma
        outsav[:,j,l] = math[:,j,l]#/g* dm /(4*np.pi*g)#factor????

    for jx in range(0,ieq):
      for l in range(nlon):
        dsigma = np.cos(np.pi/180.0*lat[jx]) * dlam_rad_int * (-1.0) * np.sin(dlat_rad[jx]/2.0)
        hout[0,:] = hout[0,:] + math[:,jx,l] * dsigma
    for jy in range(ieq,nlat):
      for l in range(nlon):
        dsigma = np.cos(np.pi/180.0*lat[jy]) * dlam_rad_int * (-1.0) * np.sin(dlat_rad[jy]/2.0)
        hout[1,:] = hout[1,:] + math[:,jy,l] * dsigma

    out = out/(2*np.pi*g)
    hout = hout*2.0/(2*np.pi*g)

  if typ=='sigzm':

    out = np.zeros(ntime)
    outsav = np.zeros((ntime,nlat))
    hout = np.zeros((2,ntime))

    for j in range(0,nlat):
      for l in range(nlon):
        dsigma = np.cos(np.pi/180.0*lat[j]) * np.sin(dlat_rad[j]/2.0) * dlam_rad_int * (-1.0)
        out = out + math[:,j] * dsigma
        outsav[:,j] = math[:,j]#/g* dm /(4*np.pi*g)#factor????

    for jx in range(0,ieq):
      for l in range(nlon):
        dsigma = np.cos(np.pi/180.0*lat[jx]) * np.sin(dlat_rad[jx]/2.0) * dlam_rad_int * (-1.0)
        hout[0,:] = hout[0,:] + math[:,jx] * dsigma
    for jy in range(ieq,nlat):
      for l in range(nlon):
        dsigma = np.cos(np.pi/180.0*lat[jy]) * np.sin(dlat_rad[jy]/2.0) * dlam_rad_int * (-1.0)
        hout[1,:] = hout[1,:] + math[:,jy] * dsigma

    out = out/(2*np.pi*g)
    hout = hout*2.0/(2*np.pi*g)

  return out,outsav,hout


def read_nc(ncfile,nmu):

  f= netcdf.netcdf_file(ncfile,'r')

  time = f.variables['time']
  lat = f.variables['lat']
  lon = f.variables['lon']
  lev = f.variables['lev']

  ntime= len(time[:])
  nlev = len(lev[:])
  nlat = len(lat[:])
  nlon = len(lon[:])

  t =  f.variables['ta']
  u =  f.variables['ua']
  v =  f.variables['va']
  wap = f.variables['wap']
  #dens = f.variables['dens']
  #psurf = f.variables['psurf']
  psurf = 0
  dens=0
  #ls = f.variables['Ls']
  ls = time[:]

  #if nmu==0:
  #  t2 = np.zeros((ntime,nlev,nlat,nlon))
  #  u2 = np.zeros((ntime,nlev,nlat,nlon))
  #  v2 = np.zeros((ntime,nlev,nlat,nlon))
  #  wap2=np.zeros((ntime,nlev,nlat,nlon))
  #  if ntime==(360*6):
  #    t2[0:60,:,:,:]     = t[360*6-60:360*6,:,:,:]
  #    t2[60:360*6,:,:,:] = t[0:360*6-60,:,:,:]
  #    u2[0:60,:,:,:]     = u[360*6-60:360*6,:,:,:]
  #    u2[60:360*6,:,:,:] = u[0:360*6-60,:,:,:]
  #    v2[0:60,:,:,:]     = v[360*6-60:360*6,:,:,:]
  #    v2[60:360*6,:,:,:] = v[0:360*6-60,:,:,:]
  #    wap2[0:60,:,:,:]     = wap[360*6-60:360*6,:,:,:]
  #    wap2[60:360*6,:,:,:] = wap[0:360*6-60,:,:,:]
  #else:
  if True:
    t2  =  t[:,:,:,:]
    u2  =  u[:,:,:,:]
    v2  =  v[:,:,:,:]
    wap2=wap[:,:,:,:]


  return lat,lev,lon,time,t2,u2,v2,wap2,dens,psurf,ls


def make_daily_mean(ncfile,nmu):

  g = 9.81
  #tx1=int(t1)-30
  #tx2=int(t2)-30
  #ty1=int(t1)+30
  #ty2=int(t2)+30

  #dirname=os.path.dirname(ncfile)

  print('reading')

  lat,lev,lon,time,ta,ua,va,wapa,dens,psurf,ls = read_nc(ncfile,nmu)

  #p=lev:]
  p=lev[:]*100
  nlat = len(lat[:])
  nlev = len(lev[:])
  nlon = len(lon[:])
  ntime= len(time[:])

  print('densa')

  densa = np.zeros((ntime,nlev,nlat,nlon))
  densa = np.reshape(p,(1,nlev,1,1))/(R_spec*ta[:,:,:,:])

  #wa = - densa[:,:,:,:] * g * wapa[:,:,:,:] 
  wa = wapa[:,:,:,:]*100
  alphaa = 1/densa[:,:,:,:]
  #betaa = ~np.isnan(ta[:,:,:,:])


  if True:
    tx = np.zeros((ntime,nlev,nlat,nlon))
    tx[:] = np.NaN
    ux = tx
    vx = tx
    wapx = tx
    densx = tx
    wx=tx
    #psurfx = np.zeros((ntime,nlat,nlon))
    alphax = tx
    betax = tx

  if True:
    ty = np.zeros((ntime,nlev,nlat,nlon))
    ty[:] = np.NaN
    uy = ty
    vy = ty
    wapy = ty
    densy = ty
    wy = ty
    #psurfy = np.zeros((ntime,nlat,nlon))
    alphay = ty
    betay = ty


  print('z')

  tz=np.concatenate((tx[:,:,:,:],ta[:,:,:,:],ty[:,:,:,:]),axis=0)
  uz=np.concatenate((ux[:,:,:,:],ua[:,:,:,:],uy[:,:,:,:]),axis=0)
  vz=np.concatenate((vx[:,:,:,:],va[:,:,:,:],vy[:,:,:,:]),axis=0)
  wapz=np.concatenate((wapx[:,:,:,:],wapa[:,:,:,:],wapy[:,:,:,:]),axis=0)
  densz=np.concatenate((densx[:,:,:,:],densa[:,:,:,:],densy[:,:,:,:]),axis=0)
  #psurfz=np.concatenate((psurfx[:,:,:],psurfa[:,:,:],psurfy[:,:,:]),axis=0)
  wz=np.concatenate((wx[:,:,:,:],wa[:,:,:,:],wy[:,:,:,:]),axis=0)
  alphaz=np.concatenate((alphax[:,:,:,:],alphaa[:,:,:,:],alphay[:,:,:,:]),axis=0)

  nlat2 = len(lat[:])
  nlev2 = len(lev[:])
  nlon2 = len(lon[:])
  ntime2= 3*len(time[:])
  #weightz = make_weight(psurfz,p,ntime2,nlev2,nlat2,nlon2)

  #betaz=np.concatenate((betax[:,:,:,:],betaa[:,:,:,:],betay[:,:,:,:]),axis=0)#*np.nan_to_num(weightz)

  print('out')

  #ntimes = ntime - 6 * int(nofy) - 6 * int(nofx) 
  t = np.zeros((ntime,nlev,nlat,nlon))
  u = np.zeros((ntime,nlev,nlat,nlon))
  v = np.zeros((ntime,nlev,nlat,nlon))
  wap = np.zeros((ntime,nlev,nlat,nlon))
  dens = np.zeros((ntime,nlev,nlat,nlon))  
  psurf = 0# np.zeros((ntime,nlat,nlon))  
  wout = np.zeros((ntime,nlev,nlat,nlon))
  alphaout = np.zeros((ntime,nlev,nlat,nlon))
  #betaout = np.zeros((ntime,nlev,nlat,nlon))

  print('time_mean')

  for i in range(ntime):
    ti1=ntime+i-3
    ti2=ntime+i+3
    t[i,:,:,:] = stats.nanmean(tz[ti1:ti2,:,:,:],axis=0)
    u[i,:,:,:] = stats.nanmean(uz[ti1:ti2,:,:,:],axis=0)
    v[i,:,:,:] = stats.nanmean(vz[ti1:ti2,:,:,:],axis=0)
    wap[i,:,:,:] = stats.nanmean(wapz[ti1:ti2,:,:,:],axis=0)
    dens[i,:,:,:] = stats.nanmean(densz[ti1:ti2,:,:,:],axis=0)
    #psurf[i,:,:] = stats.nanmean(psurfz[ti1:ti2,:,:],axis=0)
    #psurf=0
    wout[i,:,:,:] = stats.nanmean(wz[ti1:ti2,:,:],axis=0)
    alphaout[i,:,:,:] = stats.nanmean(alphaz[ti1:ti2,:,:],axis=0)
    #betaout[i,:,:,:] = stats.nanmean(betaz[ti1:ti2,:,:],axis=0) #is not nan

  #weightx = make_weight(psurf,p,ntime,nlev,nlat,nlon)

  #betaout=betaout#*np.nan_to_num(weightx)

  print('del')

  del(tz,tx,ta,ty)
  del(uz,ux,ua,uy)
  del(vz,vx,va,vy)
  del(wapz,wapx,wapa,wapy)
  del(densz,densx,densa,densy)
  del(wz,wx,wa,wy)
  #uz=np.concatenate((ux[:,:,:,:],ua[:,:,:,:],uy[:,:,:,:]),axis=0)
  #vz=np.concatenate((vx[:,:,:,:],va[:,:,:,:],vy[:,:,:,:]),axis=0)
  #wapz=np.concatenate((wapx[:,:,:,:],wapa[:,:,:,:],wapy[:,:,:,:]),axis=0)
  #densz=np.concatenate((densx[:,:,:,:],densa[:,:,:,:],densy[:,:,:,:]),axis=0)
  ##psurfz=np.concatenate((psurfx[:,:,:],psurfa[:,:,:],psurfy[:,:,:]),axis=0)
  #wz=np.concatenate((wx[:,:,:,:],wa[:,:,:,:],wy[:,:,:,:]),axis=0)
  #alphaz

  return lat,lev,lon,time,t,u,v,wap,dens,psurf,ls,wout,alphaout



if __name__ == "__main__":

  time1 = float(tt.time())

  parser.add_argument("-d","--dailymean",action="store_true")
  parser.add_argument("-n","--nmu",action="store_true")
  parser.add_argument("-p","--path",action="store",type=str)
  parser.add_argument("-o","--output",action="store",type=str)
  parser.add_argument("-v","--version",action="store",type=str)

  args, unknown = parser.parse_known_args()

  nmu=args.nmu

  a_Earth = 6400000.0
  R = 8.3144621
  M_air = 28.98  # Earth
  M_mars = 43.49 #g/mol # Mars
  R_spec = R/M_air*1000 # 1000g per kg
  print(R_spec)
  g = 9.81   # Mars
  a = a_Earth
  kappa = 0.286 #8.3144621 / 43.49 / 0.8312 # R/M/cp from Fred Taylor book
  cp = 1000.0 #spec heat in J/(kg K)
  p0 = 100000 #1000hPa in Pa #610.0 #6.1 # Mars reference 610 Pa = 6.1 hPa
  gravc = 6.673e-11 #Nm^2/kg^2
  mass_mars = 6.4185e23 #kg

  if args.path == None:
    ncfile = '/a/jupiter/local/home/jupiter/gfd2/tabataba/models/runs/diagnostics/gh-ob23/gh-ob23-1omg.010.nc'
  else:
    ncfile = args.path

  ncfile = os.path.realpath(ncfile)

  if not os.path.exists(ncfile):
    sys.stderr.write('the file at ' + ncfile + ' does not exist.')
    sys.stderr.write('continuing ...')
    sys.exit(1)



  if args.dailymean == False:

    lat,lev,lon,time,t,u,v,wap,d0,psurf,ls = read_nc(ncfile,nmu)
    w = wap[:,:,:,:]*100   # w=omega
    #alpha = 1/dens[:,:,:,:]

    p=lev[:]*100
    nlat = len(lat[:])
    nlev = len(lev[:])
    nlon = len(lon[:])
    ntime= len(time[:])


    #print(lev[:])
    dens = np.zeros((ntime,nlev,nlat,nlon))
    dens = np.reshape(p,(1,nlev,1,1))/(R_spec*t[:,:,:,:])
    print(dens[1,:,1,1])
    #time,lev,lat,lon
    #weight = make_weight(psurf,p,ntime,nlev,nlat,nlon)
    #beta = ~np.isnan(t[:,:,:,:])#*np.nan_to_num(weight)
    #print(w[:,:,:,:].shape)
    alpha = 1/dens[:,:,:,:]

  else:
    lat,lev,lon,time,t,u,v,wap,dens,psurf,ls,w,alpha = make_daily_mean(ncfile,nmu)

    p=lev[:]*100
    nlat = len(lat[:])
    nlev = len(lev[:])
    nlon = len(lon[:])
    ntime= len(time[:])


  dp = np.zeros((nlev))
  dp[0] = (p[0] - p[1])#/2.0
  dp[nlev-1] = p[nlev-2] - p[nlev-1]
  for k in range(1,nlev-1):
    dp[k] = (p[k-1] + p[k])/2.0 - (p[k] + p[k+1])/2.0
  print(dp)
  #dp=[10000,10000,10000,10000,10000,10000,10000,10000,10000,10000]


  dlat_np = abs(90 - ( (lat[0]+lat[1])/2.0 ))
  dlat_sp = abs(-90 - ( (lat[nlat-1]+lat[nlat-2])/2.0 ))

  dlat = np.zeros(nlat)
  dlat[0]      = dlat_np
  dlat[nlat-1] = dlat_sp
  for i in range (1, nlat-1):
    dlat[i] = (lat[i-1]+lat[i])/2.0 - (lat[i]+lat[i+1])/2.0
  if dlat[3] < 0: 
    dlat[0]      = - dlat[0]
    dlat[nlat-1] = - dlat[nlat-1]
  dlat_rad = dlat / 180.0 * np.pi
  print(dlat_rad)
  print(np.sum(dlat))

  dlam = lon[0] - lon[1]
  dlam_rad = dlam / 180.0 * np.pi
  dlam_rad_int = np.absolute(dlam_rad)

  vzmR   = stats.nanmean(v[:,:,:,:], axis=3)
  uzmR   = stats.nanmean(u[:,:,:,:], axis=3)
  wzmR   = stats.nanmean(w[:,:,:,:], axis=3)

  uvsq   = vzmR[:,:,:]**2 + uzmR[:,:,:]**2

  vstar  = v[:,:,:,:] - np.reshape(vzmR[:,:,:],(ntime,nlev,nlat,1))
  ustar  = u[:,:,:,:] - np.reshape(uzmR[:,:,:],(ntime,nlev,nlat,1))
  wstar  = w[:,:,:,:] - np.reshape(wzmR[:,:,:],(ntime,nlev,nlat,1))

  uvstarsq = vstar[:,:,:,:]**2 + ustar[:,:,:,:]**2
  uvstarsqzm = stats.nanmean(uvstarsq[:,:,:,:], axis=3)

  ieq = nlat/2

#####################################################
#~~~~~~~~~~~~~~~~~~~   KZ + KE    ~~~~~~~~~~~~~~~~~~#
#####################################################

  mathkz = 0.5 * uvsq[:,:,:]

  kz,kzsav,hkz=integrate(mathkz,lat,dlam_rad_int,dlat_rad,dp,ieq,ntime,nlev,nlat,nlon,typ='zm')

  mathke = 0.5 *  stats.nanmean(uvstarsq[:,:,:,:], axis=3) 

  ke,kesav,hke=integrate(mathke,lat,dlam_rad_int,dlat_rad,dp,ieq,ntime,nlev,nlat,nlon,typ='zm')

  print('kz',np.mean(kz),'ke',np.mean(ke))

#####################################################
#~~~~~~~~~~~~~~~~~~~      CK      ~~~~~~~~~~~~~~~~~~#
#####################################################

  #1
  ustarsqzm = stats.nanmean( ustar[:,:,:,:]**2, axis=3)
  f1        = uzmR[:,:,:]/np.reshape((a*np.cos(np.pi/180.0*lat[:])),(1,1,nlat))
  duRdlam   = 0 * f1

  x1 = (ustarsqzm[:,:,:] * duRdlam[:,:,:] /
        np.reshape((a*np.cos(np.pi/180.0*lat[:])),(1,1,nlat)) 
       )

  #2
  uvstarzm = stats.nanmean( ustar[:,:,:,:]*vstar[:,:,:,:], axis=3)
  duRdphi  = np.zeros((ntime,nlev,nlat))
  duRdphi[:,:,0]  = (f1[:,:,0] - f1[:,:,1]) / dlat_rad[0]
  duRdphi[:,:,nlat-1]  = (f1[:,:,nlat-2] - f1[:,:,nlat-1]) / dlat_rad[nlat-1]
  for i in range(1,nlat-1):
    duRdphi[:,:,i]  = (f1[:,:,i-1] - f1[:,:,i+1]) / (2.0* dlat_rad[i])

  x2 = uvstarzm[:,:,:] * duRdphi[:,:,:] / a

  #3
  uwstarzm = stats.nanmean(  ustar[:,:,:,:]*wstar[:,:,:,:], axis=3)
  duRdp    = np.zeros((ntime,nlev,nlat))
  duRdp[:,0,:] = (f1[:,0,:] - f1[:,1,:]) / dp[0]
  duRdp[:,nlev-1,:] = (f1[:,nlev-2,:] - f1[:,nlev-1,:]) / dp[nlev-1]
  for k in range(1,nlev-1):
    duRdp[:,k,:] = (f1[:,k-1,:] - f1[:,k+1,:]) / (2.0* dp[k])  

  x3 = uwstarzm[:,:,:] * duRdp[:,:,:]

  #4
  f2        = vzmR[:,:,:]/np.reshape((a*np.cos(np.pi/180.0*lat[:])),(1,1,nlat))
  dvRdlam   = 0 *f2

  x4 = (uvstarzm[:,:,:] * dvRdlam[:,:,:] / 
        np.reshape((a*np.cos(np.pi/180.0*lat[:])),(1,1,nlat)) 
       )

  #5
  vstarsqzm = stats.nanmean(vstar[:,:,:,:]**2, axis=3)
  dvRdphi   = np.zeros((ntime,nlev,nlat))
  dvRdphi[:,:,0]  = (f2[:,:,0] - f2[:,:,1]) / dlat_rad[0]
  dvRdphi[:,:,nlat-1]  = (f2[:,:,nlat-2] - f2[:,:,nlat-1]) / dlat_rad[nlat-1]
  for i in range(1,nlat-1):
    dvRdphi[:,:,i]  = (f2[:,:,i-1] - f2[:,:,i+1]) / (2.0*dlat_rad[i])

  x5 = vstarsqzm[:,:,:] * dvRdphi[:,:,:] / a

  #6
  vwstarzm = stats.nanmean(vstar[:,:,:,:]*wstar[:,:,:,:], axis=3)
  dvRdp    = np.zeros((ntime,nlev,nlat))
  dvRdp[:,0,:] = (f2[:,0,:] - f2[:,1,:]) / dp[0]
  dvRdp[:,nlev-1,:] = (f2[:,nlev-2,:] - f2[:,nlev-1,:]) / dp[nlev-1]
  for k in range(1,nlev-1):
    dvRdp[:,k,:] = (f2[:,k-1,:] - f2[:,k+1,:]) / (2.0*dp[k])

  x6 = vwstarzm[:,:,:] * dvRdp[:,:,:]

  #7
  x7 = (np.reshape(np.tan(np.pi/180.0*lat[:]),(1,1,nlat)) / a * 
        np.nan_to_num(uvstarsqzm[:,:,:] * f2[:,:,:])
       )

  acos = np.reshape(a * np.cos(np.pi/180.0*lat[:]),(1,1,nlat))
  mathck1 = - acos[:,:,:] * ( np.nan_to_num(x1[:,:,:]) + np.nan_to_num(x2[:,:,:]) + np.nan_to_num(x3[:,:,:]) + np.nan_to_num(x4[:,:,:]) + np.nan_to_num(x5[:,:,:]) + np.nan_to_num(x6[:,:,:]) - np.nan_to_num(x7[:,:,:]) )

  ckx1,ckx1sav,hckx1=integrate(mathck1,lat,dlam_rad_int,dlat_rad,dp,ieq,ntime,nlev,nlat,nlon,typ='zm')

  ck = ckx1
  hck = hckx1

  print('ck',np.mean(ck))

#####################################################
#~~~~~~~~~~~~~~~~~~~      CZ      ~~~~~~~~~~~~~~~~~~#
#####################################################



  alphazmR = stats.nanmean(alpha[:,:,:,:], axis=3)

  mathcz1 = -  np.nan_to_num(wzmR[:,:,:]) * np.nan_to_num(alphazmR[:,:,:])

  cz1,cz1sav,hcz1=integrate(mathcz1,lat,dlam_rad_int,dlat_rad,dp,ieq,ntime,nlev,nlat,nlon,typ='zm')

  cz = cz1
  print('cz',np.mean(cz))

#####################################################
#~~~~~~~~~~~~~~~~~~~      CE      ~~~~~~~~~~~~~~~~~~#
#####################################################

  alphastar  = alpha[:,:,:,:] - np.reshape(alphazmR[:,:,:],(ntime,nlev,nlat,1))

  mathce = -  np.nan_to_num( stats.nanmean(alphastar[:,:,:,:]*wstar[:,:,:,:], axis=3) )

  ce,cesav,hce=integrate(mathce,lat,dlam_rad_int,dlat_rad,dp,ieq,ntime,nlev,nlat,nlon,typ='zm')

  print('ce',np.mean(ce))


##start peixoto&oort

#####################################################
#~~~~~~~~~~~~~~~~~~~    gamma     ~~~~~~~~~~~~~~~~~~#
#####################################################
  theta = t[:,:,:,:] * (p0 / np.reshape(p[:],(1,nlev,1,1)))**kappa
  
  halfcosx=np.cos(np.pi/180.0*np.reshape(lat[0:ieq],(1,1,ieq,1)))

  # only NH!!!
  theta_merid=np.sum(theta[:,:,0:ieq,:]*np.reshape(dlat_rad[0:ieq],(1,1,ieq,1))*halfcosx[:],axis=2) #lat
  theta_merid_tm=np.mean(theta_merid[:,:,:],axis=0) #time
  theta_merid_tmzm=np.mean(theta_merid_tm[:,:],axis=1) #lon

  f1 = np.copy(theta_merid_tmzm)
  dthmdp    = np.zeros((nlev))
  dthmdp[0] = (f1[0] - f1[1]) / dp[0]
  dthmdp[nlev-1] = (f1[nlev-2] - f1[nlev-1]) / dp[nlev-1]
  for k in range(1,nlev-1):
    dthmdp[k] = (f1[k-1] - f1[k+1]) / (2.0* dp[k])  

  xx1=theta[:,:,:,:]/t[:,:,:,:]
  xx2=np.reshape(R_spec/(cp*p[:]),(1,nlev,1,1))
  xx3= np.reshape((1.0/dthmdp[:]),(1,nlev,1,1))

  gamma=-xx1*xx2*xx3


#####################################################
#~~~~~~~~~~~~~~~~~~~      AZ      ~~~~~~~~~~~~~~~~~~#
#####################################################
#time, lev,lat,lon

  #time mean each 30 days???
  tmt=np.mean(t[:,:,:,:],axis=0) #time

  tmt=time_mean(t)

  tmtmz=np.mean(tmt[:,:,:,:],axis=3) #lon

  #tmtmz_merid=np.mean(tmtmz[:,0:ieq],axis=1) #lat but onther northern hemisphere

  halfcos=np.cos(np.pi/180.0*np.reshape(lat[0:ieq],(1,ieq)))
  halfcos2=np.cos(np.pi/180.0*np.reshape(lat[ieq:nlat],(1,ieq)))
  fullcos=np.cos(np.pi/180.0*np.reshape(lat[0:nlat],(1,nlat)))


  tmtmz_merid=np.sum(tmtmz[:,:,0:ieq]*np.reshape(dlat_rad[0:ieq]*halfcos[:],(1,1,ieq)),axis=2) #lat
  tmtmz_merid2=np.sum(tmtmz[:,:,ieq:nlat]*np.reshape(dlat_rad[ieq:nlat]*halfcos2[:],(1,1,ieq)),axis=2) #lat
  tmtmz_merid3=np.sum(tmtmz[:,:,0:nlat]*np.reshape(dlat_rad[0:nlat]*fullcos[:],(1,1,nlat)),axis=2) #lat

  tmtmz_merid_abbr=np.zeros((12,nlev,nlat))
  for i in range(ieq):
    tmtmz_merid_abbr[:,:,i]=tmtmz[:,:,i]-tmtmz_merid[:,:]
  for i in range(ieq,nlat):
    tmtmz_merid_abbr[:,:,i]=tmtmz[:,:,i]-tmtmz_merid2[:,:]
#  tmtmz_merid_abbr =tmtmz-np.reshape(tmtmz_merid3,(12,nlev,1)) 

  gamma_n = np.reshape(np.mean(gamma,axis=0),(1,nlev,nlat,nlon))

  mathaz=cp/2*gamma_n*np.reshape(tmtmz_merid_abbr*tmtmz_merid_abbr,(12,nlev,nlat,1))

  #gamma_n = np.reshape(np.mean(gamma,axis=0),(1,nlev,nlat,nlon))

  #print(tmtmz_merid)

  #print(tmtmz_merid2) 

  az,azsav,haz=integrate(mathaz,lat,dlam_rad_int,dlat_rad,dp,ieq,12,nlev,nlat,nlon,typ='lon')

  print('az',az)
  print(haz)

  ##end peixoto&oort

  #this works!!

#####################################################
#~~~~~~~~~~~~~~~~~~~      AE      ~~~~~~~~~~~~~~~~~~#
#####################################################

  # time mean is every month!!

  tmt      = time_mean(t)
  tmt_dept = time_dept(t,tmt)
  tmt_dept2= tmt_dept*tmt_dept
  tmt_dept2_mt = time_mean(tmt_dept2)


  tmtzm      = np.mean(tmt,axis=3)
  tmtzm_dept = tmt - np.reshape(tmtzm,(12,nlev,nlat,1))
  tmtzm_dept2= tmtzm_dept*tmtzm_dept

  gamma_n = np.reshape(np.mean(gamma,axis=0),(1,nlev,nlat,nlon))

  mathae=cp/2*gamma_n*tmt_dept2_mt*tmtzm_dept2
  ae,aesav,hae=integrate(mathae,lat,dlam_rad_int,dlat_rad,dp,ieq,12,nlev,nlat,nlon,typ='lon')
  
  print('ae',ae)
  print(hae)

  #this works!!



#####################################################
#~~~~~~~~~~~~~~~~~~~      CA      ~~~~~~~~~~~~~~~~~~#
#####################################################

  vmt      = time_mean(v)
  vmt_dept = time_dept(v,vmt)
  vdTd   = vmt_dept*tmt_dept
  vdTdmt = time_mean(vdTd)
  xxca1=vdTdmt


  vmtzm      = np.mean(vmt,axis=3)
  vmtzm_dept = vmt - np.reshape(vmtzm,(12,nlev,nlat,1))
  xxca2=vmtzm_dept*tmtzm_dept

  print(xxca1.shape)
  print(xxca2.shape)

  #xxca12=np.zeros((ntime,nlev,nlat,nlon))
  #i22=-1
  #for i in range(ntime):
  #  if np.mod(i,30)==0: i22=i22+1
  #  #print(i,i22)
  #  xxca12[i,:,:,:] = xxca1[i,:,:,:] + xxca2[i22,:,:,:] 


  #sys.exit(1)

  #xxca12 = xxca1 + xxca2


  f1 = np.copy(tmtzm)
  dtmtzm_dphi  = np.zeros((12,nlev,nlat))
  dtmtzm_dphi[:,:,0]  = (f1[:,:,0] - f1[:,:,1]) / dlat_rad[0]
  dtmtzm_dphi[:,:,nlat-1]  = (f1[:,:,nlat-2] - f1[:,:,nlat-1]) / dlat_rad[nlat-1]
  for i in range(1,nlat-1):
    dtmtzm_dphi[:,:,i]  = (f1[:,:,i-1] - f1[:,:,i+1]) / (2.0* dlat_rad[i])

  xxca3 = dtmtzm_dphi / a

  #print(gamma_n.shape)
  #print(xxca1.shape)
  #print(xxca2.shape)
 # print(xxca3.shape)


  #print(xxca12.shape)

  mathca1 = -cp*gamma_n*np.reshape(np.mean(xxca1+xxca2,axis=3),(12,nlev,nlat,1))*np.reshape(xxca3,(12,nlev,nlat,1))

  


  wmt      = time_mean(w)
  wmt_dept = time_dept(w,wmt)
  wdTd   = wmt_dept*tmt_dept
  wdTdmt = time_mean(wdTd)
  xxca4=wdTdmt

  wmtzm      = np.mean(wmt,axis=3)
  wmtzm_dept = wmt - np.reshape(wmtzm,(12,nlev,nlat,1))
  xxca5=wmtzm_dept*tmtzm_dept

#  xxca45=np.zeros((ntime,nlev,nlat,nlon))
#  i22=-1
#  for i in range(ntime):
#    if np.mod(i,30)==0: i22=i22+1
#    #print(i,i22)
#    xxca45[i,:,:,:] = xxca4[i,:,:,:] + xxca5[i22,:,:,:]

  #print(tmtmz_merid_abbr.shape)


  tma_xx=tmtmz_merid_abbr*np.reshape(np.power(p[:],kappa),(1,nlev,1))
  tma_xxx=np.reshape(tma_xx,(12,nlev,nlat,1)) * gamma_n

  f1 = np.copy(tma_xxx)

  #print(f1.shape)

  dtmadp    = np.zeros((12,nlev,nlat,nlon))
  dtmadp[:,0,:,:] = (f1[:,0,:,:] - f1[:,1,:,:]) / dp[0]
  dtmadp[:,nlev-1,:,:] = (f1[:,nlev-2,:,:] - f1[:,nlev-1,:,:]) / dp[nlev-1]
  for k in range(1,nlev-1):
    dtmadp[:,k,:,:] = (f1[:,k-1,:,:] - f1[:,k+1,:,:]) / (2.0* dp[k]) 

  xxca6 = dtmadp

  mathca2 = - cp * np.reshape(np.power(p[:],-kappa),(1,nlev,1,1)) * np.reshape(np.mean(xxca4+xxca5,axis=3),(12,nlev,nlat,1))*xxca6

  ca1,ca1sav,ca1e=integrate(mathca1,lat,dlam_rad_int,dlat_rad,dp,ieq,12,nlev,nlat,nlon,typ='lon')
  ca2,ca2sav,ca2e=integrate(mathca2,lat,dlam_rad_int,dlat_rad,dp,ieq,12,nlev,nlat,nlon,typ='lon')

  print('ca1',ca1)

  print('ca2',ca2)

  ca = ca1+ca2

  print('ca',ca1+ca2)

  out=np.zeros((8,12))
  out[0,:]=az
  out[1,:]=ae
  out[2,:]=time_mean(kz)
  out[3,:]=time_mean(ke)
  out[4,:]=ca
  out[5,:]=time_mean(ce)
  out[6,:]=time_mean(ck)
  out[7,:]=time_mean(cz)

  print('kz')
  print(time_mean(kz))
  if True:
    outx = np.zeros((12))
    for i in range(12):
      outx[i] = np.mean(kz[i*30:(i+1)*30],axis=0)
      print(i,kz[30*i:30*i+30],outx[i])
  print(outx)

  print(ca1e,ca2e,ca1e+ca2e)

  outname=args.output
  if args.path == None:
    outname='test.out'

  np.save(outname, out)

  #with open(outname,'w') as outfile:
  #  outfile.write(time_mean(kz))


  sys.exit(0)







#####################################################
#~~~~~~~~~~~  Reference Atmosphere  ~~~~~~~~~~~~~~~~#
#####################################################

  #calculate potential temperature theta
  theta = t[:,:,:,:] * (p0 / np.reshape(p[:],(1,nlev,1,1)))**kappa 

  thetazmR = stats.nanmean(theta[:,:,:,:], axis=3) 

  #preparing to interpolate into isentropic coordinates:
  theta_min=np.min(theta[:,:,:])
  theta_max=np.nanmax(theta[:,:,:,:])

  dstep=3#(theta_max - theta_min) / nstep
  theta_isentrop = np.arange(theta_min+dstep,theta_max,dstep)

  ntheta=len(theta_isentrop)

  p_isentrop = np.zeros((ntime,ntheta,nlat,nlon))
  for i in range(ntime):
    for j in range(nlat):
      for l in range(nlon):
        #p_temp = barycentric_interpolate(theta[i,:,j,l],p[:],theta_isentrop)
        #p_temp = piecewise_polynomial_interpolate(theta[i,:,j,l],p[:],theta_isentrop)
        p_temp = np.interp(theta_isentrop,theta[i,:,j,l],p[:],left=p[0])
        #print(i,j,l)
        #p_temp = interp_lagrange(theta_isentrop,theta[i,:,j,l],p[:],left=psurf[i,j,l])
        #interp_lagrange(a_int,a,b)
        p_isentrop[i,:,j,l] = p_temp

  p_ref = stats.nanmean(stats.nanmean(p_isentrop[:,:,:,:],axis=3),axis=2)
  for aaa in range(ntheta):
    print(p_ref[1,aaa],theta_isentrop[aaa],p_isentrop[1,aaa,1,1])
#####################################################
#~~~~~~~~~~~~~~~~~~~      AZ      ~~~~~~~~~~~~~~~~~~#
#####################################################


  tzmR = stats.nanmean(t[:,:,:,:],axis=3)

  #thetazmR = stats.nanmean() gibts schon

  #thetaamR = stats.nanmean(stats.nanmean(theta[:,:,:,:], axis=3),axis=2)
  p_ref_intZ = np.zeros((ntime,nlev,nlat))

  #p_ref_surf_zmR =  stats.nanmean(p_ref_surf_out,axis=2)

  for i in range(ntime):
    for k in range(nlev):
      for j in range(nlat):
        p_ref_intZ[i,k,j] = np.interp(thetazmR[i,k,j],theta_isentrop[:],p_ref[i,:],left=np.min(p_ref[:]))
        #p_ref_intZ[i,k,j] = interp(thetazmR[i,k,j],theta_isentrop[:],p_ref[i,:])


        #p_ref_intZ[i,k,j] = np.interp(thetaamR[i,k],theta_isentrop[:],p_ref[i,:],left=np.min(p_ref[:]))
        if i==100: print(i,j,k,p_ref_intZ[i,k,j],p[k],thetazmR[i,k,j])
  #for aab in range(nlev):
  #  print('pref',p_ref_intZ[1,aab,1],p[aab],thetazmR[1,aab,1],theta_isentrop[aab],p_ref[i,aab])
  for aab in range(ntheta):
    print('pref',theta_isentrop[aab],p_ref[100,aab])
  Nz = 1.0 - (p_ref_intZ[:,:,:]/np.reshape(p[:],(1,nlev,1)))**kappa

  mathaz1 = cp * np.nan_to_num(Nz[:,:,:] * tzmR[:,:,:])

  az1,az1sav,haz1=integrate(mathaz1,lat,dlam_rad_int,dlat_rad,dp,ieq,ntime,nlev,nlat,nlon,typ='zm')

  az = az1
  haz = haz1
  

  print('az',np.mean(az))

  sys.exit(1)

#####################################################
#~~~~~~~~~~~~~~~~~~~      AE      ~~~~~~~~~~~~~~~~~~#
#####################################################

  pi = np.zeros((ntime,nlev,nlat,nlon))
  for i in range(ntime):
    for j in range(0,nlat):
      for l in range(nlon):
        pi[i,:,j,l]=np.interp(theta[i,:,j,l],theta_isentrop[:],p_ref[i,:],left=np.max(p_ref[:]))
  #N = np.zeros(ntime,nlev,nlat,nlon)
  #for i in range(ntime):
  #  for j in range(0,nlat):
  #    for l in range(nlon):
  N = 1.0 - (pi[:,:,:,:]/np.reshape(p[:],(1,nlev,1,1)))**kappa

  #print(N)

  mathae1 = cp * np.nan_to_num((N[:,:,:,:] -  np.reshape(Nz[:,:,:],(ntime,nlev,nlat,1))) * t[:,:,:,:])

  ae1,ae1sav,hae1=integrate(mathae1,lat,dlam_rad_int,dlat_rad,dp,ieq,ntime,nlev,nlat,nlon,typ='lon')

  ae = ae1
  hae = hae1

  print('ae',np.mean(ae))


#####################################################
#~~~~~~~~~~~~~~~~~~~      CA      ~~~~~~~~~~~~~~~~~~#
#####################################################


  tzmR = stats.nanmean(t[:,:,:,:], axis=3)
  tstar = t[:,:,:,:] - np.reshape(tzmR,(ntime,nlev,nlat,1))

  FX = t[:,:,:,:]/theta[:,:,:,:]*np.reshape(Nz[:,:,:],(ntime,nlev,nlat,1))

  dFXdlam = np.zeros((ntime,nlev,nlat,nlon))
  dFXdlam[:,:,:,0] = (FX[:,:,:,0]-FX[:,:,:,1])/dlam_rad
  dFXdlam[:,:,:,nlon-1] = (FX[:,:,:,nlon-2]-FX[:,:,:,nlon-1])/dlam_rad
  for l in range(1,nlon-1):
    dFXdlam[:,:,:,l] = (FX[:,:,:,l-1]-FX[:,:,:,l+1])/(2.0*dlam_rad)

  dFXdlam = dFXdlam / np.reshape((a*np.cos(np.pi/180.0*lat[:])),(1,1,nlat,1)) 

  xx1 = np.nan_to_num( np.reshape(stats.nanmean( tstar[:,:,:,:] * ustar[:,:,:,:],axis=3),(ntime,nlev,nlat,1)) * dFXdlam[:,:,:,:])

  dFXdphi = np.zeros((ntime,nlev,nlat,nlon))
  dFXdphi[:,:,0,:] = (FX[:,:,0,:]-FX[:,:,1,:])/dlat_rad[0]
  dFXdphi[:,:,nlat-1,:]=(FX[:,:,nlat-2,:]-FX[:,:,nlat-1,:])/dlat_rad[nlat-1]
  for i in range(1,nlat-1):
    dFXdphi[:,:,i,:] = (FX[:,:,i-1,:]-FX[:,:,i+1,:])/(2.0*dlat_rad[i])

  dFXdphi = dFXdphi / a

  xx2 =  np.nan_to_num( np.reshape(stats.nanmean( tstar[:,:,:,:] * vstar[:,:,:,:],axis=3),(ntime,nlev,nlat,1)) * dFXdphi[:,:,:,:])

  dFXdp = np.zeros((ntime,nlev,nlat,nlon))
  dFXdp[:,0,:,:] = (FX[:,0,:,:]-FX[:,1,:,:])/dp[0]
  dFXdp[:,nlev-1,:,:] = (FX[:,nlev-2,:,:]-FX[:,nlev-1,:,:])/dp[nlev-1]
  for k in range(1,nlev-1):
    dFXdp[:,k,:,:] = (FX[:,k-1,:,:]-FX[:,k+1,:,:])/(2.0*dp[k])

  xx3 =  np.nan_to_num( np.reshape(stats.nanmean(tstar[:,:,:,:] * wstar[:,:,:,:],axis=3),(ntime,nlev,nlat,1)) * dFXdp[:,:,:,:])

  mathca = - (np.nan_to_num(cp * theta[:,:,:,:] / t[:,:,:,:]) * ( xx1[:,:,:,:] + xx2[:,:,:,:] + xx3[:,:,:,:] ))

  ca,casav,hca=integrate(mathca,lat,dlam_rad_int,dlat_rad,dp,ieq,ntime,nlev,nlat,nlon,typ='lon')

  print('ca',np.mean(ca))


