#!/bin/bash

#source def.sh

START=$PWD

cd pumagt_arcb_parameters

PUMA=$PWD
#DATA="data/lorenz_en"

dir=($(ls -d rev53_r1.0_res64_radius1.00_taufr1.0_psurf*_pref*_taus*_tausurf*_nmu1))
dir=($(ls -d rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu*))
#rev53_r1.0_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu0

dir=($(ls -d rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.04_pref0.04_taus0.20_tausurf3.6_nmu*))
dir=($(ls -d rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf*_nmu*))


III=0

for d in ${dir[*]}
do
  #echo $d
  if [ -d $d ]; then #&& [ $d == "rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf3.6_nmu1" ]; then
    cd $d
    echo hi, $III
    pos=$(echo `expr index "$d" p`)
    ps=${d:$pos+4:3}
    #f="PUMAG.010"
    for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026 027 028 029 030
    do
      f="PUMAG."$YEAR
      fnc="PUMAG."$YEAR".nc"
      if [ -f $f ]; then
        LASTYEAR=$YEAR
      fi

    done
      f="PUMAG."$LASTYEAR
      fnc="PUMAG."$LASTYEAR".nc"
      #echo $f
      if [ -f $f ]; then
        if [ ! -f $fnc ]; then  #|| [ $ps != 1.0 ]; then
          echo $f
          echo $ps
          /network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/pp_psurf/burn7.x $f $fnc <$START/namelist_ps$ps.nl
        fi
          cd $START
          #if [ ! -d $DATA/$d ]; then mkdir $DATA/$d; fi
          #echo -p $PUMA/$d/$fnc
          #echo -o $START/data/lorenz_en/$d/$f
          echo $III
          for it in `seq 0 30 180`; do
            ./plot_zon_snap.py $d $LASTYEAR $it
          done
          #./plot_zon.py $d $LASTYEAR
          let "III+=1"
          #./puma_energy_boer3.py -p $PUMA/$d/$fnc -o $START/$DATA/$d/$f
          cd $PUMA
          cd $d
          #if [ $YEAR -ne "010" ]; then rm $fnc; fi
          #exit 1
        #fi
      fi
    #done
    #exit 1
    cd $PUMA
  fi
done
cd $START 

cp -rf plots/zon_new   ~/Dropbox/DPhil/thesis/.
cp -rf plots/snap_new  ~/Dropbox/DPhil/thesis/.
