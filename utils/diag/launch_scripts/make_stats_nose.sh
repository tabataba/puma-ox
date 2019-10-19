#!/bin/bash

#source def.sh

START=$PWD

cd noseasons_pumagt_arcb

PUMA=$PWD

#dir=($(ls -d *))


dir=($(ls -d *)) #all
#dir=($(ls -d  rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu*)) #specific
#files=($(ls *$FNAME* | grep -v ".nc" ))
#files=($(ls *010* | grep -v ".nc" ))
#echo ${files[*]}

#TESTFLAG=0

#echo ${dir[*]}
#exit 1

cd $START


for d in ${dir[*]}
do
  iter=0
  cd $PUMA
  echo $d
  if [ -d $d ]; then
    cd $d
    echo $d
    #pos=$(echo `expr index "$d" p`)
    #ps=${d:$pos+4:3}

    pos=$(echo `expr index "$d" p`)
    ps=${d:$pos+4:3}
    pos2=$(echo `expr index "$d" psurf`)
    ps2=${d:$pos+4:4}
    #pos3=$(echo `expr index "$d" "pref"`)
    #let "pos4=pos+4-pos3"
    #echo $pos,$pos4,$pos3
    #ps3=${d:$pos+4:}
    #echo $ps $ps2 $ps3
    #f="PUMAG.010"
    echo $ps $ps2
    if [ $ps2 == 0.01 ] || [ $ps2 == 100.0 ]; then ps=$ps2; fi
    echo $ps

    #TESTFLAG=1
    #cd pumagt_arcb_parameters/$d
    for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 #016 017 018 019 020 021 022 023 024 025
    do
      echo HERERERER
      pwd
      f="PUMAG."$YEAR
      fnc="PUMAG."$YEAR".nc"
      #echo $f
      if [ -f $f ]; then #&& [ ! -f $START/data/lorenz_en/$d/$f".npy" ]; then
        if [ ! -f $fnc ]; then  #|| [ $ps != 1.0 ]; then
          echo $f
          echo $ps
          /network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/pp_psurf/burn7.x $f $fnc <$START/namelist_ps$ps.nl
        fi
          cd $START
          #if [ ! -d $DATA/$d ]; then mkdir $DATA/$d; fi
          echo -p $PUMA/$d/$fnc
          echo -o $START/data/lorenz_en/$d/$f
          for st in $(seq 0 30 359)
          do
            ./plot_nose_stats.py $d $YEAR -s $st -i $iter -d 30 # -d 30 
            let "iter+=1" 
            echo $iter
          done 
          cd $PUMA/$d
          #./puma_energy_boer3.py -p $PUMA/$d/$fnc -o $START/$DATA/$d/$f
          #cd $PUMA
          #cd $d
          #if [ $YEAR -ne "010" ]; then rm $fnc; fi
          #exit 1
        #fi
      fi
    done
    #cd $PUMA
  fi
done
cd $START
exit
