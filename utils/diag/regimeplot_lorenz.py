#!/usr/bin/python

import matplotlib
#matplotlib.use('Agg')

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

from mpl_toolkits.mplot3d import Axes3D

infile='data/lorenz.dat' #suprot.dat'
outdir='plots/regime/'
outdirpng='plots/regime/'


#print infile

data = np.genfromtxt(infile,skip_header=1)

#print data

#print data[1,:]
#print data[:,0]

Ro_E=0.02
Ek_E=0.08
At_E=400
#alpha_E=









G=data[:,6]/2.0

omega=(2*np.pi)/360
alpha=1.0/omega/(data[:,7])

Ro=Ro_E/(data[:,0]**2)*(1+0.19*2.05*(data[:,7]==36)+0.45*2.05*(data[:,7]==3.6))#add tausurf
Ek=Ek_E/data[:,0]/data[:,3]*(1+0.28*1.6*(G==1)+0.68*1.6*(G==5))#add tausw
At=At_E*data[:,0]*data[:,4]
ps=data[:,4]
rot=data[:,0]
print alpha

nmu=data[:,8]
#     rot       res       rad      tauf        ps      pref     tausw   tausurf       nmu     sglob    ustreq    usemin

#a = 6400000.0*afac#/20.0
g = 9.8
kappa = 0.286
M_air = 28.98
k = 1.38E-23
R=8.3144621
#p0=100000*pfac

title='Global superrotation index'
title='Upper atmosphere equatorial wind'
titles=['Global superrotation index','Upper atmosphere equatorial wind']
shorts=['S','u']
labs=['S','u (m/s)']
#for ipl in [0,1]:
#  for imu in [0,1]:
#    for pfac in [0.2,1,5]:
#      fig = plt.figure(figsize=(7,6))
#      cmap = plt.cm.get_cmap('CMRmap')
#
#      cmaplist = [cmap(i) for i in range(cmap.N)]
#      #cmaplist[0] = (.5,.5,.5,1.0)
#      cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
#      if ipl==1: bounds = np.linspace(0,170,10)
#      if ipl==0: bounds = [-0.25,0,0.5,1,1.5,2,2.5,3]#np.linspace(0,3,13)
#      norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)
#
#      mask=(nmu==imu)&(ps==pfac)
#      amask0=(mask)&(rot==1.0)&(data[:,7]==3.6)&(data[:,3]==1.0)&(G==0.0)
#      amask1=(mask)&(rot==1.0)&(data[:,7]==360)&(data[:,3]==1.0)&(G==0.0)
#      amask2=(mask)&(rot==1.0)&(data[:,7]==3.6)&(data[:,3]==1.0)&(G==5.0)
#      asx=Ro[amask0][0]*(0.85)
#      asy=Ek[amask0][0]*(0.85)
#      aqx=(Ro[amask1][0]- Ro[amask0][0])*(2.0)
#      aqy=(Ek[amask2][0]- Ek[amask0][0])*(2.0)
#
#      #print (mask)&(rot==0.0625)&(data[:,7]==360)&(data[:,3]==1.0)&(G==0.0)
#      #print Ro[(mask)&(rot==0.0625)&(data[:,7]==3.6)&(data[:,3]==1.0)&(G==0.0)]#&(G==0)
#      print ipl,imu,pfac
#      print Ro[amask0],Ro[amask1][0],Ro[amask2]
#      print Ek[amask0],Ek[amask1],Ek[amask2]
#
#      ax = fig.add_subplot(111)#, projection='3d')
#      sp = ax.scatter(Ro[mask],Ek[mask],c=data[mask,ipl+9],cmap=cmap,norm=norm,s=60)
#      ax.annotate("", xy=(asx+aqx,asy), xytext=(asx, asy),arrowprops=dict(arrowstyle="->"))
#      ax.annotate("", xy=(asx,asy+aqy), xytext=(asx, asy),arrowprops=dict(arrowstyle="->"))
#      ax.annotate(r"$\alpha$", xy=(asx+aqx,asy), xytext=(asx+aqx, asy))
#      ax.annotate(r"$\mathcal{G}$", xy=(asx,asy+aqy), xytext=(asx, asy+aqy))
#      plt.colorbar(sp)
#      ax.set_xlabel('Ro')
#      ax.set_ylabel('Ek')
#      #ax.set_zlabel('At')
#      plt.yscale('log')
#      plt.xscale('log')
#      ax.set_label(labs[ipl])
#      ax.set_title(titles[ipl])
#      #ax.xaxis.set_scale('log')
#      #ax.yaxis.set_scale('log')
#      plt.tight_layout()
#      #plt.show()
#      plt.savefig(outdirpng+'1regRoEk'+shorts[ipl]+'_ps'+str(pfac)+'_nmu_'+str(imu)+'.png',format='png')

