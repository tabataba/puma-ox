#!/bin/bash

#source def.sh

START=$PWD

cd pumagt_arcb_parameters

PUMA=$PWD

dir=($(ls -d *))
dir=($(ls -d  rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu*)) #specific
dir=($(ls -d  rev53_r0.0625_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu*)) #specific

#files=($(ls *$FNAME* | grep -v ".nc" ))
#files=($(ls *010* | grep -v ".nc" ))
#echo ${files[*]}

#TESTFLAG=0

#echo ${dir[*]}
#exit 1

echo test

cd $START

for d in ${dir[*]}
do
  if [ -d "pumagt_arcb_parameters/$d" ]; then
    #for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012
    for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026 027 028 029 030
      do
      echo $d
      #TESTFLAG=1
      #f="PUMAG"
      #MONTH="M"$YEAR
      MONTH=$YEAR
      #f="PUMAG_NWPD12_M."$YEAR".nc"
      f="PUMAG."$YEAR".nc"
      echo "pumagt_arcb_parameters/$d/$f"
      if [ -f "pumagt_arcb_parameters/$d/$f" ]; then #&& [ ! -f $plot ]; then
        echo $d
        ./plot_zon_momflx.py $d $MONTH $f
      fi
    done
  fi
  #if [ $TESTFLAG == 1 ]; then exit 1; fi
done

#for f in ${files[*]}
#do
#  echo $f
#  if [ ! -f "$f.nc" ]; then
#  burn7.x $f "$f.nc" <namelist.nl
#  fi 
#done 
