#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')

import numpy as np
from scipy.io import netcdf
import math
import matplotlib.pyplot as plt
import sys
import os
import gc
from matplotlib import cm
from mpl_toolkits.axes_grid1 import AxesGrid
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import LogNorm
from matplotlib.ticker import MultipleLocator
import matplotlib.ticker as ticker
#import matplotlib


matplotlib.rcParams.update({'font.size': 16})



from argparse import ArgumentParser
parser = ArgumentParser()

a = 6400000.0#/8.0
g = 9.8
kappa = 0.286
M_air = 28.98
k = 1.38E-23
R=8.3144621
p0=100000


parser.add_argument("-d","--dailymean",action="store_true")
parser.add_argument("-i","--number",action="store",type=str)
parser.add_argument("-p","--path",action="store",type=str)
parser.add_argument("-o","--output",action="store",type=str)
parser.add_argument("-v","--version",action="store",type=str)

args, unknown = parser.parse_known_args()

nx1=['0.0625','0.125','0.25','0.5','1.0','2.0','4.0']
ny1=['0.5','7','30','90','360']

nx2=[float(i) for i in nx1]
ny2=[float(i) for i in ny1]

labels1=[r'$A_Z$',r'$K_Z$',r'$A_E$',r'$K_E$']
labels2=[r'$C_A$',r'$C_E$',r'$C_K$',r'$C_Z$']



lnx=len(nx1)
lny=len(ny1)

#omega='0.125'
#taus='0.5'
nmu='0'
res='64'

alorenz = np.zeros((lnx,lny,8))
for i,omega in enumerate(nx1):
  for j,taus in enumerate(ny1):
    print omega,taus
    res='64'
    if omega=='4.0': res='128'
    infile = 'lorenz/rot_r'+omega+'_res'+res+'_tausurf'+taus+'_nmu'+nmu+'.010.nc_output.npy'
    try:
      lorenz=np.load(infile)
      print infile,' found'
    except:
      lorenz=np.zeros((8,12))

    alorenz[i,j,0]=np.mean(lorenz[0,:],axis=0)#az
    alorenz[i,j,1]=np.mean(lorenz[1,:],axis=0)#ae
    alorenz[i,j,2]=np.mean(lorenz[2,:],axis=0)#kz
    alorenz[i,j,3]=np.mean(lorenz[3,:],axis=0)#ke
    alorenz[i,j,4]=np.mean(lorenz[4,:],axis=0)#ca
    alorenz[i,j,5]=np.mean(lorenz[5,:],axis=0)#ce
    alorenz[i,j,6]=np.mean(lorenz[6,:],axis=0)#ck
    alorenz[i,j,7]=np.mean(lorenz[7,:],axis=0)#cz

#fig, axarr = plt.subplots(1, 5, sharey='col', figsize=(6*5-2,10))

fig, axarr = plt.subplots(1, 5, sharey='col', figsize=(5*5,5))

for j,ax in enumerate(axarr):
  #for j in range(lnx):
  if True:
    ax.set_yscale('log')
    #ax.set_xscale('log')
    ax.plot(nx2[:],alorenz[:,j,0],marker='o', label=labels1[0], linewidth=1.5)
    ax.plot(nx2[:],alorenz[:,j,1],marker='o', label=labels1[1], linewidth=1.5)
    ax.plot(nx2[:],alorenz[:,j,2],marker='o', label=labels1[2], linewidth=1.5)
    ax.plot(nx2[:],alorenz[:,j,3],marker='o', label=labels1[3], linewidth=1.5)
    #ax.plot([ae,float(ny1[i])])

  if j==0:
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:], labels[:], loc=4)

  #ax.set_xlabel(r'$\tau_{surf} [days]$')
  ax.set_xlabel(r'$\Omega (\Omega_E)$')
  ax.set_title(r'$\tau_{surf}=$'+ny1[j]+' days')
  if j==0: ax.set_ylabel(r'Energy terms (Jm$^{-2}$)')



plt.tight_layout()
#plt.plot([1,2,3,4])
outname='lorenz_tau_en_omega'
plt.savefig(outname+'.pdf',format='pdf',dpi=800)
#plt.show()




fig, axarr = plt.subplots(1, 5, sharey='col', figsize=(5*5,5))

