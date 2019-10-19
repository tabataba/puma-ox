#!/bin/bash

#source def.sh

START=$PWD

cd pumagt_arcb_parameters

PUMA=$PWD
#DATA="data/lorenz_en"

xxx=(rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu rev53_r0.0625_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu rev53_r0.5_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.04_pref0.04_taus0.00_tausurf3.6_nmu rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.04_pref0.04_taus0.20_tausurf3.6_nmu)

#xxx=(
#rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu 
#rev53_r0.0625_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu 
#rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu 
#rev53_r0.5_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu 
#rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.04_pref0.04_taus0.00_tausurf3.6_nmu 
#rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.04_pref0.04_taus0.20_tausurf3.6_nmu
#)

dir=($(ls -d rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus*.00_tausurf360_nmu*))



dir=($(ls -d rev53_r0.125_res64_radius1.00_taufr1.0_psurf0.04_pref0.04_taus0.00_tausurf3.6_nmu*))

dir=($(ls -d rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu*))
#dir=($(ls -d ))
dir=($(ls -d rev53_r0.0625_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu*))

dir=($(ls -d rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.04_pref0.04_taus0.20_tausurf3.6_nmu*))

dir=($(ls -d rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.2_pref0.2_taus2.00_tausurf3.6_nmu*))

#dir=($(ls -d rev53_r1.0_res64_radius1.00_taufr*_psurf1.0_pref1.0_taus0.00_tausurf360_nmu*))
#rev53_r1.0_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu0

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
    for YEAR in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
    do
      f="PUMAG."$(printf %03d $YEAR)
      fnc="PUMAG."$(printf %03d $YEAR)".nc"
      if [ -f $f ]; then
        LASTYEAR=$YEAR
      fi

    done
    #echo $LASTYEAR
    #let "Y1=LASTYEAR-2"
    #let "Y2=LASTYEAR-1"
    #let "Y3=LASTYEAR"
    #echo $Y1 $Y2 $Y3
    LASTYEAR=$(printf %02d $LASTYEAR)
    echo $LASTYEAR
    let "Y1=LASTYEAR-2"
    let "Y2=LASTYEAR-1"
    let "Y3=LASTYEAR"
    echo $Y1 $Y2 $Y3
    Y1=$(printf %03d $Y1)
    Y2=$(printf %03d $Y2)
    Y3=$(printf %03d $Y3)
    for YEAR in $Y3 #$Y1 $Y2 $Y3
    do
      f="PUMAG."$YEAR
      fnc="PUMAG."$YEAR".nc"
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
          #for it in `seq 0 30 90`; do
          #  ./plot_zon_snap.py $d $LASTYEAR $it
          #done
          ./fft.py $d $YEAR
          ./hovmoller.py $d $YEAR
          #./plot_zon.py $d $LASTYEAR
          let "III+=1"
          #./puma_energy_boer3.py -p $PUMA/$d/$fnc -o $START/$DATA/$d/$f
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

#cp -rf plots/zon_new   ~/Dropbox/DPhil/thesis/.
cp -rf plots/wav3  ~/Dropbox/DPhil/thesis/.
