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

  for ic,conv in enumerate([0, 4]):

    fig, axarr = plt.subplots(1, 1, sharey='col', figsize=(6,5))
    if True:
    #for i,ax in enumerate(axarr):
      ax=axarr
      i=0
    #  fig, axarr = plt.subplots(1, 1, sharey='col', figsize=(5*5,5))
      if conv == 0:
        ax.set_yscale('log')
        ax.set_ylim([1000,1E8])
      ax.set_xscale('log')
      if conv == 0: labs = labels1
      if conv == 4: labs = labels2
      ax.plot(nx2[:],mlorenz[years-1,:,0+conv],marker='o', label=labs[0], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,1+conv],marker='o', label=labs[1], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,2+conv],marker='o', label=labs[2], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,3+conv],marker='o', label=labs[3], linewidth=1.5)

      if i==0:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[:], labels[:], loc=2,prop={'size':14})
      ax.set_xlabel(r'$\Omega [\Omega_E]$')
      #if i==0:
      if conv == 0: ax.set_ylabel(r'Energy terms (Jm$^{-2}$)')
      if conv == 4: ax.set_ylabel(r'Conversion terms (Wm$^{-2}$)')
    plt.tight_layout()
    #plt.plot([1,2,3,4])
    if conv == 0: outname='lorenz_omega_en'
    if conv == 4: outname='lorenz_omega_conv'
    plt.savefig(args.output+outname+'.pdf',format='pdf',dpi=800)
    #plt.show()





if True:

  nx1=['0.00','2.00','10.00']
  tausurf=360
  nmu=1
  nx2=[float(i) for i in nx1]
  lnx=len(nx1)
  omega='1.0'


years=1

if OFLAG==1:

  alorenz = np.zeros((years,lnx,8,12))
  mlorenz = np.zeros((years,lnx,12))
  for i,sol in enumerate(nx1):
    #for j,taus in enumerate(ny1):
      print omega
      res='64'
      if omega=='4.0': res='128'
      #path = 'data/lorenz_en/rot_r'+omega+'_res'+res+'_tausurf'+taus+'_nmu'+nmu+'.010.nc_output.npy'
      path = 'data/lorenz_en/rev53_r'+omega+'_res'+res+'_radius1.00_taufr1.0_psurf1.0_pref1.0_taus'+sol+'_tausurf360_nmu'+str(nmu)
      onlyfiles=os.listdir(path)
      onlyfiles = sorted(onlyfiles)
      print onlyfiles
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

  for ic,conv in enumerate([0, 4]):

    fig, axarr = plt.subplots(1, 1, sharey='col', figsize=(6,5))
    if True:
    #for i,ax in enumerate(axarr):
      ax=axarr
      i=0
    #  fig, axarr = plt.subplots(1, 1, sharey='col', figsize=(5*5,5))
      if conv == 0:
        ax.set_yscale('log')
        ax.set_ylim([10000,1E9])
      if conv == 4: ax.set_ylim([-0.5,2.0])
      ax.set_xlim([-2,12])
      #ax.set_xscale('log')
      if conv == 0: labs = labels1
      if conv == 4: labs = labels2
      ax.plot(nx2[:],mlorenz[years-1,:,0+conv],marker='o', label=labs[0], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,1+conv],marker='o', label=labs[1], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,2+conv],marker='o', label=labs[2], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,3+conv],marker='o', label=labs[3], linewidth=1.5)

      if i==0:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[:], labels[:], loc=2,prop={'size':14})
      ax.set_xlabel(r'$\chi_{sw}$')
      #if i==0:
      if conv == 0: ax.set_ylabel(r'Energy terms (Jm$^{-2}$)')
      if conv == 4: ax.set_ylabel(r'Conversion terms (Wm$^{-2}$)')
    plt.tight_layout()
    #plt.plot([1,2,3,4])
    if conv == 0: outname='lorenz_sol_en'
    if conv == 4: outname='lorenz_sol_conv'
    plt.savefig(args.output+outname+'.pdf',format='pdf',dpi=800)




