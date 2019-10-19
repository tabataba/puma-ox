#!/bin/bash

round()
{
echo $(printf %.$2f $(echo "scale=$2;(((10^$2)*$1)+0.5)/(10^$2)" | bc))
};

STARTPOINT=$PWD

DAT="/data/pam/ftabatabavakili/"
DIRNAME="pumas_arcb_similarity/"
HOM="/home/pam/ftabatabavakili/"
LOCATION=$DAT$DIRNAME
BASENAME="pumas_rot"
NAME2="_a"

if [ ! -d $LOCATION ]; then
  cd $DAT
  mkdir $DIRNAME
fi

cd $LOCATION
echo $LOCATION

echo $PWD

for i in 0.0625 #2.0 4.0 8.0 #0.125 0.25 0.5 1.0 #2.0 4.0 8.0   ###1.0 0.44 0.14 0.044 2.0 #0.44 1.0
do
for j in 64 #64 128 256 #512 
do
  a="$(round 1.0 2)" #"$(round 1.0/$i 2)"
  #a=0.0625 #"$(round 1/16.0 2)" 
  if [ $j == 64 ]; then xx=12; fi
  if [ $j == 128 ]; then xx=24; fi
  if [ $j == 256 ]; then xx=24; fi
  if [ $j == 512 ]; then xx=120; fi
  cp -rf $HOM/puma/trunk/pumas $LOCATION/$BASENAME$i$NAME2$a
  cd $LOCATION/$BASENAME$i$NAME2$a
  cp -rf puma_namelist_bkp2 puma_namelist
  #a1="$(round 1.00/$i 2)"
  #a2="$(round 2.71/$i 2)"
  #a3="$(round 7.39/$i 2)"
  echo $a #1 $a2 $a3
  echo $i
  #a1=1.00
  #a2=2.71
  #a3=7.39
  sed -i -e 's/ROTSPD  =     1.0/ROTSPD  =     '$i'/g' puma_namelist
  #sed -i -e 's/TFRC    = 0 0 0 0 0 0 0 7.39 2.71 1.00/ TFRC   = 0 0 0 0 0 0 0 '$a3' '$a2' '$a1'/g' pumag/puma_namelist
  #cp -rf pumag $BASENAME$i$NAME2$a1
  #cd $BASENAME$i$NAME2$a1
  afac="$(round $a*6371000.0 1)"
  sidfac="$(round 86164.0*$a 1)"
  echo $afac
  cp -rf most_puma_run_mpi_bkp most_puma_run_mpi
  sed -i -e 's/mpiexec -np $NPROC puma.x 64 10/mpiexec -np $NPROC puma.x '$j' 10/g' most_puma_run_mpi
  sed -i -e 's/NLAT = 128/ NLAT = '$j'/g' resolution_namelist
  cp -rf puma_bkp2.f90 puma.f90
  #sed -i -e 's/parameter(PLARAD_EARTH = 6371000.0)/parameter(PLARAD_EARTH = '$afac')/g' puma.f90
  #sed -i -e 's/parameter(SID_DAY_EARTH= 86164.)/parameter(SID_DAY_EARTH= '$sidfac')/g' puma.f90
 # cp -rf start.q_bkp start.q
  sed -i -e 's/parameter(PLARAD_EARTH = 6371000.0)/parameter(PLARAD_EARTH = '$afac')/g' puma.f90
  sed -i -e 's/parameter(SID_DAY_EARTH= 86164.)/parameter(SID_DAY_EARTH= '$sidfac')/g' puma.f90
  sed -i -e 's/#SBATCH --time=2:00:00/#SBATCH --time='$xx':00:00/g' start.sq
  sleep 1
  make -f make_mpi
  #sleep 1
  ./runb.sh
  echo "started run $BASENAME$i$NAME2$a"
  #cd ..
done
done
#cp -rf pumag/puma_namelist_bkp pumag/puma_namelist

cd $STARTPOINT