for j,ax in enumerate(axarr):
  #for j in range(lnx):
  if True:
    #ax.set_yscale('log')
    #ax.set_xscale('log')
    ax.plot(nx2[:],alorenz[:,j,4],marker='o', label=labels2[0], linewidth=1.5)
    ax.plot(nx2[:],alorenz[:,j,5],marker='o', label=labels2[1], linewidth=1.5)
    ax.plot(nx2[:],alorenz[:,j,6],marker='o', label=labels2[2], linewidth=1.5)
    ax.plot(nx2[:],alorenz[:,j,7],marker='o', label=labels2[3], linewidth=1.5)
    #ax.plot([ae,float(ny1[i])])

  if j==4:
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:], labels[:], loc=1)

  #ax.set_xlabel(r'$\tau_{surf} [days]$')
  ax.set_xlabel(r'$\Omega (\Omega_E)$')
  ax.set_title(r'$\tau_{surf}=$'+ny1[j]+' days')
  if j==0: ax.set_ylabel(r'Conversion terms (Wm$^{-2}$)')



plt.tight_layout()
#plt.plot([1,2,3,4])
outname='lorenz_tau_conv_omega'
plt.savefig(outname+'.pdf',format='pdf',dpi=800)
#plt.show()




fig, axarr = plt.subplots(1, 7, sharey='col', figsize=(5*5,5))

for i,ax in enumerate(axarr):
  #for j in range(lnx):
  if True:
    ax.set_yscale('log')
    ax.set_ylim([1000,1E8])
    ax.set_xscale('log')
    ax.plot(ny2[:],alorenz[i,:,0],marker='o', label=labels1[0], linewidth=1.5)
    ax.plot(ny2[:],alorenz[i,:,1],marker='o', label=labels1[1], linewidth=1.5)
    ax.plot(ny2[:],alorenz[i,:,2],marker='o', label=labels1[2], linewidth=1.5)
    ax.plot(ny2[:],alorenz[i,:,3],marker='o', label=labels1[3], linewidth=1.5)
    #ax.plot([ae,float(ny1[i])])

  if i==0:
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:], labels[:], loc=2,prop={'size':14})

  ax.set_xlabel(r'$\tau_{surf} [days]$')
  #ax.set_xlabel(r'$\Omega (\Omega_E)$')
  #ax.set_title(r'$\tau_{surf}=$'+ny1[j]+' days')
  ax.set_title(r'$\Omega =$'+nx1[i]+r'$\Omega_E$')
  if i==0: ax.set_ylabel(r'Energy terms (Jm$^{-2}$)')



plt.tight_layout()
#plt.plot([1,2,3,4])
outname='lorenz_omega_en_tau'
plt.savefig(outname+'.pdf',format='pdf',dpi=800)
#plt.show()




fig, axarr = plt.subplots(1, 7, sharey='col', figsize=(5*5,5))

for i,ax in enumerate(axarr):
  #for j in range(lnx):
  if True:
    #ax.set_yscale('log')
    #ax.set_ylim([1000,1E8])
    ax.set_xscale('log')
    ax.plot(ny2[:],alorenz[i,:,4],marker='o', label=labels2[0], linewidth=1.5)
    ax.plot(ny2[:],alorenz[i,:,5],marker='o', label=labels2[1], linewidth=1.5)
    ax.plot(ny2[:],alorenz[i,:,6],marker='o', label=labels2[2], linewidth=1.5)
    ax.plot(ny2[:],alorenz[i,:,7],marker='o', label=labels2[3], linewidth=1.5)
    #ax.plot([ae,float(ny1[i])])

  if i==0:
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:], labels[:], loc=2,prop={'size':14})

  ax.set_xlabel(r'$\tau_{surf} [days]$')
  #ax.set_xlabel(r'$\Omega (\Omega_E)$')
  #ax.set_title(r'$\tau_{surf}=$'+ny1[j]+' days')
  ax.set_title(r'$\Omega =$'+nx1[i]+r'$\Omega_E$')
  if i==0: ax.set_ylabel(r'Conversion terms (Wm$^{-2}$)')



plt.tight_layout()
#plt.plot([1,2,3,4])
outname='lorenz_omega_conv_tau'
plt.savefig(outname+'.pdf',format='pdf',dpi=800)
#plt.show()


fig, axarr = plt.subplots(1, 7, sharey='col', figsize=(5*5,5))