if True:

  nx1=['0.2','1.0','5.0']
  nxx=[0.2,1.0,5.0]
  tausurf=360
  nmu=1
  nx2=[float(i) for i in nx1]
  lnx=len(nx1)
  omega='1.0'
  sol = '0.00'

years=1

if OFLAG==1:

  alorenz = np.zeros((years,lnx,8,12))
  mlorenz = np.zeros((years,lnx,12))
  for i,press in enumerate(nx1):
    #for j,taus in enumerate(ny1):
      print omega
      res='64'
      if omega=='4.0': res='128'
      #path = 'data/lorenz_en/rot_r'+omega+'_res'+res+'_tausurf'+taus+'_nmu'+nmu+'.010.nc_output.npy'
      path = 'data/lorenz_en/rev53_r'+omega+'_res'+res+'_radius1.00_taufr1.0_psurf'+press+'_pref'+press+'_taus'+sol+'_tausurf360_nmu'+str(nmu)
      onlyfiles=os.listdir(path)
      onlyfiles = sorted(onlyfiles)
      print onlyfiles
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

  for ic,conv in enumerate([0, 4]):

    fig, axarr = plt.subplots(1, 1, sharey='col', figsize=(6,5))
    if True:
    #for i,ax in enumerate(axarr):
      ax=axarr
      i=0
    #  fig, axarr = plt.subplots(1, 1, sharey='col', figsize=(5*5,5))
      if conv == 0:
        ax.set_yscale('log')
        ax.set_ylim([10000,1E9])
      if conv == 4: ax.set_ylim([-1.0,2.0])
      ax.set_xscale('log')
      if conv == 0: labs = labels1
      if conv == 4: labs = labels2
      ax.plot(nx2[:],mlorenz[years-1,:,0+conv]/nxx[:],marker='o', label=labs[0], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,1+conv]/nxx[:],marker='o', label=labs[1], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,2+conv]/nxx[:],marker='o', label=labs[2], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,3+conv]/nxx[:],marker='o', label=labs[3], linewidth=1.5)

      if i==0:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[:], labels[:], loc=2,prop={'size':14})
      ax.set_xlabel(r'$p_{surf} [p_{0}]$')
      #if i==0:
      if conv == 0: ax.set_ylabel(r'Energy terms/$p_{surf}$ (Jm$^{-2}Pa^{-1}$)')
      if conv == 4: ax.set_ylabel(r'Conversion terms/$p_{surf}$ (Wm$^{-2}Pa^{-1}$)')
    plt.tight_layout()
    #plt.plot([1,2,3,4])
    if conv == 0: outname='lorenz_p1_en'
    if conv == 4: outname='lorenz_p1_conv'
    plt.savefig(args.output+outname+'.pdf',format='pdf',dpi=800)




if True:

  nx1=['0.1','1.0','10.0']
  tausurf=360
  nmu=1
  nx2=[float(i) for i in nx1]
  lnx=len(nx1)
  omega='1.0'
  sol = '0.00'
  press = '1.0'

years=1

