#!/bin/bash

START=$PWD

DATA="data/lorenz_en/"

cd $DATA

dir=($(ls -d *)) #all
#dir=($(ls -d  rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu*)) #specific
dir=($(ls -d  rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu*))

for d in ${dir[*]}
do
  #echo $d
  if [ -d $d ]; then
    #cd $d
    #echo $d
    #files=($(ls *.npy))
    #ii=0

    cd $START
    echo $d
    ./output_lorenz.py -p $DATA -f $d

    #for YEAR in 001 002 003 004 005 006 007 008 009 010
    #do
    #  #echo $YEAR
    #  if [ "${files[$ii]}" == "PUMAG."$YEAR".npy" ]; then 
    #    let "ii+=1"
    #  else
    #    echo $YEAR $d 
    #    break
    #  fi
    #done
    cd $START/$DATA
  fi
done

cd $START
