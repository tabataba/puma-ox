#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')

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

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument("-t","--testcase",action="store",type=int)
parser.add_argument("-y","--yaxis",action="store",type=int)
parser.add_argument("-n","--noseasons",action="store",type=int)

args, unknown = parser.parse_known_args()

if args.testcase ==None:
  print "enter test case number"
  sys.exit(1)
else:
  itest=args.testcase

if args.yaxis ==None:
  print "enter y axis number"
  sys.exit(1)
else:
  iy=args.yaxis

if args.noseasons ==None:
  print "enter 1 if no seasons and 0 if seasons"
  sys.exit(1)
elif args.noseasons == 1:
  ins=1
  nsstr="_nose"
elif args.noseasons == 0:
  ins=0
  nsstr=""

#infile='data/suprot_noseasons2.dat'

if ins==0:
  infile='data/suprot_new5.dat'
elif ins==1:
  infile='data/suprot_nose.dat'

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

At2=At_E*data[:,4]*data[:,0]
At3=At_E*data[:,4]*(data[:,0]*data[:,0])
At4=At_E*data[:,4]/data[:,0]
At5=At_E*data[:,4]/(data[:,0]*data[:,0])
Ro2=Ro_E/(data[:,0]**2)
G2=(2.0-data[:,6])/(2.0+data[:,6])
#print alpha

nmu=data[:,8]

mu1=(nmu==1)#(rot<=0.5)&(nmu==1)
mu0=(nmu==0)#(rot<=0.5)&(nmu==0)
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

colors=['c','r','b','g','k']
shapes=['*','d','o','^','p','d']
sizes=[20,15,10,6,4,2]

#         0     1     2     3     4      5     6       7         8     9       10        11     12      13       14         15       16         17
labelsn=['rot','res','rad','tauf','ps','pref','tausw','tausurf','nmu','sglob','ustreq','usemin','umean','uemean','usmean','usemean','sloc_seq',r'$sloc_eq$']
labels=['rot','res','rad','tauf','ps','pref','tausw','tausurf','nmu',r'$S$','ustreq','usemin','umean',r'$u_{eq}$','usmean','usemean','sloc_seq',r'$s_{eq}$']

if ins==1:
  pslist=[0.1,1.0,10.0,100]
  colors=['r','b','g','y']
  tauswlist=[0,0.2,2,10]
  tauflist=[1.0]
elif ins==0:
  pslist=[0.04,0.2,1.0,5.0,30.0]
  tauswlist=[0,0.1,2,10]
  tauflist=[0.1,1.0,10.0]
