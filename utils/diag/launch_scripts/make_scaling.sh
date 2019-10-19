#!/bin/bash

for k in 0 1; do
  for j in {9..10..1}; do
    for i in {19..21..1}; do
      ./sup_comp_2.py -t $i -y $j -n $k
    done
  done
done

cp plots/scaling/scaling* ~/Dropbox/DPhil/thesis/scaling/.
mv ~/Dropbox/DPhil/thesis/scaling/*nose* ~/Dropbox/DPhil/thesis/scaling/nosea/.
