#!/bin/bash

#source def.sh

START=$PWD

cd pumagt_arcb_parameters

PUMA=$PWD
DATA="data/lorenz_en_dm"

dir=($(ls -d *)) # all
dir=($(ls -d  rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu*)) #specific
dir=($(ls -d  rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.04_pref0.04_taus0.00_tausurf3.6_nmu*))

#rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.04_pref0.04_taus0.20_tausurf3.6_nmu1
for d in ${dir[*]}
do
  echo $d
  if [ -d $d ]; then
    cd $d
    pwd
    pos=$(echo `expr index "$d" p`)
    ps=${d:$pos+4:3}
    pos2=$(echo `expr index "$d" psurf`)
    ps2=${d:$pos+4:4}
    if [ $ps2 == 0.04 ] || [ $ps2 == 30.0 ]; then ps=$ps2; fi
    echo $ps
    #f="PUMAG.010"
    #for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025
    #mkdir $START/data/lorenz_en_dm/$d'_tot'
    #mkdir $START/data/lorenz_en_dm/$d'_dm'
    for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012
    do
      f="PUMAG_NWPD12_M."$YEAR
      fnc="PUMAG_NWPD12_M."$YEAR".nc"
      echo $fnc
      #echo $f
      if [ -f $f ] && [ ! -f $START/data/lorenz_en_dm/$d/$f"_dm.npy" ] && [ ! -f $START/data/lorenz_en_dm/$d/$f".npy" ]; then
        if [ ! -f $fnc ]; then  #|| [ $ps != 1.0 ]; then
          echo $f

          echo $ps
          /network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/pp_psurf/burn7.x $f $fnc <$START/namelist_ps$ps.nl
        fi
          cd $START
          if [ ! -d $DATA/$d ]; then mkdir $DATA/$d; fi
          #if [ ! -d $DATA/$d'_tot' ]; then mkdir $DATA/$d'_tot'; fi
          echo -p $PUMA/$d/$fnc
          echo -o $START/data/lorenz_en/$d/$f
          ./puma_energy_boer3.py -d -p $PUMA/$d/$fnc -o $START/$DATA/$d/$f'_dm'
          #exit
          ./puma_energy_boer3.py -p $PUMA/$d/$fnc -o $START/$DATA/$d/$f
          cd $PUMA
          cd $d
          #exit
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