if OFLAG==1:

  alorenz = np.zeros((years,lnx,8,12))
  mlorenz = np.zeros((years,lnx,12))
  for i,fr in enumerate(nx1):
    #for j,taus in enumerate(ny1):
      print omega
      res='64'
      if omega=='4.0': res='128'
      #path = 'data/lorenz_en/rot_r'+omega+'_res'+res+'_tausurf'+taus+'_nmu'+nmu+'.010.nc_output.npy'
      path = 'data/lorenz_en/rev53_r'+omega+'_res'+res+'_radius1.00_taufr'+fr+'_psurf'+press+'_pref'+press+'_taus'+sol+'_tausurf360_nmu'+str(nmu)
      onlyfiles=os.listdir(path)
      onlyfiles = sorted(onlyfiles)
      print onlyfiles
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

  for ic,conv in enumerate([0, 4]):

    fig, axarr = plt.subplots(1, 1, sharey='col', figsize=(6,5))
    if True:
    #for i,ax in enumerate(axarr):
      ax=axarr
      i=0
    #  fig, axarr = plt.subplots(1, 1, sharey='col', figsize=(5*5,5))
      if conv == 0:
        ax.set_yscale('log')
        ax.set_ylim([1000,1E9])
      if conv == 4: ax.set_ylim([-1.0,2.0])
      ax.set_xscale('log')
      ax.set_xlim([5E-2,2E1])
      if conv == 0: labs = labels1
      if conv == 4: labs = labels2
      ax.plot(nx2[:],mlorenz[years-1,:,0+conv],marker='o', label=labs[0], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,1+conv],marker='o', label=labs[1], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,2+conv],marker='o', label=labs[2], linewidth=1.5)
      ax.plot(nx2[:],mlorenz[years-1,:,3+conv],marker='o', label=labs[3], linewidth=1.5)

      if i==0:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[:], labels[:], loc=2,prop={'size':14})
      ax.set_xlabel(r'$\tau_{f} [days]$')
      #if i==0:
      if conv == 0: ax.set_ylabel(r'Energy terms (Jm$^{-2}$)')
      if conv == 4: ax.set_ylabel(r'Conversion terms (Wm$^{-2}$)')
    plt.tight_layout()
    #plt.plot([1,2,3,4])
    if conv == 0: outname='lorenz_fr_en'
    if conv == 4: outname='lorenz_fr_conv'
    plt.savefig(args.output+outname+'.pdf',format='pdf',dpi=800)






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
  for i,omega in enumerate(['0.0625','0.125','0.25','0.5','1.0','2.0']):
    for tausurf in ['3.6','36','360']:
      for nmu in [0, 1]:
        for fr in ['0.1','1.0','10.0']:
          for press in ['0.2','1.0','5.0']:
            for sol in ['0.00','2.00','10.00']:
              iter=iter+1
              print omega,tausurf,nmu,fr,press,sol
              res='64'
              if omega=='4.0': res='128'
              #path = 'data/lorenz_en/rev53_r'+omega+'_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu'+str(1)
              name = 'rev53_r'+omega+'_res'+res+'_radius1.00_taufr'+fr+'_psurf'+press+'_pref'+press+'_taus'+sol+'_tausurf'+tausurf+'_nmu'+str(nmu)
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
              dt=0.08333333
              time = np.arange(dt,years,dt)

              #print len(time),len(alorenz2[:,i])

              #print alorenz2[:,1]

              #print timels
              #print time
              fig = plt.figure(figsize=(10,6))
              ax1 = fig.add_subplot(2,1,1)
              ax2 = fig.add_subplot(2,1,2)
              #fig.suptitle('Tidal effect',fontsize=20)
              lab=['AZ','KZ','AE','KE']
              for i in range(4):
                ax1.plot(time[:], alorenz2[:,i], label=lab[i], linewidth=1.2)
              ax1.set_yscale('log')
              #ax1.set_xlabel('Time (Sols)')
              ax1.set_ylabel('Energy (Jm$^{-2}$)')
              #ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
              #ax1.set_xlim([24.3,27.9])
              ax1.set_xlim([0,years+0.6])
              handles, labels = ax1.get_legend_handles_labels()
              ax1.legend(handles[:], labels[:])
              lab=['CA','CE','CK','CZ']
              for i in range(4):
                ax2.plot(time[:], alorenz2[:,i+4], label=lab[i], linewidth=1.2)
              #ax2.set_yscale('log')
              ax2.set_xlabel('Time (years)')
              ax2.set_ylabel('Conversion Terms (Wm$^{-2}$)')
              ax2.set_xlim([0,years+0.6])
              handles, labels = ax2.get_legend_handles_labels()
              ax2.legend(handles[:], labels[:])
              #plt.show()
              outname='lorenz_time_'
              plt.savefig(args.output+outname+name+'.pdf',format='pdf',dpi=800)
              #plt.savefig('energies3x_n.png', dpi=300)

















sys.exit(1)

iii=-1
for filen in onlyfiles:

  iii=iii+1

  try:
    dat=np.load(path+'/'+filen)
  except:
    break
  if iii>0:  prev = np.copy(tot)








n=44#38
nd=44#39
#hem='_nh'
hem=''

