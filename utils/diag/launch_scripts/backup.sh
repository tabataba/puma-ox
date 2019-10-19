#!/bin/bash

BKPDIR=/network/home/aopp/tabatabavakili/Dropbox/DPhil/bkp/.

echo copy data
cp -rf data  $BKPDIR
echo copt py
cp *.py      $BKPDIR
echo copy *.*
cp *.*       $BKPDIR
echo copy plots
cp -rf plots $BKPDIR
echo copy pics
cp -rf pics  $BKPDIR
echo copy pics2
cp -rf pics2 $BKPDIR