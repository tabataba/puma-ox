#!/bin/bash
#if [ $# -ne 1 ]
#then
a=$PWD
name=$(basename $a)
qsub -N $name -v var=$a start.q
#else
#  qsub -N $1 start.q $PWD
#fi
