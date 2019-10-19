#!/bin/bash

round()
{
echo $(printf %.$2f $(echo "scale=$2;(((10^$2)*$1)+0.5)/(10^$2)" | bc))
};

STARTPOINT=$PWD
RUN=echo ${STARTPOINT##*/}
# find year

files=(PUMAG.0*)
for file in ${files[@]}; do
  s=`echo $file | cut -c 8-9`
done
echo $s
s2=$((s+100))
YEAR=`printf '%03d' $s`
echo $YEAR

# 

#cp puma_namelist old_puma_namelist
#sed -i -e 's/NWPD    =     1/NWPD    =     6/g' puma_namelist
#sed -i -e 's/NENERGY = 1/NENERGY = 0/g' puma_namelist
#sed -i -e 's/NENTROPY = 1/NENTROPY = 0/g' puma_namelist
sed -i -e 's/rm -f puma_restart/#rm -f puma_restart/g' most_puma_run_mpi
sed -i -e 's/YEAR=[0-9]/YEAR='$s' #/g' most_puma_run_mpi
#sed -i -e 's/YEARS=/YEARS='$s2' #/g' most_puma_run_mpi
time="50"
echo $time
sed -r -i -e 's/#SBATCH --time=.*:00:00/#SBATCH --time='$time':00:00/g' start.sq

./runb.sh

echo restarted run $RUN
sleep 1
