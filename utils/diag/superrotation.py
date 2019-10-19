#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')

import numpy as np
from scipy.io import netcdf
import math
import matplotlib.pyplot as plt
import sys
import os
import subprocess as sub
import re

YEAR='010'
indir= '/network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/'+'/pumagt_arcb_parameters/'##'/noseasons_pumagt_arcb/'
outdir='plots/'
outdirpng='pics/'


      #path = ''
      ##onlyfiles=os.listdir(path)
      #onlyfiles = sorted(onlyfiles)
YEAR=sys.argv[2]


filename='PUMAG.'+YEAR+'.nc'

def find_folders(dirpath):
  folders = [ f for f in os.listdir(dirpath) \
              if os.path.isdir(os.path.join(dirpath,f)) ]
  modelruns = []
  for f in folders:
    matchstr=re.match(f[0:4],folders[len(folders)/2][0:4])
    if not matchstr == None:
      modelruns.append(f)
      modelname=matchstr.group()
  rotspds = [ float(re.sub("[^0-9.]", " ", x)) for x in modelruns ]

  return modelruns,rotspds



class nc:

  def __init__(self,path,ncfile,inputfile='',namelistfile=''):
    self.fullpath = path + '/' + ncfile
    self.inputpath = path + '/' + inputfile
    self.dirname = path
    self.ncfile  = ncfile
    self.inputfile = inputfile
    if namelistfile == '':
      self.namelistfile = 'standard2.nl'
    else:
      self.namelistfile = namelistfile
    self.namelistpath = self.dirname + '/' + self.namelistfile

  def path_exists(self):
    if os.path.exists(self.dirname):
      return 1
    else:
      return 0

  def file_exists(self, fullpath):
    try:
      with open(fullpath, 'r') as f: pass
      return 1
    except:
      return 0

  def create(self, fullpath, text=''):
    self.path_exists()
    file = open(self.fullpath, 'w')
    if text != '':
      if not isinstance(text, str): text=str(text)
      file.write(text)
    file.close

  def make_nl(self,options=''):
    if not self.file_exists(self.namelistpath):
      file = open(self.namelistpath, 'w')
      if options != '':
        if not isinstance(options, str): options=str(options)
        file.write(options)
      file.close

  def make(self):
    if self.path_exists():
      if not self.file_exists(self.fullpath):
        if self.file_exists(self.inputpath) and not (self.inputfile) == '':
          pwd = os.getcwd()
          self.make_nl(options="""code=ta,ua,va,vtype=p,htype=g,mean=0,netcdf=1
hpa=1000,900,800,700,600,500,400,300,200,100""")
          os.chdir(self.dirname)
          callstr='burn7.x '+self.inputfile+' '+self.ncfile+' <'+self.namelistfile
          sub.call(callstr,shell=True)
          os.chdir(pwd)
        else:
          print('The inputfile file "' + self.inputfile + '" at '\
                + self.dirname +' does not exist.') 
          sys.exit(1)
      else:
        print('The netcdf file ' + self.fullpath + ' already exists.')
    else:
      print('The directory ' + self.path + ' does not exist.')
      sys.exit(1)


class data:

  def __init__(self,ncfilepath,inputfile=''):  
    self.fullpath = ncfilepath
    self.ncfile   = os.path.basename(self.fullpath)
    self.dirname  = os.path.dirname(self.fullpath)
    self.inputfile = inputfile
    if inputfile == '': self.inputfile = 'MOST.010'


  def readncfile(self):
    self.nc=nc(path=self.dirname,ncfile=self.ncfile,    \
               inputfile=self.inputfile,namelistfile='')
    self.nc.make()
    self.f=netcdf.netcdf_file(nc.fullpath,'r')

#  def which_plots(self):
#    if re.match(self.plot)

  def get_data(self,data=''):
    self.readncfile()
    self.time = self.f.variables['time']
    self.lev = self.f.variables['lev']
    self.lat = self.f.variables['lat']
    self.lon = self.f.variables['lon']
    self.t = self.f.variables['ta']
    self.u = self.f.variables['ua']
    self.v = self.f.variables['va']

    self.ntime = time.shape[0]
    self.nlev = lev.shape[0]
    self.nlat = lat.shape[0]
    self.nlon = lon.shape[0]