title='Global superrotation index'
title='Upper atmosphere equatorial wind'
t1 = ['', 'standard deviation ']
t2 = ['','sd']
titles=[r'AZ',r'KZ',r'AE',r'KE',r'CA',r'CE',r'CK',r'CZ',]
tt = ['a) ','b) ','c) ','d) ']
#shorts=['S','u']
#labs=['S','u (m/s)']

for isd,tit1 in enumerate(t1):
  for ilor,title in enumerate(titles):
    for imu in [1]:
      for pfac in [1]:

        lab=tit1 + title
        if ilor>3: lab=tt[ilor-4]+tit1 + title

        fig = plt.figure(figsize=(7,6))
        cmap = plt.cm.get_cmap('CMRmap')
        if ilor>3 and isd==0: cmap = plt.cm.get_cmap('bwr')
        cmaplist = [cmap(i) for i in range(cmap.N)]
        #cmaplist[0] = (.5,.5,.5,1.0)
        cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
        #if ilor==1: bounds = np.linspace(0,max(data[mask,ilor+9]),10)
        #if ipl==0: bounds = [-0.25,0,0.5,1,1.5,2,2.5,3]#np.linspace(0,3,13)


        mask=(nmu==imu)&(ps==pfac)
        amask0=(mask)&(rot==1.0)&(data[:,7]==360)&(data[:,3]==1.0)&(G==0.0)
        amask1=(mask)&(rot==1.0)&(data[:,7]==3.6)&(data[:,3]==1.0)&(G==0.0)
        amask2=(mask)&(rot==1.0)&(data[:,7]==360)&(data[:,3]==1.0)&(G==5.0)
        asx=Ro[amask0][0]*(0.82)
        asy=Ek[amask0][0]*(0.80)
        aqx=(Ro[amask1][0]- Ro[amask0][0])*(2.0)
        aqy=(Ek[amask2][0]- Ek[amask0][0])*(2.0)

        if ilor<4 and isd==1:
          div=np.mean((data[mask,ilor+9]))
        else:
          div=1

        bounds = np.linspace(0,max(np.abs(data[mask,ilor+9+8*isd])/div),10)
        if ilor>3 and isd==1:  bounds = np.linspace(0,0.25,11)
        if ilor>3 and isd==0:  bounds = np.linspace(-1,1,21)
        norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

        #print (mask)&(rot==0.0625)&(data[:,7]==360)&(data[:,3]==1.0)&(G==0.0)
        #print Ro[(mask)&(rot==0.0625)&(data[:,7]==3.6)&(data[:,3]==1.0)&(G==0.0)]#&(G==0)
        print ilor,imu,pfac
        print Ro[amask0],Ro[amask1][0],Ro[amask2]
        print Ek[amask0],Ek[amask1],Ek[amask2]

        ax = fig.add_subplot(111)#, projection='3d')
        sp = ax.scatter(Ro[mask],Ek[mask],c=data[mask,ilor+9+8*isd]/div,cmap=cmap,norm=norm,s=60*2.0)
        ax.annotate("", xy=(asx+aqx,asy), xytext=(asx, asy),arrowprops=dict(arrowstyle="->"))
        ax.annotate("", xy=(asx,asy+aqy), xytext=(asx, asy),arrowprops=dict(arrowstyle="->"))
        ax.annotate(r"$\alpha$", xy=(asx+aqx,asy), xytext=(asx+aqx, asy))
        ax.annotate(r"$\mathcal{G}$", xy=(asx,asy+aqy), xytext=(asx, asy+aqy))
        plt.colorbar(sp)
        ax.set_xlabel('Ro')
        ax.set_ylabel('Ek')
        #ax.set_zlabel('At')
        plt.yscale('log')
        plt.xscale('log')
        ax.set_xlim([1E-3,2E1])
        ax.set_label(lab)
        ax.set_title(lab)
        #ax.xaxis.set_scale('log')
        #ax.yaxis.set_scale('log')
        plt.tight_layout()
        #plt.show()
        plt.savefig(outdirpng+'1lor_'+title+t2[isd]+'_RoEk_ps'+str(pfac)+'_nmu_'+str(imu)+'.png',format='png',dpi=200)
  