data = np.genfromtxt('energy_out'+str(n)+'.dat'+hem,skip_header=1)
datar = np.genfromtxt('energy_out'+str(nd)+'_dailyrunningmean.dat'+hem,skip_header=1)
datap = np.genfromtxt('energy_out'+str(n)+'.dat'+hem+'_parts',skip_header=1)
datapr = np.genfromtxt('energy_out'+str(nd)+'_dailyrunningmean.dat'+hem+'_parts',skip_header=1)
#print data
labels2 = ['180','270','0','90','180','270','0','90','180','270','0','90','180']
print data[:,0]
time = (data[:,0] + data[:,1])/2.0
time = time - 316
timels = np.array([141.468,157.232,173.847,191.361,209.728,228.788,248.261,267.784,286.983,305.552,323.296,340.145,356.123,11.3231,25.8743,39.9237,53.6243,67.1298,80.5934,94.1682,108.007,122.265,137.092,152.63,168.993,186.249,204.382,223.268,242.657,262.204,281.532,300.307,318.3,335.407,351.627,7.03832,21.761,35.9387,49.7235,63.2692,76.7293,90.2565,104.004,118.126,132.775,148.095,164.213,181.21,199.099,217.789,237.066,256.607,276.035,294.997,313.23,330.595,347.065,2.69681,17.6027,31.9213,45.803,59.4015,72.8705])
timels2=np.copy(timels)
timels=timels/360.0+24
a=0.0
for i in range(1,len(timels)):
  if timels[i-1] > timels[i]+a: a = a + 1.0
  print timels[i-1],timels[i]+a,a
  timels[i]=timels[i]+a

#timels
print timels
print time
fig = plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)
#fig.suptitle('Tidal effect',fontsize=20)
lab=['AZ','KZ','AE','KE']
for i in range(4):
  ax1.plot(timels[1:-1],data[1:-1,i+2]-datar[1:-1,i+2], label=lab[i], linewidth=1.2)
#ax1.set_yscale('log')
#ax1.set_xlabel('Time (Sols)')
ax1.set_ylabel('Energy (Jm$^{-2}$)')
ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.set_xlim([24.3,27.9])
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[:], labels[:])
lab=['CA','CE','CK','CZ']
for i in range(4):
  ax2.plot(timels[1:-1],data[1:-1,i+6]-datar[1:-1,i+6], label=lab[i], linewidth=1.2)
#ax2.set_yscale('log')
ax2.set_xlabel('Time (MY)')
ax2.set_ylabel('Conversion Terms (Wm$^{-2}$)')
ax2.set_xlim([24.3,27.9])
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles[:], labels[:])
#plt.show()
plt.savefig('energies3x_n_tidal.png', dpi=300)




fig = plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)
#fig.suptitle('Tidal effect',fontsize=20)
lab=['AZ','KZ','AE','KE']
for i in range(4):
  ax1.plot(timels[1:-1],data[1:-1,i+2], label=lab[i], linewidth=1.2)
ax1.set_yscale('log')
#ax1.set_xlabel('Time (Sols)')
ax1.set_ylabel('Energy (Jm$^{-2}$)')
#ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.set_xlim([24.3,27.9])
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[:], labels[:])
lab=['CA','CE','CK','CZ']
for i in range(4):
  ax2.plot(timels[1:-1],data[1:-1,i+6], label=lab[i], linewidth=1.2)
#ax2.set_yscale('log')
ax2.set_xlabel('Time (MY)')
ax2.set_ylabel('Conversion Terms (Wm$^{-2}$)')
ax2.set_xlim([24.3,27.9])
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles[:], labels[:])
#plt.show()
plt.savefig('energies1x_n_normal.png', dpi=300)

fig = plt.figure(figsize=(10,6))
ax1 = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)
#fig.suptitle('Tidal effect',fontsize=20)
lab=['AZ','KZ','AE','KE']
for i in range(4):
  ax1.plot(timels[1:-1],datar[1:-1,i+2], label=lab[i], linewidth=1.2)
ax1.set_yscale('log')
#ax1.set_xlabel('Time (Sols)')
ax1.set_ylabel('Energy (Jm$^{-2}$)')
#ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.set_xlim([24.3,27.9])
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[:], labels[:])
lab=['CA','CE','CK','CZ']
for i in range(4):
  ax2.plot(timels[1:-1],datar[1:-1,i+6], label=lab[i], linewidth=1.2)