class atmoplot:

  def __init__(self,data):
    self.d=data

  def mean(inp,time=False,lev=False,lat=False,lon=False):
    if time == False and lev == False and lat == False and lon == False: 
      time == True
    if lon == True:
      np.mean(inp, axis=3)
    if lat == True:
      np.mean(inp, axis=2)
    if lev == True:
      np.mean(inp, axis=1)
    if time == True:
      np.mean(inp, axis=0)
    return inp

  def mmstrm(self):
    vm=mean(self.v,time=True,lon=True)
    vml=np.zeros((self.nlev,self.nlat))
    for i in range(1,self.nlev-1):
      for j in range(self.nlat):
        vml[i,j] = np.sum(vm[i:self.nlev,j])*10000.0

    strm = np.zeros((self.nlev,self.nlat))
    for i in range(self.nlev):
      for j in range(self.nlat):
	strm[i,j] = 2*np.pi*a*math.cos(self.lat[j]*np.pi/180.0)*vml[i,j]/g

  #local super rotation
  def super_loc(self,rotfac=1.0):
    day = 24.0 * 60.0 * 60.0 # 1 day in seconds
    rotationrate = rotfac *  2.0 * np.pi / day
    radius = 6400000.0
    g = 9.8

    umlon = mean(self.u,lon=True)
    m0[:] = rotationrate * radius**2 * (np.cos(self.lat[:]/180*np.pi))**2 

    for i in range(0,self.ntime):
      for j in range(0,self.nlev):
        mmlon[i,j,:] = m0[:] + umlon[i,j,:] * radius * np.cos(self.lat[:]/180*np.pi)

    sloc = np.zeros((self.ntime,self.nlev,self.nlat))
    sloc[:,:,:] = (mmlon[:,:,:] / (rotationrate * radius**2)) - 1.0
    sloc[sloc<=0] = 0



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

  if typ=='lat':
    out = np.zeros(ntime)
    outsav = np.zeros((ntime,nlev,nlat))
    hout = np.zeros((2,ntime))
    for k in range(nlev):
      for j in range(0,nlat):
        for l in range(nlon):
          dm = np.cos(np.pi/180.0*lat[j]) * np.sin(dlat_rad[j]/2.0) * dlam_rad_int * dp[k]# *a**2
          out = out + math[j] * dm
          outsav[:,k,j] = math[j]#/g* dm /(4*np.pi*g)#factor????
      #Northern Hemisphere
      for jx in range(0,ieq):
        for l in range(nlon):
          dm = np.cos(np.pi/180.0*lat[jx]) * np.sin(dlat_rad[jx]/2.0) * dlam_rad_int  * dp[k]# *a**2
          hout[0,:] = hout[0,:] + math[jx] * dm
      #Southern Hemisphere
      for jy in range(ieq,nlat):
        for l in range(nlon):
          dm = np.cos(np.pi/180.0*lat[jy]) * np.sin(dlat_rad[jy]/2.0) * dlam_rad_int * dp[k]# *a**2
          hout[1,:] = hout[1,:] + math[jy] * dm

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


rotspds=[1.0]
ii=0

#g = 9.81


#path='/home/octoraid/gfd/tabataba/10y_per_file/variable_rotation_rate_noSeasons/puma_rot_1'
#ncfile='puma_out.nc'
#inputfile='MOST.010'
#path='/home/octoraid/gfd/tabataba/variable_rotation_rate_noSeasons_T42_NTSPD144/puma_rot_0.125'
ncfile='puma_outxx.nc'
inputfile='MOST.010'

#path='/home/octoraid/gfd/tabataba/variable_rotation_rate_noSeasons_T42_NTSPD240'

#path='/home/octoraid/gfd/tabataba/10y_per_file/variable_rotation_rate_noSeasons'
path='/home/octoraid/gfd/tabataba/variable_rotation_rate_noSeasons_T42_NTSPD144'
#path='/home/octoraid/gfd/tabataba/variable_rotation_rate_noSeasons_T42'

