#!/bin/bash

#source def.sh

START=$PWD

cd pumagt_arcb_parameters

PUMA=$PWD

dir=($(ls -d *))
#files=($(ls *$FNAME* | grep -v ".nc" ))
#files=($(ls *010* | grep -v ".nc" ))
#echo ${files[*]}

TESTFLAG=0

#echo ${dir[*]}
#exit 1



for d in ${dir[*]}
do
  echo $d
  #echo 1
  if [ -d $d ]; then
    cd $d
    pos=$(echo `expr index "$d" p`)
    ps=${d:$pos+4:3}
    #TESTFLAG=1
    f="PUMAG.010"
    #echo 2
    if [ -f $f ]; then
      if [ ! -f "$f.nc" ] || [ $ps != 1.0 ]; then
        echo $f
        echo $ps
        #TESTFLAG=1
        /media/Seagate5TB/puma/pp_psurf/burn7.x $f "$f.nc" <$START/namelist_ps$ps.nl
      fi
    fi
    cd $PUMA
  fi
  #if [ $TESTFLAG == 1 ]; then exit 1; fi
done
cd $START

#for f in ${files[*]}
#do
#  echo $f
#  if [ ! -f "$f.nc" ]; then
#  burn7.x $f "$f.nc" <namelist.nl
#  fi 
#done 