#ax2.set_yscale('log')
ax2.set_xlabel('Time (MY)')
ax2.set_ylabel('Conversion Terms (Wm$^{-2}$)')
ax2.set_xlim([24.3,27.9])
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles[:], labels[:])
#plt.show()
plt.savefig('energies2x_n_dailymean.png', dpi=300)




matplotlib.rcParams.update({'font.size': 14})



fig = plt.figure(figsize=(10,11))
ax1 = fig.add_subplot(4,1,1)
ax2 = fig.add_subplot(4,1,2,label='b)')
#fig.subplots_adjust(hspace=.5)
ax3 = fig.add_subplot(4,1,3)
#fig.subplots_adjust(hspace=.5)
ax4 = fig.add_subplot(4,1,4)

#fig.suptitle('Tidal effect',fontsize=20)
lab=['AZ','KZ','AE','KE']
for i in range(4):
  ax1.plot(timels[1:-1],data[1:-1,i+2], label=lab[i], linewidth=1.2)
ax1.set_yscale('log')

#ax1.set_xlabel('Time (Sols)')
ax1.set_ylabel('Energy (Jm$^{-2}$)')
#ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.set_xlim([24.3,27.9])
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[:], labels[:])
ax1.text(0.03,0.90,'a)', ha='center', va='center', transform=ax1.transAxes)
lab=['CA','CE','CZ']
for i in range(2):
  if i == 2: x=1
  else: x = 0
  ax2.plot(timels[1:-1],data[1:-1,i+6], label=lab[i], linewidth=1.2)
ax2.plot(timels[1:-1],datap[1:-1,6], label='CK1', linewidth=1.2,color='purple')
ax2.plot(timels[1:-1],datap[1:-1,7], label='CK2', linewidth=1.2,color='purple',ls='--')
ax2.plot(timels[1:-1],data[1:-1,3+6], label='CZ', linewidth=1.2)
#ax2.set_yscale('log')
#ax2.set_xlabel('Time (MY)')
ax2.set_ylabel('Conversion Terms (Wm$^{-2}$)')
ax2.set_xlim([24.3,27.9])
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles[:], labels[:])
ax2.text(0.03,0.90,'b)', ha='center', va='center', transform=ax2.transAxes)
#plt.show()
lab=['AZ','KZ','AE','KE']
for i in range(4):
  if i == 3: lw=1.2 
  else:lw=1
  ax3.plot(timels[1:-1],(data[1:-1,i+2]-datar[1:-1,i+2])/data[1:-1,i+2]*100, label=lab[i], linewidth=lw)
#ax1.set_yscale('log')
#ax1.set_xlabel('Time (Sols)')
#ax3.set_title('Tidal contribution')
ax3.set_ylabel('Tidal Contribution \n to Energy (%)', multialignment='center') #('Energy (Jm$^{-2}$)')
#ax3.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax3.set_xlim([24.3,27.9])
handles, labels = ax1.get_legend_handles_labels()
ax3.legend(handles[:], labels[:])
ax3.text(0.03,0.90,'c)', ha='center', va='center', transform=ax3.transAxes)
lab=['CA','CE','CZ']
for i in range(2):
  lw=1.2
  if i == 2: x=1
  else: x = 0
  ax4.plot(timels[1:-1],(data[1:-1,i+6]-datar[1:-1,i+6]), label=lab[i], linewidth=lw)
ax4.plot(timels[1:-1],(datap[1:-1,6]-datapr[1:-1,6]), label='CK1', linewidth=1.2,color='purple')
ax4.plot(timels[1:-1],(datap[1:-1,7]-datapr[1:-1,7]), label='CK2', linewidth=1.2,color='purple',ls='--')
ax4.plot(timels[1:-1],(data[1:-1,9]-datar[1:-1,9]), label='CZ', linewidth=lw)
#ax2.set_yscale('log')
ax4.set_xlabel('Time (MY)')
ax4.set_ylabel('Tidal Component of \n Conversion Terms (Wm$^{-2}$)', multialignment='center')
ax4.set_xlim([24.3,27.9])
handles, labels = ax2.get_legend_handles_labels()
ax4.legend(handles[:], labels[:])
ax4.text(0.03,0.90,'d)', ha='center', va='center', transform=ax4.transAxes)

