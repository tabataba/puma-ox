#!/bin/bash

#source def.sh

START=$PWD

cd pumagt_arcb_parameters

PUMA=$PWD

dir=($(ls -d *))
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
    f="PUMAG.010"
    if [ -f "pumagt_arcb_parameters/$d/$f.nc" ]; then #&& [ ! -f $plot ]; then
      echo $d
      #./superrotation.py $d
      matlab -nojvm -nodesktop -nosplash -r "clear,name='$d',new_ep,exit"
    fi
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
