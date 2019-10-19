#!/bin/bash

#source def.sh

DATA="data/augier_pumagt360_chap65/"
DATALOR="data/lorenz_chap65"
PLOTS="plots/chap65/"

START=$PWD
mkdir $START/plots/chap65
mkdir $START/plots/chap65/zon
mkdir $START/plots/chap65/momflx
mkdir $START/plots/chap65/augier
mkdir $START/plots/chap65/momflx_month

mkdir $DATA
mkdir $DATALOR


cd pumagt_arcb_parameters

PUMA=$PWD

xxx=(rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu rev53_r0.0625_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu rev53_r0.5_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf360_nmu rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.04_pref0.04_taus0.00_tausurf3.6_nmu rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.04_pref0.04_taus0.20_tausurf3.6_nmu)

xxx=(rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.2_pref0.2_taus2.00_tausurf3.6_nmu rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.2_pref0.2_taus0.00_tausurf3.6_nmu rev53_r0.5_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf3.6_nmu rev53_r0.5_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu rev53_r0.5_res64_radius1.00_taufr1.0_psurf0.2_pref0.2_taus0.00_tausurf360_nmu rev53_r0.5_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus0.00_tausurf360_nmu)
#xxx=(rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu)

cd $PUMA

for x in ${xxx[*]}; do 
echo $x
cd $PUMA
#dir=($(ls -d *))
#dir=($(ls -d  rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus2.00_tausurf360_nmu*)) #specific
dir=($(ls -d  $x*)) #specific



for d in ${dir[*]}
do
  echo $d

#exit

  if [ -d $d ]; then #&& [ $d == "rev53_r0.125_res64_radius1.00_taufr1.0_psurf1.0_pref1.0_taus10.00_tausurf3.6_nmu1" ]; then
    cd $d
    echo hi, $III
    pos=$(echo `expr index "$d" p`)
    ps=${d:$pos+4:3}
    pos2=$(echo `expr index "$d" psurf`)
    ps2=${d:$pos+4:4}
    if [ $ps2 == 0.04 ] || [ $ps2 == 30.0 ]; then ps=$ps2; fi
    #f="PUMAG.010"
    for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012 013 014 015 016 017 018 019 020 021 022 023 024 025 026 027 028 029 030
    do
      f="PUMAG."$YEAR
      fnc="PUMAG."$YEAR".nc"
      if [ -f $f ]; then #lastyear
        LASTYEAR=$YEAR
      fi
    done #last year!
    f="PUMAG."$LASTYEAR
    fnc="PUMAG."$LASTYEAR".nc"
    #echo $f
    if [ -f $f ]; then
      if [ ! -f $fnc ]; then  #|| [ $ps != 1.0 ]; then
        echo $f
        echo $ps
        /network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/pp_psurf/burn7.x $f $fnc <$START/namelist_ps$ps.nl
      fi
      #if [ $ps2 == 0.04 ]; then
      #  /network/group/aopp/planetary/PLR005_TABATABAVAKILI_PUMAGT/pp_psurf/burn7.x $f $fnc <$START/namelist_ps$ps.nl
      #fi
      cd $START
      #if [ ! -d $DATA/$d ]; then mkdir $DATA/$d; fi
      #echo -p $PUMA/$d/$fnc
      #echo -o $START/data/lorenz_en/$d/$f
      echo $III

      echo "plot_zon"
      ./plot_zon.py $d $LASTYEAR

      echo "zon_momflx"
      ./plot_zon_momflx.py $d $LASTYEAR $fnc

      echo "augier"
      SPECT=~/soft/spectratmo/
      NAME=$d #${d:: -3}
      NAMEE=$d"_eddy"
      cd $SPECT
      ./spectrun.py -n $NAME -p $PUMA/$d/$fnc -o $START/$DATA -e 0 -i 36
      #cp gamma  to eddy
      mkdir $START/$DATA/$NAMEE
      cp $START/$DATA/$NAME/gamma.nc $START/$DATA/$NAMEE/.
      ./spectrun.py -n $NAMEE -p $PUMA/$d/$fnc -o $START/$DATA -e 1 -i 36
      cd $PUMA

      echo "plot augier"
      cd $START
      ./plot_spec_eddy.py -p $DATA/$d -n $d -o $START/$PLOTS/augier -e $DATA/$d'_eddy'
      cd $PUMA


      echo  cp -rf $START"/plots/zon_new/"*$d$LASTYEAR* $START/$PLOTS/zon/.
      cp -rf "${START}/plots/zon_new/"*"${d}${LASTYEAR}"* "${START}/${PLOTS}/zon/."
      echo cp -rf $START"/plots/momflx2_ex2/"*$d$LASTYEAR* $START/$PLOTS/momflx/.
      cp -rf "${START}/plots/momflx2_ex2/"*"${d}${LASTYEAR}"* "${START}/${PLOTS}/momflx/."


      let "III+=1"
      #./puma_energy_boer3.py -p $PUMA/$d/$fnc -o $START/$DATA/$d/$f
      cd $PUMA
      cd $d
      #if [ $YEAR -ne "010" ]; then rm $fnc; fi
      #exit 1
      #fi
    fi
    #done #all years!
    #exit 1
    cd $PUMA
  fi