#folders,rotspds = find_folders(path)
#print folders
#print rotspds

outname=''
if len(sys.argv) == 1:
  #ncfile = os.environ['HDD']+'/runs/PUMA_test/pumagt_dialy/pumag010.nc'
  #ncfile = os.environ['HDD']+'/runs/PUMA_test/pumag/pumag010.nc'
  #ncfile = os.environ['HDD']+'/runs/puma_lat64_ntspd240_lev20_rot1_nS/puma010.nc'
  ncfile = '/network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT'+'/pumagt_arcb_parameters/rev53_r0.5_res64_radius1.00_taufr10.0_psurf1.0_pref1.0_taus10.00_tausurf36_nmu1/PUMAG.010.nc'
  afac=1
  pfac=1
  outname='test'
  rotfac=0.5
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

  #path = ncfile
  #onlyfiles=os.listdir(path)
  #onlyfiles = sorted(onlyfiles)
  #sys.exit(1)


  #f=netcdf.netcdf_file(ncf.fullpath,'r')
  f = netcdf.netcdf_file(ncfile,'r',mmap=False)
  #print f.variables
  time = f.variables['time']
  lev = f.variables['lev']
  lat = f.variables['lat']
  lon = f.variables['lon']
  t = f.variables['ta']
  u = f.variables['ua']
  v = f.variables['va']

  p=lev[:]*100 #*pfac
  lev = lev[:]#*pfac

  ntime = time.shape[0]
  nlev = lev.shape[0]
  nlat = lat.shape[0]
  nlon = lon.shape[0]

  dp = np.zeros((nlev))
  dp[0] = (p[0] - p[1])/2.0
  dp[nlev-1] = p[nlev-2] - p[nlev-1]
  for k in range(1,nlev-1):
    dp[k] = (p[k-1] + p[k])/2.0 - (p[k] + p[k+1])/2.0

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

  ieq = nlat/2

  print(time.shape)
  print(lev.shape)
  print(lat.shape)
  print(lon.shape)
  print(t.shape)
  print(u.shape)
  print(v.shape)


  #rotfac = 0.0625#1.0#rotspds[ii]
  day = 24.0 * 60.0 * 60.0 # 1 day in seconds
  rotationrate = rotfac *  2.0 * np.pi / day

  radius = 6400000.0
  #radius = 6371000.0
  g = 9.8
  p0= 100000*pfac


  umlon = np.mean(u[:,:,:,:], axis=3)

  umlonmt = np.mean(umlon[:,:,:], axis=0)

  deg=int(np.ceil(nlat/18.0))

  ustrateqmax = np.max(umlonmt[7:nlev,ieq-deg:ieq+deg])
  ustrateqmin = np.min(umlonmt[7:nlev,ieq-deg:ieq+deg])

  usemean = np.mean(umlonmt[7:nlev,ieq-deg:ieq+deg])
  usmean  = np.mean(umlonmt[7:nlev,:])

  umean   = np.mean(umlonmt[:,:])
  uemean  = np.mean(umlonmt[:,ieq-deg:ieq+deg])

  print lev[7:nlev]

  print ustrateqmax

  #axial angular momentum per unit mass
  m = np.zeros((ntime,nlev,nlat,nlon))
  #axial angular momentum per unit mass for atmosphere at rest
  m0 = np.zeros((nlat))
  #zonally averaged axial angular momentum per unit mass
  mmlon = np.zeros((ntime,nlev,nlat))

  m0[:] = rotationrate * radius**2 * (np.cos(lat[:]/180.0*np.pi))**2 

  M00,M00sav,hM00=integrate(m0[:],lat,dlam_rad_int,dlat_rad,dp,ieq,ntime,nlev,nlat,nlon,typ='lat')
  M00 = M00/(p0/g)