ilabel=6
for i2,itauf in enumerate(tauflist):
  plt.figure(i2)
  for i1,irot in enumerate([0.0625,0.125,0.25,0.5,1.0,2.0]):
  #for i2,itauf in enumerate([0.1]):#([1.0,0.1,10.0]):#, 1.0, 10.0]):
    for i3,ips in enumerate(pslist):#([0.01,0.1,1.0,10.0,100.0]):#,1.0, 5.0]): #[0.2, 1.0, 5.0]:
      for i4,itausw in enumerate(tauswlist):#([0,0.2,2,10]): #[2 ,10]:
        for i5,itausurf in enumerate([3.6,36,360]):
          mask=(rot==irot)&(tauf==itauf)&(ips==ps)&(tausw==itausw)&(tausurf==itausurf)
          mask0=mu0*mask
          mask1=mu1*mask
          #print mask0
          #print mask1
          vph = 460*irot #phase velocity
          #print irot,itauf,ips,itausw,mu1*mask
          #print irot,itauf,ips,itausw,mu0*mask
          #print irot,itauf,ips,itausw,itausurf
          ii=0
          if data[mask0,10] > -500 and data[mask1,10] > -500:
            #for i in [10,12,13,14,15]:
            #  print i,label[ii],
            #  print data[mask0,10],data[mask1,i],vph-data[mask1,i],
            #  print vph+data[mask1,i],vph
            #  print data[mask0,10]/(vph-data[mask1,i])
            #  print data[mask0,10]/(vph+data[mask1,i])
            #  print data[mask0,10]/(-vph-data[mask1,i])
            #  print data[mask0,10]/(-vph+data[mask1,i])
            #  print
            #  ii=ii+1
            #print
            #print data[mask0,0:7], 
            imax=15
            i10=12
            y1[inp,i1]=data[mask0,imax]
            #x1[inp,i1]=data[mask0,i10]/(vph-data[mask1,i])
            #x11[inp,i1]=abs(vph-data[mask1,i10])
            yy=data[mask0,imax]#-data[mask1,imax]
            xx=data[mask1,i10]#data[mask1,i10]#vph-data[mask1,i10]
            #aa=np.power(data[mask0,imax],2)-np.power(data[mask1,imax],2) #speed up form data
            aa=data[mask0,iy]-data[mask1,iy]
            xx2=data[mask0,ilabel]
            xx3=data[mask0,0]*alpha[mask0]*np.exp((2.0-data[mask0,6])/(2.0+data[mask0,6]))*data[mask0,5]*data[mask0,3]
            xx3=np.exp(-(2.0-data[mask0,6])/(2.0+data[mask0,6]))#*np.exp((2.0-data[mask0,6])/(2.0+data[mask0,6]))/data[mask0,5]*data[mask0,3]
            xx3=1/data[mask0,0]
            xx3=data[mask0,6]
            #if itest == 1:
            #xx3=1/(data[mask0,0])*np.exp(-(2.0-data[mask0,6])/(2.0+data[mask0,6]))*1/data[mask0,4]#*1/data[mask0,3]#*1/alpha[mask0]#np.exp(data[mask0,6]/2)#*1/data[mask0,0]#*data[mask0,6]#At2[mask0]
            #xx3=np.exp(-(2.0-data[mask0,6])/(2.0+data[mask0,6]))*1/data[mask0,4]
            if itest == 2:
              xx3=1/(data[mask0,0])*np.exp(-(2.0-data[mask0,6])/(2.0+data[mask0,6]))*1/data[mask0,4]
              sss=r'$e^{-\mathcal{G}}/\Omega^*p_s$'#labels[ilabel]
              ss1='_test2'
            if itest == 1:
              xx3=1/(data[mask0,0])*np.exp(-(2.0-data[mask0,6])/(2.0+data[mask0,6]))
              sss=r'$e^{-\mathcal{G}}/\Omega^*$'#labels[ilabel]
              ss1='_test1'        
            if itest == 3:
              xx3=Ro2[mask0]*np.exp(-(2.0-data[mask0,6])/(2.0+data[mask0,6]))
              sss=r'$e^{-\mathcal{G}}\mathcal{R}o$'#labels[ilabel]
              ss1='_test3'
            if itest == 4:
              xx3=Ro2[mask0]*np.exp(-(2.0-data[mask0,6])/(2.0+data[mask0,6]))*1/data[mask0,4]
              sss=r'$e^{-\mathcal{G}}\mathcal{R}o/p_s$'#labels[ilabel]
              ss1='_test4'
            if itest == 5:
              xx3=Ro2[mask0]*np.exp(-(2.0-data[mask0,6])/(2.0+data[mask0,6]))/At2[mask0]
              sss=r'$e^{-\mathcal{G}}\mathcal{R}o/\mathcal{A}$'#labels[ilabel]
              ss1='_test5'
            if itest == 6:
              xx3=Ro2[mask0]*np.exp(-(2.0-data[mask0,6])/(2.0+data[mask0,6]))*At2[mask0]
              sss=r'$e^{-\mathcal{G}}\mathcal{R}o\mathcal{A}$'#labels[ilabel]
              ss1='_test6'
            if itest == 7:
              xx3=1/(data[mask0,0])*(-G2[mask0])*np.exp(-G2[mask0])*1/data[mask0,4]
              sss=r'$-\mathcal{G}e^{-\mathcal{G}}/\Omega^*p_s$'#labels[ilabel]
              ss1='_test7'
            if itest == 8:
              xx3=1/(data[mask0,0])*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/data[mask0,4]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}/\Omega^*p_s$'#labels[ilabel]
              ss1='_test8'
            if itest == 9:
              xx3=Ro2[mask0]*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/data[mask0,4]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}\mathcal{Ro}/p_s$'#labels[ilabel]
              ss1='_test9'
            if itest == 10:
              xx3=Ro2[mask0]*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/At2[mask0]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}\mathcal{R}o/\mathcal{A}$'#labels[ilabel]
              ss1='_test10'
            if itest == 11:
              xx3=Ro2[mask0]*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*At2[mask0]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}\mathcal{R}o\mathcal{A}$'#labels[ilabel]
              ss1='_test11'
            if itest == 12:
              xx3=Ro2[mask0]*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/At3[mask0]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}\mathcal{R}o/\mathcal{A}3$'#labels[ilabel]
              ss1='_test12'
            if itest == 13:
              xx3=Ro2[mask0]*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*At3[mask0]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}\mathcal{R}o\mathcal{A}3$'#labels[ilabel]
              ss1='_test13'
            if itest == 14:
              xx3=Ro2[mask0]*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/At4[mask0]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}\mathcal{R}o/\mathcal{A}4$'#labels[ilabel]
              ss1='_test14'
            if itest == 15:
              xx3=Ro2[mask0]*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*At4[mask0]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}\mathcal{R}o\mathcal{A}4$'#labels[ilabel]
              ss1='_test15'
            if itest == 16:
              xx3=Ro2[mask0]*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/At5[mask0]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}\mathcal{R}o/\mathcal{A}5$'#labels[ilabel]
              ss1='_test16'
            if itest == 17:
              xx3=Ro2[mask0]*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*At5[mask0]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}\mathcal{R}o\mathcal{A}5$'#labels[ilabel]
              ss1='_test17'
            if itest == 18:
              xx3=Ro2[mask0]*(-G2[mask0]+1.001)*np.exp(-G2[mask0]+1)*1/At4[mask0]
              sss=r'$(-\mathcal{G}+1.001)e^{-\mathcal{G}+1}\mathcal{R}o/\mathcal{A}4$'#labels[ilabel]
              ss1='_test18'
            if itest == 19:
              xx3=Ro2[mask0]*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/At4[mask0]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}\mathcal{R}o/\mathcal{A}4$'#labels[ilabel]
              ss1='_test19'
              #plt.xscale('log') #xx3=data[mask0,6]
            if itest == 20:
              xx3=(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/At2[mask0]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}/\mathcal{A}2$'#labels[ilabel]
              sss=r'$P$'
              ss1='_test20'
            if itest == 21:
              xx3=(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/At2[mask0]*1/data[mask0,7]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}/\mathcal{A}2/\tau_{surf}$'#labels[ilabel]
              ss1='_test21'            #print data[mask0,0:7],aa
            if itest == 22:
              xx3=(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/At2[mask0]*data[mask0,7]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}/\mathcal{A}2*\tau_{surf}$'#labels[ilabel]
              ss1='_test22'
            if itest == 23:
              xx3=(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/At2[mask0]*1/data[mask0,7]/data[mask0,0]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}/\mathcal{A}2\mathcal{S}$'#labels[ilabel]
              ss1='_test23'
            if itest == 24:
              xx3=(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/At2[mask0]*1/np.power(data[mask0,7]/data[mask0,0],0.5)
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}/\mathcal{A}2\sqrt{\mathcal{S}}$'#labels[ilabel]
              ss1='_test24'
            if itest == 25:
              xx3=(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/At2[mask0]+(G2[mask0])*np.exp(G2[mask0]) /data[mask0,7]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}/\mathcal{A}2+ Ge^G/\tau_{surf}$'#labels[ilabel]
              ss1='_test25'
            if itest == 26:
              xx3=1/(data[mask0,0])*(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/data[mask0,4]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}/\Omega^*p_s$'#labels[ilabel]
              ss1='_test26'
            if itest == 27:
              xx3=(-G2[mask0]+1)*np.exp(-G2[mask0]+1)*1/data[mask0,4]
              sss=r'$(-\mathcal{G}+1)e^{-\mathcal{G}+1}/p_s$'#labels[ilabel]
              ss1='_test27'
            if itest == 28:
              xx3=1/(data[mask0,0])*np.exp(-G2[mask0]+1)*1/data[mask0,4]
              sss=r'$e^{-\mathcal{G}+1}/\Omega^*p_s$'#labels[ilabel]
              ss1='_test28'
            if itest == 29:
              xx3=np.exp(-G2[mask0]+1)*1/data[mask0,4]
              sss=r'$e^{-\mathcal{G}+1}/p_s$'#labels[ilabel]
              ss1='_test29'
            if itest == 30:
              xx3=1/(data[mask0,0])*np.exp(data[mask0,6])*1/data[mask0,4]
              sss=r'$e^{\chi_{sw}}/\Omega^*p_s$'#labels[ilabel]
              ss1='_test30' #xx3=np.power(xx3,2)
            if itest == 31:
              xx3=np.exp(data[mask0,6])*1/data[mask0,4]
              sss=r'$e^{\chi_{sw}}/p_s$'#labels[ilabel]
              ss1='_test31' #xx3=np.power(xx3,2)
              #aa=np.power(aa,2)
            #alpha=1.0/omega/(data[:,7])
            print irot,itauf,ips,itausw,itausurf,aa,xx3
            plt.plot(xx3,np.abs(aa),marker=shapes[i4],color=colors[i3],markersize=sizes[i1])
            #plt.plot(data[mask0,10],data[mask0,10]/(vph-data[mask1,10]),marker=shapes[i2],color=colors[i3],markersize=15)
            x11[inp,i1]=vph-data[mask1,i10]
                            
            inp=inp+1
            #mx = ma.masked_array(data, mask=mask)
            #print mx
        
  #plt.plot(x11[:,0],y1[:,0],'*')
  #plt.plot(x11[:,1],y1[:,1],'o')
  plt.xscale('log')
  plt.yscale('log')

  #plt.plot(0,0,color='c',marker='s', label=r'$p_s=100.0$ bar',linestyle="None")
  if ins==1:
    plt.plot(0,0,color='y',marker='s', label=r'$p_s=100$ bar',linestyle="None")
    plt.plot(0,0,color='g',marker='s', label=r'$p_s=10.0$ bar',linestyle="None")
    plt.plot(0,0,color='b',marker='s', label=r'$p_s=1.0$ bar',linestyle="None")
    plt.plot(0,0,color='r',marker='s', label=r'$p_s=0.1$ bar',linestyle="None")
    #plt.plot(0,0,color='c',marker='s', label=r'$p_s=0.01$ bar',linestyle="None")
  else:
    plt.plot(0,0,color='k',marker='s', label=r'$p_s=30.0$ bar',linestyle="None")
    plt.plot(0,0,color='g',marker='s', label=r'$p_s=5.0$ bar',linestyle="None")
    plt.plot(0,0,color='b',marker='s', label=r'$p_s=1.0$ bar',linestyle="None")
    plt.plot(0,0,color='r',marker='s', label=r'$p_s=0.2$ bar',linestyle="None")
    plt.plot(0,0,color='c',marker='s', label=r'$p_s=0.04$ bar',linestyle="None")

  #plt.plot(0,0,color='k',marker='o', label=r'$G=0$ days',linestyle="None")

  #plt.plot(0,0,color='k',marker='*', label=r'$G=0.1$ days',linestyle="None")
  plt.plot(0,0,color='k',marker='*', label=r'$\mathcal{G}=1$',linestyle="None")
  plt.plot(0,0,color='k',marker='d', label=r'$\mathcal{G}=0.8$',linestyle="None")
  plt.plot(0,0,color='k',marker='o', label=r'$\mathcal{G}=0$',linestyle="None")
  plt.plot(0,0,color='k',marker='^', label=r'$\mathcal{G}=-0.7$',linestyle="None")


  #plt.plot(0,0,color='k',marker='o', label=r'$\tau_f=0.1$ days',linestyle="None")
  #plt.plot(0,0,color='k',marker='*', label=r'$\tau_f=1$ days',linestyle="None")
  #plt.plot(0,0,color='k',marker='^', label=r'$\tau_f=10$ days',linestyle="None")
  import matplotlib
  matplotlib.rcParams['legend.handlelength'] = 0
  matplotlib.rcParams['legend.numpoints'] = 1

  params = {'legend.fontsize': 12,
          'legend.linewidth': 2}
  plt.rcParams.update(params)

  plt.legend(loc='upper left')
  #x2=np.arange(80)
  #print x2
  print itest,iy
  #plt.xlim([-10,80])
  #plt.ylim([0,200])
  #plt.plot(x2[:],3.14*x2[:])
  #plt.plot(x2[:],3.45*x2[:])
  #plt.plot(x2[:],2.83*x2[:])
  #plt.plot(x2[:],2.14*x2[:])
  #plt.plot(x11[:,0],3.14*x11[:,0]-10,'.')
  #plt.plot(x11[:,0],3.14*x11[:,0]+10,'.')
  plt.title(r'$\tau_f=$'+str(itauf)+' days')
  plt.ylabel(r'$U(n_{\overline{\mu}=0})-U(n_{\overline{\mu}=1})$')
  plt.ylabel('diff '+labels[iy])
  #plt.xlabel(labels[ilabel])#(r'$U_{mean}$')i
  #sss=r'$e^{-\mathcal{G}}/\Omega^*p_s$'#labels[ilabel]
  #ss1='_test2_noG1'
  #ss1='_test2'
  plt.xlabel(sss)#(r'$U_{mean}$')i
  plt.savefig('plots/scaling/scaling_tauf_log'+str(itauf)+'_'+str(iy)+labelsn[iy]+ss1+nsstr+'.png', dpi=200)
  #plt.xlabel(labels[ilabel])#(r'$U_{mean}$')i
  #plt.show()
