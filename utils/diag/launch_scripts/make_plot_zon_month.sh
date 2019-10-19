#!/bin/bash

#source def.sh

START=$PWD

cd pumagt_arcb_parameters

PUMA=$PWD

#dir=($(ls -d *))


#dir=($(ls -d *)) #all
dir=($(ls -d  rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu*)) #specific
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
    pos=$(echo `expr index "$d" p`)
    ps=${d:$pos+4:3}
    #TESTFLAG=1
    #cd pumagt_arcb_parameters/$d
    for YEAR in 001 002 003 004 005 #006 007 008 009 010 011 012 013 014 015
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
          /media/Seagate5TB/puma/pp_psurf/burn7.x $f $fnc <$START/namelist_ps$ps.nl
        fi
          cd $START
          if [ ! -d $DATA/$d ]; then mkdir $DATA/$d; fi
          echo -p $PUMA/$d/$fnc
          echo -o $START/data/lorenz_en/$d/$f
          for st in 0 30 60 90 120 150 180 210 240 270 300 330 
          do
            ./plot_zon_month2.py $d $YEAR -s $st -i $iter
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

for d in ${dir[*]}
do
  iter=0
  cd $PUMA
  echo $d
  if [ -d $d ]; then
    cd $d
    echo $d
    pos=$(echo `expr index "$d" p`)
    ps=${d:$pos+4:3}
    #TESTFLAG=1
    #cd pumagt_arcb_parameters/$d
    for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015
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
          /media/Seagate5TB/puma/pp_psurf/burn7.x $f $fnc <$START/namelist_ps$ps.nl
        fi
          cd $START
          if [ ! -d $DATA/$d ]; then mkdir $DATA/$d; fi
          echo -p $PUMA/$d/$fnc
          echo -o $START/data/lorenz_en/$d/$f
          for st in 0 30 60 90 120 150 180 210 240 270 300 330
          do
            ./plot_zon_month2.py $d $YEAR -s $st -i $iter
            let "iter+=1"
            echo $iter
          done
          cd $PUMA/$d
          #./puma_energy_boer3.py -p $PUMA/$d/$fnc -o $START/$DATA/$d/$f
          #cd $PUMA
          #cd $d
#          if [ $YEAR -ne "010" ]; then rm $fnc; fi
          #exit 1
        #fi
      fi
    done
    #cd $PUMA
  fi
done


  #  for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015
  #  do
  #  #f="PUMAG.010"
  #    f="PUMAG."$YEAR
  #    fnc="PUMAG."$YEAR".nc"
  #    if [ -f "pumagt_arcb_parameters/$d/$f.nc" ]; then #&& [ ! -f $plot ]; then
  #    echo $d
  #    cd $START
  #    ./plot_zon_month.py $d
  #    cd $PUMA
  #    cd $d
  #    if [ $YEAR -ne "010" ]; then rm $fnc; fi
#  fi
 # fi
  #if [ $TESTFLAG == 1 ]; then exit 1; fi
#done

#for f in ${files[*]}
#do
#  echo $f
#  if [ ! -f "$f.nc" ]; then
#  burn7.x $f "$f.nc" <namelist.nl
#  fi 
#done 
