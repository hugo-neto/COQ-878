#!/bin/bash

for i in 0.960 0.965 0.970 0.975 0.980 0.985 0.990 0.995 1.000 1.005 1.010 1.020 1.030
do
  if test -d $i
  then
    vol=$(grep vol $i/OUTCAR|tail -1|awk '{print $5}')
    ene=$(grep 'free  ene' $i/OUTCAR |tail -1 |awk '{print $6}')
    echo $vol $ene
  fi
done