fig.tight_layout()

plt.savefig('energies_n_paper'+str(n)+'.eps')


fig = plt.figure(figsize=(10,11))
ax1 = fig.add_subplot(4,1,1)
ax2 = fig.add_subplot(4,1,2,label='b)')
#fig.subplots_adjust(hspace=.5)
ax3 = fig.add_subplot(4,1,3)
#fig.subplots_adjust(hspace=.5)
ax4 = fig.add_subplot(4,1,4)

#fig.suptitle('Tidal effect',fontsize=20)
lab=['AZ1','AZ2','AE1','AE2']
for i in range(4):
  ax1.plot(timels[1:-1],datap[1:-1,i+2], label=lab[i], linewidth=1.2)
ax1.set_yscale('log')

#ax1.set_xlabel('Time (Sols)')
ax1.set_ylabel('Energy (Jm$^{-2}$)')
#ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.set_xlim([24.3,27.9])
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[:], labels[:])
ax1.text(0.03,0.90,'a)', ha='center', va='center', transform=ax1.transAxes)
lab=['CK1','CK2','CZ1','CZ2']
for i in range(4):
  ax2.plot(timels[1:-1],datap[1:-1,i+6], label=lab[i], linewidth=1.2)
#ax2.set_yscale('log')
#ax2.set_xlabel('Time (MY)')
ax2.set_ylabel('Conversion Terms (Wm$^{-2}$)')
ax2.set_xlim([24.3,27.9])
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles[:], labels[:])
ax2.text(0.03,0.90,'b)', ha='center', va='center', transform=ax2.transAxes)
#plt.show()
lab=['AZ1','AZ2','AE1','AE2']
for i in range(4):
  if i == 3: lw=1.2 
  else:lw=1
  ax3.plot(timels[1:-1],(datap[1:-1,i+2]-datapr[1:-1,i+2])/datap[1:-1,i+2]*100, label=lab[i], linewidth=lw)
#ax1.set_yscale('log')
#ax1.set_xlabel('Time (Sols)')
#ax3.set_title('Tidal contribution')
ax3.set_ylabel('Tidal Contribution \n to Energy (%)', multialignment='center') #('Energy (Jm$^{-2}$)')
#ax3.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax3.set_xlim([24.3,27.9])
handles, labels = ax1.get_legend_handles_labels()
ax3.legend(handles[:], labels[:])
ax3.text(0.03,0.90,'c)', ha='center', va='center', transform=ax3.transAxes)
lab=['CK1','CK2','CZ1','CZ2']
for i in range(4):
  lw=1.2
  ax4.plot(timels[1:-1],(datap[1:-1,i+6]-datapr[1:-1,i+6]), label=lab[i], linewidth=lw)
#ax2.set_yscale('log')
ax4.set_xlabel('Time (MY)')
ax4.set_ylabel('Tidal Component of \n Conversion Terms (Wm$^{-2}$)', multialignment='center')
ax4.set_xlim([24.3,27.9])
handles, labels = ax2.get_legend_handles_labels()
ax4.legend(handles[:], labels[:])
ax4.text(0.03,0.90,'d)', ha='center', va='center', transform=ax4.transAxes)

fig.tight_layout()

plt.savefig('energies_n_paper'+str(n)+'_parts.eps')






fig = plt.figure(figsize=(10,8))
ax1 = fig.add_subplot(3,1,1)
ax2 = fig.add_subplot(3,1,2,label='b)')
#fig.subplots_adjust(hspace=.5)
ax3 = fig.add_subplot(3,1,3)
#fig.subplots_adjust(hspace=.5)
#ax4 = fig.add_subplot(4,1,4)
#fig.suptitle('Tidal effect',fontsize=20)
lab=['$A_Z$','$K_Z$','$A_E$','$K_E$']
for i in range(4):
  ax1.plot(timels[1:-1],data[1:-1,i+2], label=lab[i], linewidth=1.2)
