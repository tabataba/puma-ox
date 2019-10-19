#!/usr/bin/python

#import matplotlib
#matplotlib.use('Agg')

import numpy as np
#from scipy.io import netcdf
import math
#import matplotlib.pyplot as plt
import sys
import os
#from matplotlib import cm
#from mpl_toolkits.axes_grid1 import AxesGrid
#from mpl_toolkits.axes_grid1 import make_axes_locatable
#from matplotlib.colors import LogNorm
#from matplotlib.ticker import MultipleLocator

from argparse import ArgumentParser
parser = ArgumentParser()


parser.add_argument("-p","--path",action="store",type=str)
parser.add_argument("-f","--folder",action="store",type=str)

parser.add_argument("-o","--output",action="store",type=str)


args, unknown = parser.parse_known_args()

if args.path == None and args.folder == None: 
  path = 'data/lorenz_en/rev53_r1.0_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu0/'
else:
  path = str(args.path)+'/'+str(args.folder)

prev = np.zeros((3))
tot = np.zeros((3))
CFLAG = np.ones((3))

from os import listdir
onlyfiles=os.listdir(path)
onlyfiles = sorted(onlyfiles)#.sort()

#sys.exit(1)
#for YEAR in range(1,11):

  #if YEAR < 10: 
  #  YEARSTR = '00'+str(YEAR)
  #else:
  #  YEARSTR = '0'+str(YEAR)
iii=-1
for filen in onlyfiles:

  iii=iii+1
  #filen='PUMAG.'+YEARSTR+'.npy'
  try:
    dat=np.load(path+'/'+filen)
  except:
    break
  if iii>0:  prev = np.copy(tot)

  #energy
  tot[0]= np.mean(dat[0,:]+dat[1,:]+dat[2,:]+dat[3,:])

  #kinetic
  tot[1]=np.mean(dat[2,:]+dat[3,:])
  #potential
  tot[2]=np.mean(dat[0,:]+dat[1,:])
  print filen
  print 'en                 ', 'kin                 ', 'pot        '
  print tot

  for i in range(3):
    if prev[i] < tot[i]:
      print prev[i],tot[i]
    else:
      CFLAG[i] = 0
    if abs(prev[i]-tot[i])> tot[i]/100:
      CFLAG[i] = 0.01
    if abs(prev[i]-tot[i])> tot[i]/50:
      CFLAG[i] = 0.02
    if abs(prev[i]-tot[i])> tot[i]/33:
      CFLAG[i] = 0.03
    if abs(prev[i]-tot[i])> tot[i]/20:
      CFLAG[i] = 0.05
    if abs(prev[i]-tot[i])> tot[i]/10:
      CFLAG[i] = 0.10
    if abs(prev[i]-tot[i])> tot[i]/5:
      CFLAG[i] = 0.20
    if abs(prev[i]-tot[i])> tot[i]/2:
      CFLAG[i] = 0.50
  print CFLAG


  #print prev

if np.sum(CFLAG) == 0: 
  print 'CONVERVERGED'
  with open("conv.txt", "a") as myfile:
    myfile.write(str(args.folder)+'\n')
else:
  print 'NOT CONVERGED'
  with open("unconv_details.txt", "a") as myfile:
    myfile.write(str(args.folder)+'  '+ onlyfiles[iii][6:9]  + '\n tot1: '+str(prev[0])+' tot2: '+str(tot[0])+' FLAG: '+str(CFLAG[0])+ '\n kin1: '+str(prev[1])+' kin2: '+str(tot[1])+' FLAG: '+str(CFLAG[1])+ '\n pot1: '+str(prev[2])+' pot2: '+str(tot[2])+' FLAG: '+str(CFLAG[2]) +'\n')
  with open("unconv.txt", "a") as myfile:
    myfile.write(str(args.folder)+'\n')

if np.sum(CFLAG) == 0.01: 
  with open("unconv0.01.txt", "a") as myfile:
    myfile.write(str(args.folder)+'\n')

if np.sum(CFLAG) > 0.01 and np.sum(CFLAG) <= 0.05: 
  with open("unconv0.05.txt", "a") as myfile:
    myfile.write(str(args.folder)+'\n')

if np.sum(CFLAG) > 0.05 and np.sum(CFLAG) <= 0.10: 
  with open("unconv0.10.txt", "a") as myfile:
    myfile.write(str(args.folder)+'\n')

if np.sum(CFLAG) > 0.10 and np.sum(CFLAG) <= 0.20: 
  with open("unconv0.20.txt", "a") as myfile:
    myfile.write(str(args.folder)+'\n')

if np.sum(CFLAG) > 0.20 and np.sum(CFLAG) <= 1.00: 
  with open("unconv0.20.txt", "a") as myfile:
    myfile.write(str(args.folder)+'\n')

if np.sum(CFLAG) > 0.20 and np.sum(CFLAG) <= 1.00: 
  with open("unconv1.00.txt", "a") as myfile:
    myfile.write(str(args.folder)+'\n')

if np.sum(CFLAG) > 1.00 and np.sum(CFLAG) <= 3.00: 
  with open("unconv3.00.txt", "a") as myfile:
    myfile.write(str(args.folder)+'\n')
