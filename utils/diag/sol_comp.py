#!/usr/bin/python

import matplotlib
#matplotlib.use('Agg')

import numpy as np
import numpy.ma as ma
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

from mpl_toolkits.mplot3d import Axes3D


x=7
#x=7
aa=['r','g','b','k','y']
bb=['--','-']

a=0

#s=5
#end=3

#s=1
#end=4

s=1
end=6

line=np.arange(0,4.5,0.1)

for ii,sol in enumerate([0.25, 0.5, 1.0, 2.0, 4.0]):
#for ii in [0, 1]:
#if True:
  #i=0.25
  infile0='data/stats_sol_ex1/ustats_ex1_nmu0_sol'+str(sol)+'_dt30.txt'
  infile1='data/stats_sol_ex1/ustats_ex1_nmu1_sol'+str(sol)+'_dt30.txt'
  data0 = np.genfromtxt(infile0,skip_header=1)
  data1 = np.genfromtxt(infile1,skip_header=1)
  step = data0[:,0]
  acc0=(data0[a+s:a+end+s,x]-data0[a:a+end,x])/30
  acc1=(data1[a+s:a+end+s,x]-data1[a:a+end,x])/30
  #plt.plot(step[0:end],data0[0:end,x],'--',color=aa[ii])
  #plt.plot(step[0:end],data1[0:end,x],'-',color=aa[ii])
  #plt.plot(step[0:end],acc0[0:end],'--',color=aa[ii])
  #plt.plot(step[0:end],acc1[0:end],'-',color=aa[ii])
  #plt.plot(step,data0[:,x]-data1[:,x])
  plt.plot(sol,np.mean(acc0[0:end]),color='g',marker='o')
  plt.plot(sol,np.mean(acc0[0:end])-np.mean(acc1[0:end]),color='r',marker='s')
  plt.plot(line,0.023*line**2)
  plt.xlabel(r'$S [S_0]$')
  plt.ylabel(r'$\dot{U} [$ms$^{-1}$day$^{-1}]$')
  #plt.xlog

  print sol**2, np.mean(acc0[0:end]), np.mean(acc1[0:end]), np.mean(acc0[0:end])-np.mean(acc1[0:end])

plt.savefig('solcomp_s'+str(s)+'_end'+str(end)+'.png', dpi=200)
plt.show()