ax1.set_yscale('log')
y1max=np.max(data[1:-1,2:6])
y1min=np.min(data[1:-1,2:6])
y2max=np.max(datar[1:-1,2:6])
y2min=np.min(datar[1:-1,2:6])

yymin=min([y1min,y2min])
yymax=max([y1max,y2max])

#ax1.set_xlabel('Time (Sols)')
ax1.set_ylabel('Energy (Jm$^{-2}$)')
#ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax1.set_xlim([24.3,27.7])
ax1.set_ylim([yymin,yymax])
ax1.set_xticks(np.arange(24.5, 27.75, 0.25))
ax1.set_xticklabels(labels2)
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[:], labels[:],prop={'size':14})
ax1.text(0.03,0.80,'a)', ha='center', va='center', transform=ax1.transAxes)
lab=['$A_Z$','$K_Z$','$A_E$','$K_E$']
for i in range(4):
  ax2.plot(timels[1:-1],datar[1:-1,i+2], label=lab[i], linewidth=1.2)
ax2.set_yscale('log')
#ax1.set_xlabel('Time (Sols)')
ax2.set_ylabel('Daily-averaged \n Energy (Jm$^{-2}$)')
#ax1.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax2.set_xlim([24.3,27.7])
ax2.set_ylim([yymin,yymax])
ax2.set_xticks(np.arange(24.5, 27.75, 0.25))
ax2.set_xticklabels(labels2)
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles[:], labels[:],prop={'size':14})
ax2.text(0.03,0.80,'b)', ha='center', va='center', transform=ax2.transAxes)
lab=['$A_Z$','$K_Z$','$A_E$','$K_E$']
for i in range(4):
  if i == 3: lw=1.2 
  else:lw=1
  ax3.plot(timels[1:-1],(data[1:-1,i+2]-datar[1:-1,i+2])/data[1:-1,i+2]*100, label=lab[i], linewidth=lw)
#ax1.set_yscale('log')
#ax1.set_xlabel('Time (Sols)')
#ax3.set_title('Tidal contribution')
ax3.set_xlabel('Solar Longitude $L_s$ [$^\circ$]')
ax3.set_ylabel('Tidal Contribution \n to Energy (%)', multialignment='center') #('Energy (Jm$^{-2}$)')
#ax3.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ax3.set_xlim([24.3,27.7])
ax3.set_xticks(np.arange(24.5, 27.75, 0.25))
ax3.set_xticklabels(labels2)
handles, labels = ax1.get_legend_handles_labels()
ax3.legend(handles[:], labels[:],prop={'size':14})
ax3.text(0.03,0.80,'c)', ha='center', va='center', transform=ax3.transAxes)


fig.tight_layout()

plt.savefig('energies_nxxy_paper'+str(n)+hem+'.eps')











fac=1
facstr=''
add=0
if hem != '': 
  fac=0.01
  facstr='$\cdot 10^{-2}$'
  add=0.2

fig = plt.figure(figsize=(10,8))
ax1 = fig.add_subplot(3,1,1)
ax2 = fig.add_subplot(3,1,2,label='b)')
#fig.subplots_adjust(hspace=.5)
ax3 = fig.add_subplot(3,1,3)
#fig.subplots_adjust(hspace=.5)
#ax4 = fig.add_subplot(3,1,4)
#fig.suptitle('Tidal effect',fontsize=20)

data1=np.copy(data)
datar1=np.copy(datar)
data1[:,9]=data1[:,9]*fac
datar1[:,9]=datar1[:,9]*fac

y1max=np.max(data1[1:-1,6:10])
y1min=np.min(data1[1:-1,6:10])
y2max=np.max(datar1[1:-1,6:10])
y2min=np.min(datar1[1:-1,6:10])
y3max=np.max(data1[1:-1,6:10]-datar1[1:-1,6:10])
y3min=np.min(data1[1:-1,6:10]-datar1[1:-1,6:10])

yymin=min([y1min,y2min,y3min])
yymax=max([y1max,y2max,y3max])


