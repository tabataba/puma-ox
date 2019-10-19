########!/bin/bash
#PBS -S /bin/bash

#PBS -l walltime=12:00:00
#PBS -l nodes=1:ppn=16
########PBS -q consort
#PBS -m bea -M tabataba-vakili@atm.ox.ac.uk 
#PBS -V

echo $PBS_O_WORKDIR

module load openmpi/1.6.2__gcc-4.6.3
#module load openmpi/1.6.1/gcc-4.6.1

####cd /temp/eisox067/issi/1omg-1ps
#cd /home/eisox126/models/most16.020

nprocs=`wc -l $PBS_NODEFILE | awk '{ print $1 }'`

cd $var

echo $var

cd $PBS_O_WORKDIR

. enable_arcus_mpi.sh

./most_puma_run_mpi $nprocs