for i,ax in enumerate(axarr):
  #for j in range(lnx):
  if True:
    ax.set_yscale('log')
    ax.set_ylim([1000,1E8])
    ax.set_xscale('log')
    ax.plot(ny2[:],alorenz[i,:,0],marker='o', label=labels1[0], linewidth=1.5)
    ax.plot(ny2[:],alorenz[i,:,1],marker='o', label=labels1[1], linewidth=1.5)
    ax.plot(ny2[:],alorenz[i,:,2],marker='o', label=labels1[2], linewidth=1.5)
    ax.plot(ny2[:],alorenz[i,:,3],marker='o', label=labels1[3], linewidth=1.5)
    #ax.plot([ae,float(ny1[i])])

  if i==0:
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:], labels[:], loc=2,prop={'size':14})

  ax.set_xlabel(r'$\tau_{surf} [days]$')
  #ax.set_xlabel(r'$\Omega (\Omega_E)$')
  #ax.set_title(r'$\tau_{surf}=$'+ny1[j]+' days')
  ax.set_title(r'$\Omega =$'+nx1[i]+r'$\Omega_E$')
  if i==0: ax.set_ylabel(r'Energy terms (Jm$^{-2}$)')



plt.tight_layout()
#plt.plot([1,2,3,4])
outname='lorenz_omega_en_tau'
plt.savefig(outname+'.pdf',format='pdf',dpi=800)
#plt.show()








fig, axarr = plt.subplots(1, 4, sharey='col', figsize=(5*5,5))

for k,ax in enumerate(axarr):
  #for j in range(lnx):
  if True:
    ax.set_yscale('log')
    ax.set_ylim([1000,1E7])
    #ax.set_xscale('log')
    for i,taus in enumerate(ny1):
      ax.plot(nx2[:],alorenz[:,i,k],marker='o', label=r'$\tau_{surf}=$'+taus+' d', linewidth=1.5)
      #ax.plot(nx2[:],alorenz[:,0,k],marker='o', label=labels2[0], linewidth=1.5)
      #ax.plot(nx2[:],alorenz[:,0,k],marker='o', label=labels2[0], linewidth=1.5)
    
    #ax.plot(ny2[:],alorenz[i,:,5],marker='o', label=labels2[1], linewidth=1.5)
    #ax.plot(ny2[:],alorenz[i,:,6],marker='o', label=labels2[2], linewidth=1.5)
    #ax.plot(ny2[:],alorenz[i,:,7],marker='o', label=labels2[3], linewidth=1.5)
    #ax.plot([ae,float(ny1[i])])

  if k==0:
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:], labels[:], loc=4,prop={'size':17})

  #ax.set_xlabel(r'$\tau_{surf} [days]$')
  ax.set_xlabel(r'$\Omega (\Omega_E)$')
  #ax.set_title(r'$\tau_{surf}=$'+ny1[j]+' days')
  ax.set_title(labels1[k])
  if k==0: ax.set_ylabel(r'Energy terms (Jm$^{-2}$)')



plt.tight_layout()
#plt.plot([1,2,3,4])
outname='lorenz_en_tau_omega'
plt.savefig(outname+'.pdf',format='pdf',dpi=800)
#plt.show()



fig, axarr = plt.subplots(1, 4, sharey='col', figsize=(5*5,5))

for k,ax in enumerate(axarr):
  #for j in range(lnx):
  if True:
    #ax.set_yscale('log')
    #ax.set_ylim([1000,1E7])
    #ax.set_xscale('log')
    for i,taus in enumerate(ny1):
      ax.plot(nx2[:],alorenz[:,i,k+4],marker='o', label=r'$\tau_{surf}=$'+taus+' d', linewidth=1.5)
      #ax.plot(nx2[:],alorenz[:,0,k],marker='o', label=labels2[0], linewidth=1.5)
      #ax.plot(nx2[:],alorenz[:,0,k],marker='o', label=labels2[0], linewidth=1.5)
    
    #ax.plot(ny2[:],alorenz[i,:,5],marker='o', label=labels2[1], linewidth=1.5)
    #ax.plot(ny2[:],alorenz[i,:,6],marker='o', label=labels2[2], linewidth=1.5)
    #ax.plot(ny2[:],alorenz[i,:,7],marker='o', label=labels2[3], linewidth=1.5)
    #ax.plot([ae,float(ny1[i])])

  if k==3:
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:], labels[:], loc=1,prop={'size':15})

  #ax.set_xlabel(r'$\tau_{surf} [days]$')
  ax.set_xlabel(r'$\Omega (\Omega_E)$')
  #ax.set_title(r'$\tau_{surf}=$'+ny1[j]+' days')
  ax.set_title(labels2[k])
  if k==0: ax.set_ylabel(r'Conversion terms (Wm$^{-2}$)')