lab=['$C_A$','$C_E$','$C_Z$'+facstr]
for i in range(2):
  if i == 2: x=1
  else: x = 0
  ax1.plot(timels[1:-1],data[1:-1,i+6], label=lab[i], linewidth=1.2)
ax1.plot(timels[1:-1],datap[1:-1,6], label='$C_{K1}$', linewidth=1.2,color='purple')
ax1.plot(timels[1:-1],datap[1:-1,7], label='$C_{K2}$', linewidth=1.2,color='purple',ls='--')
ax1.plot(timels[1:-1],data[1:-1,3+6]*fac, label='$C_Z$'+facstr, linewidth=1.2)
#ax2.set_yscale('log')
#ax2.set_xlabel('Time (MY)')
ax1.set_ylabel('Conversion Terms (Wm$^{-2}$)')
ax1.set_xlim([24.3,27.7+add])
ax1.set_ylim([yymin,yymax])
ax1.set_xticks(np.arange(24.5, 27.75, 0.25))
ax1.set_xticklabels(labels2)
handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles[:], labels[:],prop={'size':14})
ax1.text(0.03,0.80,'a)', ha='center', va='center', transform=ax1.transAxes)
#plt.show()acstr='10$^{-2}$'
lab=['$C_A$','$C_E$','$C_Z$'+facstr]
for i in range(2):
  if i == 2: x=1
  else: x = 0
  ax2.plot(timels[1:-1],datar[1:-1,i+6], label=lab[i], linewidth=1.2)
ax2.plot(timels[1:-1],datapr[1:-1,6], label='$C_{K1}$', linewidth=1.2,color='purple')
ax2.plot(timels[1:-1],datapr[1:-1,7], label='$C_{K2}$', linewidth=1.2,color='purple',ls='--')
ax2.plot(timels[1:-1],datar[1:-1,3+6]*fac, label='$C_Z$'+facstr, linewidth=1.2)
#ax2.set_yscale('log')
#ax2.set_xlabel('Time (MY)')
ax2.set_ylabel('Daily-averaged Conv-\nersion Terms (Wm$^{-2}$)', multialignment='center')
ax2.set_xlim([24.3,27.7+add])
ax2.set_ylim([yymin,yymax])
ax2.set_xticks(np.arange(24.5, 27.75, 0.25))
ax2.set_xticklabels(labels2)
handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles[:], labels[:],prop={'size':14})
ax2.text(0.03,0.80,'b)', ha='center', va='center', transform=ax2.transAxes)
#plt.show()
lab=['$C_A$','$C_E$','$C_Z$']
for i in range(2):
  lw=1.2
  if i == 2: x=1
  else: x = 0
  ax3.plot(timels[1:-1],(data[1:-1,i+6]-datar[1:-1,i+6]), label=lab[i], linewidth=lw)
ax3.plot(timels[1:-1],(datap[1:-1,6]-datapr[1:-1,6]), label='$C_{K1}$', linewidth=1.2,color='purple')
ax3.plot(timels[1:-1],(datap[1:-1,7]-datapr[1:-1,7]), label='$C_{K2}$', linewidth=1.2,color='purple',ls='--')
ax3.plot(timels[1:-1],(data[1:-1,9]-datar[1:-1,9]), label='$C_Z$', linewidth=lw)
#ax2.set_yscale('log')
ax3.set_xlabel('Solar Longitude $L_s$ [$^\circ$]')
ax3.set_ylabel('Diurnal Component of \n Conversion Terms (Wm$^{-2}$)', multialignment='center')
ax3.set_xlim([24.3,27.7+add])
ax3.set_ylim([yymin,yymax])
ax3.set_xticks(np.arange(24.5, 27.75, 0.25))
ax3.set_xticklabels(labels2)
handles, labels = ax3.get_legend_handles_labels()
ax3.legend(handles[:], labels[:],prop={'size':14})
ax3.text(0.03,0.8,'c)', ha='center', va='center', transform=ax3.transAxes)

fig.tight_layout()

plt.savefig('conversions_nxxy_paper'+str(n)+hem+'.eps')
