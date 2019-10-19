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

from argparse import ArgumentParser
parser = ArgumentParser()


OFLAG=0
parser.add_argument("-p","--path",action="store",type=str)
parser.add_argument("-f","--folder",action="store",type=str)
parser.add_argument("-y","--year",action="store",type=str)

parser.add_argument("-o","--output",action="store",type=str)

args, unknown = parser.parse_known_args()

if args.path == None and args.folder == None: 
  path = 'data/lorenz_en/rev53_r1.0_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu0/'
  OFLAG=1
  nx1=['0.0625','0.125','0.25','0.5','1.0','2.0','4.0']
  tausurf=360
  nmu=1
  nx2=[float(i) for i in nx1]
  lnx=len(nx1)
else:
  path = str(args.path)+'/'+str(args.folder)

from os import listdir
#.sort()

labels1=[r'$A_Z$',r'$K_Z$',r'$A_E$',r'$K_E$']
labels2=[r'$C_A$',r'$C_E$',r'$C_K$',r'$C_Z$']

if args.output == None: args.output = 'plots_lorenz/'

years=3

if OFLAG==1:

  alorenz = np.zeros((years,lnx,8,12))
  mlorenz = np.zeros((years,lnx,12))
  for i,omega in enumerate(nx1):
    #for j,taus in enumerate(ny1):
      print omega
      res='64'
      if omega=='4.0': res='128'
      #path = 'data/lorenz_en/rot_r'+omega+'_res'+res+'_tausurf'+taus+'_nmu'+nmu+'.010.nc_output.npy'
      path = 'data/lorenz_en/rev53_r'+omega+'_res'+res+'_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu'+str(nmu)
      onlyfiles=os.listdir(path)
      onlyfiles = sorted(onlyfiles)
      for y in range(years):
        yy=y-(years)
        print y,yy
        try:
          infile=path+'/'+onlyfiles[yy]
          print onlyfiles[yy]
          lorenz=np.load(infile)
          print lorenz
          print infile,' found'
        except:
          lorenz=np.zeros((8,12))
        for ii in range(8):
          alorenz[y,i,ii,:]=lorenz[ii,:]
          mlorenz[y,i,ii] = np.mean(lorenz[ii,:],axis=0)
                               #np.mean(lorenz[0,:],axis=0)#az
      #alorenz[i,1]=lorenz[0,:]#np.mean(lorenz[1,:],axis=0)#ae
      #alorenz[i,2]=lorenz[0,:]#np.mean(lorenz[2,:],axis=0)#kz
      #alorenz[i,3]=lorenz[0,:]#np.mean(lorenz[3,:],axis=0)#ke
      #alorenz[i,4]=lorenz[0,:]#np.mean(lorenz[4,:],axis=0)#ca
      #alorenz[i,5]=lorenz[0,:]#np.mean(lorenz[5,:],axis=0)#ce
      #alorenz[i,6]=lorenz[0,:]#np.mean(lorenz[6,:],axis=0)#ck
      #alorenz[i,7]=lorenz[0,:]#np.mean(lorenz[7,:],axis=0)#cz

  print alorenz



#ADD TIME LINE STUFF


#nx1=['0.1','1.0','10.0']
tausurf=360
nmu=1
nx2=[float(i) for i in nx1]
lnx=len(nx1)
#omega='1.0'
sol = '0.00'
press = '1.0'
fr='1.0'
years=3


