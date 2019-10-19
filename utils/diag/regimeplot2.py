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

infile='data/suprot_new2.dat'
outdir='plots/regsup/'
outdirpng='pics/regsup/'


#print infile

data = np.genfromtxt(infile,skip_header=1)

#print data

#print data[1,:]
#print data[:,0]

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







G=data[:,6]/2.0

omega=(2*np.pi)/360
alpha=1.0/omega/(data[:,7])

#Ro=Ro_E/(data[:,0]**2)*(1+0.2*(data[:,7]==36)+0.45*(data[:,7]==360))#add tausurf
#Ek=Ek_E/data[:,0]/data[:,3]*(1+0.3*(G==1)+0.7*(G==5))#add tausw
#At=At_E*data[:,0]*data[:,4]
#ps=data[:,4]
#rot=data[:,0]
#print alpha

Ro=Ro_E/(data[:,0]**2)*(1+0.19*2.05*(data[:,7]==36)+0.45*2.05*(data[:,7]==3.6))#add tausurf
Ek=Ek_E/data[:,0]/data[:,3]*(1+0.28*1.6*(G==1)+0.68*1.6*(G==5))#add tausw
At=At_E*data[:,0]*data[:,4]*(1+0.28*1.6*(G==1)+0.68*1.6*(G==5))#add tausw
ps=data[:,4]
tauf=data[:,3]
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
pfac=1
#p0=100000*pfac

title='Global superrotation index'
title='Upper atmosphere equatorial wind'
titles=['Global superrotation index','Upper atmosphere equatorial wind','equatorial superrotation index',r'$S_{up,eq}$']
shorts=['S','u','Seq','Su,eq']
labs=[r'$S$','u (m/s)',r'$S_{eq}$',r'$S_{u,eq}$']