#  for i in range(0,ntime):
#    for j in range(0,nlev):
#      #for k in range(0,nlat):
#        for l in range(0,nlon):
#          m[i,j,:,l] = m0[:] + u[i,j,:,l] * radius * np.cos(lat[:]/180.0*np.pi)

  for i in range(0,ntime):
    for j in range(0,nlev):
      mmlon[i,j,:] = m0[:] + umlon[i,j,:] * radius * np.cos(lat[:]/180.0*np.pi)
      #mmlon[i,j,:] = umlon[i,j,:] * radius * np.cos(lat[:]/180.0*np.pi)

  M1,M1sav,hM1=integrate(mmlon[:,:,:],lat,dlam_rad_int,dlat_rad,dp,ieq,ntime,nlev,nlat,nlon,typ='zm')  
  M1 = M1/(p0/g)

  #Global super-rotation
  sglob = np.zeros(ntime)

  sglob = M1/M00-1.0


  sglobmean=np.mean(sglob)
  print 'sglob',sglobmean

  #local super rotation
  sloc = np.zeros((ntime,nlev,nlat))

  #sloc[:,:,:] = (mmlon[:,:,:] / (rotationrate * radius**2)) - 1.0
  sloc[:,:,:] = (mmlon[:,:,:] - (rotationrate * radius**2)) / (rotationrate * radius**2)
  #sloc[sloc<=0] = 0

  slocmt=np.mean(sloc,axis=0)

  slsteqmean = np.mean(slocmt[7:nlev,ieq-deg:ieq+deg])
  sleqmean  = np.mean(slocmt[:,ieq-deg:ieq+deg])
  

  #M0 = m0[:] * radius**2 * np.cos(lat[:]/180.0*np.pi) * Deltalat * Deltalon * Deltaz

  
  #for jj in range(nlev):
  
  for ilev in range(nlev):
  #if False:
    #print ilev
    fig = plt.figure()
    ax = plt.gca()
    ax.text(-110, 400, ncfile, fontsize=6.5, horizontalalignment='left',verticalalignment='top')
    #try:
    if True:
      cs = plt.contour(lat[:],time[:],sloc[:,ilev,:],5,colors='k')
      #cs = plt.contourf(lat[:],time[:],sloc[:,9,:],10)
      plt.clabel(cs, fontsize=9, inline=1)
      plt.xlabel(r'Lattitude ($^\circ$)')
      plt.ylabel('Time (days)')
      plt.title('Local super-rotation at %s hPa'%lev[ilev]+'/ Global value: S='+str(round(sglobmean,3)))
      #str='super_loc_rot%s_np_NTSPD144.eps'%(rotspds[ii])
      #plt.savefig(outdir+'1sup_lev'+str(ilev)+'_'+outname+'.pdf',format='pdf')
      plt.savefig(outdirpng+'1sup_'+outname+'_lev'+str(ilev)+'.png',format='png')
    #except:
    #  print ilev,'ERROR'
    #  continue
    



outname2='data/'+'suprot_new6.dat'


#facs=[rotfac,resfac,radfac,tfrfac,psfac,prfac,tsfac,tsufac,nmufac]
#zz=[0.5, 64.0, 1.0, 10.0, 1.0, 1.0, 10.0, 36.0, 1.0]
try:
  with open(outname2) as x:
    outfile=open(outname2,'a')
    outfile.write('%8.5f  %8.1f  %8.4f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8d  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f\n' % (facs[0], facs[1], facs[2], facs[3], facs[4], facs[5], facs[6], facs[7], facs[8], sglobmean, ustrateqmax, ustrateqmin, umean, uemean, usmean,usemean,slsteqmean,sleqmean) )
except:
  with open(outname2,'w') as outfile:
    outfile.write('%8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s\n' % ('rot','res','rad','tauf','ps','pref','tausw','tausurf','nmu','sglob','ustreq','usemin','umean','uemean','usmean','usemean','sloc_seq','sloc_eq'))
    outfile.write('%8.5f  %8.1f  %8.4f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8d  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f\n' % (facs[0], facs[1], facs[2], facs[3], facs[4], facs[5], facs[6], facs[7], facs[8], sglobmean, ustrateqmax, ustrateqmin, umean, uemean, usmean,usemean,slsteqmean,sleqmean) )
  #S = m(rot,rad,lat,u)*rad**2*math.cos(lat/180*np.pi)*
