#!/bin/bash

#source def.sh

START=$PWD

cd pumagt_arcb_parameters

PUMA=$PWD
DATA="data/lorenz_en"

dir=($(ls -d *)) # all
dir=($(ls -d  rev53_r0.*_res64_radius1.00_taufr1.0_psurf*_pref*_taus10.00_tausurf*_nmu*)) #specific

#dir=($(ls -d rev53_r1.0_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu1))

for d in ${dir[*]}
do
  echo $d
  if [ -d $d ]; then
    cd $d
    pos=$(echo `expr index "$d" p`)
    ps=${d:$pos+4:3}
    pos2=$(echo `expr index "$d" psurf`)
    ps2=${d:$pos+4:4}
    if [ $ps2 == 0.04 ] || [ $ps2 == 30.0 ]; then ps=$ps2; fi    
    #ps="0.04"
    #f="PUMAG.010"
    LASTYEAR=0
    for YEAR in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
    do
      f="PUMAG."$(printf %03d $YEAR)
      fnc="PUMAG."$(printf %03d $YEAR)".nc"
      if [ -f $f ]; then
        LASTYEAR=$YEAR
      fi
      echo $LASTYEAR

    done
#    for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025
#    do
#      f="PUMAG."$YEAR
#      fnc="PUMAG."$YEAR".nc"
#      #echo $f
    echo $LASTYEAR
    LASTYEAR=$(printf %02d $LASTYEAR)
    echo $LASTYEAR
    let "Y1=LASTYEAR-2"
    let "Y2=LASTYEAR-1"
    let "Y3=LASTYEAR"
    echo $Y1 $Y2 $Y3
    for YEAR in $Y3 #$Y1 $Y2 $Y3
    do
      f="PUMAG."$(printf %03d $YEAR)
      fnc="PUMAG."$(printf %03d $YEAR)".nc"
      echo $f
      if [ -f $f ]; then #&& [ ! -f $START/data/lorenz_en/$d/$f".npy" ]; then
        if [ ! -f $fnc ]; then  #|| [ $ps != 1.0 ]; then
          echo $f
          echo $ps
          /network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/pp_psurf/burn7.x $f $fnc <$START/namelist_ps$ps.nl
        fi
          cd $START
          if [ ! -d $DATA/$d ]; then mkdir $DATA/$d; fi
          echo -p $PUMA/$d/$fnc
          echo -o $START/data/lorenz_en/$d/$f
          ./puma_energy_boer3.py -p $PUMA/$d/$fnc -o $START/$DATA/$d/$f
          cd $PUMA
          cd $d
          #if [ $YEAR -ne "010" ]; then rm $fnc; fi
          #exit 1
        #fi
      fi
    done
    #exit 1
    cd $PUMA
  fi
done
cd $START 