for ipl in [0,1,2,3]:
  for imu in [0,1]:
    for taufac in [0.1,1,10]:
    #for pfac in [0.2,1,5]:
      fig = plt.figure(figsize=(7,6))
      cmap = plt.cm.get_cmap('CMRmap')
      cmapg = plt.cm.get_cmap('Greys')

      cmaplist = [cmap(i) for i in range(cmap.N)]
      #cmaplist[0] = (.5,.5,.5,1.0)
      cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)
      if ipl==1: bounds = np.linspace(-20,180,11)
      if ipl==0 or ipl==2 or ipl==3: bounds = [-0.25,0,0.5,1,1.5,2,2.5,3]#np.linspace(0,3,13)
      norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

      #mask=(nmu==imu)&(ps==pfac)
      #amask0=(mask)&(rot==1.0)&(data[:,7]==3.6)&(data[:,3]==1.0)&(G==0.0)
      #amask1=(mask)&(rot==1.0)&(data[:,7]==360)&(data[:,3]==1.0)&(G==0.0)
      #amask2=(mask)&(rot==1.0)&(data[:,7]==3.6)&(data[:,3]==1.0)&(G==5.0)
      #asx=Ro[amask0][0]*(0.85)
      #asy=Ek[amask0][0]*(0.85)
      #aqx=(Ro[amask1][0]- Ro[amask0][0])*(2.0)
      #aqy=(Ek[amask2][0]- Ek[amask0][0])*(2.0)

      mask=(nmu==imu)&(tauf==taufac)
      amask0=(mask)&(rot==1.0)&(data[:,7]==360)&(data[:,4]==1.0)&(G==0.0)
      amask1=(mask)&(rot==1.0)&(data[:,7]==3.6)&(data[:,4]==1.0)&(G==0.0)
      amask2=(mask)&(rot==1.0)&(data[:,7]==360)&(data[:,4]==1.0)&(G==5.0)
      asx=Ro[amask0][0]*(0.82)
      #asy=Ek[amask0][0]*(0.80)
      asy=At[amask0][0]*(0.80)
      aqx=(Ro[amask1][0]- Ro[amask0][0])*(2.0)
      #aqy=(Ek[amask2][0]- Ek[amask0][0])*(2.0)
      aqy=(At[amask2][0]- At[amask0][0])*(2.0)




      #print (mask)&(rot==0.0625)&(data[:,7]==360)&(data[:,3]==1.0)&(G==0.0)
      #print Ro[(mask)&(rot==0.0625)&(data[:,7]==3.6)&(data[:,3]==1.0)&(G==0.0)]#&(G==0)
      print ipl,imu,pfac,taufac
      print Ro[amask0],Ro[amask1][0],Ro[amask2]
      print Ek[amask0],Ek[amask1],Ek[amask2]

      ax = fig.add_subplot(111)#, projection='3d')

      #sp = ax.scatter(Ro[mask],Ek[mask],c=data[mask,ipl+9],cmap=cmap,norm=norm,s=60)
      #ax.annotate("", xy=(asx+aqx,asy), xytext=(asx, asy),arrowprops=dict(arrowstyle="->"))
      #ax.annotate("", xy=(asx,asy+aqy), xytext=(asx, asy),arrowprops=dict(arrowstyle="->"))
      #ax.annotate(r"$\alpha$", xy=(asx+aqx,asy), xytext=(asx+aqx, asy))
      #ax.annotate(r"$\mathcal{G}$", xy=(asx,asy+aqy), xytext=(asx, asy+aqy))
 
      ipx=ipl
      if ipl == 2: ipx=16-9
      if ipl == 3: ipx=15-9
      sp = ax.scatter(Ro[mask],At[mask],c=data[mask,9+ipx],cmap=cmap,norm=norm,s=60*2.0)
      ax.annotate("", xy=(asx+aqx,asy), xytext=(asx, asy),arrowprops=dict(arrowstyle="->"))
      ax.annotate("", xy=(asx,asy+aqy), xytext=(asx, asy),arrowprops=dict(arrowstyle="->"))
      ax.annotate(r"$\alpha$", xy=(asx+aqx,asy), xytext=(asx+aqx, asy))
      ax.annotate(r"$\mathcal{G}$", xy=(asx,asy+aqy), xytext=(asx, asy+aqy))

      """
      if True:
        pos=0.03

        Esx=Earth[0]
        Esy=Earth[2]
        Exx=Earth[4]
        Eyy=Earth[3]

        spE= ax.scatter(Earth[0]*(1+2*Exx/16),Earth[2]*(1+2*Eyy/5),c=Edat[ilor],norm=norm,cmap=cmap)
        ax.annotate(r"Earth", xy=(Earth[0],Earth[2]), xytext=(Earth[0],Earth[2]*pos),arrowprops=dict(arrowstyle="->"))
        ax.annotate("", xy=(Esx+2.2*Esx,Esy), xytext=(Esx, Esy),arrowprops=dict(color='green',arrowstyle="->"))
        ax.annotate("", xy=(Esx,Esy+3*Esy), xytext=(Esx, Esy),arrowprops=dict(color='green',arrowstyle="->"))

        Esx=Mars[0]
        Esy=Mars[2]
        Exx=Mars[4]
        Eyy=Mars[3]
        spE= ax.scatter(Esx*(1+2*Exx/16),Esy*(1+2*Eyy/5),c=Mdat[ilor],norm=norm,cmap=cmap)
        ax.annotate(r"Mars", xy=(Mars[0],Mars[2]), xytext=(Mars[0],Mars[2]*pos*10),arrowprops=dict(arrowstyle="->"))
        ax.annotate("", xy=(Esx+2.2*Esx,Esy), xytext=(Esx, Esy),arrowprops=dict(color='green',arrowstyle="->"))
        ax.annotate("", xy=(Esx,Esy+3*Esy), xytext=(Esx, Esy),arrowprops=dict(color='green',arrowstyle="->"))

        Esx=Venus[0]
        Esy=Venus[2]
        Exx=Venus[4]
        Eyy=Venus[3]
        spE= ax.scatter(Esx*(1+2*Exx/16),Esy*(1+2*Eyy/5),c=-0.5,norm=normg,cmap=cmapg)
        ax.annotate(r"Venus", xy=(Venus[0],Venus[2]), xytext=(Venus[0]/10,Venus[2]*pos*10),arrowprops=dict(arrowstyle="->"))
        ax.annotate("", xy=(Esx+2.2*Esx,Esy), xytext=(Esx, Esy),arrowprops=dict(color='green',arrowstyle="->"))
        ax.annotate("", xy=(Esx,Esy+3*Esy), xytext=(Esx, Esy),arrowprops=dict(color='green',arrowstyle="->"))

        Esx=Titan[0]
        Esy=Titan[2]
        Exx=Titan[4]
        Eyy=Titan[3]
        spE= ax.scatter(Esx*(1+2*Exx/16),Esy*(1+2*Eyy/5),c=-0.5,norm=normg,cmap=cmapg)
        ax.annotate(r"Titan", xy=(Titan[0],Titan[2]), xytext=(Titan[0],Titan[2]*pos*10),arrowprops=dict(arrowstyle="->"))
        ax.annotate("", xy=(Esx+2.2*Esx,Esy), xytext=(Esx, Esy),arrowprops=dict(color='green',arrowstyle="->"))
        ax.annotate("", xy=(Esx,Esy+3*Esy), xytext=(Esx, Esy),arrowprops=dict(color='green',arrowstyle="->"))
##*(1+0.19*2.05*Earth[4]/10),Earth[2]*(1+0.28*1.6*Earth[3]),c=1,cmap=cmapg)

      """

      plt.colorbar(sp)
      ax.set_xlabel('Ro')
      ax.set_ylabel('Ek')
      ax.set_ylabel('At')
      #ax.set_zlabel('At')
      plt.yscale('log')
      plt.xscale('log')
      ax.set_ylim([1,1E5])
      #ax.set_xlim([1E-3,2E1])
      ax.set_xlim([1E-2,2E2])
      ax.set_label(labs[ipl])
      ax.set_title(titles[ipl])
      #ax.xaxis.set_scale('log')
      #ax.yaxis.set_scale('log')
      plt.tight_layout()
      #plt.show()
      plt.savefig(outdir+'1nregRoAt'+shorts[ipl]+'_ps'+str(pfac)+'_tauf'+str(taufac)+'_nmu_'+str(imu)+'.png',format='png')


mu1=(rot<=0.125)&(nmu==1)
mu0=(rot<=0.125)&(nmu==0)
umean=data[:,12]
usmean=data[:,13]
usemean=data[:,14]
usemax=data[:,10]