plt.tight_layout()
#plt.plot([1,2,3,4])
outname='lorenz_co_tau_omega'
plt.savefig(outname+'.pdf',format='pdf',dpi=800)
#plt.show()











fig, axarr = plt.subplots(1, 4, sharey='col', figsize=(5*5,5))

for k,ax in enumerate(axarr):
  #for j in range(lnx):
  if True:
    ax.set_yscale('log')
    ax.set_ylim([1000,1E7])
    ax.set_xscale('log')
    for j,omega in enumerate(nx1):
      ax.plot(ny2[:],alorenz[j,:,k],marker='o', label=r'$\Omega=$'+omega+r'$\Omega_E$', linewidth=1.5)
      #ax.plot(nx2[:],alorenz[:,0,k],marker='o', label=labels2[0], linewidth=1.5)
      #ax.plot(nx2[:],alorenz[:,0,k],marker='o', label=labels2[0], linewidth=1.5)
    
    #ax.plot(ny2[:],alorenz[i,:,5],marker='o', label=labels2[1], linewidth=1.5)
    #ax.plot(ny2[:],alorenz[i,:,6],marker='o', label=labels2[2], linewidth=1.5)
    #ax.plot(ny2[:],alorenz[i,:,7],marker='o', label=labels2[3], linewidth=1.5)
    #ax.plot([ae,float(ny1[i])])

  if k==0:
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:], labels[:], loc=4,prop={'size':11})

  ax.set_xlabel(r'$\tau_{surf} [days]$')
  #ax.set_xlabel(r'$\Omega (\Omega_E)$')
  #ax.set_title(r'$\tau_{surf}=$'+ny1[j]+' days')
  ax.set_title(labels1[k])
  if k==0: ax.set_ylabel(r'Energy terms (Jm$^{-2}$)')



plt.tight_layout()
#plt.plot([1,2,3,4])
outname='lorenz_en_omega_tau'
plt.savefig(outname+'.pdf',format='pdf',dpi=800)
#plt.show()




fig, axarr = plt.subplots(1, 4, sharey='col', figsize=(5*5,5))

for k,ax in enumerate(axarr):
  #for j in range(lnx):
  if True:
    #ax.set_yscale('log')
    #ax.set_ylim([1000,1E7])
    ax.set_xscale('log')
    for j,omega in enumerate(nx1):
      ax.plot(ny2[:],alorenz[j,:,k+4],marker='o', label=r'$\Omega=$'+omega+r'$\Omega_E$', linewidth=1.5)
      #ax.plot(nx2[:],alorenz[:,0,k],marker='o', label=labels2[0], linewidth=1.5)
      #ax.plot(nx2[:],alorenz[:,0,k],marker='o', label=labels2[0], linewidth=1.5)
    
    #ax.plot(ny2[:],alorenz[i,:,5],marker='o', label=labels2[1], linewidth=1.5)
    #ax.plot(ny2[:],alorenz[i,:,6],marker='o', label=labels2[2], linewidth=1.5)
    #ax.plot(ny2[:],alorenz[i,:,7],marker='o', label=labels2[3], linewidth=1.5)
    #ax.plot([ae,float(ny1[i])])

  if k==2:
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:], labels[:], loc=1,prop={'size':11})

  ax.set_xlabel(r'$\tau_{surf} [days]$')
  #ax.set_xlabel(r'$\Omega (\Omega_E)$')
  #ax.set_title(r'$\tau_{surf}=$'+ny1[j]+' days')
  ax.set_title(labels2[k])
  if k==0: ax.set_ylabel(r'Conversion terms (Wm$^{-2}$)')



plt.tight_layout()
#plt.plot([1,2,3,4])
outname='lorenz_conv_omega_tau'
plt.savefig(outname+'.pdf',format='pdf',dpi=800)
#plt.show()