if OFLAG==1:
  iter=0
  jj=0
  alorenz = np.zeros((years,8,12))
  mlorenz = np.zeros((years,12))
  alorenz2 = np.zeros((years*12,8))
  for i,omega in enumerate(['0.0625','0.125','0.25','0.5','1.0']): #,'2.0'
    for tausurf in ['3.6','36','360']:
      for nmu in [0, 1]:
        for fr in ['1.0']: #['0.1','1.0','10.0']:
          for press in ['0.04']:#,'0.2','1.0','5.0']:
            for sol in ['0.20']: #['0.00','2.00','10.00']:
              iter=iter+1
              print omega,tausurf,nmu,fr,press,sol
              res='64'
              if omega=='4.0': res='128'
              #path = 'data/lorenz_en/rev53_r'+omega+'_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu'+str(1)
              name = 'rev53_r'+omega+'_res'+res+'_radius1.00_taufr'+fr+'_psurf'+press+'_pref'+press+'_taus'+sol+'_tausurf'+tausurf+'_nmu'+str(nmu)



              facs=[omega,res,'1.00',fr,press,press,sol,tausurf,nmu]
              facs=[float(i) for i in facs]

              path = 'data/lorenz_en/'+name
              try:
                onlyfiles=os.listdir(path)
              except:
                continue
              onlyfiles = sorted(onlyfiles)
              for y in range(years):
                yy=y-(years)
                print iter,omega,tausurf,nmu,fr,press,sol
                print y,yy
                try:
                  infile=path+'/'+onlyfiles[yy]
                  print onlyfiles[yy]
                  lorenz=np.load(infile)
                  #print lorenz
                  print infile,' found'
                except:
                  lorenz=np.zeros((8,12))
                jj=jj+1
                for ii in range(8):
                  alorenz[y,ii,:]=lorenz[ii,:]
                  #print y,lorenz[ii,:]
                  mlorenz[y,ii] = np.mean(lorenz[ii,:],axis=0) 
                  for m in range(12): 
                    alorenz2[m+y*12,ii]=lorenz[ii,m]
              meanlorenz = np.mean(alorenz2[:,:],axis=0)
              print len(alorenz2[:,0])
              variance = ( alorenz2[:,:] - np.reshape(meanlorenz[:],(1,8)) )**2.0 / len(alorenz2[:,0])
              variance2 = np.mean(variance,axis=0)
              standard_deviation = variance2**0.5
              #print variance2
              print standard_deviation

              outname2='data/'+'lorenz.dat'              

              try:
                with open(outname2) as x:
                  outfile=open(outname2,'a')
                  outfile.write('%8.5f  %8.1f  %8.4f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8d  %12.2f  %12.2f  %12.2f  %12.2f  %8.3f  %8.3f  %8.3f  %8.3f  %12.2f  %12.2f  %12.2f  %12.2f  %8.3f  %8.3f  %8.3f  %8.3f\n' % (facs[0], facs[1], facs[2], facs[3], facs[4], facs[5], facs[6], facs[7], facs[8], meanlorenz[0], meanlorenz[1], meanlorenz[2], meanlorenz[3], meanlorenz[4], meanlorenz[5], meanlorenz[6], meanlorenz[7], standard_deviation[0], standard_deviation[1], standard_deviation[2], standard_deviation[3], standard_deviation[4], standard_deviation[5], standard_deviation[6], standard_deviation[7]) )
              except:
                with open(outname2,'w') as outfile:
                  outfile.write('%8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %8s  %12s  %12s  %12s  %12s  %8s  %8s  %8s  %8s  %12s  %12s  %12s  %12s  %8s  %8s  %8s  %8s\n' % ('rot','res','rad','tauf','ps','pref','tausw','tausurf','nmu','AZ','KZ','AE','KE','CA','CE','CK','CZ','sd AZ','sd KZ','sd AE','sd KE','sd CA','sd CE','sd CK','sd CZ'))
                  outfile.write('%8.5f  %8.1f  %8.4f  %8.3f  %8.3f  %8.3f  %8.3f  %8.3f  %8d  %12.2f  %12.2f  %12.2f  %12.2f  %8.3f  %8.3f  %8.3f  %8.3f  %12.2f  %12.2f  %12.2f  %12.2f  %8.3f  %8.3f  %8.3f  %8.3f\n' % (facs[0], facs[1], facs[2], facs[3], facs[4], facs[5], facs[6], facs[7], facs[8], meanlorenz[0], meanlorenz[1], meanlorenz[2], meanlorenz[3], meanlorenz[4], meanlorenz[5], meanlorenz[6], meanlorenz[7], standard_deviation[0], standard_deviation[1], standard_deviation[2], standard_deviation[3], standard_deviation[4], standard_deviation[5], standard_deviation[6], standard_deviation[7]) )




sys.exit(1)










