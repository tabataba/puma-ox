#!/bin/bash

#source def.sh

START=$PWD

cd pumagt_arcb_parameters
#cd pumas_yixiong/pumas

PUMA=$PWD

dir=($(ls -d *))
dir=($(ls -d rev53_r*_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu1))
#dir=($(ls -d pumas_*omg_zg*))
#files=($(ls *$FNAME* | grep -v ".nc" ))
#files=($(ls *010* | grep -v ".nc" ))
#echo ${files[*]}

#TESTFLAG=0

#echo ${dir[*]}
#exit 1

cd $START

for d in ${dir[*]}
do
  if [ -d "pumagt_arcb_parameters/$d" ]; then
    #TESTFLAG=1
    echo $d
    f="PUMAG.010"
    if [ -f "pumagt_arcb_parameters/$d/$f.nc" ]; then #&& [ ! -f $plot ]; then
      echo $d
      #./plot_zon.py $d
      ./plot_zonx.py $d
    exit
    fi
  #exit
  fi
  #exit
  #if [ $TESTFLAG == 1 ]; then exit 1; fi
done

#for f in ${files[*]}
#do
#  echo $f
#  if [ ! -f "$f.nc" ]; then
#  burn7.x $f "$f.nc" <namelist.nl
#  fi 
#done 
