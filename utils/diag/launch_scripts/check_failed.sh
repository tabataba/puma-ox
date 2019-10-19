#!/bin/bash

START=$PWD

DATA="data/lorenz_en/"

cd $DATA

dir=($(ls -d *))

for d in ${dir[*]}
do
  #echo $d
  if [ -d $d ]; then
    cd $d
    #echo $d
    files=($(ls *.npy))
    ii=0
    for YEAR in 001 002 003 004 005 006 007 008 009 010
    do
      #echo $YEAR
      if [ "${files[$ii]}" == "PUMAG."$YEAR".npy" ]; then 
        let "ii+=1"
      else
        echo $YEAR $d 
        break
      fi
    done
    cd $START/$DATA
  fi
done