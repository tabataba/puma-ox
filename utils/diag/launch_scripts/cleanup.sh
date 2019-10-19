#!/bin/bash

#source def.sh

START=$PWD

cd pumagt_arcb_parameters

PUMA=$PWD
DATA="data/lorenz_en"

dir=($(ls -d *)) # all
#dir=($(ls -d  rev53_r*_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu*)) #specific

#dir=($(ls -d rev53_r1.0_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu1))

for d in ${dir[*]}
do
  echo $d
  if [ -d $d ]; then
    cd $d
    pos=$(echo `expr index "$d" p`)
    ps=${d:$pos+4:3}
    #f="PUMAG.010"
    LASTYEAR=0
    for YEAR in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38
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
    Y1=$(printf %03d $Y1)
    Y2=$(printf %03d $Y2)
    Y3=$(printf %03d $Y3)
    echo $Y1 $Y2 $Y3
    mkdir /media/Seagate5TB/puma/pumagt_arcb_parameters_backup/$d
    #for YEAR in $Y1 $Y2 $Y3
    for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026 027 028 029 030
    do
      f="PUMAG."$YEAR
      fnc="PUMAG."$YEAR".nc"
      #mkdir /media/Seagate5TB/puma/pumagt_arcb_parameters_backup/$d
      #echo $f
      #if [ -f $f ] && [ ! -f $START/data/lorenz_en/$d/$f".npy" ]; then
        #if [ ! -f $fnc ]; then  #|| [ $ps != 1.0 ]; then
        #  echo $f
        #  echo $ps
        #  /network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/pp_psurf/burn7.x $f $fnc <$START/namelist_ps$ps.nl
        #fi
          #cd $START
          #if [ ! -d $DATA/$d ]; then mkdir $DATA/$d; fi
          #echo -p $PUMA/$d/$fnc
          #echo -o $START/data/lorenz_en/$d/$f
          #./puma_energy_boer3.py -p $PUMA/$d/$fnc -o $START/$DATA/$d/$f
          #cd $PUMA
          #cd $d
          
          if [ $YEAR -ne $Y1 ] && [ $YEAR -ne $Y2 ] && [ $YEAR -ne $Y3 ]; then
            #rm $fnc;
            if [ -f $fnc ]; then
              echo moving $d/$fnc
              #mkdir /media/Seagate5TB/puma/pumagt_arcb_parameters_backup/$d
              mv $fnc /media/Seagate5TB/puma/pumagt_arcb_parameters_backup/$d/.
            fi
          fi
          #exit 1
        #fi
      #fi
    done
    #exit 1
    cd $PUMA
  fi
done
cd $START 
