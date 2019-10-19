#!/bin/bash

#source def.sh

START=$PWD

DIR=noseasons_pumagt_arcb

cd $DIR

PUMA=$PWD

dir=($(ls -d *))
#dir=($(ls -d  rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu*)) #specific
#dir=($(ls -d  rev53_r0.0625_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu*)) #specific

#files=($(ls *$FNAME* | grep -v ".nc" ))
#files=($(ls *010* | grep -v ".nc" ))
#echo ${files[*]}

#TESTFLAG=0

#echo ${dir[*]}
#exit 1

echo test





cd $START

echo START
iii=0

for d in ${dir[*]}
do
  if [ -d "$DIR/$d" ]; then
    #TESTFLAG=1
    let "iii += 1"
    echo $iii 


    pos=$(echo `expr index "$d" p`)
    ps=${d:$pos+4:3}
    pos2=$(echo `expr index "$d" psurf`)
    ps2=${d:$pos+4:4}
    pos3=$(echo `expr index "$d" psurf`)
    ps3=${d:$pos+4:5}
    #pos3=$(echo `expr index "$d" "pref"`)
    #let "pos4=pos+4-pos3"
    #echo $pos,$pos4,$pos3
    #ps3=${d:$pos+4:}
    #echo $ps $ps2 $ps3
    #f="PUMAG.010"
    echo $ps $ps2
    if [ $ps2 == 0.01 ] || [ $ps2 == 10.0 ]; then ps=$ps2; fi
    if [ $ps3 == 100.0 ]; then ps=$ps3; fi
    echo $ps











    echo cd $DIR/$d
    cd $DIR/$d

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

      YEAR=$LASTYEAR
      f="PUMAG."$(printf %03d $YEAR)
      fnc="PUMAG."$(printf %03d $YEAR)".nc"
      echo $f
      echo $fnc
      if [ -f $f ]; then #&& [ ! -f $START/data/lorenz_en/$d/$f".npy" ]; then
        if [ ! -f $fnc ]; then  #|| [ $ps != 1.0 ]; then
          echo $f
          echo $ps
          /network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/pp_psurf/burn7.x $f $fnc <$START/namelist_ps$ps.nl
        fi
      fi

    cd $START

    f="PUMAG."$(printf %03d $YEAR)
    if [ -f "$DIR/$d/$f.nc" ]; then #&& [ ! -f $plot ]; then
      echo $d
      #./superrotation.py $d $(printf %03d $YEAR)
      ./plot_zon_momflx_nose.py $d $(printf %03d $YEAR) $f".nc"
    fi

  fi
  #if [ $TESTFLAG == 1 ]; then exit 1; fi
done









exit










cd $START

for d in ${dir[*]}
do
  if [ -d "$DIR/$d" ]; then
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
      echo "$DIR/$d/$f"
      if [ -f "$DIR/$d/$f" ]; then #&& [ ! -f $plot ]; then
        echo $d
        ./plot_zon_momflx_nose.py $d $MONTH $f
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
