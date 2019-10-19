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

infile='data/suprot_noseasons2.dat'

data = np.genfromtxt(infile,skip_header=1)

Ro_E=0.02
Ek_E=0.08
At_E=400
#alpha_E=

Mfac=0.007

Edat=[40,5,7,8,1.86,1.97,-0.5,0.12]
Mdat=[10,0.7,0.13,0.47,0.05/Mfac,0.11/Mfac,0.03/Mfac,0.05/Mfac]



# Ro, Ek, At, G, alpha
Earth= [0.02, 0.08, 400, 0.1, 0.04]
Mars = [0.1 , 0.04,  12, 0.3, 20]
Venus= [300 , 6   , 190, 0.2, 0]
Titan= [ 10 , 0.4 , 5000, 2.8, 10]

tausw=data[:,6]
tausurf=data[:,7]

G=data[:,6]/2.0

omega=(2*np.pi)/360
alpha=1.0/omega/(data[:,7])

Ro=Ro_E/(data[:,0]**2)*(1+0.19*2.05*(data[:,7]==36)+0.45*2.05*(data[:,7]==3.6))#add tausurf
Ek=Ek_E/data[:,0]/data[:,3]*(1+0.28*1.6*(G==1)+0.68*1.6*(G==5))#add tausw
At=At_E*data[:,0]*data[:,4]*(1+0.28*1.6*(G==1)+0.68*1.6*(G==5))#add tausw
ps=data[:,4]
tauf=data[:,3]
rot=data[:,0]
#print alpha

nmu=data[:,8]

mu1=(rot<=0.5)&(nmu==1)
mu0=(rot<=0.5)&(nmu==0)
umean=data[:,12]
uemean=data[:,13]
usmean=data[:,14]
usemean=data[:,15]
usemax=data[:,10]

label=['usemax ','umean  ','uemean ','usmean ','usemean']

x1=np.empty([1000,5])
x11=np.empty([1000,5])
y1=np.empty([1000,5])

inp=0

colors=['y','r','b','g','c']
shapes=['^','o','^','p','d']
sizes=[20,15,10,6,4,2]

for i1,irot in enumerate([0.0625,0.125]):
  for i2,itauf in enumerate([1.0]):#, 1.0, 10.0]):
    for i3,ips in enumerate([0.01,0.1,1.0,10.0,100.0]):#,1.0, 5.0]): #[0.2, 1.0, 5.0]:
      for i4,itausw in enumerate([2,10]):#([0,0.2,2,10]): #[2 ,10]:
        for i5,itausurf in enumerate([360]):
          mask=(rot==irot)&(tauf==itauf)&(ips==ps)&(tausw==itausw)&(tausurf==itausurf)
          mask0=mu0*mask
          mask1=mu1*mask
          vph = 460*irot #phase velocity
          #print irot,itauf,ips,itausw,mu1*mask
          #print irot,itauf,ips,itausw,mu0*mask
          print irot,itauf,ips,itausw,itausurf
          ii=0
          if data[mask0,10] > -500:
            for i in [10,12,13,14,15]:
              print i,label[ii],
              print data[mask0,10],data[mask1,i],vph-data[mask1,i],
              print vph+data[mask1,i],vph
              print data[mask0,10]/(vph-data[mask1,i])
              print data[mask0,10]/(vph+data[mask1,i])
              print data[mask0,10]/(-vph-data[mask1,i])
              print data[mask0,10]/(-vph+data[mask1,i])
              print
              ii=ii+1
            print
            imax=15
            i10=12
            y1[inp,i1]=data[mask0,imax]
            #x1[inp,i1]=data[mask0,i10]/(vph-data[mask1,i])
            #x11[inp,i1]=abs(vph-data[mask1,i10])
            yy=data[mask0,imax]#-data[mask1,imax]
            xx=data[mask1,i10]#data[mask1,i10]#vph-data[mask1,i10]
            plt.plot(xx,yy,marker=shapes[i4],color=colors[i3],markersize=sizes[i1])
            #plt.plot(data[mask0,10],data[mask0,10]/(vph-data[mask1,10]),marker=shapes[i2],color=colors[i3],markersize=15)
            x11[inp,i1]=vph-data[mask1,i10]
                            
            inp=inp+1
            #mx = ma.masked_array(data, mask=mask)
            #print mx
        
#plt.plot(x11[:,0],y1[:,0],'*')
#plt.plot(x11[:,1],y1[:,1],'o')

plt.plot(0,0,color='c',marker='s', label=r'$p_s=100.0$ bar',linestyle="None")
plt.plot(0,0,color='g',marker='s', label=r'$p_s=10.0$ bar',linestyle="None")
plt.plot(0,0,color='b',marker='s', label=r'$p_s=1.0$ bar',linestyle="None")
plt.plot(0,0,color='r',marker='s', label=r'$p_s=0.1$ bar',linestyle="None")
#plt.plot(0,0,color='y',marker='s', label=r'$p_s=0.01$ bar',linestyle="None")

#plt.plot(0,0,color='k',marker='o', label=r'$G=0$ days',linestyle="None")

#plt.plot(0,0,color='k',marker='*', label=r'$G=0.1$ days',linestyle="None")
plt.plot(0,0,color='k',marker='^', label=r'$\mathcal{G}=0$',linestyle="None")
plt.plot(0,0,color='k',marker='o', label=r'$\mathcal{G}=-0.7$',linestyle="None")

#plt.plot(0,0,color='k',marker='o', label=r'$\tau_f=0.1$ days',linestyle="None")
#plt.plot(0,0,color='k',marker='*', label=r'$\tau_f=1$ days',linestyle="None")
#plt.plot(0,0,color='k',marker='^', label=r'$\tau_f=10$ days',linestyle="None")
import matplotlib
matplotlib.rcParams['legend.handlelength'] = 0
matplotlib.rcParams['legend.numpoints'] = 1

plt.legend(loc='upper right')
x2=np.arange(80)
print x2
#plt.xlim([-10,80])
#plt.ylim([0,200])
plt.plot(x2[:],3.14*x2[:])
#plt.plot(x2[:],3.45*x2[:])
#plt.plot(x2[:],2.83*x2[:])
#plt.plot(x2[:],2.14*x2[:])
#plt.plot(x11[:,0],3.14*x11[:,0]-10,'.')
#plt.plot(x11[:,0],3.14*x11[:,0]+10,'.')
plt.ylabel(r'$U$')
plt.xlabel(r'$U_{mean}$')
plt.savefig('nsupcomp_noseasons_imax'+str(imax)+'_imean'+str(i10)+'.png', dpi=200)
#plt.show()
