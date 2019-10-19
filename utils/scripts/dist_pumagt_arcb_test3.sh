#!/bin/bash

round()
{
echo $(printf %.$2f $(echo "scale=$2;(((10^$2)*$1)+0.5)/(10^$2)" | bc))
};

STARTPOINT=$PWD

DAT="/data/pam/ftabatabavakili/"
DIRNAME="pumagt_arcb_similaritytest2/"
HOM="/home/pam/ftabatabavakili/"
LOCATION=$DAT$DIRNAME
BASENAME="rot_r"
NAME2="_res"
NAME3="_tausurf"
NAME4="_nmu"
NAME21="_radius"
NAME22="_taufr"
NAME23="_psurf"
NAME24="_pref"
ADD3="_o_rdmd"


if [ ! -d $LOCATION ]; then
  cd $DAT
  mkdir $DIRNAME
fi

cd $LOCATION
echo $LOCATION

echo $PWD

# i does rotation rate
# k does tausurf
# iii does diurnalmean 1=yes 0=no
# j does resolution

a="$(round 1.0 2)"
#fricfac="$(round 1.0 1)"
psurffac="$(round 20.0 1)"
preffac="$(round 20.0 1)"
for i in 0.05 #0.03125  0.0455  #0.0625 #2.0 4.0 8.0 0.125 0.25 0.5 1.0 #2.0 4.0 8.0 #2.0 4.0 8.0 #0.125 0.25 0.5 1.0 #2.0 4.0 8.0   ###1.0 0.44 0.14 0.044 2.0 #0.44 1.0
do
for k in 360 #0.5 7 30 90 360 
do
for iii in 1
do
for fric in 0.05 1 20 400 
do
#for j in 64 #128 256 #512 #64 128 256 512 
#do
  #a="$(round 1.0/$i 5)"
  fricfac="$(round $fric 2)"
  tau="$(round $k*60*60*24  1)"
  echo $tau
  j=64
  if [ $i == 4.0 ]; then j=128; fi
  if [ $i == 8.0 ]; then j=128; fi
  if [ $j == 64 ]; then xx=11; zz=480; fi
  if [ $j == 128 ]; then xx=42; zz=240; fi
  if [ $j == 256 ]; then xx=24; zz=480; fi
  if [ $j == 512 ]; then xx=120; zz=720; fi
  RUNNAME=$LOCATION/$BASENAME$i$NAME2$j$NAME21$a$NAME22$fricfac$NAME23$psurffac$NAME24$ADD3$preffac$NAME3$k$NAME4$iii

  cp -rf $HOM/puma/trunk/pumagt $RUNNAME
  cd $RUNNAME
  #cp -rf puma_namelist_bkp2 puma_namelist
  #a1="$(round 1.00/$i 2)"
  #a2="$(round 2.71/$i 2)"
  #a3="$(round 7.39/$i 2)"
  echo $a #1 $a2 $a3
  echo $i
  #a1=1.00
  #a2=2.71
  #a3=7.39
  sed -i -e 's/real :: tausurfx = 15552000 !0.5 years/real :: tausurfx = '$tau' !'$k' days/g' radmod.f90

  sed -i -e 's/NTSPD = 240/NTSPD = '$zz'/g' puma_namelist
  sed -i -e 's/ROTSPD  =     1.0/ROTSPD  =     '$i'/g' puma_namelist
  sed -i -e 's/integer  :: nmumean = 0/integer  :: nmumean = '$iii'/g' radmod.f90
  #sed -i -e 's/TFRC    = 0 0 0 0 0 0 0 7.39 2.71 1.00/ TFRC   = 0 0 0 0 0 0 0 '$a3' '$a2' '$a1'/g' pumag/puma_namelist
  #cp -rf pumag $BASENAME$i$NAME2$a1
  #cd $BASENAME$i$NAME2$a1
  afac="$(round $a*6371000.0 1)"
  fric="$(round $fricfac 1)"
  psurf="$(round $psurffac*101100.0 1)"
  pref="$(round $preffac*100000.0 1)"
  sidfac="$(round 86164.0*$a 1)"
  echo $afac
  #cp -rf most_puma_run_mpi_bkp most_puma_run_mpi
  sed -i -e 's/mpiexec puma.x 64 10 $NPROC/mpiexec puma.x '$j' 10 $NPROC/g' most_puma_run_mpi
  #sed -i -e 's/NLAT = 128/ NLAT = '$j'/g' resolution_namelist
  #cp -rf puma_bkp2.f90 puma.f90
  sed -i -e 's/parameter(PLARAD_EARTH = 6371000.0)/parameter(PLARAD_EARTH = '$afac')/g' puma.f90
  sed -i -e 's/parameter(PSURF_EARTH  = 101100.0)/parameter(PSURF_EARTH  = '$psurf')/g' puma.f90
#  sed -i -e 's/parameter(PREF_EARTH   = 100000.0)/parameter(PREF_EARTH   = '$pref')/g' puma.f90
  sed -i -e 's/tauf(jlev) = /tauf(jlev) = '$fric' * /g' puma.f90
  #real    :: pref    = PREF_EARTH

  sed -i -e 's/real    :: pref    = PREF_EARTH/real    :: pref    = '$pref'/g' radmod.f90

  #sed -i -e 's/parameter(SID_DAY_EARTH= 86164.)/parameter(SID_DAY_EARTH= '$sidfac')/g' puma.f90
 # cp -rf start.q_bkp start.q
  sed -i -e 's/#SBATCH --time=2:00:00/#SBATCH --time='$xx':00:00/g' start.sq
  sleep 1
  make -f make_mpi clean
  make -f make_mpi
  #sleep 1
  ./runb.sh
  echo "started run $RUNNAME"
  #cd ..
done
done
done
done
#cp -rf pumag/puma_namelist_bkp pumag/puma_namelist

cd $STARTPOINT