#########compile and delete
done
cd $START


done
cd $START

exit 1

  if [ -d $d ]; then

    #cd $d
    #for YEAR in 001 002 003 004 005 006 007 008 009 010 011 012
    for MONTH in 001 002 003 004 005 006 007 008 009 010 011 012
    do
      f="PUMAG_NWPD12_M."$MONTH
      fnc="PUMAG_NWPD12_M."$MONTH".nc"
      echo $fnc
      echo -f $START/$DATALOR/$d/$f"_dm.npy"
      echo -f $START/$DATALOR/$d/$f".npy"
      if [ ! -f $START/$DATALOR/$d/$f"_dm.npy" ] && [ ! -f $START/$DATALOR/$d/$f".npy" ]; then
      if [ -f $d/$f ]; then
        if [ ! -f $d/$fnc ]; then  #|| [ $ps != 1.0 ]; then
          echo $f

          echo $ps
          /media/Seagate5TB/puma/pp_psurf/burn7.x $f $fnc <$START/namelist_ps$ps.nl
        fi
          cd $START
          if [ ! -d $DATALOR/$d ]; then mkdir $DATALOR/$d; fi
          #if [ ! -d $DATA/$d'_tot' ]; then mkdir $DATA/$d'_tot'; fi
          echo -p $PUMA/$d/$fnc
          echo -o $START/$DATALOR/$d/$f
          echo HAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
          ./puma_energy_boer3.py -d -p $PUMA/$d/$fnc -o $START/$DATALOR/$d/$f'_dm'
          #exit
          ./puma_energy_boer3.py -p $PUMA/$d/$fnc -o $START/$DATALOR/$d/$f
          ./output_lorenz.py -p $DATALOR -f $d
          cd $PUMA
          cd $d
          #exit./output_lorenz.py -p $DATA -f $d
          #if [ $YEAR -ne "010" ]; then rm $fnc; fi
          #exit 1
        #fi
      fi
      fi
      #./output_lorenz.py -p $DATALOR -f $d
      
      echo MONTH $MONTH
      echo $d
      #TESTFLAG=1
      #f="PUMAG"
      #MONTH="M"$YEAR
      #MONTH=$YEAR
      f="PUMAG_NWPD12_M."$MONTH".nc"
      #f="PUMAG."$YEAR".nc"
      echo "$d/$f"
      if [ -f "$d/$f" ]; then #&& [ ! -f $plot ]; then
        echo hi $d
        cd $START 
        ./plot_zon_momflx.py $d $MONTH $f
        cd $PUMA
        cp -rf "${START}/plots/momflx2_ex2/"*"${d}${MONTH}"* "${START}/${PLOTS}/momflx_month/."
      fi
    done
  fi

echo hi

#vmake_plot_momflx.sh


done
cd $START


done
cd $START


cp -rf $PLOTS ~/Dropbox/DPhil/thesis/.
